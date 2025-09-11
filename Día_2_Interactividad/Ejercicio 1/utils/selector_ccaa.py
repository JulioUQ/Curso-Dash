import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import functions as f # type:ignore

def selector_ccaa():

    ccaas = f.consulta("SELECT Id, Descripcion FROM SGP_SIPE.cat.CCAA")

    ccaas = ccaas.sort_values(by= "Descripcion")

    excluir = ["COMUNIDAD DE MADRID"]

    dict_options = [{"label": nombre["Descripcion"], "value": nombre["Id"]} for _, nombre in ccaas.iterrows() 
               if nombre["Descripcion"] not in excluir]
    
    selector = dbc.Card([
        dbc.CardBody(dcc.Dropdown(
            id= "selector-ccaa",
            options = dict_options,
            placeholder= "Selecciona una CCAA",
            style = {"fontSize": "14px", "fontFamily": "Arial", "maxHeight": "400px", "border": "none", "width": "100%", 
                     "boxShadow": "none", "borderRadius": "0"}
        ))
    ])

    return selector

