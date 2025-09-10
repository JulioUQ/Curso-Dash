import os
import sys
import json
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine

# === Añadir el directorio raíz al path para imports ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Importar ruta por defecto de la configuración
from config import config_path_exp 

# === Funciones auxiliares ===

def cargar_configuracion_json(config_file: str = config_path_exp) -> dict:
    """Carga un archivo JSON de configuración y lo convierte en diccionario."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_file}")
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# === Función principal ===

def ejecutar_consulta_sql(
    query: str,
    database_key: str = "SGP_SIPE_EXPLOTACION",
    ruta_config: str = config_path_exp
) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL en SQL Server usando SQLAlchemy y pyodbc.
    
    :param query: Consulta SQL como string.
    :param database_key: Clave de la base de datos en el JSON de configuración.
    :param ruta_config: Ruta al archivo de configuración JSON.
    :return: DataFrame de pandas con los resultados.
    """
    all_confs = cargar_configuracion_json(ruta_config)

    if "common" not in all_confs:
        raise KeyError("No se encontró la sección 'common' en la configuración.")
    if database_key not in all_confs:
        raise KeyError(f"No se encontró la base de datos '{database_key}' en la configuración.")

    # Combinar configuración común + específica
    conf = {**all_confs["common"], **all_confs[database_key]}

    # Crear cadena de conexión ODBC
    conn_str = (
        f"DRIVER={conf['Driver']};"
        f"SERVER={conf['Server']};"
        f"DATABASE={conf['Database']};"
        f"UID={conf['UID']};"
        f"PWD={conf['PWD']}"
    )

    # Crear engine SQLAlchemy
    conn_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}"
    engine = create_engine(conn_url)

    # Ejecutar consulta y devolver DataFrame
    df = pd.read_sql_query(query, con=engine)
    return df