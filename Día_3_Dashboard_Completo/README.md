# DÍA 3 - CURSO DASH PYTHON
## Pestañas, Descargas y Generación de Informes

---

## 1. CREACIÓN DE PESTAÑAS (TABS)

### 1.1 Estructura básica de tabs
```python
import dash_bootstrap_components as dbc
from dash import dcc, html

# Definición de las pestañas
tabs = dbc.Row(html.Div([
    dcc.Tabs(
        id="tabs-dash",
        value='tab1',  # Pestaña activa por defecto
        children=[
            dcc.Tab(
                label='Información General', 
                value='tab1',
                style={
                    'display': 'flex', 
                    'alignItems': 'center', 
                    'justifyContent': 'center'
                }
            ),
            dcc.Tab(
                label='Otra Información', 
                value='tab2',
                style={
                    'display': 'flex', 
                    'alignItems': 'center', 
                    'justifyContent': 'center'
                }
            ),
        ]
    )
]))
```

### 1.2 Callback para manejar pestañas
```python
@app.callback(
    Output("contenido", "children"),
    [Input('selector-ccaa', 'value'),
     Input("tabs-dash", "value")]
)
def update_content(value, tab):
    if value is None:
        return html.Div("Seleccione una CCAA")
    
    # Contenido específico para cada pestaña
    if tab == "tab1":
        contenido = html.Div([
            html.H3("Información General"),
            # Componentes de la primera pestaña
        ])
        return contenido
    
    elif tab == "tab2":
        contenido = html.Div([
            html.H3("Otra Información"),
            # Componentes de la segunda pestaña
        ])
        return contenido
```

**📝 Conceptos clave:**
- `dcc.Tabs`: Contenedor principal de las pestañas
- `dcc.Tab`: Cada pestaña individual
- `value`: Identificador único de cada pestaña
- El callback debe incluir el input de las pestañas para detectar cambios

---

## 2. BOTONES DE DESCARGA

### 2.1 Creación del menú con botones
```python
menu = dbc.Row([
    dbc.Col(
        html.H1(
            "Ventas y Desembarques por CCAA", 
            style={
                "textAlign": "center", 
                "color": "#000000", 
                "font-size": 40
            }
        ), 
        width=9
    ),
    dbc.Col(se.selector_ccaa(), width=3),
    dbc.Col([
        # Botón descarga Excel
        dbc.Button(
            "Descargar Excel", 
            id="boton-descarga-excel",
            color="primary", 
            outline=True, 
            n_clicks=0
        ),
        dcc.Download(id="descargar-datos-excel"),
        
        # Botón descarga Informe
        dbc.Button(
            "Descargar Informe", 
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
        "justifyContent": "space-around",
        "marginLeft": "40px",
        "marginRight": "0px",
        "padding": "0px",
        "marginTop": "10px"
    })
])
```

### 2.2 Componente de contenido
```python
contenido = html.Div(dbc.Row(id="contenido"))
```

---

## 3. FUNCIONES DE OBTENCIÓN DE DATOS

### 3.1 Datos de buques
```python
def get_data_buques(value, puerto=None):
    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.historico_flota")
    data = data[data["IdCcaa"] == value]
    
    if puerto:
        data = data[data["puerto"] == puerto]
    
    data = data.groupby("año")["buques"].sum().reset_index()
    return data
```

### 3.2 Datos de especies
```python
def get_data_especies(value, puerto=None, informe=False):
    data = f.consulta("""
        SELECT * FROM SGP_CUADROSMANDO.cm.ccaa_desembarques 
        WHERE año = 2024
    """)
    data = data[data["idccaa_base"] == value]
    
    if puerto:
        data = data[data["PuertoBase"] == puerto]
    
    data = data.groupby(['Especie'])[["Peso", "valor"]].sum().reset_index()
    data = data.sort_values(by="Peso", ascending=False)
    
    # Para informes: solo top 10
    if informe:
        data = data.nlargest(10, "Peso")
    
    return data
```

### 3.3 Datos de provincias
```python
def get_data_provincias(value, puerto=None):
    data = f.consulta("SELECT * FROM SGP_CUADROSMANDO.cm.ccaa_desembarques")
    data = data[data["Año"] == 2024]
    data = data[data["idccaa_base"] == value]
    
    if puerto:
        data = data[data["PuertoBase"] == puerto]
    
    data = data.groupby("ProvinciaDesembarque")["valor"].sum().reset_index()
    
    return data
```

**🔧 Patrones importantes:**
- Todas las funciones tienen parámetros `value` (CCAA) y `puerto` opcionales
- Se aplican filtros condicionales según los parámetros
- Las funciones devuelven DataFrames procesados y agrupados

---

## 4. DESCARGA DE ARCHIVOS EXCEL

