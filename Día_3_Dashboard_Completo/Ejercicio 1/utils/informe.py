import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd


from moduls import tabla_desembarques as tb #type: ignore
from moduls import graf_especies as ge #type: ignore
from moduls import graf_provincias as gp #type: ignore
from moduls import graf_buques as gb #type: ignore

import functions as f #type: ignore



def generar_informe(ccaa, puerto):
    nombre_ca = f.consulta(f"SELECT Descripcion FROM SGP_SIPE.cat.CCAA WHERE Id = {ccaa}").squeeze()

    if puerto is not None:
        titulo = puerto

    else:
        titulo = nombre_ca

    # Datos en bruto
    data_buques = gb.get_data_buques(ccaa, puerto)
    data_especies = ge.get_data_especies(ccaa, puerto, True)
    data_provincias = gp.get_data_provicias(ccaa, puerto)
    data_desembarques = tb.get_data_desembarques(ccaa, puerto)
    #------------------------------------------------------------#

    # Datos html
    buques_html = data_buques.to_html(index= False)
    especies_html = data_especies.to_html(index= False)
    provincias_html = data_provincias.to_html(index= False)
    desembarques_html = data_desembarques.to_html(index= False)
    #-------------------------------------------------------------#

    # graficos html
    graf_buques= gb.variacion_buques(ccaa, puerto, True)
    graf_especies = ge.graf_especies(ccaa, puerto, True)
    graf_provincias = gp.provincias_desembarque(ccaa, puerto, True)

    #-------------------------------------------------------------#


    contenido_html = f"""
    <!DOCTYPE html>
        <html lang = "es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <title>Informe de: {titulo}</title>

            <style>
            @page {{
                size: A4;
                margin: 20mm;
            }}

            @media screen {{
                html, body {{
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}

            .wrapper {{
                display: flex;
                justify-content: center;
                width: 100%;
            }}

            .container {{
                width: 900px; 
                min-height: 1100px;
                background: white;
                padding: 40px;
                margin: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
        }}

            @media print{{
                body {{
                    font-size: 11px;
                }}
            }}

            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
                font-size: 15px;
            }}

            .container {{
                max-width: 100%;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-sizing: border-box;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                margin: auto;
            }}

            h1 {{
                text-align: center;
                border-bottom: 3px solid #8db9df;
                padding-bottom: 10px;
                margin-bottom: 10px;
                color: #003c70;
            }}

            h2, h3, h4 {{
                color: #488cc6;
            }}

            h2 {{
                border-bottom: 3px solid #cfe3f8;
            }}

            h3 {{
                margin-left: 20px;
            }}

            h4 {{
                margin-left: 40px;
            }}

            .section {{
                margin-bottom: 25px;
                padding-bottom: 15px;
                border-bottom: 2px solid #ddd;
            }}

            p, ul {{
                line-height: 1.6;
            }}

            ul {{
                padding-left: 40px;
                list-style-type: circle;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}

            th, td {{
                padding: 10px;
                text-align: left;
                border: 1px solid #ddd;
            }}

            th {{
                background-color: #0073e6;
                color: white;
                font-weight: bold;
                text-align: left !important;
            }}

            tr:nth-child(even){{
                background-color: #f7f7f7;
            }}

            .highlight {{
            font-weight: bold;
            color: #d9534f;
            }}
            </style>
        </head>

        <body>
            <div class = "container">
                <h1>Informe de caracterización de: {titulo}</h1>

                <div class = "section">
                    <h2>1. Análisis de la de flota: {titulo}:</h2>
                        <h3>1.1 Evolución del Nº de buques:</h3>
                        <p>{buques_html}</p>
                        <p>{graf_buques}</p>
                    </div>            

                <div class = "section">
                    <h2>2.Peso y valor desembarcados</h2>
                    <p>{desembarques_html}</p>
                </div>

            <div class="section">
                <h2>3. Especies principales:</h2>
                <div style="display: flex; gap: 10px;">
                    <div style="flex: 1;">
                        {especies_html}
                    </div>
                    <div style="flex: 1;">
                        {graf_especies}
                    </div>
                </div>
            </div>
        
                <div class = "section">
                    <h2>4. Provincias de desembarque:</h2>
                    <p>{provincias_html}</p>
                    <p>{graf_provincias}</p>
                </div>
        </body>
        </html>
    """

    return contenido_html
