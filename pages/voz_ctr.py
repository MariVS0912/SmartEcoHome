import streamlit as st
import paho.mqtt.client as mqtt
import json

BROKER = "broker.hivemq.com"
TOPIC_CONTROL = "smarteco/control"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.connect(BROKER, 1883, 60)

st.title("🎤 Control por Voz – SmartEcoHome")

st.write("Haz clic en el botón y permite acceso al micrófono.")

# ----------- JAVASCRIPT PARA CAPTURAR VOZ -----------
voice_script = """
<script>
function startRecognition(){
    const recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "es-ES";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = function(event){
        const text = event.results[0][0].transcript;
        document.getElementById("voice_text").value = text;
        document.getElementById("voice_form").dispatchEvent(new Event("submit"));
    }

    recognition.start();
}
</script>
"""

st.components.v1.html(voice_script, height=0)

# ----------- FORMULARIO OCULTO PARA RECIBIR TEXTO -----------
with st.form("voice_form", clear_on_submit=True):
    text = st.text_input("", key="voice_text")
    submitted = st.form_submit_button("")

if st.button("🎙️ Iniciar reconocimiento de voz"):
    st.components.v1.html("<script>startRecognition()</script>", height=0)

if submitted and text:
    st.success(f"Comando detectado: {text}")

    # -------- MAPEO DE COMANDOS --------
    text_l = text.lower()

    if "encender luz" in text_l:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "luz_on"}))
    elif "apagar luz" in text_l:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "luz_off"}))
    elif "encender ventilador" in text_l:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "vent_on"}))
    elif "apagar ventilador" in text_l:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "vent_off"}))
    elif "abrir puerta" in text_l:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "puerta", "value": 90}))
    elif "cerrar puerta" in text_l:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "puerta", "value": 0}))
    else:
        st.error("No reconocí un comando válido.")
        st.error("No entendí la instrucción")
