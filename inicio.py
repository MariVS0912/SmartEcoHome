# Inicio.py
import streamlit as st

st.set_page_config(page_title="SmartEcoHome", page_icon="🌱", layout="wide")

st.title("SmartEcoHome 🌱")
st.markdown("""
Bienvenida/o a SmartEcoHome — proyecto final de Interfaces Multimodales.

Navega a **Control** para interactuar por botones/texto, a **Voz** para enviar comandos por audio (sube un archivo .wav/.mp3), o a **Imagen** para detectar personas desde una foto.
""")

st.header("Objetivos del proyecto")
st.markdown("""
- Interacción multimodal: texto, voz (archivo), imagen, botones.  
- Comunicación con ESP32 (simulado en WOKWI) por MQTT.  
- 2+ páginas en Streamlit.  
- Control de actuadores: luz (LED), ventilador, puerta (servo).  
- Lectura de sensores en tiempo real (topic `smarteco/sensores`).
""")

st.info("Antes de usar: configura el broker MQTT en las páginas o en la barra lateral de Control/Voz/Imagen.")

st.write("Si necesitas, mira el README para instrucciones de ejecución.")
