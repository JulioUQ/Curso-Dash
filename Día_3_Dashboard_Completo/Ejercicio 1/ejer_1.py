from dash import Dash, html, dcc, exceptions
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State 
import io

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
menu = dbc.Row([
    dbc.Col(
        html.H1(
            "Ventas y Desembarques",
            style={
                "textAlign": "center",
                "color": "#000000",
                "font-size": 40
            }
        ),
        width=7
    ),
    dbc.Col(
        sc.selector_ccaa(),
        width=3
    ),
    dbc.Col(
        [
            # Botón y descarga de Excel
            dbc.Button(
                "Descarga Excel",
                id="boton-descarga-excel",
                color="primary",
                outline=True,
                n_clicks=0
            ),
            dcc.Download(id="descargar-datos-excel"),

            # Botón y descarga de Informe
            dbc.Button(
                "Descarga Informe",
                id="boton-descarga-informe",
                color="primary",
                outline=True,
                n_clicks=0
            ),
            dcc.Download(id="descargar-datos-informe")
        ],
        width=2,
        style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-around"
        }
    )
])

# Pestañas
tabs = dbc.Row([
    html.Div([
        dcc.Tabs(
            id="tabs-dash",  # Para que al cambiar de pestaña se active un callback 
            value="tab-1",   # Será el input del callback por defecto
            children=[       # Cada uno de los tabs individuales (pestañas)
                dcc.Tab(
                    label="Información general",
                    value="tab-1",  # El valor es el que se usará en el callback
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center"
                    }
                ),
                dcc.Tab(
                    label="Otra información",
                    value="tab-2",  # El valor es el que se usará en el callback
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center"
                    }
                ),
                dcc.Tab(
                    label="Otra tercera información",
                    value="tab-3",  # El valor es el que se usará en el callback
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center"
                    }
                )
            ]
        )
    ])
])


contenido = html.Div([dbc.Row(id = "contenido")])

# Layout (estructura)
app.layout = dcc.Loading(type= "circle", fullscreen= True, children= [menu, tabs, contenido])

#------------------------------------------------------------#
# CALLBACKS (interactividad)
# Configuramos los callbacks para que la app sea interactiva
# La función debe devolver un elemento por Output, es decir además de contenido devolveria el resto de elementos
#------------------------------------------------------------#
@app.callback(
    Output("contenido", "children"),
    Input("selector-ccaa", "value"),
    Input("tabs-dash", "value")

)   

def update_content(ccaa, tab):
    if ccaa is None:
        return html.P("")
    

    if tab == "tab-1":

        contenido = html.Div([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Principales Especies", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                    dbc.CardBody(id= "graf-pie")
                    ]), width= 3),

                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Desembarque por PuertoBase", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                    dbc.CardBody(tb.tabla_desembarques(ccaa))
                    ]), width= 4),

                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Principales Provincias de Desembarque", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                    dbc.CardBody(id = "barras-provincia")
                    ]), width= 5),
            ], style= {"paddingBottom": "20px"}),
            dbc.Row([
                dbc.Card([dbc.CardHeader(html.H4("Variación del Número de Buques", style= {"text-align": "center"}), style= {"backgroundColor": "#f9feff"}),
                        dbc.CardBody(id= "line-buques")
                        ])
            ])
        ], style= {"padding": "20px"})
    
    elif tab == "tab-2":
        contenido = html.P("Contenido de la tab-2")

    elif tab == "tab-3":
        contenido = html.P("Contenido de la tab-3")

    return contenido


#-------------------------------------------#
# Callback para actualizar los tres gráficos
@app.callback(
    # Al ser un id de un componente de tarjeta, ponemos children
    Output("graf-pie", "children"), 
    Output("barras-provincia", "children"),
    Output("line-buques", "children"),

    Input("selector-ccaa", "value"), # El input es el mismo para los tres gráficos
    Input("tabla-desembarques", "selected_rows"), # Input para que se actualice al filtrar la tabla. Esto nos da el indice de la fila seleccionada
    State("tabla-desembarques", "data") # State para obtener los datos de la tabla, pudiendo asi obtener el puerto base seleccionado
)   

