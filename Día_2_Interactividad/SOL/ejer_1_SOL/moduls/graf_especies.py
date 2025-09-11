import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import Dash, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import functions as f # type: ignore


def graf_especies(value):
    data= f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.notas_venta WHERE año = 2024")

    data = data[data["unidadproductiva"] != "Instalación de acuicultura"]

    data = data[data["IdCCAA"] == value]
    data = data.groupby(['Especie'])[["peso", "importe"]].sum().reset_index().sort_values(by= "peso", ascending = False)

    total = data["peso"].sum()
    data["porcentaje"] = data["peso"] / total * 100

    data["especie_agrupada"] = data.apply(lambda row: f"{row["Especie"]}" if row["porcentaje"] >= 5 else "Otros < 5%", axis = 1)

    pie = px.pie(data, names= "especie_agrupada", values = "peso", color_discrete_sequence = px.colors.sequential.RdBu_r)
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
    
    fig_pie = dcc.Graph(figure= pie, id= "graf-pie", style= {"width": "100%", "height": "100%"})

    return fig_pie