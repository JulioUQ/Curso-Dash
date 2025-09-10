import sys
import os

# Ruta raíz del directorio (Ejercicio 3)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_dir)

from dash import html
import dash_bootstrap_components as dbc
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
        bi.IdPuertoBase AS IdPuerto
    FROM [censo].[BuqueEstado] be
        INNER JOIN [censo].[BuqueIdentificacion] bi ON be.IdBuque = bi.IdBuque
        INNER JOIN [fenix].[Puerto] p_in ON bi.IdPuertoBase = p_in.Id
        INNER JOIN [cat].[Provincia] pr ON pr.Id = p_in.IdProvincia
    WHERE GETDATE() BETWEEN be.FcEfectoInicial AND be.FcEfectoFinal
      AND GETDATE() BETWEEN bi.FcEfectoInicial AND bi.FcEfectoFinal
      AND be.IdTipoEstado IN (1, 5)
    GROUP BY bi.IdPuertoBase
) AS A
INNER JOIN [fenix].[Puerto] prt ON A.IdPuerto = prt.Id;
"""


import folium
from folium.plugins import Fullscreen
from shapely import wkt
import pandas as pd
from dash import html
import utils.functions_Python_BBDD as f

query = f"""
SELECT 
    prt.Descripcion, 
    prt.Coordenadas.STAsText() AS Coordenadas
FROM (
    SELECT 
        bi.IdPuertoBase AS IdPuerto
    FROM [censo].[BuqueEstado] be
        INNER JOIN [censo].[BuqueIdentificacion] bi ON be.IdBuque = bi.IdBuque
        INNER JOIN [fenix].[Puerto] p_in ON bi.IdPuertoBase = p_in.Id
        INNER JOIN [cat].[Provincia] pr ON pr.Id = p_in.IdProvincia
    WHERE GETDATE() BETWEEN be.FcEfectoInicial AND be.FcEfectoFinal
      AND GETDATE() BETWEEN bi.FcEfectoInicial AND bi.FcEfectoFinal
      AND be.IdTipoEstado IN (1, 5)
    GROUP BY bi.IdPuertoBase
) AS A
INNER JOIN [fenix].[Puerto] prt ON A.IdPuerto = prt.Id;
"""


def mapa():
    sqlstr = f"""
        Select prt.Descripcion, prt.Coordenadas.STAsText() as Coordenadas from
        (select bi.IdPuertoBase IdPuerto from [censo].[BuqueEstado] be inner join [censo].[BuqueIdentificacion] bi on be.IdBuque=bi.idbuque 
        inner join fenix.Puerto prt on bi.IdPuertoBase=prt.id
        inner join cat.Provincia pr on pr.id=prt.IdProvincia
        where  GETDATE() between be.FcEfectoInicial and be.FcEfectoFinal and
            GETDATE() between bi.FcEfectoInicial and bi.FcEfectoFinal and 
            idtipoestado in (1,5) 
        group  by bi.IdPuertoBase) A
        inner join fenix.Puerto prt on A.IdPuerto=prt.id
        """

    data = f.ejecutar_consulta_sql(sqlstr, database_key="SGP_SIPE")
    data = data.rename(columns= {"Descripcion": "PuertoDesembarque"})
    data = data.dropna()

    data_buques = f.ejecutar_consulta_sql("SELECT * FROM cm.ccaa_desembarques", database_key="SGP_CUADROSMANDO")
    data_buques = data_buques[data_buques["Año"] == 2024]
    data_buques = data_buques.groupby("PuertoDesembarque")["Peso"].sum().reset_index()

    data_total = pd.merge(data, data_buques, how = "left", on = "PuertoDesembarque")

    # Calcular centro
    data["geometry"] = data["Coordenadas"].apply(wkt.loads) # type: ignore
    data["lat"] = data["geometry"].apply(lambda x: x.y)
    data["lon"] = data["geometry"].apply(lambda x: x.x)
    center_lat = data["lat"].mean()
    center_lon = data["lon"].mean()

    mapa = folium.Map(location=[center_lat, center_lon], zoom_start=4, height= 450)

# Añadir marcadores al mapa
    for _, row in data_total.iterrows():
        # Convertir la coordenada WKT a un objeto de Shapely
        coordenada = wkt.loads(row["Coordenadas"])
        
        # Obtener latitud y longitud
        lat, lon = coordenada.y, coordenada.x # type: ignore
        
        # Añadir el marcador en el mapa
        folium.CircleMarker(
            location=[lat, lon],
            radius=5 + row["Peso"] / 1000 * 0.001,  
            color="#2e86de",
            fill=True,
            fill_color="#3498db",
            fill_opacity=0.6,
            popup=f'{row["PuertoDesembarque"]}<br>Peso desembarque: {row["Peso"] / 1000} T'
        ).add_to(mapa)

    # Mostrar el mapa
    Fullscreen(position="topright").add_to(mapa)
    map_html_content = mapa.get_root().render()
   
    return dbc.Card(
        dbc.CardBody(
            html.Iframe(
                srcDoc=map_html_content,
                width="100%",  
                height=450,  
                style={"border": "none", "height": "100%"}  
            ),
            style={"height": "450px", "padding": "0px", "width": "100%", "display": "flex", "justify-content": "center", "align-items": "center"}  
        ),
        style={"padding": "0px", "border": "none", "height": "100%", "display": "flex", "justify-content": "center", "align-items": "center"}  
    )
