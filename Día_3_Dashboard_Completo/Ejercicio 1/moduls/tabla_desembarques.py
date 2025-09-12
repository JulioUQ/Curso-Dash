import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import Dash, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

import functions as f # type: ignore

def tabla_desembarques(value):
    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.ccaa_desembarques WHERE año = 2024")
    data = data[data["IdCCAADesembarque"] == value]
    data = data.groupby(["PuertoBase"])[["Peso", "valor"]].sum().reset_index()

    data["Peso"] = data["Peso"].round(2)
    data["valor"] = data["valor"].round(2)

    data = data.sort_values(by= "valor", ascending= False)

    tabla = dash_table.DataTable(id= "tabla-desembarques",
                                 columns=[{"name": i, "id": i} for i in data.columns],
                                 data = data.to_dict("records"),
                                style_header={"fontWeight": "bold", "backgroundColor": "#ebf5fb", "fontFamily": "Arial", "minWidth": 350, "whiteSpace": "normal", "text-align": "center", "fontSize": "15px"},
                                style_data={"backgroundColor": "#ffffff", "color": "#333333", "fontFamily": "Arial", "fontSize": "13px"},
                                style_table={"overflowY": "auto"},
                                style_cell={"minWidth": 100, "width": "auto", "text-align": "left"},
                                style_data_conditional=[
                                    {"if": {"row_index": "odd"}, "backgroundColor": "#f8f9f9"},
                                    {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"}
                                ], # type: ignore
                                cell_selectable=False,
                                fixed_rows={"headers": True},
                                sort_action="native",
                                filter_action= "native",
                                page_size=12,
                                row_selectable = "single"
                                 )

    return tabla

#-------------------------------------------#

def get_tabla_desembarques(value, puerto = None):
    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.ccaa_desembarques WHERE año = 2024")
    data = data[data["IdCCAADesembarque"] == value]

    if puerto:
        data = data[data["PuertoBase"] == puerto]
        
    data = data.groupby(["PuertoBase"])[["Peso", "valor"]].sum().reset_index()

    data["Peso"] = data["Peso"].round(2)
    data["valor"] = data["valor"].round(2)

    data = data.sort_values(by= "valor", ascending= False)

    return data