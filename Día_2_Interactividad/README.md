# 📊 Apuntes Día 2 - Interactividad y Callbacks en Dash

_Curso de Dashboards con Python_

---

## 🎯 Objetivos del Día 2

El segundo día del curso se enfocó en transformar dashboards estáticos en aplicaciones completamente interactivas, implementando filtros dinámicos y comunicación entre componentes mediante el sistema de **callbacks** de Dash.

---

## 1. Arquitectura Modular Avanzada 🏗️

### 1.1 Organización de Selectores

Creamos una nueva estructura que separa los **componentes de selección** (filtros) del resto de componentes:

```
📂 Proyecto_Dash/
├── 📁 utils/
│   ├── 🐍 functions.py              # Funciones de conexión BBDD
│   └── 🐍 selector_ccaa.py          # ⭐ NUEVO: Selector de CCAA
├── 📁 moduls/
│   ├── 🐍 graf_capturas_censo.py
│   ├── 🐍 mapa_desembarques.py
│   └── 🐍 tabla_desembarques.py
└── 📄 app_interactiva.py             # Dashboard principal
```

### 1.2 Imports y Configuración de Rutas

**Aspecto clave**: Configuración correcta de rutas para importar módulos desde diferentes directorios:

```python
import sys
import os
# Añadir el directorio padre al path para importar desde utils/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
from utils import functions as f  # type: ignore
```

---

## 2. Creación de Componentes de Filtrado 🔍

### 2.1 Selector de Comunidades Autónomas

#### Obtención de Datos

```python
# Consulta SQL para obtener CCAA disponibles
ccaas = f.consulta("""SELECT distinct Id, Descripcion FROM [SGP_SIPE].[cat].[CCAA]""")
ccaas = ccaas.sort_values(by="Descripcion")
```

#### Creación del Diccionario de Opciones

```python
# Filtrado de CCAA específicas y creación de opciones para dropdown
options_dict = [
    {'label': ccaa["Descripcion"], 'value': ccaa["Id"]} 
    for _, ccaa in ccaas.iterrows() 
    if ccaa["Descripcion"] not in ["CASTILLA Y LEÓN", "COMUNIDAD DE MADRID", "MELILLA"]
]
```

#### Componente Selector

```python
def selector_ccaa(id="selector-ccaa"):
    selector = dbc.Card([
        dbc.CardBody(dcc.Dropdown(
            id=id,
            options=options_dict,
            clearable=False,
            className="app-stock-selector",
            placeholder="Selecciona o introduce Comunidad Autónoma",
            style={"font-size": "15px", "font-family": "Arial, sans-serif", "maxHeight": "500px"}
        ))
    ], 
    className="mt4",
    style={"border": "none", "borderRadius": "0", "width": "100%", "height": "70px", "boxShadow": "none"})
    
    return selector
```

---

## 3. Reestructuración del Layout para Interactividad 🔄

### 3.1 Nuevo Layout con Menú Superior

```python
# Estructura de menú con título y selector
menu = dbc.Row([
    dbc.Col(html.H1("Ventas y Desembarques por CCAA", 
                   style={"textAlign": "center", "color": "#000000", "font-size": 40}), 
            width=9),
    dbc.Col(se.selector_ccaa(), width=3)
])

# Layout principal con loading y contenido dinámico
app.layout = dcc.Loading(
    type="circle", 
    fullscreen=True, 
    children=[menu, contenido]
)
```

### 3.2 Contenedor Dinámico

```python
# Contenedor que se actualizará dinámicamente
contenido = html.Div(dbc.Row(id="contenido"))
```

---

## 4. Sistema de Callbacks: El Corazón de la Interactividad ❤️

### 4.1 Concepto de Callback

Un **callback** es una función que se ejecuta automáticamente cuando cambian los valores de ciertos componentes de entrada (**Inputs**), actualizando los componentes de salida (**Outputs**).

### 4.2 Callback Principal - Filtrado por CCAA

```python
from dash.dependencies import Input, Output

@app.callback(
    Output("contenido", "children"),      # Qué componente se actualiza
    Input('selector-ccaa', 'value'),      # Qué desencadena la actualización
)
def update_content(value):
    if value is None:
        return ""                         # No mostrar nada si no hay selección
    
    # Generar contenido filtrado por la CCAA seleccionada
    # Todo el código de los gráficos va aquí, pero filtrado por 'value'
    return [componentes_filtrados]
```

### 4.3 Patrón de Callbacks Anidados

**Innovación del Día 2**: Creamos un segundo nivel de interactividad donde los gráficos reaccionan a la selección en la tabla:

```python
from dash.dependencies import Input, Output, State
from dash import exceptions

@app.callback(
    Output("pie-especies", "children"),
    Output("barras-provincias", "children"), 
    Output("line-buques", "children"),
    Input("selector-ccaa", "value"),          # Input 1: CCAA seleccionada
    Input("tabla-desembarques", "selected_rows"), # Input 2: Fila seleccionada en tabla
    State("tabla-desembarques", "data")       # State: Datos actuales de la tabla
)
def update_graphs(ccaa, selected_rows, table_data):
    if ccaa is None:
        raise exceptions.PreventUpdate    # Prevenir actualización innecesaria
    
    # Lógica condicional basada en selección
    if not selected_rows or len(selected_rows) == 0:
        puerto = None  # Mostrar datos agregados
    else:
        row_index = selected_rows[0]
        puerto = table_data[row_index]["PuertoBase"]  # Filtrar por puerto específico
    
    # Generar gráficos con doble filtrado: CCAA + Puerto
    especies = ge.graf_especies(ccaa, puerto)
    provincias = gp.provincias_desembarque(ccaa, puerto) 
    buques = gb.variacion_buques(ccaa, puerto)
    
    return especies, provincias, buques
```

