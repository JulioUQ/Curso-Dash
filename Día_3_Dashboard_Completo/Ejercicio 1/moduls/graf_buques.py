import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import functions as f # type: ignore

def variacion_buques(value, puerto = None, html = False):
    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.historico_flota")
    data = data[data["IdCcaa"] == value]

    if puerto:
        data = data[data["puerto"] == puerto]

    data = data.groupby("año")["buques"].sum().reset_index()

    line = px.line(data, x= "año", y= "buques")

    contenido = dcc.Graph(id= "line-buques-fig", figure= line)

    if html == True:
        contenido = line.to_html(full_html = True)

    return contenido


def get_data_buques(value, puerto = None):
    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.historico_flota")
    data = data[data["IdCcaa"] == value]

    if puerto:
        data = data[data["puerto"] == puerto]

    data = data.groupby("año")["buques"].sum().reset_index()

    return data