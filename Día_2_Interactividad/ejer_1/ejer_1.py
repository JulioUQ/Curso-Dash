from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

from moduls import tabla_desembarques as tb #type: ignore
from moduls import graf_especies as ge #type: ignore
from moduls import graf_provincias as gp #type: ignore
from moduls import graf_buques as gb #type: ignore

from utils import selector_ccaa as sc # type:ignore
#-------------------------------------------#

# Instanciar la app
app = Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP], meta_tags = [{"name": "viewport", "content": "width, initial-scale=1"}])

# Contenido
menu = dbc.Row([dbc.Col(html.H1("Ventas y Desembarques", style={"textAlign": "center",
                                                     "color": "#000000",
                                                     "font-size": 40}
                                                     ), width = 9),
                dbc.Col(sc.selector_ccaa(), width = 3)])

contenido = html.Div([dbc.Row(id = "contenido")])



# Layout (estructura)
app.layout = dcc.Loading(type= "circle", fullscreen= True, children= [menu, contenido])

#------------------------------------------------------------#
# CALLBACKS (interactividad)
# Configuramos los callbacks para que la app sea interactiva
# La funcion debe devolver un elemento por Output, es decir además de contenido devolveria el resto de elemntos
#------------------------------------------------------------#
@app.callback(
    Output("contenido", "children"),
    Input("selector-ccaa", "value")
)   

def update_content(ccaa):
    if ccaa is None:
        return html.P("Seleccione una CCAA")
    
    contenido = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H4("Principales Especies", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                dbc.CardBody(ge.graf_especies())
                ]), width= 3),

            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H4("Principales puertos de Desembarque", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                dbc.CardBody(tb.tabla_desembarques())
                ]), width= 4),

            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H4("Principales Provincias de Desembarque", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                dbc.CardBody(gp.provincias_desembarque())
                ]), width= 5),
        ], style= {"paddingBottom": "20px"}),
        dbc.Row([
            dbc.Card([dbc.CardHeader(html.H4("Variación del Número de Buques", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                    dbc.CardBody(gb.variacion_buques())
                    ])
        ])
    ], style= {"padding": "20px"})
    
    return contenido

#--------------
#--------------
#--------------

# Ejecución de la app
#-------------------------------------------#
if __name__ == "__main__":
    app.run(debug= True)