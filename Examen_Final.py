"""
Sistema de Análisis Climático
----------------------------------------------------
Materia: Programación II
Profesor: Ing. Mario Martínez
Alumno: Braian Alejandro Pucheta

Este módulo contiene la lógica principal para la descarga y visualización
de datos climáticos, incluyendo generación de gráficos y un mapa.
"""

import streamlit as st
#import pandas as pd #
import datetime as dt
import utils as utl
import api as api
import folium
from streamlit_folium import st_folium


# Configuración de la página principal
st.set_page_config(
    page_title="Sistema de Análisis Climático",
    layout="wide",
)

# Estilo personalizado para los botones de descarga
st.markdown(
    """
    <style>
    .stDownloadButton > button {
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Generación del menú de navegación
utl.generarMenu()

# Título y descripción principal
st.title(":sun_behind_rain_cloud: Sistema de Análisis Climático")
st.write("""
Herramienta integral para monitorear el clima actual y acceder a la previsión meteorológica de la próxima semana. 
Además, permite la descarga de datos históricos, brindando la posibilidad de analizar patrones y tendencias climáticas 
a lo largo del tiempo. Ideal para investigadores, agricultores y cualquier persona interesada en comprender mejor las 
condiciones climáticas.
""")

st.divider()

# Carga y procesamiento de datos geográficos
data = utl.obtenerPaises()

# Distribución de elementos en columnas
col1, col2, col3, col4, col5 = st.columns(5)

# Selector de país
with col1:
    countries = data["country"].unique()
    country = st.selectbox('País', options=countries, index=8)

# Selector de ciudad
with col2:
    country_data = data.loc[data["country"] == country, :]
    cities = country_data["city_ascii"].unique()
    city = st.selectbox('Ciudad', options=cities)

# Obtención de coordenadas geográficas
lat = float(country_data.loc[data["city_ascii"] == city, "lat"].iloc[0])
lng = float(country_data.loc[data["city_ascii"] == city, "lng"].iloc[0])

# Configuración de fechas para el análisis histórico
fecha_min = min_value=dt.date(2020, 1, 1)
fecha_max = dt.date.today()

# Selector de fecha inicial
with col3:
    fecha_desde = st.date_input("Fecha desde", fecha_min, format="DD/MM/YYYY", 
                               min_value=fecha_min, max_value=fecha_max)

# Selector de fecha final
with col4:
    fecha_hasta = st.date_input("Fecha hasta", fecha_max, format="DD/MM/YYYY", 
                               min_value=fecha_min, max_value=fecha_max)

# Botón de descarga de datos históricos
with col5:
    st.write('<div style="height: 1.7em;">Datos</div>', unsafe_allow_html=True)
    st.download_button(
        label="Descargar historial",
        data=api.obtenerTemperaturaHistorica(lat, lng, fecha_desde, fecha_hasta).to_csv(index=False),
        file_name=f"{country}_{city}_{fecha_desde}_{fecha_hasta}.csv"
    )

st.divider()

# Obtención y visualización de datos meteorológicos actuales
temp_json, temp_actual = api.obtenerTemperaturaActual(lat, lng)

st.subheader(f"{':sun_with_face:' if temp_json['is_day'] == 1 else ':new_moon_with_face:'} Temperatura en {city}, {country}")

st.info(f"La temperatura actual es de {temp_json['temperature']} °C, la velocidad del viento es {temp_json['windspeed']} m/s, "
        f"y el viento va en dirección {temp_json['common_dir']}.")

# Visualización del pronóstico semanal
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Pronóstico para la Semana")
    st.write('Pronóstico de temperatura y lluvia para la próxima semana.', unsafe_allow_html=True)
    st.dataframe(utl.temperaturaDiaria(temp_actual), use_container_width=True, hide_index=True)

with col2:
    fig = utl.mostrarGraficoSemanal(temp_actual)
    st.pyplot(fig)

st.divider()

# Visualización del mapa
st.subheader(":world_map: Ubicación en el Mapa")

# Configuración del mapa centrado en la ubicación seleccionada
m = folium.Map(location=[lat, lng], zoom_start=6, titles="Mapa")

# Agregar marcador en la ubicación seleccionada
folium.Marker(
    [lat, lng],
    popup=f"{city}, {country}",
    tooltip=f"{city}, {country}",
    icon=folium.Icon(color='green')
).add_to(m)

# Mostrar el mapa
st_data = st_folium(m, width=1200, height=420, returned_objects=[])
