import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd

import functions as f # type: ignore

def selector_ccaa():
    ccaas = f.consulta("""SELECT distinct Id, Descripcion FROM [SGP_SIPE].[cat].[CCAA]""")
                        
    ccaas = ccaas.sort_values(by= "Descripcion")

    options_dict = [{'label': ccaa["Descripcion"], 'value': ccaa["Id"]} for _, ccaa in ccaas.iterrows() if ccaa["Descripcion"] != "CASTILLA Y LEÓN" and ccaa["Descripcion"] != "COMUNIDAD DE MADRID" and ccaa["Descripcion"] != "MELILLA" and ccaa["Descripcion"] != "ADM.GENERAL DEL ESTADO"]

    selector =  dbc.Card([
                    dbc.CardBody(dcc.Dropdown(
                                id = "selector-ccaa",
                                options= options_dict,
                                clearable=False,
                                className="app-stock-selector",
                                placeholder= "Selecciona o introduce Comunidad Autónoma", 
                                style = {"font-size": "15px","font-family": "Arial, sans-serif", "maxHeight": "500px"}))],
                                className="mt4",
                                style = {"border": "none",
                                    "borderRadius": "0",
                                    "width": "100%",
                                    "height": "70px",
                                    "boxShadow": "none"})

    return selector