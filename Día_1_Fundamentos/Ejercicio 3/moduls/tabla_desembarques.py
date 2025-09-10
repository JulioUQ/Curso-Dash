import sys
import os
from dash import dash_table
import pandas as pd
import utils.functions_Python_BBDD as f

# Ajuste opcional de ruta raíz (si es estrictamente necesario)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)


def tabla_d():
    """
    Crea un DataTable de Dash con los desembarques por CCAA para el año 2024.
    """
    # Consulta a la BBDD    
    data = f.ejecutar_consulta_sql(
        "SELECT * FROM cm.ccaa_desembarques WHERE Año = 2024",
        database_key="SGP_CUADROSMANDO"
    )

    if data is None or data.empty:
        # Si no hay datos, devolver un DataFrame vacío
        data = pd.DataFrame(columns=["CCAADesembarque", "Peso"])
    else:
        # Filtrar y procesar datos
        data = data.groupby(["CCAADesembarque"]).agg({"Peso": "sum"}).reset_index()
        data = data.sort_values(by="Peso", ascending=False)

    # Crear DataTable de Dash
    tabla = dash_table.DataTable(
        # ID de la tabla para callbacks 
        id="tabla-desembarques-ccaa",
        # Convierte DataFrame a lista de diccionarios
        data=data.to_dict('records'),    # type: ignore
        # Definimos las columnas con un dict comprensible
        columns=[
            {"name": i, "id": i} for i in data.columns
        ], 
        # Estilos para la cabecera
        style_header={
            "fontWeight": "bold",
            "backgroundColor": "#ebf5fb",
            "fontFamily": "Arial",
            "textAlign": "center",
            "fontSize": "15px"
        }, 
        # Estilos generales para las celdas
        style_data={
            "backgroundColor": "#ffffff",
            "color": "#333333",
            "fontSize": "13px"
        },
        # Estilos condicionales (pares e impares)
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#f9f9f9"},
            {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"}
        ], # type: ignore
        cell_selectable=False,
        sort_action="native",
        filter_action="native",
        page_size=10,
        fixed_rows={"headers": True}  # Se queda el encabezado fijo al hacer scroll
    )

    return tabla
