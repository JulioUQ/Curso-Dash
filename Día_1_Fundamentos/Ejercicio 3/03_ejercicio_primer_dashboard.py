import sys
import os

# Sube dos niveles desde /Día_1_Fundamentos/Ejercicio 3/
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

# Importa las funciones personalizadas desde utils
import utils.functions_Python_BBDD as f

# Importa las bibliotecas necesarias de Dash
from dash import Dash, html, dcc

# Importa componentes de Bootstrap para Dash
import dash_bootstrap_components as dbc

# Importa los módulos del Dashboard
from moduls import graf_capturas_censo as gcc
from moduls import tabla_desembarques as td
from moduls import mapa_desembarques as md

# Crea una instancia de la aplicación Dash con un tema de Bootstrap
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # Puedes añadir varios temas si quieres
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]  # Hace que la app sea responsive
)

# Layout de la aplicación (Estructura de la página)

## Un título principal
titulo = html.H1("Mi primer Dashboard con Dash")

## Un párrafo de resumen
resumen = html.P("Usamos Dash para crear aplicaciones web interactivas en Python.")

## Generamos el contenido en una fila Bootstrap
contenido = html.Div([
    dbc.Row([
        dbc.Col(gcc.graf_capturas_censo(), width=4),
        dbc.Col(td.tabla_d(), width=4),
        dbc.Col(md.mapa(), width=4),
    ])
])

# Componente que muestra un indicador de carga mientras se renderiza el contenido
app.layout = dcc.Loading(
    type="circle",
    fullscreen=True,
    children=[titulo, resumen, contenido]
)

# CALLBACKS
#-----------#

# Ejecución de la aplicación
if __name__ == '__main__':
    app.run(debug=True)