---

## 5. Diferencias Clave: Input vs State vs Output 🔄

### 5.1 Input
- **Función**: Desencadena la ejecución del callback cuando cambia su valor
- **Uso**: Componentes que el usuario manipula activamente (dropdowns, sliders, botones)

### 5.2 State  
- **Función**: Proporciona datos actuales sin desencadenar el callback
- **Uso**: Obtener información contextual (como datos de una tabla)

### 5.3 Output
- **Función**: Define qué componente se actualizará con el resultado del callback
- **Uso**: Cualquier propiedad de cualquier componente (children, style, options, etc.)

---

## 6. Implementación de Interactividad en Componentes 🔗

### 6.1 Tabla Seleccionable

```python
# Configuración de tabla para permitir selección
dash_table.DataTable(
    data=data.to_dict('records'),
    columns=[{"name": i, "id": i} for i in data.columns],
    page_size=12,
    row_selectable="single",  # ⭐ Permite seleccionar UNA fila
    id="tabla-desembarques"
)
```

### 6.2 Contenedores Dinámicos en Layout

```python
# Reemplazo de componentes estáticos por IDs dinámicos
dbc.Col(dbc.Card([
    dbc.CardHeader(html.H4("Principales Provincias de Desembarque", 
                          style={"text-align": "center"})),
    dbc.CardBody(id="barras-provincias")  # ⭐ ID dinámico, no componente fijo
]), width=5),
```

---

## 7. Modificación de Módulos para Filtrado 🔧

### 7.1 Adaptación de Funciones

Todas las funciones de los módulos se modificaron para aceptar parámetros de filtrado:

```python
# Antes (estático)
def graf_especies():
    data = consulta_fija()
    return grafico

# Después (dinámico)  
def graf_especies(ccaa_id, puerto=None):
    data = f.consulta("SELECT * FROM tabla WHERE idccaa_base = ?", ccaa_id)
    if puerto:
        data = data[data["PuertoBase"] == puerto]
    return grafico_filtrado
```

### 7.2 Patrones de Filtrado

```python
# Filtrado condicional en las consultas
data = data[data["idccaa_base"] == value]           # Filtro obligatorio por CCAA
if puerto:
    data = data[data["PuertoBase"] == puerto]       # Filtro opcional por puerto
```

---

## 8. Flujo de Interactividad Completo 🌊

### Diagrama de Flujo

```
Usuario selecciona CCAA → Callback 1 ejecuta → Actualiza tabla y gráficos base
                                    ↓
Usuario selecciona fila tabla → Callback 2 ejecuta → Actualiza gráficos específicos
```

### Casos de Uso

1. **Caso inicial**: Usuario entra → No hay selección → Contenido vacío
2. **Caso básico**: Usuario selecciona CCAA → Mostrar todos los puertos de esa CCAA
3. **Caso avanzado**: Usuario selecciona puerto específico → Mostrar detalles de ese puerto

---

## 9. Conceptos Avanzados Introducidos 🎯

### 9.1 PreventUpdate
```python
if ccaa is None:
    raise exceptions.PreventUpdate  # Evita ejecutar callback innecesariamente
```

### 9.2 Múltiples Outputs
```python
@app.callback(
    Output("componente1", "children"),
    Output("componente2", "children"),  # Un callback puede actualizar múltiples componentes
    Output("componente3", "children"),
    # ... inputs
)
```

### 9.3 Callbacks Encadenados
- **Callback 1**: Selector → Contenido principal
- **Callback 2**: Contenido principal + Selección tabla → Gráficos específicos

---

## 10. Ejercicio Propuesto: Filtro de Año 📅

### Reto para los Alumnos

Implementar un filtro adicional de año que:

1. **Se ubique** junto al selector de CCAA en el menú
2. **Filtre** todos los datos mostrados
3. **Interactúe** con los filtros existentes

### Pasos Sugeridos

1. Crear `selector_año.py` en utils/
2. Añadir al menú superior
3. Modificar callbacks para incluir el nuevo Input
4. Adaptar consultas SQL para filtrar por año

---

## 💡 Conclusiones del Día 2

El segundo día transformó completamente la naturaleza de nuestro dashboard:

- **✅ Interactividad real**: Los usuarios pueden explorar datos dinámicamente
- **✅ Sistema de callbacks**: Dominio del patrón Input/Output/State de Dash  
- **✅ Arquitectura escalable**: Estructura que permite agregar más filtros fácilmente
- **✅ UX mejorada**: Experiencia de usuario fluida con retroalimentación visual
- **✅ Comunicación entre componentes**: Los elementos del dashboard "hablan" entre sí

**Resultado**: Un dashboard completamente interactivo donde cada selección del usuario desencadena actualizaciones inteligentes en tiempo real, creando una experiencia de análisis de datos dinámica y profesional.

---

## 🚀 Próximos Pasos

Con estos fundamentos de interactividad, el dashboard está listo para:
- Filtros adicionales (fecha, categorías, etc.)
- Gráficos más complejos
- Exportación de datos filtrados
- Personalización avanzada de la interfaz