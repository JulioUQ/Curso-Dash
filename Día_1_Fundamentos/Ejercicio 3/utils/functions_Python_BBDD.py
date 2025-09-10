import sys
import os
import warnings
import json
import pyodbc
import pandas as pd
import geopandas as gpd
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from typing import Literal, Optional

# === Añadir el directorio raíz al path para imports ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
warnings.simplefilter(action='ignore', category=UserWarning)

# Importar ruta por defecto de la configuración
from config import config_path_exp 

# === Funciones auxiliares ===

def cargar_configuracion_json(config_file: str = config_path_exp) -> dict:
    """Carga un archivo JSON de configuración y lo convierte en diccionario."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_file}")
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def obtener_configuracion_conexion(database_key: str, ruta_config: str = config_path_exp) -> dict:
    """Obtiene configuración combinada 'common' + específica desde JSON."""
    confs = cargar_configuracion_json(ruta_config)
    if "common" not in confs or database_key not in confs:
        raise ValueError(f"Faltan claves en la configuración: 'common' o '{database_key}'")
    return {**confs["common"], **confs[database_key]}

def crear_cadena_conexion_odbc(conf: dict) -> str:
    """Genera una cadena de conexión ODBC a SQL Server."""
    return (
        f"DRIVER=ODBC Driver 17 for SQL Server;"
        f"SERVER={conf['Server']};"
        f"DATABASE={conf['Database']};"
        f"UID={conf['UID']};"
        f"PWD={conf['PWD']}"
    )

# === Funciones principales ===
def ejecutar_consulta_sql(
    query: str,
    database_key: str = "SGP_SIPE_EXPLOTACION",
    ruta_config: str = config_path_exp):

    all_confs = cargar_configuracion_json(ruta_config)

    if "common" not in all_confs:
        raise KeyError("No se encontró la sección 'common' en la configuración.")
    if database_key not in all_confs:
        raise KeyError(f"No se encontró la base de datos '{database_key}' en la configuración.")

    conf = {**all_confs["common"], **all_confs[database_key]}

    conn_str = (
        f"DRIVER={conf['Driver']};"
        f"SERVER={conf['Server']};"
        f"DATABASE={conf['Database']};"
        f"UID={conf['UID']};"
        f"PWD={conf['PWD']}"
    )
    conn_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}"
    engine = create_engine(conn_url)

    df = pd.read_sql_query(query, con=engine)
    return df


def importar_shapefile_a_sqlserver(
        ruta_shapefile: str, 
        nombre_tabla: str, 
        database_key: str, 
        ruta_config: str = config_path_exp):
    """Importa un shapefile o GeoJSON a una tabla de SQL Server con geometría."""
    gdf = gpd.read_file(ruta_shapefile)
    gdf = gdf.to_crs(epsg=4326)
    gdf["geometry_WKT"] = gdf.geometry.apply(lambda geom: geom.wkt if geom else None)
    df = gdf.drop(columns='geometry')

    conf = obtener_configuracion_conexion(database_key, ruta_config)
    conn_str = crear_cadena_conexion_odbc(conf)
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    schema = "dbo"
    cursor.execute(f"IF OBJECT_ID('{schema}.{nombre_tabla}', 'U') IS NOT NULL DROP TABLE {schema}.{nombre_tabla};")
    conn.commit()

    definicion_columnas = ",\n    ".join([
        f"[{col}] NVARCHAR(MAX)" if df[col].dtype == 'object' else
        f"[{col}] FLOAT" if 'float' in str(df[col].dtype) else
        f"[{col}] INT"
        for col in df.columns
    ])
    cursor.execute(f"CREATE TABLE {schema}.{nombre_tabla} (\n    {definicion_columnas}\n);")
    conn.commit()

    df = df.where(pd.notnull(df), None)
    columnas = ', '.join(f"[{col}]" for col in df.columns)
    placeholders = ', '.join('?' for _ in df.columns)
    insert_sql = f"INSERT INTO {schema}.{nombre_tabla} ({columnas}) VALUES ({placeholders})"

    for row in df.itertuples(index=False, name=None):
        cursor.execute(insert_sql, row)
    conn.commit()

    cursor.execute(f"ALTER TABLE {schema}.{nombre_tabla} ADD geometry_GEOM geometry;")
    cursor.execute(f"""
        UPDATE {schema}.{nombre_tabla}
        SET geometry_GEOM = geometry::STGeomFromText(REPLACE(geometry_WKT, ' Z', ''), 4326)
        WHERE geometry_WKT IS NOT NULL;
    """)
    conn.commit()

    cursor.close()
    conn.close()
    print(f"Shapefile cargado correctamente en la tabla [{schema}].[{nombre_tabla}].")


def importar_geodataframe_a_sqlserver(
        gdf: gpd.GeoDataFrame,
        nombre_tabla: str,
        database_key: str,
        ruta_config: str = config_path_exp):
    """
    Importa un GeoDataFrame a SQL Server convirtiendo la geometría a WKT y generando geometry_GEOM.
    
    - Crea o reemplaza la tabla si ya existe.
    - Convierte CRS a EPSG:4326 si no lo está.
    """
    # Asegurar CRS en EPSG:4326
    gdf = gdf.to_crs(epsg=4326)

    # Asegurar geometría válida
    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty]

    # Crear columna con geometría WKT
    gdf["geometry_WKT"] = gdf.geometry.apply(lambda geom: geom.wkt if geom else None)
    df = gdf.drop(columns="geometry")

    # Obtener configuración y conexión
    conf = obtener_configuracion_conexion(database_key, ruta_config)
    conn_str = crear_cadena_conexion_odbc(conf)
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    schema = "dbo"

    # Eliminar tabla si existe
    cursor.execute(f"IF OBJECT_ID('{schema}.{nombre_tabla}', 'U') IS NOT NULL DROP TABLE {schema}.{nombre_tabla};")
    conn.commit()

    # Crear tabla con tipos adecuados
    definicion_columnas = ",\n    ".join([
        f"[{col}] NVARCHAR(MAX)" if df[col].dtype == 'object' else
        f"[{col}] FLOAT" if 'float' in str(df[col].dtype) else
        f"[{col}] INT"
        for col in df.columns
    ])
    cursor.execute(f"CREATE TABLE {schema}.{nombre_tabla} (\n    {definicion_columnas}\n);")
    conn.commit()

    # Rellenar valores nulos
    df = df.where(pd.notnull(df), None)

    # Insertar datos
    columnas = ', '.join(f"[{col}]" for col in df.columns)
    placeholders = ', '.join('?' for _ in df.columns)
    insert_sql = f"INSERT INTO {schema}.{nombre_tabla} ({columnas}) VALUES ({placeholders})"

    for row in df.itertuples(index=False, name=None):
        cursor.execute(insert_sql, row)
    conn.commit()

    # Crear y poblar columna geometry
    cursor.execute(f"ALTER TABLE {schema}.{nombre_tabla} ADD geometry_GEOM geometry;")
    cursor.execute(f"""
        UPDATE {schema}.{nombre_tabla}
        SET geometry_GEOM = geometry::STGeomFromText(REPLACE(geometry_WKT, ' Z', ''), 4326)
        WHERE geometry_WKT IS NOT NULL;
    """)
    conn.commit()

    cursor.close()
    conn.close()
    print(f"GeoDataFrame cargado correctamente en la tabla [{schema}].[{nombre_tabla}].")


def importar_dataframe_a_sqlserver(
    df: pd.DataFrame,
    nombre_tabla: str,
    database_key: str,
    esquema: str = "dbo",
    if_exists: Literal["replace", "fail", "append"] = "replace",
    ruta_config: str = config_path_exp
):
    """Importa un DataFrame de pandas a SQL Server."""
    conf = obtener_configuracion_conexion(database_key, ruta_config)
    conn_str = quote_plus(crear_cadena_conexion_odbc(conf))
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}", fast_executemany=True)

    df = df.where(pd.notnull(df), None)

    print(f"Importando a {conf['Database']}.{esquema}.{nombre_tabla} ...")
    print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    df.to_sql(nombre_tabla, engine, schema=esquema, if_exists=if_exists, index=False)
    print("Importación completada con éxito.")


# === Funciones AUXILIARES ===

def describe_df(data):
    """
    Proporciona un resumen del DataFrame, incluyendo forma, tipos de datos, estadísticas básicas,
    conteo de valores nulos, valores únicos, mediana y rango de fechas para columnas tipo datetime.

    :param data: DataFrame de pandas.
    :return: DataFrame con el resumen del DataFrame dado.
    """
    # Crear base del resumen
    total = len(data)
    summary = pd.DataFrame({
        'Column': data.columns,
        'Data Type': data.dtypes.astype(str),
        'Non-null Count': data.count().values,
        '% Null Values': ((data.isnull().sum() / total) * 100).round(2).values,
        'Unique Values': data.nunique().values
    })

    summary['Shape'] = f"{data.shape[0]} rows, {data.shape[1]} columns"

    # Estadísticas para columnas numéricas
    numeric_cols = data.select_dtypes(include=['number']).columns
    if not numeric_cols.empty:
        describe_stats = data[numeric_cols].describe().T
        describe_stats = describe_stats.rename(columns={'50%': 'median'})[
            ['mean', 'median', 'std', 'min', '25%',  '75%', 'max']
        ]
        describe_stats.reset_index(inplace=True)
        describe_stats.rename(columns={'index': 'Column'}, inplace=True)

        summary = pd.merge(summary, describe_stats, on='Column', how='left')

    # Rango de fechas para columnas datetime
    datetime_cols = data.select_dtypes(include=['datetime', 'datetime64[ns]']).columns
    if not datetime_cols.empty:
        date_ranges = pd.DataFrame({
            'Column': datetime_cols,
            'Min Date': data[datetime_cols].min().values,
            'Max Date': data[datetime_cols].max().values
        })
        summary = pd.merge(summary, date_ranges, on='Column', how='left')

    return summary


def detect_duplicates(df):
    """
    Detecta duplicados en un DataFrame y devuelve un nuevo DataFrame con los duplicados.

    :param df: DataFrame de pandas.
    :return: DataFrame con los duplicados detectados.
    """
    try:
        return df[df.duplicated(keep=False)]
    except Exception as e:
        print("Error detectando duplicados:", e)
        return None


def unique_df(df):
    """
    Imprime un resumen de las categorías únicas para las variables categóricas de un DataFrame.

    :param df: DataFrame de pandas.
    """
    categorical_columns = df.select_dtypes(include=['category', 'object']).columns

    if len(categorical_columns) == 0:
        print("No se encontraron columnas categóricas u objeto en el DataFrame.")
        return

    for column in categorical_columns:
        print(f"Resumen para la columna '{column}':\n{df[column].unique()}\n")