def update_graphs(ccaa, selected_rows, table_data):
    if ccaa is None:
        raise exceptions.PreventUpdate
    
    # Si no hay ninguna fila seleccionada, mostramos los datos de la CCAA
    if not selected_rows or len(selected_rows) == 0:
        puerto = None

    else: # Si hay una fila seleccionada, obtenemos el puerto base de esa fila
        row_index = selected_rows[0] # Obtenemos el indice de la fila seleccionada
        puerto = table_data[row_index]["PuertoBase"] # Obtenemos el puerto base de esa fila

    grafico_especies = ge.graf_especies(ccaa, puerto) # Gráfico de especies
    grafico_provincias = gp.provincias_desembarque(ccaa, puerto) # Gráfico de provincias
    grafico_buques = gb.variacion_buques(ccaa, puerto) # Gráfico de buques  

    return grafico_especies, grafico_provincias, grafico_buques



#-------------------------------------------#
# Callbacks para las descargas
@app.callback(
    Output("descargar-datos-excel", "data"), # El output es el id del componente de descarga
    Output("boton-descarga-datos", "n_clicks"), # Reiniciamos el número de clicks a 0 para que se pueda volver a descargar
    Input("boton-descarga-excel", "n_clicks"), # Cuando el número de clicks cambie, se ejecuta el callback
    Input("selector-ccaa", "value"), # El input es el mismo para los tres gráficos
    Input("tabla-desembarques", "selected_rows"), # Input para que se actualice al filtrar la tabla. Esto nos da el indice de la fila seleccionada
    State("tabla-desembarques", "data"), # State para obtener los datos de la tabla, pudiendo asi obtener el puerto base seleccionado
    prevent_initial_call= True
)

def descargar_excel(n_clicks, ccaa, selected_rows, table_data):
    if not n_clicks:
        return None
    
    if ccaa is None:
        return None
    
    # Si no hay ninguna fila seleccionada, mostramos los datos de la CCAA
    if not selected_rows or len(selected_rows) == 0:
        puerto = None

    else: # Si hay una fila seleccionada, obtenemos el puerto base de esa fila
        row_index = selected_rows[0] # Obtenemos el indice de la fila seleccionada
        puerto = table_data[row_index]["PuertoBase"] # Obtenemos el puerto base de esa fila
    
    # Obtenemos los datos de las tablas y gráficos
    data_buques = gb.get_data_buques(ccaa, puerto)
    data_provincias = gp.get_data_provincias_desembarque(ccaa, puerto)
    data_especies = ge.get_data_especies(ccaa, puerto)  
    data_tabla = tb.get_tabla_desembarques(ccaa)

    # Creamos un archivo Excel con los datos
    dict_data = {
        "Variación Buques": data_buques,
        "Especies": data_especies,
        "Provincias Desembarque": data_provincias,
        "Desembarques por Puerto": data_tabla
    }

    output_excel = io.BytesIO() # Manda la informacion en forma de bytes, y los genera y guarda en el componente


    # Usamos un contexto para crear el archivo Excel en memoria
    with pd.ExcelWriter(output_excel, engine="xlsxwriter") as writer: 
        for sheet_name, df in dict_data.items():
            df.to_excel(writer, sheet_name= sheet_name, index= False, startrow=1, startcol=1) # type: ignore
        writer.book.close() # type: ignore
        output_excel.seek(0) # Por temas de memoria, volvemos al inicio del archivo

    return (dcc.send_bytes(output_excel.read(), # type: ignore
                          filename= f"Datos_{ccaa}.xlsx")), 0 # Reiniciamos el número de clicks a 0 para que se pueda volver a descargar


#-------------------------------------------#
# Ejecución de la app
#-------------------------------------------#
if __name__ == "__main__":
    app.run(debug= True)