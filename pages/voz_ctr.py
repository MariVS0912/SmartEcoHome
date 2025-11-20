import streamlit as st
import speech_recognition as sr
import paho.mqtt.client as mqtt
import json
import time

# Configuración de la página
st.set_page_config(page_title="Control por Voz - SmartEcoHome", page_icon="🎤")

st.title("🎤 Control por Voz – SmartEcoHome")

# MQTT CONFIG
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_TOPIC = "smarteco/acciones"
CLIENT_ID = "streamlit_voice"

# Función para enviar comandos MQTT
def send_mqtt(action, value=None):
    try:
        client = mqtt.Client(client_id=CLIENT_ID)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)

        payload = {"action": action}
        if value is not None:
            payload["value"] = value

        client.publish(MQTT_TOPIC, json.dumps(payload))
        client.disconnect()
        return True
    except Exception as e:
        return False, str(e)

# Interpretador de la orden hablada
def interpretar_comando(texto):
    texto = texto.lower()

    if "encender luz" in texto or "prender luz" in texto:
        return ("luz_on", None)
    if "apagar luz" in texto:
        return ("luz_off", None)

    if "encender ventilación" in texto or "encender ventilador" in texto:
        return ("vent_on", None)
    if "apagar ventilación" in texto or "apagar ventilador" in texto:
        return ("vent_off", None)

    if "abrir puerta" in texto or "abrir escotilla" in texto:
        return ("puerta", 180)
    if "cerrar puerta" in texto or "cerrar escotilla" in texto:
        return ("puerta", 0)

    return (None, None)

st.write("Pulsa el botón y da una orden como:")
st.markdown("""
- **'Encender luz'**  
- **'Apagar ventilación'**  
- **'Abrir puerta'**  
- **'Cerrar escotilla'**  
""")

# GRABACIÓN DE VOZ
if st.button("🎤 Escuchar"):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("🎙️ Escuchando... habla ahora")
        audio = r.listen(source)

    try:
        st.info("🔍 Procesando...")
        text = r.recognize_google(audio, language="es-ES")
        st.success(f"🗣️ Dijiste: **{text}**")

        action, value = interpretar_comando(text)

        if action is None:
            st.error("❌ No reconocí una orden válida.")
        else:
            ok = send_mqtt(action, value)
            if ok:
                st.success(f"📡 Enviado → acción: `{action}`, valor: `{value}`")
            else:
                st.error("❌ Error enviando comando MQTT.")

    except sr.UnknownValueError:
        st.error("No entendí lo que dijiste 😔")
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