### 4.1 Callback de descarga Excel
```python
@app.callback(
    Output("descargar-datos-excel", "data"),
    [Input("boton-descarga-excel", "n_clicks"),
     Input("selector-ccaa", "value"),
     Input("tabla-desembarques", "selected_rows"),
     State("tabla-desembarques", "data")],
    prevent_initial_call=True
)
```

### 4.2 Función de descarga Excel
```python
import io
import pandas as pd

def download_excel(n_clicks, ccaa, selected_rows, table_data):
    # Validaciones
    if not n_clicks:
        return None
    if not ccaa:
        return None
    
    # Determinar puerto seleccionado
    if not selected_rows or len(selected_rows) == 0:
        puerto = None
    else:
        row_index = selected_rows[0]
        puerto = table_data[row_index]["PuertoBase"]
    
    # Obtener datos
    data_buques = gb.get_data_buques(ccaa, puerto)
    data_especies = ge.get_data_especies(ccaa, puerto)
    data_provincias = gp.get_data_provincias(ccaa, puerto)
    data_desembarques = tb.get_data_desembarques(ccaa, puerto)
    
    # Diccionario con todos los datos
    dict_data = {
        "Buques": data_buques,
        "Especies": data_especies,
        "Provincias": data_provincias,
        "Desembarques": data_desembarques
    }
    
    # Crear archivo Excel en memoria
    output_excel = io.BytesIO()
    with pd.ExcelWriter(output_excel, engine="xlsxwriter") as writer:
        for key, df in dict_data.items():
            df.to_excel(
                writer, 
                sheet_name=key, 
                index=False, 
                startrow=1, 
                startcol=1
            )
        writer.book.close()
    
    output_excel.seek(0)
    return dcc.send_bytes(output_excel.read(), filename="Datos.xlsx")
```

**💾 Conceptos clave:**
- `io.BytesIO()`: Crear archivo en memoria
- `pd.ExcelWriter()`: Escribir múltiples hojas
- `dcc.send_bytes()`: Enviar archivo al cliente
- `prevent_initial_call=True`: Evitar ejecución inicial

---

## 5. GENERACIÓN DE INFORMES HTML

### 5.1 Callback de descarga informe
```python
@app.callback(
    Output("descargar-datos-informe", "data"),
    [Input("boton-descarga-informe", "n_clicks"),
     Input("selector-ccaa", "value"),
     Input("tabla-desembarques", "selected_rows"),
     State("tabla-desembarques", "data")],
    prevent_initial_call=True
)
def download_informe(n_clicks, ccaa, selected_rows, table_data):
    if not n_clicks or not ccaa:
        return None
    
    # Determinar puerto
    if not selected_rows or len(selected_rows) == 0:
        puerto = None
    else:
        row_index = selected_rows[0]
        puerto = table_data[row_index]["PuertoBase"]
    
    # Generar informe
    informe_nacional = inf.generar_informe(ccaa, puerto)
    output_informe = io.BytesIO(informe_nacional.encode("utf-8"))
    output_informe.seek(0)
    
    return dcc.send_bytes(
        output_informe.read(), 
        filename="Informe de caracterización.html"
    )
```

### 5.2 Archivo informe.py (utils)
```python
# Imports necesarios
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from moduls import tabla_desembarques as tb
from moduls import graf_especies as ge
from moduls import graf_provincias as gp
from moduls import graf_buques as gb
import functions as f
```

### 5.3 Función principal del informe
```python
def generar_informe(ccaa, puerto):
    # Obtener nombre de la CCAA
    nombre_ca = f.consulta(
        f"SELECT Descripcion FROM SGP_SIPE.cat.CCAA WHERE Id = {ccaa}"
    ).squeeze()
    
    # Determinar título
    titulo = puerto if puerto is not None else nombre_ca
    
    # Obtener datos en bruto
    data_buques = gb.get_data_buques(ccaa, puerto)
    data_especies = ge.get_data_especies(ccaa, puerto, True)  # informe=True
    data_provincias = gp.get_data_provincias(ccaa, puerto)
    data_desembarques = tb.get_data_desembarques(ccaa, puerto)
    
    # Convertir datos a HTML
    buques_html = data_buques.to_html(index=False)
    especies_html = data_especies.to_html(index=False)
    provincias_html = data_provincias.to_html(index=False)
    desembarques_html = data_desembarques.to_html(index=False)
    
    # Obtener gráficos como HTML
    graf_buques = gb.variacion_buques(ccaa, puerto, True)  # html=True
    graf_especies = ge.graf_especies(ccaa, puerto, True)
    graf_provincias = gp.provincias_desembarque(ccaa, puerto, True)
    
    # Generar contenido HTML completo
    contenido_html = generar_html_template(
        titulo, buques_html, desembarques_html, especies_html,
        graf_especies, provincias_html, graf_buques, graf_provincias
    )
    
    return contenido_html
```

