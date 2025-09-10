from dash import Dash, html

# Instancia de la aplicación Dash
app = Dash(__name__)

# Contenedor de la aplicación, todos los contenidos están adentro de un Div
contenido = html.Div(["¡Hola Dash!"])

# Layout de la app
app.layout = contenido

# Ejecución de la app
if __name__ == "__main__":
    app.run(debug=True)  # Forma correcta en Dash 3.x seria app.run(debug=True) pero ponemos run_server para compatibilidad con servidores