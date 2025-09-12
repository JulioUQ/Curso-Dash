import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import functions as f # type: ignore



def provincias_desembarque(value, puerto = None, html = False):

    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.ccaa_desembarques")
    data = data[data["Año"] == 2024]
    data = data[data["idccaa_base"] == value]

    if puerto:
        data = data[data["PuertoBase"] == puerto]

    data = data.groupby("ProvinciaDesembarque")["valor"].sum().reset_index()

    bar = px.bar(data, x= "valor", y= "ProvinciaDesembarque")

    contenido = dcc.Graph(id = "barras-provincias-fig", figure = bar)

    if html == True:
        contenido = bar.to_html(full_html = True)
   
    return contenido


def get_data_provicias(value, puerto = None):

    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.ccaa_desembarques")
    data = data[data["Año"] == 2024]
    data = data[data["idccaa_base"] == value]

    if puerto:
        data = data[data["PuertoBase"] == puerto]

    data = data.groupby("ProvinciaDesembarque")["valor"].sum().reset_index()
   
    return data