---

## 6. MODIFICACIONES EN FUNCIONES EXISTENTES

### 6.1 Funciones de gráficos con salida HTML
```python
def graf_especies(ccaa, puerto=None, html=False):
    # ... código de generación del gráfico ...
    
    if html == True:
        fig_pie = pie.to_html(full_html=True)
        return fig_pie
    else:
        fig_pie = dcc.Graph(
            figure=pie, 
            id="pie-especies-fig", 
            style={"width": "100%", "height": "100%"}
        )
        return fig_pie
```

### 6.2 Patrón para todas las funciones de gráficos
```python
def variacion_buques(ccaa, puerto=None, html=False):
    # ... generación del gráfico ...
    
    if html == True:
        contenido = line.to_html(full_html=True)
        return contenido
    else:
        # Retornar componente Dash normal
        return dcc.Graph(figure=line, ...)
```

**🔄 Patrón de modificación:**
- Agregar parámetro `html=False` a todas las funciones de gráficos
- Usar `figura.to_html(full_html=True)` para HTML
- Mantener comportamiento original cuando `html=False`

---

## 7. PLANTILLA HTML DEL INFORME

### 7.1 Estructura CSS
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe de: {titulo}</title>
    <style>
        /* Configuración para impresión */
        @page {
            size: A4;
            margin: 20mm;
        }
        
        /* Estilos responsivos para pantalla */
        @media screen {
            html, body {
                width: 100%;
                height: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .container {
                width: 900px;
                min-height: 1100px;
                background: white;
                padding: 40px;
                margin: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }
        }
        
        /* Estilos para impresión */
        @media print {
            body {
                font-size: 11px;
            }
        }
        
        /* Estilos generales */
        body {
            font-family: Arial, sans-serif;
            color: #333;
            font-size: 15px;
        }
        
        h1 {
            text-align: center;
            border-bottom: 3px solid #8db9df;
            padding-bottom: 10px;
            color: #003c70;
        }
        
        h2, h3, h4 {
            color: #488cc6;
        }
        
        h2 {
            border-bottom: 3px solid #cfe3f8;
        }
        
        /* Estilos para tablas */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        
        th, td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }
        
        th {
            background-color: #0073e6;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f7f7f7;
        }
    </style>
</head>
```

### 7.2 Contenido HTML
```html
<body>
    <div class="container">
        <h1>Informe de caracterización de: {titulo}</h1>
        
        <div class="section">
            <h2>1. Análisis de la flota: {titulo}</h2>
            <h3>1.1 Evolución del Nº de buques:</h3>
            <p>{buques_html}</p>
            <p>{graf_buques}</p>
        </div>
        
        <div class="section">
            <h2>2. Peso y valor desembarcados</h2>
            <p>{desembarques_html}</p>
        </div>
        
        <div class="section">
            <h2>3. Especies principales:</h2>
            <div style="display: flex; gap: 10px;">
                <div style="flex: 1;">{especies_html}</div>
                <div style="flex: 1;">{graf_especies}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>4. Provincias de desembarque:</h2>
            <p>{provincias_html}</p>
            <p>{graf_provincias}</p>
        </div>
    </div>
</body>
</html>
```

---

## 8. PUNTOS CLAVE Y MEJORES PRÁCTICAS

### 8.1 Gestión de estado
- Usar `State` para datos que no deben disparar callbacks
- `prevent_initial_call=True` para evitar ejecuciones innecesarias
- Validar siempre inputs antes de procesamiento

### 8.2 Manejo de archivos
- Usar `io.BytesIO()` para archivos en memoria
- `seek(0)` para resetear el puntero del archivo
- Codificación UTF-8 para textos en español

### 8.3 Flexibilidad de funciones
- Parámetros opcionales (`puerto=None`, `html=False`)
- Funciones que sirven para múltiples propósitos
- Filtrado condicional de datos

### 8.4 CSS responsivo
- `@media` queries para diferentes dispositivos
- Estilos específicos para impresión
- Flexbox para layouts adaptativos

---

## 9. FLUJO COMPLETO DEL DÍA 3

1. **Crear pestañas** → Organizar contenido en secciones
2. **Implementar callbacks** → Manejar navegación entre pestañas
3. **Agregar botones de descarga** → Excel e informes HTML
4. **Desarrollar funciones de datos** → Obtener información filtrada
5. **Crear sistema de descarga Excel** → Múltiples hojas de datos
6. **Implementar generación de informes** → HTML con CSS profesional
7. **Modificar funciones existentes** → Soporte para salida HTML
8. **Probar funcionalidades** → Validar descargas y formatos

Este día integra todos los conocimientos previos y añade capacidades avanzadas de exportación y generación de reportes profesionales.