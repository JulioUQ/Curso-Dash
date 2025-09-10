# 📊 Apuntes Día 1 - Fundamentos de Dash

_Curso de Dashboards con Python_

---

## 🎯 Objetivos del Día 1

El primer día del curso se centró en establecer los fundamentos necesarios para desarrollar dashboards interactivos con Dash, abarcando desde los conceptos teóricos básicos hasta la implementación práctica de un dashboard completo con múltiples componentes.

---

## 1. Estructura Básica de una Aplicación Dash 🏗️

### Componentes Fundamentales

#### 1.1 Instanciación de la Aplicación

```python
from dash import Dash
app = Dash(__name__)
```

#### 1.2 Definición del Layout

El **layout** es la estructura visual de la aplicación. Define qué componentes se mostrarán y cómo se organizarán:

```python
from dash import html, dcc
app.layout = html.Div([
    html.H1("Mi Dashboard"),
    dcc.Graph(id="mi-grafico")
])
```

**Tipos de componentes:**

- **`dash.html`**: Elementos HTML (Div, H1, P, Button, etc.)
- **`dash.dcc`**: Componentes interactivos (Graph, Dropdown, Slider, etc.)
- **`dash_table`**: Tablas de datos interactivas
- **`dash_bootstrap_components`**: Componentes con estilos Bootstrap

#### 1.3 Ejecución de la Aplicación

```python
if __name__ == "__main__":
    app.run(debug=True)  # Puerto por defecto: 8050
```

### Flujo de Desarrollo

1. **Importar** Dash y componentes necesarios
2. **Crear** instancia de la aplicación
3. **Definir** el layout
4. **Ejecutar** la aplicación

---

## 2. Configuración de Base de Datos 🗄️

### 2.1 Instalación de Dependencias

Para conectar con bases de datos SQL Server, necesitamos:

```bash
pip install pyodbc sqlalchemy pandas
```

### 2.2 Configuración Externa

**Buena práctica**: Mantener credenciales fuera del código usando archivos de configuración:

**config.json:**

```json
{
  "common": {
    "Driver": "ODBC Driver 17 for SQL Server"
  },
  "SGP_SIPE_EXPLOTACION": {
    "Server": "MI_SERVIDOR",
    "Database": "MI_BASE",
    "UID": "usuario",
    "PWD": "contraseña"
  }
}
```

### 2.3 Función de Conexión

```python
def ejecutar_consulta_sql(query, database_key="SGP_SIPE_EXPLOTACION"):
    # Cargar configuración
    config = cargar_configuracion_json()
    
    # Construir cadena de conexión
    conn_str = f"DRIVER={config['Driver']};SERVER={config['Server']};..."
    conn_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}"
    
    # Ejecutar consulta
    engine = create_engine(conn_url)
    df = pd.read_sql_query(query, con=engine)
    return df
```

---

## 3. Implementación Práctica: Dashboard Completo 🚀

En la sesión práctica desarrollamos un dashboard con **tres componentes principales**:
### 3.1 Gráfico de Barras - Capturas por Censo

**Tecnologías**: Plotly + Dash
### 3.2 Tabla de Desembarques por Comunidad

**Tecnologías**: dash_table
### 3.3 Mapa Interactivo de Puertos

**Tecnologías**: Folium + dash_bootstrap_components + dash.html

---

## 4. Estructura del Dia 1 📁

### Organización de Archivos

```
📂 Proyecto_Dash/
├── 📁 config/
│   ├── 🔧 app-config-exp.json    # Configuración de conexión
│   └── 📁 __pycache__/
├── 📁 Ejercicio 1/
│   └── 📄 01_ejercicio_arquitectura_basica.py
├── 📁 Ejercicio 2/
│   └── 📄 02_ejercicio_conexion_BBDD.py
├── 📁 Ejercicio 3/
│   ├── 📁 moduls/
│   │   ├── 🐍 graf_capturas_censo.py       # Módulo gráfico barras
│   │   ├── 🐍 mapa_desembarques.py         # Módulo mapa
│   │   └── 🐍 tabla_desembarques.py        # Módulo tabla
│   └── 📄 03_ejercicio_primer_dashboard.py  # Dashboard principal
├── 📁 utils/
│   └── 🐍 functions_Python_BBDD.py         # Funciones de conexión
└── 📄 README.md
```

---

## 5. Conceptos Clave Aprendidos 🎯

### 5.1 Separación de Responsabilidades

- **Configuración**: Archivos JSON externos
- **Lógica de datos**: Funciones de conexión en `utils/`
- **Componentes visuales**: Módulos específicos en `moduls/`
- **Orquestación**: Script principal que integra todo

### 5.2 Flujo de Datos

```
Base de Datos → función SQL → DataFrame → Componente Dash → Layout → Aplicación Web
```

### 6.3 Interactividad vs Estaticidad

- **Componentes estáticos**: Se cargan una vez al iniciar la app, y al modificarlos solo hay que recargar la pagina en el navegador para visualizar los cambios.

---

## 💡 Conclusiones del Día 1

El primer día nos proporcionó una base sólida para el desarrollo de dashboards con Dash:

- **✅ Conceptos fundamentales** claros sobre qué es Dash y cómo funciona
- **✅ Conexión exitosa** con base de datos SQL Server
- **✅ Dashboard funcional** con tres tipos diferentes de visualizaciones
- **✅ Estructura de proyecto** profesional y escalable
- **✅ Buenas prácticas** de seguridad y organización del código

**Resultado**: Un dashboard completamente funcional que integra gráficos, tablas y mapas interactivos, conectado a una base de datos real y con una arquitectura que permite el crecimiento futuro del proyecto.