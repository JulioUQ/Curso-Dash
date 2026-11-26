<div align="center">

![Curso](https://img.shields.io/badge/CURSO-6A1B9A?style=for-the-badge)

# Dashboards con Dash

Curso práctico de tres días para construir dashboards web con Python: arquitectura de una aplicación Dash, interactividad con callbacks y un dashboard completo con informes descargables.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Dash](https://img.shields.io/badge/Dash-008DE4?style=flat-square&logo=plotly&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white) ![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white) ![SQL Server](https://img.shields.io/badge/SQL_Server-CC2927?style=flat-square)

</div>

---

## Descripción general

Dash permite crear aplicaciones web analíticas sin escribir JavaScript. El curso avanza desde la estructura mínima de una aplicación hasta un dashboard modular con pestañas y exportación de informes, usando datos de ejemplo del sector pesquero (desembarques, capturas y buques).

## Contenido

| Día | Contenido | Ejercicios |
| --- | --- | --- |
| [1. Fundamentos](D%C3%ADa_1_Fundamentos) | Arquitectura de Dash (Flask, React, Plotly), layout y conexión a base de datos | Arquitectura básica, conexión a SQL Server, primer dashboard con gráficos, mapa y tabla |
| [2. Interactividad](D%C3%ADa_2_Interactividad) | Callbacks, filtros dinámicos y comunicación entre componentes | Selectores por comunidad autónoma que actualizan gráficos de buques, especies y provincias |
| [3. Dashboard completo](D%C3%ADa_3_Dashboard_Completo) | Pestañas, descargas y generación de informes | Dashboard con pestañas e informes en HTML y Excel |

Cada día tiene su propio `README.md` con los apuntes.

## Tecnologías y herramientas

| Ámbito | Herramientas |
| --- | --- |
| Aplicación | Dash, Dash Bootstrap Components |
| Gráficos | Plotly |
| Datos | pandas, pyodbc (SQL Server) |

## Instalación y uso

```bash
pip install -r requirements.txt
cd "Día_3_Dashboard_Completo/Ejercicio 1"
python ejer_1.py
```

Los ejercicios leen los datos de una base de datos SQL Server a través de pyodbc. La conexión se configura en la carpeta `config/` de cada día.

## Aspectos técnicos destacados

- Estructura modular: cada gráfico y cada tabla es un módulo independiente que reutilizan los ejercicios.
- Callbacks encadenados para que un único filtro actualice todo el dashboard.
- Exportación de informes en HTML y Excel desde la propia aplicación.

## Autor

**Julio Úbeda Quesada** · Data Scientist

[![Portfolio](https://img.shields.io/badge/Portfolio-0B2545?style=flat-square&logo=astro&logoColor=white)](https://juliouq.github.io/Portfolio-Web---JulioUQ/es/) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square)](https://www.linkedin.com/in/juliouq/) [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/JulioUQ)
