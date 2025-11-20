import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.client as paho
import json

broker = "broker.mqttdashboard.com"
port = 1883

client = paho.Client(client_id="SmartEco_Voz", callback_api_version=paho.CallbackAPIVersion.VERSION1)
client.connect(broker, port)

st.title("Control por Voz – SmartEco")

st.write("Da clic y habla (ej: 'encender luz', 'apagar ventilador', 'abrir puerta 120')")

stt_button = Button(label=" 🎤 Hablar ", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
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
    refresh_on_update=False,
    override_height=75
)

def interpretar(cmd):
    cmd = cmd.lower()

    if "encender luz" in cmd: return ("luz_on", 0)
    if "apagar luz" in cmd: return ("luz_off", 0)
    if "encender ventilador" in cmd: return ("vent_on", 0)
    if "apagar ventilador" in cmd: return ("vent_off", 0)

    if "abrir puerta" in cmd or "cerrar puerta" in cmd:
        import re
        match = re.search(r'\d+', cmd)
        pos = int(match.group()) if match else 90
        return ("puerta", pos)

    return (None, None)

if result and "GET_TEXT" in result:
    texto = result["GET_TEXT"]
    st.write(f"🗣 Dijiste: **{texto}**")

    action, value = interpretar(texto)

    if action:
        msg = json.dumps({"action": action, "value": value})
        client.publish("SmartEcoHome/voz_ctr", msg)
        st.success("Comando enviado")
    else:
        st.error("No entendí el comando 😢")
