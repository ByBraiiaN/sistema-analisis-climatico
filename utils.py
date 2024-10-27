"""
Sistema de Análisis Climático
----------------------------------------------------
Materia: Programación II
Profesor: Ing. Mario Martínez
Alumno: Braian Alejandro Pucheta

Este módulo contiene funciones auxiliares para el procesamiento y visualización
de datos climáticos, incluyendo generación de gráficos, cálculos estadísticos
y manipulación de datos meteorológicos.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
import numpy as np

# Constantes globales
FILE_PAISES = 'paises_ciudades.csv'

# Configuración del estilo de visualización
plt.style.use("dark_background")

def generarMenu():
    """Genera el menú lateral de navegación de la aplicación."""
    with st.sidebar:
        st.header(":sun_behind_rain_cloud: Sistema de Análisis Climático")
        # Enlaces a las diferentes páginas de la aplicación
        st.page_link('Examen_Final.py', label='Datos', icon="🌡️")
        st.page_link('pages/analisis.py', label='Análisis', icon="📊")
        st.page_link('pages/proyecto.py', label='Proyecto', icon="👨‍🎓")
        
        st.image('img/logo-ucasal.png', use_column_width=True)

@st.cache_data
def obtenerPaises():
    """
    Carga y ordena el dataset de países y ciudades.
    """
    data = pd.read_csv(FILE_PAISES)
    data.sort_values(by=['country','city_ascii'], ascending=True, inplace=True)

    return data

def obtenerDireccionViento(direction):
    """
    Convierte la dirección del viento en grados a su representación cardinal.
    """
    # Incremento para ajustar el rango de grados en cada dirección
    ddeg = 11.25

    # Mapeo de rangos de grados a direcciones cardinales
    if direction >= (360 - ddeg) or direction < (0 + ddeg):
        common_dir = "N"
    elif direction >= (337.5 - ddeg) and direction < (337.5 + ddeg):
        common_dir = "N/NO"
    elif direction >= (315 - ddeg) and direction < (315 + ddeg):
        common_dir = "NO"
    elif direction >= (292.5 - ddeg) and direction < (292.5 + ddeg):
        common_dir = "O/NO"
    elif direction >= (270 - ddeg) and direction < (270 + ddeg):
        common_dir = "O"
    elif direction >= (247.5 - ddeg) and direction < (247.5 + ddeg):
        common_dir = "O/SO"
    elif direction >= (225 - ddeg) and direction < (225 + ddeg):
        common_dir = "SO"
    elif direction >= (202.5 - ddeg) and direction < (202.5 + ddeg):
        common_dir = "S/SO"
    elif direction >= (180 - ddeg) and direction < (180 + ddeg):
        common_dir = "S"
    elif direction >= (157.5 - ddeg) and direction < (157.5 + ddeg):
        common_dir = "S/SE"
    elif direction >= (135 - ddeg) and direction < (135 + ddeg):
        common_dir = "SE"
    elif direction >= (112.5 - ddeg) and direction < (112.5 + ddeg):
        common_dir = "E/SE"
    elif direction >= (90 - ddeg) and direction < (90 + ddeg):
        common_dir = "E"
    elif direction >= (67.5 - ddeg) and direction < (67.5 + ddeg):
        common_dir = "E/NE"
    elif direction >= (45 - ddeg) and direction < (45 + ddeg):
        common_dir = "NE"
    elif direction >= (22.5 - ddeg) and direction < (22.5 + ddeg):
        common_dir = "N/NE"

    return common_dir


def mostrarGraficoSemanal(df):
    """
    Genera un gráfico de líneas con temperatura y precipitaciones semanales.
    """
    # Crear figura con dos ejes
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    # Gráfico de temperatura
    ax1.plot(df["Fecha"], df['Temperatura °C'], label="Temperatura °C", color="tab:orange")
    ax1.set_ylabel("Temperatura °C", color="tab:orange")
    ax1.set_title('Temperatura Semanal')

    # Gráfico de precipitaciones
    ax2.plot(df["Fecha"], df['Precipitacion mm'], label="Precipitacion mm", color="tab:cyan")
    ax2.set_ylabel("Precipitacion mm", color="tab:cyan")
    ax2.set_ylim(0, 30)

    # Configuración del formato de fechas
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
    fig.autofmt_xdate(rotation=45)

    # Configuración de la leyenda
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95))
    plt.tight_layout()

    return fig


def mostrarGraficoTemperatura(df):
    """
    Genera un gráfico completo de variables climáticas (temperatura, precipitación, viento).
    """
    # Preparación de datos
    df_data = df.dropna(subset=['temperature_2m_max', 'temperature_2m_min', 
                               'precipitation_sum', 'wind_speed_10m_max'])
    df_data.loc[:, "date"] = pd.to_datetime(df_data['date'], format='%d/%m/%Y')
    df_data.set_index('date', inplace=True)
    
    # Determinar período de agrupación según cantidad de días
    num_dias = len(df_data)
    if num_dias <= 30:
        df_data = df_data  # Datos diarios
    elif 30 < num_dias <= 180:
        df_data = df_data.resample('W').mean()  # Datos semanales
    elif 180 < num_dias <= 2000:
        df_data = df_data.resample('ME').mean()  # Datos mensuales
    else:
        df_data = df_data.resample('A').mean()  # Datos anuales

   # Conversión a arrays NumPy para mejor rendimiento
    dias = df_data.index
    temperatura_max = df_data['temperature_2m_max'].to_numpy()
    temperatura_min = df_data['temperature_2m_min'].to_numpy()
    precipitacion = df_data['precipitation_sum'].to_numpy()
    viento = df_data['wind_speed_10m_max'].to_numpy()

    # Creación del gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Gráficos de variables climáticas
    ax.plot(dias, temperatura_max, label="Temperatura Max (°C)", color='orange', linestyle='-')
    ax.plot(dias, temperatura_min, label="Temperatura Min (°C)", color='cyan', linestyle='-')
    ax.bar(dias, precipitacion, label="Precipitación (mm)", color='g', alpha=0.7, width=30)
    ax.plot(dias, viento, label="Viento (km/h)", color='r', linestyle='-.', marker='^')

    # Configuración del gráfico
    ax.set_title('Evolución Climática: Temperatura, Viento y Precipitaciones')
    ax.set_xlabel('Fechas')
    ax.set_ylabel('Mediciones')
    plt.xticks(rotation=45)
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    return fig

def mostrarGraficoLuz(df):
    """
    Genera un gráfico de barras apiladas mostrando la duración de la luz solar.
    """
    # Preparación de datos
    df_data = df.dropna(subset=['daylight_duration', 'sunshine_duration'])
    df_data.loc[:, "date"] = pd.to_datetime(df_data['date'], format='%d/%m/%Y')
    df_data['month'] = pd.to_datetime(df_data['date']).dt.month

    # Conversión de segundos a horas
    df_data.loc[:, 'daylight_duration'] /= 3600
    df_data.loc[:, 'sunshine_duration'] /= 3600
    df_data.set_index('date', inplace=True)

    # Agrupación mensual
    monthly_data = df_data.groupby('month').agg({
        'daylight_duration': 'mean',
        'sunshine_duration': 'mean'
    }).reindex(range(1, 13))

    # Cálculo de tiempo nublado
    monthly_data['cloudy_duration'] = (monthly_data['daylight_duration'] - 
                                     monthly_data['sunshine_duration'])

    # Creación del gráfico
    fig, ax = plt.subplots(figsize=(7, 4))
    
    # Barras apiladas
    ax.bar(monthly_data.index, monthly_data['sunshine_duration'],
           label='Luz directa del sol', color='orange')
    ax.bar(monthly_data.index, monthly_data['cloudy_duration'],
           bottom=monthly_data['sunshine_duration'],
           label='Luz sin sol directo', color='skyblue')

    # Configuración de etiquetas y formato
    month_names_es = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    present_months = monthly_data.index[monthly_data['sunshine_duration'].notnull()]
    ax.set_xticks(present_months)
    ax.set_xticklabels([month_names_es[i - 1] for i in present_months])
    
    ax.set_xlabel('Meses')
    ax.set_ylabel('Horas')
    ax.set_title('Media de duración de luz de día y de sol por mes')
    ax.set_ylim(0, 24)
    ax.legend()
    fig.autofmt_xdate(rotation=25)
    plt.tight_layout()

    return fig


def mostrarGraficoRadiacion(df):
    """
    Genera un gráfico de dispersión para mostrar la relación entre duración
    de luz solar y radiación solar.
    """
    # Preparación de datos
    df_data = df.dropna(subset=['daylight_duration', 'sunshine_duration',
                               'shortwave_radiation_sum'])
    df_data.loc[:, "date"] = pd.to_datetime(df_data['date'], format='%d/%m/%Y')
    df_data.set_index('date', inplace=True)
    df_data = df_data[['daylight_duration', 'sunshine_duration',
                       'shortwave_radiation_sum']]

    # Conversión de unidades
    df_data.loc[:, 'sunshine_duration'] /= 3600
    df_data.loc[:, 'shortwave_radiation_sum'] /= 3600

    # Determinar período de agrupación
    num_dias = len(df_data)
    if num_dias <= 30:
        df_data = df_data  # Datos diarios
    elif 30 < num_dias <= 180:
        df_data = df_data.resample('W').mean()  # Datos semanales
    elif 180 < num_dias <= 2000:
        df_data = df_data.resample('ME').mean()  # Datos mensuales
    else:
        df_data = df_data.resample('A').mean()  # Datos anuales

    # Creación del gráfico
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    ax1.scatter(df_data['sunshine_duration'], df_data['shortwave_radiation_sum'],
                color='r', alpha=0.6)
    ax1.set_title('Relación entre la Duración de Luz Solar y la Radiación Solar a Corto Plazo')
    ax1.set_xlabel('Duración de la Luz Solar (horas)')
    ax1.set_ylabel('Radiación Solar (MJ/m²)')
    ax1.grid(True)
    plt.tight_layout()

    return fig


def temperaturaDiaria(df):
    """
    Procesa y agrupa datos de temperatura por día.
    """
    df['datetime'] = pd.to_datetime(df['Fecha'])
    
    # Agrupación por fecha para temperaturas
    result = df.groupby(df['datetime'].dt.date)['Temperatura °C'].agg(
        ['min', 'max']
    ).reset_index()
    
    # Agregar precipitaciones
    precipitacion = df.groupby(df['datetime'].dt.date)['Precipitacion mm'].agg(
        'sum'
    ).reset_index()

    # Unificar datos
    result = result.merge(precipitacion, on='datetime', how='left')
    result.columns = ['Fecha', 'Mínima °C', 'Máxima °C', 'Precipitación mm']
    
    # Agregar nombre del día
    result['Fecha'] = (result['Fecha'].astype(str) + " - " + 
                      pd.to_datetime(result['Fecha']).dt.day_name(locale='es'))

    return result

def cargarHistorial(archivo):
    """
    Carga datos históricos desde un archivo.
    """
    if archivo.type == "text/csv":
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)

    return df

def obtenerDatosEstadisticos(df):
    """
    Calcula estadísticas básicas a partir de un DataFrame con datos meteorológicos.
    """
    # Eliminar filas con valores nulos en las columnas relevantes
    df = df.dropna(subset=['temperature_2m_max', 'temperature_2m_min', 
                          'precipitation_sum', 'wind_speed_10m_max'])

    # Convertir las columnas del DataFrame a arrays de NumPy para optimizar cálculos
    temperatura_max = df['temperature_2m_max'].to_numpy()
    temperatura_min = df['temperature_2m_min'].to_numpy()
    precipitacion = df['precipitation_sum'].to_numpy()
    viento = df['wind_speed_10m_max'].to_numpy()
    luz = df['daylight_duration'].to_numpy()

    # Calcular estadísticas básicas utilizando funciones de NumPy
    temp_max = np.max(temperatura_max)
    temp_min = np.min(temperatura_min)
    temp_media = np.mean([temperatura_max, temperatura_min])
    precipitacion_media = np.mean(precipitacion)
    viento_media = np.mean(viento)
    luz_media = np.mean(luz) / 3600

    # Crear diccionario con las estadísticas y sus unidades correspondientes
    estadisticas_climaticas = {
        "temp_max": f"{temp_max:.2f} °C",
        "temp_min": f"{temp_min:.2f} °C",
        "temp_media": f"{temp_media:.2f} °C",
        "precipitacion_media": f"{precipitacion_media:.2f} mm",
        "viento_media": f"{viento_media:.2f} km/h",
        "luz_media": f"{luz_media:.2f} h",
    }

    return estadisticas_climaticas
