"""
Sistema de Análisis Climático
----------------------------
Materia: Programación II
Profesor: Ing. Mario Martínez
Alumno: Braian Alejandro Pucheta

Este módulo implementa una interfaz web utilizando Streamlit para el análisis
de datos climáticos. Permite visualizar información sobre el proyecto y sus requerimientos.
"""

import streamlit as st
import utils as utl

# Configuración de la página principal
st.set_page_config(
    page_title="Sistema de Análisis Climático",
    layout="wide",
)

# Genera el menú de navegación
utl.generarMenu()

# Título principal y subtítulo
st.title(":orange_book: Sobre el Proyecto")
st.subheader(":sun_behind_rain_cloud: Sistema de Análisis Climático")

# Información sobre el equipo y contexto académico
st.write("**Profesor:** Ing. Mario Martinez")
st.write("**Alumno:** Braian Alejandro Pucheta")
st.write("**Materia:** Programación II")
st.write("**Carrera:** Lic. en Ciencia de Datos")
st.write("**Escuela:** Universidad Católica de Salta")

st.divider()

# Sección de requisitos del examen final
st.subheader(":pushpin: Examen Final")
st.write("""
Tomando como base el Ejercicio 14 del TP 4, mejorar el mismo incorporando más herramientas y complejidad. Si por cualquier motivo desea cambiar el tema de su trabajo y que no tenga relación con el 
Ej. 14 mencionado, puede hacerlo, pero se recomienda que sí lo haga a partir de lo ya desarrollado. El ejercicio debe poseer tanto su enunciado claro como su programación en Python. El trabajo 
es ***totalmente individual***. Poner en el programa de Python una primera línea de comentario con su Apellido y Nombre, y nombrar el archivo con el siguiente formato: "Examen_Final.py".
Subir todos los archivos de su proyecto comprimidos y agrupados en uno solo. Inventar un ejercicio de enunciado propio y desarrollo ***individual***, que contenga todo lo visto en la materia, 
***al menos una vez*** cada herramienta vista. Es decir, la resolución del enunciado debe tener:
""")

# Crear layout de dos columnas para los requisitos
col1, col2 = st.columns(2)

# Primera columna: Requisitos técnicos básicos
with col1:
    st.write("""
    \n- Cálculos secuenciales
    \n- Ingreso de datos por parte del usuario, y mostrarle resultados
    \n- Funciones para el tratamiento de cadenas de texto
    \n- Estructuras de selección
    \n- Bucles
    \n- Diccionario de Datos
    \n- Lectura de un archivo CSV
    \n- Gráficos con Matplotlib
    \n- Array NumPy
    """)

# Segunda columna: Requisitos adicionales y recomendaciones
with col2:
    st.write("""
    \n\nDebe notarse claramente una mejora en comparación con lo presentado en el TP4. Algunas herramientas y recursos que pueden implementar en pos de una mejor calificación son:
    \n- Pantalla de Bienvenida del Sistema, mostrando su autor, comisión, etc.
    \n- Pantalla adicional que explique de qué se trata el proyecto realizado.
    \n- Clara interacción del usuario con el sistema.
    \n- Mensajes cordiales y claros para que el usuario sepa lo que deba hacer.
    \n- Prolijidad en la programación, definición de variables, comentarios en líneas de código detallando que hace cada parte. 
    """)

st.divider()

# Sección del enunciado del proyecto
st.subheader(":bookmark_tabs: Enunciado")

st.write("""
Desarrolle un programa de análisis climático que permita al usuario obtener y filtrar la temperatura actual de diversas ciudades. 
La aplicación deberá ofrecer la posibilidad de descargar un archivo CSV con datos históricos a través de una API, proporcionando una fuente de datos climáticos precisa y actualizada. 
Este archivo puede ser posteriormente subido para el análisis dentro del programa, donde se calcularán estadísticas relevantes y se generan gráficos de fácil interpretación.

\n\n:speech_balloon: ***Funcionalidades Principales***
\n***Temperatura en Tiempo Real***: Filtrar por ciudades y obtener la temperatura actual.
\n***Ingreso de Datos***: Permitir al usuario ingresar manualmente datos climáticos en el DataFrame.
\n***Cálculo de Estadísticas***: Calcular y mostrar la temperatura máxima, mínima, promedio, así como la velocidad del viento, utilizando las funciones de NumPy.
\n***Lectura de Archivos CSV***: Cargar datos históricos desde un archivo CSV y almacenarlos en un DataFrame.
\n***Análisis de Datos***: Generar gráficos que muestren la evolución de la temperatura, precipitaciones y la velocidad del viento a lo largo del tiempo.
\n***Interacción***: Implementar un menú que permita al usuario seleccionar las diferentes opciones.
\n***Mejoras***: Implementar un sistema de interfaces gráficas para hacer la navegación más amigable.
""")

st.divider()

# Enlaces útiles y recursos
st.subheader(':paperclip: Enlaces de utilidad')
st.write("""
Fuentes de datos del clima: [http://open-meteo.com](http://open-meteo.com) \n\n
Lista de ciudades y países: [https://simplemaps.com/data/world-cities](https://simplemaps.com/data/world-cities) \n\n
Repositorio de Github: [sistema-analisis-climatico](https://github.com/ByBraiiaN/sistema-analisis-climatico) \n\n
""")