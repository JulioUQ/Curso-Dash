import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import functions as f # type: ignore

def variacion_buques(ccaa, puerto= None):
    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.historico_flota")

    data = data[data["IdCcaa"] == ccaa] # Filtramos por la CCAA seleccionada en el callback

    if puerto is not None:
        data = data[data["puerto"] == puerto] # Filtramos por el puerto seleccionado en la tabla
    else:
        data = data

    data = data.groupby("año")["buques"].sum().reset_index()

    line = px.line(data, x= "año", y= "buques")

    contenido = dcc.Graph(#id= "line-buques", 
                          figure= line)

    return contenido