import sys
import os

# Ruta raíz del directorio (Ejercicio 3)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_dir)

from dash import html
import folium
from folium.plugins import Fullscreen
from shapely import wkt
import pandas as pd
import utils.functions_Python_BBDD as f


query = f"""
SELECT 
    prt.Descripcion, 
    prt.Coordenadas.STAsText() AS Coordenadas
FROM (
    SELECT 
        bi.IdPuertoBase
    FROM [censo].[BuqueEstado] be
        INNER JOIN [censo].[BuqueIdentificacion] bi ON be.IdBuque = bi.IdBuque
        INNER JOIN [fenix].[Puerto] p_in ON be.IdPuertoBase = p_in.Id
        INNER JOIN [cat].[Provincia] pr ON p_in.IdProvincia = pr.Id
    WHERE GETDATE() BETWEEN be.FechaInicial AND be.FcEfectoFinal
          AND be.IdTipoEstado IN (1, 5)
    GROUP BY bi.IdPuertoBase
) AS A
INNER JOIN [fenix].[Puerto] prt ON A.IdPuertoBase = prt.Id;
"""


def mapa():
    df = f.ejecutar_consulta_sql(query, database_key="SGP_CUADROSMANDO")

    df = df.rename(columns={"Descripcion": "PuertoDesembarque"})
    df = df.dropna()

    df_desembarques = f.ejecutar_consulta_sql(
        "SELECT * FROM cm.ccaa_desembarques WHERE Año = 2024",
        database_key="SGP_CUADROSMANDO"
    )
    df_desembarques = df_desembarques.groupby(["CCAADesembarque"]).agg({"Peso": "sum"}).reset_index()
    df_desembarques = df_desembarques.sort_values(by="Peso", ascending=False)

    data_total = pd.merge(df, df_desembarques, on="PuertoDesembarque", how="left")    

