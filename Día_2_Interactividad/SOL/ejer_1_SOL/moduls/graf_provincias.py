import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly_express as px

import functions as f # type: ignore



def provincias_desembarque(value):

    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.ccaa_desembarques")
    data = data[data["Año"] == 2024]
    data = data[data["IdCCAADesembarque"] == value]
    data = data.groupby("ProvinciaDesembarque")["valor"].sum().reset_index()

    bar = px.bar(data, x= "valor", y= "ProvinciaDesembarque")

    contenido = dcc.Graph(id = "barras-provincia", figure = bar)
   
    return contenido