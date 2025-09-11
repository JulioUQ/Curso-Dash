from dash import Dash, html, dcc, exceptions
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State

from moduls import tabla_desembarques as tb #type: ignore
from moduls import graf_especies as ge #type: ignore
from moduls import graf_provincias as gp #type: ignore
from moduls import graf_buques as gb #type: ignore

from utils import selector_ccaa as se #type: ignore
#-------------------------------------------#

# Instanciar la app
app = Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP], meta_tags = [{"name": "viewport", "content": "width, initial-scale=1"}])

# Contenido
menu = dbc.Row([
    dbc.Col(html.H1("Ventas y Desembarques por CCAA", style={"textAlign": "center", "color": "#000000", "font-size": 40}), width = 9),
    dbc.Col(se.selector_ccaa(), width= 3)                                                 
])


contenido = html.Div(dbc.Row(id= "contenido"))

# Layout (estructura)
app.layout = dcc.Loading(type= "circle", fullscreen= True, children= [menu, contenido])

@app.callback(
    Output("contenido", "children"),
    Input('selector-ccaa', 'value'), 
)
def update_content(value):
    if value is None:
        return html.P("Selecciona una Comunidad Autónoma", style= {"text-align": "center", "fontSize": 20, "fontFamily": "Arial", "paddingTop": "50px"})

    contenido = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H4("Principales Especies", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                dbc.CardBody(id="pie-especies")
                ]), width= 3),

            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H4("Desembarques por Puerto Base", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                dbc.CardBody(tb.tabla_desembarques(value))
                ]), width= 4),

            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H4("Principales Provincias de Desembarque", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                dbc.CardBody(id="barras-provincias")
                ]), width= 5),
        ]),
        dbc.Row([
            dbc.Card([dbc.CardHeader(html.H4("Variación del Número de Buques", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                    dbc.CardBody(id="line-buques")
                    ])
        ])
    ], style= {"padding": "20px"})

    return contenido

#-------------------------------------------#

@app.callback(
    Output("pie-especies", "children"),
    Output("barras-provincias", "children"),
    Output("line-buques", "children"),
    Input("selector-ccaa", "value"),
    Input("tabla-desembarques", "selected_rows"),
    State("tabla-desembarques", "data")
)
def update_graphs(ccaa, selected_rows, table_data):
    if ccaa is None:
        raise exceptions.PreventUpdate

    # Caso 1: no se ha seleccionado ninguna fila -> puerto=None
    if not selected_rows or len(selected_rows) == 0:
        puerto = None
    else:
        # Caso 2: fila seleccionada -> puerto correspondiente
        row_index = selected_rows[0]
        puerto = table_data[row_index]["PuertoBase"]

    # Generar gráficos
    especies = ge.graf_especies(ccaa, puerto)
    provincias = gp.provincias_desembarque(ccaa, puerto)
    buques = gb.variacion_buques(ccaa, puerto)

    return especies, provincias, buques

# Ejecución de la app
#-------------------------------------------#
if __name__ == "__main__":
    app.run_server(debug= True)