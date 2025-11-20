import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.client as paho
import json

st.title("🎤 Control por Voz - SmartEcoHome")

broker = "broker.mqttdashboard.com"
port = 1883

client = paho.Client("SmartEcoHome_Voz")

st.write("""
Pulsa el botón y di comandos como:

- encender luz  
- apagar luz  
- encender ventilador  
- apagar ventilador  
- abrir puerta  
- cerrar puerta
""")

# Botón de voz
stt_button = Button(label="🎙️ Hablar", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "es-ES";

    recognition.onresult = function (e) {
        var value = e.results[0][0].transcript;
        document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
    }

    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="voz",
    override_height=75
)

if result and "GET_TEXT" in result:
    texto = result["GET_TEXT"].lower()
    st.success(f"🔊 Dijiste: **{texto}**")

    client.connect(broker, port)

    if "encender luz" in texto:
        msg = {"action": "luz_on"}

    elif "apagar luz" in texto:
        msg = {"action": "luz_off"}

    elif "encender ventilador" in texto:
        msg = {"action": "vent_on"}

    elif "apagar ventilador" in texto:
        msg = {"action": "vent_off"}

    elif "abrir puerta" in texto:
        msg = {"action": "puerta", "value": 90}

    elif "cerrar puerta" in texto:
        msg = {"action": "puerta", "value": 0}

    else:
        st.error("Comando no reconocido")
        msg = None

    if msg:
        client.publish("smarteco/acciones", json.dumps(msg))
        st.success("📡 Comando enviado al ESP32")
