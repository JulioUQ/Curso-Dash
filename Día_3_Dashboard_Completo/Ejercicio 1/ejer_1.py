from dash import Dash, html, dcc, exceptions
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
import io

from moduls import tabla_desembarques as tb #type: ignore
from moduls import graf_especies as ge #type: ignore
from moduls import graf_provincias as gp #type: ignore
from moduls import graf_buques as gb #type: ignore

from utils import selector_ccaa as se #type: ignore
from utils import informe as inf # type:ignore
#-------------------------------------------#

# Instanciar la app
app = Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP], meta_tags = [{"name": "viewport", "content": "width, initial-scale=1"}])

# Contenido
menu = dbc.Row([
    dbc.Col(html.H1("Ventas y Desembarques por CCAA", style={"textAlign": "center", "color": "#000000", "font-size": 40}), width = 7),
    dbc.Col(se.selector_ccaa(), width= 3),
    dbc.Col([
        dbc.Button("Descargar Excel", id= "boton-descarga-excel", color= "primary", outline = True, n_clicks = 0),
            dcc.Download(id = "descargar-datos-excel"),

        dbc.Button("Descargar Informe", id= "boton-descarga-informe", color= "primary", outline = True, n_clicks = 0),
            dcc.Download(id = "descargar-datos-informe")
    ], width = 2, style = {
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-around"
    })                                                 
])

tabs= dbc.Row([html.Div([
    dcc.Tabs(
        id= "tabs-dash",
        value = "tab1",
        children= [
            dcc.Tab(label ="Información General", value=  "tab1", style= {"display": "flex", 
                                                                          "alignItems": "center", "justifyContent": "center"}),
            dcc.Tab(label ="Otra información", value=  "tab2", style= {"display": "flex", 
                                    "alignItems": "center", "justifyContent": "center"}),

            dcc.Tab(label ="Otra tercera información", value=  "tab3", style= {"display": "flex", 
                                 "alignItems": "center", "justifyContent": "center"})
        ]
    )
])])


contenido = html.Div(dbc.Row(id= "contenido"))

# Layout (estructura)
app.layout = dcc.Loading(type= "circle", fullscreen= True, children= [menu, tabs, contenido])

@app.callback(
    Output("contenido", "children"),
    Input('selector-ccaa', 'value'), 
    Input("tabs-dash", "value")
)
def update_content(value, tab):
    if value is None:
        return html.P("Selecciona una Comunidad Autónoma", style= {"text-align": "center", "fontSize": 20, "fontFamily": "Arial", "paddingTop": "50px"})

    if tab == "tab1":
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

    elif tab == "tab2":
        contenido = html.P("CONTENIDO DE LA TAB 2")  

    elif tab == "tab3":
        contenido = html.P("CONTENIDO DE LA PESTAÑA 3")


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

#-----------------------------------------#
# DESCARGAR EXCEL

@app.callback(
    Output("descargar-datos-excel", "data"),
    Output("boton-descarga-excel", "n_clicks"),
    Input("boton-descarga-excel", "n_clicks"),
    Input("selector-ccaa", "value"),
    Input("tabla-desembarques", "selected_rows"),
    State("tabla-desembarques", "data"),
    prevent_initial_call = True
)
def download_excel(n_clicks, ccaa, selected_rows, table_data):
    if not n_clicks:
        return None
    
    if not ccaa:
        return None
    
    if not selected_rows or len(selected_rows) == 0:
        puerto = None
    else:
        row_index = selected_rows[0]
        puerto = table_data[row_index]["PuertoBase"]

    data_buques = gb.get_data_buques(ccaa, puerto)
    data_especies = ge.get_data_especies(ccaa, puerto)
    data_provincias = gp.get_data_provicias(ccaa, puerto)
    data_desembarques = tb.get_data_desembarques(ccaa, puerto)

    dict_data = {
        "Buques": data_buques,
        "Especies": data_especies,
        "Provincias": data_provincias,
        "Desembarques": data_desembarques
    }

    output_excel = io.BytesIO()

    with pd.ExcelWriter(output_excel, engine= "xlsxwriter") as writer:
        for key, df in dict_data.items():
            df.to_excel(writer, sheet_name = key, index = False, startrow= 1, startcol= 1)

        writer.book.close()
        output_excel.seek(0)

    return (dcc.send_bytes(output_excel.read(), filename = "Datos.xlsx")), 0 # type: ignore
        
#--------------------------------------------------------------#
# Descargar informe

@app.callback(
    Output("descargar-datos-informe", "data"),
    Output("boton-descarga-informe", "n_clicks"),
    Input("boton-descarga-informe", "n_clicks"),
    Input("selector-ccaa", "value"),
    Input("tabla-desembarques", "selected_rows"),
    State("tabla-desembarques", "data"),
    prevent_initial_call = True
)
def download_informe(n_clicks, ccaa, selected_rows, table_data):
    if not n_clicks:
        return None
    
    if not ccaa:
        return None
    
    if not selected_rows or len(selected_rows) == 0:
        puerto = None
    else:
        row_index = selected_rows[0]
        puerto = table_data[row_index]["PuertoBase"]

    informe_nacional = inf.generar_informe(ccaa, puerto)

    output_informe = io.BytesIO(informe_nacional.encode("utf-8"))
    output_informe.seek(0)

    return (dcc.send_bytes(output_informe.read(), filename = "Informe de caracterización.html")), 0 # type: ignore


# Ejecución de la app
#-------------------------------------------#
if __name__ == "__main__":
    app.run(debug= True)