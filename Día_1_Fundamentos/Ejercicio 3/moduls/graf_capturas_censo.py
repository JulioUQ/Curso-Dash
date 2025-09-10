import sys
import os

# Ruta a Día_1_Fundamentos (dos niveles arriba)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_dir)

from dash import dcc
import plotly.express as px
import pandas as pd
import utils.functions_Python_BBDD as f

def graf_capturas_censo():
    # Consulta a la BBDD
    data = f.ejecutar_consulta_sql(
        "SELECT * FROM cm.ccaa_desembarques",
        database_key="SGP_CUADROSMANDO"
    )
    
    # Filtrar y procesar datos
    data = data[data['Año'] == 2024]
    data = data.groupby(['Censo']).agg({'Peso': 'sum'}).reset_index()
    data = data.sort_values(by='Peso', ascending=False).head(6)
    
    # Gráfico
    bar = px.bar(
        data,
        x='Censo',
        y='Peso',
        labels={'Censo': 'Censo', 'Peso': 'Peso (kg)'}
    )

    bar.update_layout(
        xaxis_title='',
        xaxis_tickangle=30,  # Rota las etiquetas del eje x para mejor legibilidad
        height = 500,
        margin=dict(l=10, r=20, t=0, b=0)  # Ajusta los márgenes para evitar recortes
    )
    
    fig_bar = dcc.Graph(figure=bar, id="graph-bar_capturas_censo")
    return fig_bar
