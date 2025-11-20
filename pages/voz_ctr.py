import streamlit as st
import paho.mqtt.client as mqtt
import json

BROKER = "broker.hivemq.com"
TOPIC_CONTROL = "smarteco/control"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.connect(BROKER, 1883, 60)

st.title("🎤 Control por Voz – SmartEcoHome")
st.write("Haz clic en el botón y permite acceso al micrófono.")

# -----------------------------
# VARIABLES DE ESTADO
# -----------------------------
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

# Callback seguro para limpiar el texto
def clear_voice_text():
    st.session_state["voice_text"] = ""


# -----------------------------
# SCRIPT DE RECONOCIMIENTO DE VOZ
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

        // enviar texto al streamlit
        const streamlitInput = window.parent.document.querySelector('input[data-voice-input]');
        if(streamlitInput){
            streamlitInput.value = text;
            streamlitInput.dispatchEvent(new Event("input", { bubbles: true }));
        }

        const streamlitSubmit = window.parent.document.querySelector('button[data-voice-submit]');
        if(streamlitSubmit){
            streamlitSubmit.click();
        }
    }

    recognition.start();
}
</script>
"""

st.components.v1.html(voice_script, height=0)

# -----------------------------
# FORMULARIO STREAMLIT
# -----------------------------
with st.form("formulario_voz"):
    text = st.text_input(
        "Comando detectado:",
        key="voice_text",
        label_visibility="collapsed",
        help="(Este campo se llena automáticamente)",
        kwargs={"data-voice-input": "true"}  # atributo HTML permitido
    )
    submitted = st.form_submit_button(
        "Procesar comando",
        kwargs={"data-voice-submit": "true"}  # atributo HTML permitido
    )

# -----------------------------
# BOTÓN PARA ACTIVAR MICRÓFONO
# -----------------------------
if st.button("🎙️ Iniciar reconocimiento de voz"):
    st.components.v1.html("<script>startRecognition()</script>", height=0)

# -----------------------------
# PROCESAMIENTO DE COMANDO
# -----------------------------
# -----------------------------
# PROCESAMIENTO DE COMANDO
# -----------------------------
if submitted and text:
    comando = text.lower()
    st.success(f"Comando detectado: {comando}")

    if "encender luz" in comando:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "luz_on"}))
        st.info("💡 Luz encendida")
    elif "apagar luz" in comando:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "luz_off"}))
        st.info("💡 Luz apagada")
    elif "encender ventilador" in comando:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "vent_on"}))
        st.info("🌀 Ventilador encendido")
    elif "apagar ventilador" in comando:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "vent_off"}))
        st.info("🌀 Ventilador apagado")
    elif "abrir puerta" in comando:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "puerta", "value": 90}))
        st.info("🚪 Puerta abierta")
    elif "cerrar puerta" in comando:
        client.publish(TOPIC_CONTROL, json.dumps({"action": "puerta", "value": 0}))
        st.info("🚪 Puerta cerrada")
    else:
        st.error("❌ No se reconoció un comando válido.")

    # Reinicia la app para limpiar el text_input sin violar reglas de Streamlit
    st.experimental_rerun()
