"""
Sistema de Análisis Climático
----------------------------------------------------
Materia: Programación II
Profesor: Ing. Mario Martínez
Alumno: Braian Alejandro Pucheta

Este módulo contiene funciones para la obtención de datos
mediantes apis y enviar un dataframe
"""

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
import json
from datetime import datetime, timezone as tmz
import utils as util
import pytz
from timezonefinder import TimezoneFinder

# Inicialización del cliente Open-Meteo
# Se configura el sistema de caché para optimizar las solicitudes y reducir llamadas redundantes
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# URL base para la API de datos históricos de Open-Meteo
url = "https://archive-api.open-meteo.com/v1/archive"

def obtenerTemperaturaActual(lat, lng):
    """
    Obtiene la temperatura actual y pronóstico horario para una ubicación específica.
    """
    timezone_str = 'America/Sao_Paulo'

    response_current = requests.get(
        f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}'
        f'&current_weather=true&hourly=temperature_2m,precipitation&timezone={timezone_str}'
    )
    result_current = json.loads(response_current._content)
    current = result_current["current_weather"]
    current["common_dir"] = util.obtenerDireccionViento(current["winddirection"])

    # Procesamiento de datos horarios
    hourly = result_current["hourly"]
    hourly_df = pd.DataFrame.from_dict(hourly)
    hourly_df.rename(columns={
        'time': 'Fecha',
        'temperature_2m': 'Temperatura °C',
        'precipitation': 'Precipitacion mm'
    }, inplace=True)

    timezone_loc = pytz.timezone(timezone_str)
    dt = datetime.now()
    tzoffset = timezone_loc.utcoffset(dt)

    week_ahead = pd.to_datetime(hourly_df['Fecha'], format="%Y-%m-%dT%H:%M")
    week_ahead + tzoffset
    hourly_df["Fecha"] = week_ahead

    return current, hourly_df


def obtenerTemperaturaHistorica(lat, lng, fecha_inicio, fecha_final):
    """
    Obtiene datos históricos de temperatura y condiciones meteorológicas para un período específico.
    """
    params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": fecha_inicio,
        "end_date": fecha_final,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "daylight_duration",
            "sunshine_duration",
            "precipitation_sum",
            "wind_speed_10m_max",
            "shortwave_radiation_sum"
        ],
        "timezone": "America/Sao_Paulo"
    }

     # Realizar solicitud a la API
    responses = openmeteo.weather_api(url, params=params)

    # Verificar si hay una respuesta y procesarla
    if responses:
        response = responses[0]

        # Procesamiento de datos diarios
        daily = response.Daily()
        if daily:
            daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
            daily_temperature_2m_mean = daily.Variables(2).ValuesAsNumpy()
            daily_daylight_duration = daily.Variables(3).ValuesAsNumpy()
            daily_sunshine_duration = daily.Variables(4).ValuesAsNumpy()
            daily_precipitation_sum = daily.Variables(5).ValuesAsNumpy()
            daily_wind_speed_10m_max = daily.Variables(6).ValuesAsNumpy()
            daily_shortwave_radiation_sum = daily.Variables(7).ValuesAsNumpy()

            daily_data = {"date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            )}
            
            daily_data["temperature_2m_max"] = daily_temperature_2m_max
            daily_data["temperature_2m_min"] = daily_temperature_2m_min
            daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
            daily_data["daylight_duration"] = daily_daylight_duration
            daily_data["sunshine_duration"] = daily_sunshine_duration
            daily_data["precipitation_sum"] = daily_precipitation_sum
            daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
            daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum

            # Crear un dataframe
            daily_dataframe = pd.DataFrame(data=daily_data)
            daily_dataframe['date'] = daily_dataframe['date'].dt.strftime('%d/%m/%Y')

            return daily_dataframe

    else:
        print("No se recibieron respuestas de la API.")
