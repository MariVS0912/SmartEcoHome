# Inicio.py
import streamlit as st

st.set_page_config(page_title="SmartEcoHome", page_icon="🌱", layout="wide")

st.title("SmartEcoHome 🌱")
st.markdown("""
Bienvenida/o a SmartEcoHome — proyecto final de Interfaces Multimodales.

""")

st.header("Objetivos del proyecto")
st.markdown("""
- Interacción multimodal.  
- Comunicación con ESP32 (simulado en WOKWI) por MQTT.  
- 2+ páginas en Streamlit.  
- Control de actuadores: luz (LED), ventilador, puerta (servo).  
""")


