# pages/voz_ctr.py
import streamlit as st
import speech_recognition as sr
import json
import paho.mqtt.client as mqtt

st.set_page_config(page_title="Voz - SmartEcoHome")

with st.sidebar:
    st.subheader("MQTT (Voz)")
    broker = st.text_input("Broker MQTT", value="broker.mqttdashboard.com", key="b2")
    port = st.number_input("Puerto", value=1883, min_value=1, max_value=65535, key="p2")
    action_topic = st.text_input("Tópico acciones", value="smarteco/acciones", key="t2")
    client_id = st.text_input("Client ID", value="smarteco_streamlit_voice", key="c2")

def publish_command(cmd: dict):
    try:
        client = mqtt.Client(client_id=client_id)
        client.connect(broker, int(port), 60)
        client.publish(action_topic, json.dumps(cmd))
        client.disconnect()
        return True, None
    except Exception as e:
        return False, str(e)

st.title("Control por Voz (sube un archivo)")

st.markdown("""
Por limitaciones del navegador, la app solicita que subas un archivo de audio (.wav o .mp3) con el comando de voz.
El audio se transcribe localmente con `speech_recognition`.
""")

audio_file = st.file_uploader("Sube el archivo de audio (wav/mp3)", type=["wav", "mp3", "m4a", "ogg"])
if audio_file:
    st.audio(audio_file)
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="es-ES")
        st.success("Transcripción:")
        st.write(text)

        # Mapeo simple de frases a comandos
        text_lower = text.lower()
        cmd = None
        if "luz" in text_lower and ("encend" in text_lower or "prend" in text_lower):
            cmd = {"action": "luz_on", "value": 1}
        elif "luz" in text_lower and ("apagar" in text_lower or "apag" in text_lower):
            cmd = {"action": "luz_off", "value": 0}
        elif "ventil" in text_lower or "venti" in text_lower:
            if "encend" in text_lower or "prend" in text_lower:
                cmd = {"action": "vent_on", "value": 1}
            else:
                cmd = {"action": "vent_off", "value": 0}
        elif "abrir" in text_lower or "abre" in text_lower:
            cmd = {"action": "puerta", "value": 180}
        elif "cerrar" in text_lower or "cierra" in text_lower:
            cmd = {"action": "puerta", "value": 90}
        else:
            st.info("No se reconoció una acción automática. Puedes enviar el texto como JSON manualmente.")

        if cmd:
            if st.button("Enviar comando detectado"):
                ok, err = publish_command(cmd)
                st.success("Comando enviado") if ok else st.error(f"Error: {err}")
    except sr.UnknownValueError:
        st.error("No se pudo transcribir el audio")
    except Exception as e:
        st.error(f"Error al procesar audio: {e}")
