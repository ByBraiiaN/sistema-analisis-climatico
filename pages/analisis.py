"""
Sistema de Análisis Climático
----------------------------------------------------
Materia: Programación II
Profesor: Ing. Mario Martínez
Alumno: Braian Alejandro Pucheta

Este módulo contiene funciones para el procesamiento y visualización
de datos climáticos, incluyendo generación de gráficos, cálculos estadísticos
y manipulación de datos meteorológicos.
"""

import streamlit as st
import utils as utl
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="Sistema de Análisis Climático",
    layout="wide",
)

# Título y descripción principal
st.title(":first_quarter_moon: Análisis de datos climáticos")
st.write(
    "Carga aquí el archivo histórico descargado para iniciar el análisis. "
    "Podrás explorar y modificar los datos de temperatura máxima y mínima, "
    "velocidad del viento, cantidad de luz directa y niveles de radiación. "
    "Obtén información valiosa sobre el comportamiento climático y mejora "
    "tus decisiones basadas en datos."
)

st.divider()

# Generación del menú de navegación
utl.generarMenu()

# Carga de archivo CSV
uploaded_files = st.file_uploader(
    label=":date: Seleccione el archivo CSV a analizar",
    type=["csv"],
    help="Seleccione el archivo descargado con los datos"
)

# Procesamiento de datos si se carga un archivo
if uploaded_files:
    st.snow()

    # Obtener un dataframe desde el archivo
    df_clima = utl.cargarHistorialDesdeArchivos(uploaded_files)

    # Visualización y edición de datos
    df_clima = st.data_editor(df_clima, height=300)

    st.divider()

     # Sección de estadísticas
    st.subheader(f":triangular_ruler: Estadisticas para {uploaded_files.name}")

    # Obtener el estadisticas en un dicccionario
    estadisticas = utl.obtenerDatosEstadisticos(df_clima)

    # Visualización de estadísticas en dos columnas
    col1, col2 = st.columns(2)

    with col1:
        st.error(f":fire: La temperatura máxima registrada es: {estadisticas['temp_max']}")
        st.warning(f":partly_sunny: La temperatura media registrada es: {estadisticas['temp_media']}")
        st.info(f":snowflake: La temperatura mínima registrada es: {estadisticas['temp_min']}")

    with col2:
        st.info(f":sun_small_cloud: La luz media registrada es: {estadisticas['luz_media']}")
        st.info(f":ocean: La precipitación media registrada es: {estadisticas['precipitacion_media']}")
        st.info(f":fog: La velocidad media de viento registrada es: {estadisticas['viento_media']}")

    # Sección de gráficos
    st.divider()
    st.subheader(":male-scientist: Gráfico de la evolución climática")
    st.pyplot(utl.mostrarGraficoTemperatura(df_clima))

    st.divider()
    st.subheader(":sunny: Gráfico de la evolución de la luz solar mensual")
    st.pyplot(utl.mostrarGraficoLuz(df_clima))

    st.divider()
    st.subheader(":warning: Gráfico de la exposición de la luz solar y la radiacción")
    st.pyplot(utl.mostrarGraficoRadiacion(df_clima))

else:
    st.info('Esperando por el archivo...')
