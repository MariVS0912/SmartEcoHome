import streamlit as st
import paho.mqtt.client as mqtt
import json

# -----------------------------
# CONFIGURACIÓN MQTT
# -----------------------------
BROKER = "broker.hivemq.com"
TOPIC_CONTROL = "smarteco/control"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.connect(BROKER, 1883, 60)

# -----------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------
st.title("🎤 Control por Voz – SmartEcoHome")
st.write("Haz clic en el botón y permite acceso al micrófono para comenzar.")

# -----------------------------
# INICIALIZACIÓN DE SESSION_STATE
# -----------------------------
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "voice_trigger" not in st.session_state:
    st.session_state.voice_trigger = False


# -----------------------------
# SCRIPT DE JAVASCRIPT PARA VOZ
# -----------------------------
voice_script = """
<script>
function startRecognition(){
    const recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "es-ES";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = function(event){
        const text = event.results[0][0].transcript;
        const input = document.getElementById("voice_text_input");
        input.value = text;
        input.dispatchEvent(new Event("input", { bubbles: true }));
        
        const submitBtn = document.getElementById("voice_submit_btn");
        submitBtn.click();
    }

    recognition.start();
}
</script>
"""

st.components.v1.html(voice_script, height=0)


# -----------------------------
# FORMULARIO QUE RECIBE LA VOZ
# -----------------------------
with st.form("voice_form"):
    text = st.text_input("", key="voice_text", id="voice_text_input")
    submitted = st.form_submit_button("Procesar comando", type="primary", disabled=True, id="voice_submit_btn")


# -----------------------------
#
