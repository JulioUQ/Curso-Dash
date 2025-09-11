import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import Dash, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import functions as f # type: ignore


def graf_especies(value, puerto = None):
    data= f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.ccaa_desembarques WHERE año = 2024")

    data = data[data["idccaa_base"] == value]

    if puerto:
        data = data[data["PuertoBase"] == puerto]

    data = data.groupby(['Especie'])[["Peso", "valor"]].sum().reset_index().sort_values(by= "Peso", ascending = False)

    total = data["Peso"].sum()
    data["porcentaje"] = data["Peso"] / total * 100

    data["especie_agrupada"] = data.apply(lambda row: f"{row["Especie"]}" if row["porcentaje"] >= 5 else "Otros < 5%", axis = 1)

    pie = px.pie(data, names= "especie_agrupada", values = "Peso", color_discrete_sequence = px.colors.sequential.RdBu_r)
    pie.update_traces(
        hovertemplate= (
            "Especie: %{label}<br>" +
            "Peso total: %{value:.2f} Kg<br>"
        )
    )


    pie.update_layout(
    margin = dict(l=0, r=0, t=0, b=0),
    legend=dict(
        orientation="h",   
        y=-0.1,           
        x=0.5,
        xanchor="center"
    ))
    
    fig_pie = dcc.Graph(figure= pie, id= "pie-especies-fig", style= {"width": "100%", "height": "100%"})

    return fig_pie