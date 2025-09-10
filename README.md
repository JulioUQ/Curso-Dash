# Curso Dash

## Día 1 – Fundamentos de Dash y primeras visualizaciones
**Objetivo:** Conocer la librería Dash, conectar con bases de datos y realizar representaciones gráficas con Plotly Express.

### 1. Introducción
- **Comparación Dash vs Power BI / Tableau**
  - Dash: librería de Python, flexible, orientada a desarrolladores.
  - Power BI/Tableau: herramientas “low-code”, más rápidas para usuarios finales.
  - Pros y contras en velocidad, personalización, despliegue y control.
- **Arquitectura básica de Dash**
  - Componentes: `html.Div`, `dcc.Graph`, `dcc.Dropdown`, `Button`.
  - Layout: cómo organizar visualmente el dashboard.
  - Callbacks: funciones que conectan interacción del usuario con actualización de componentes.
- **Conexión a Base de Datos**
  - Uso de librerías como `pandas`, `SQLAlchemy` o `psycopg2`.
  - Cargar datos en DataFrames para visualización.
- **Primer dashboard**
  - Añadir título, texto descriptivo y controles básicos (dropdowns, sliders).
- **Layout**
  - Uso de `html` y `Dash Core Components`.
  - Introducción a `Dash Bootstrap Components` para estilo y organización responsive.

### 2. Visualizaciones con Plotly
- **Tipos de gráficos más usados**
  - `line`, `bar`, `scatter`, `pie`.
- **Personalización**
  - Colores, ejes, títulos, leyendas, formatos.

### 3. Ejercicio guiado
- Crear un dashboard con **2 gráficos sincronizados**.
- Filtrado básico usando un **dropdown**.

---

## Día 2 – Interactividad avanzada
**Objetivo:** Aprender a crear dashboards dinámicos con datos reales desde una base de datos.

### 1. Repaso rápido del día 1
- Revisión de layout, gráficos básicos y conexión a BBDD.

### 2. Callbacks avanzados
- **Múltiples entradas y salidas**
  - Ejemplo: actualizar varios gráficos a la vez según un filtro.
- **Actualización de gráficos con filtros**
  - Cambiar ejes, valores o visibilidad de elementos dinámicamente.
- **Estado de componentes (`State`)**
  - Mantener información de componentes sin que disparen el callback por sí mismos.

### 3. Ejercicio práctico
- Creación de un dashboard completo:
  - Tablas dinámicas con `dash_table.DataTable`.
  - Gráficos sincronizados.
  - Interactividad entre distintos componentes (dropdown, slider, radio buttons).

---

## Día 3 – Construcción de un Dashboard Completo, automatización y descarga de datos
**Objetivo:** Integrar todo lo aprendido y automatizar informes desde el dashboard.

- **Repaso y resolución de dudas**
  - Revisión de errores comunes y mejores prácticas.
- **Generación de informes HTML**
  - Exportar dashboards filtrados a HTML.
- **Exportación de datos a Excel**
  - Uso de `pandas.DataFrame.to_excel`.
- **Ejercicio práctico**
  - Crear un botón en el dashboard que:
    - Permita descargar un Excel filtrado.
    - Genere un informe en HTML con los datos seleccionados.

---

# Estructura de repositorio GitHub - Curso Dash

CursoDash/  
│  
├── README.md                 
├── requirements.txt           
│  
├── Día_1_Fundamentos/         
│   ├── README.md              
│   ├── 01_introduccion.ipynb   
│   ├── 02_conexion_BBDD.py    
│   ├── 03_primer_dashboard.py   
│   ├── 04_layout_dash.ipynb   
│   └── 05_plotly_visualizaciones.ipynb   
│  
├── Día_2_Interactividad/      
│   ├── README.md             
│   ├── 01_repaso_dia1.ipynb   
│   ├── 02_callbacks_basicos.py   
│   ├── 03_callbacks_avanzados.py   
│   ├── 04_dashboard_completo.py   
│   └── 05_interactividad_componentes.ipynb   
│  
├── Día_3_Dashboard_Completo/   
│   ├── README.md              
│   ├── 01_repaso_dias1_2.ipynb   
│   ├── 02_export_html.py     
│   ├── 03_export_excel.py     
│   ├── 04_dashboard_final.py   
│   └── 05_ejercicio_final.ipynb   
│  
└── assets/                    
    ├── logo.png  
    ├── estilos.css  
    └── datos_ejemplo.csv  
