import streamlit as st
import json
import paho.mqtt.client as mqtt

# ---------------------------------------------
# CONFIG MQTT
# ---------------------------------------------
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC_CONTROL = "smarteco/control"
TOPIC_ESTADO = "smarteco/estado"

# paho-mqtt v2 requiere el parámetro callback_api_version
client = mqtt.Client(client_id="SmartEcoHome_ControlWeb", callback_api_version=5)

ultimo_estado = "Esperando datos..."

# ---------------------------------------------
# CALLBACKS MQTT
# ---------------------------------------------
def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(TOPIC_ESTADO)

def on_message(client, userdata, message):
    global ultimo_estado
    try:
        data = json.loads(message.payload.decode())
        tipo = data.get("tipo", "")
        detalle = data.get("detalle", "")
        ultimo_estado = f"{tipo}: {detalle}"
    except:
        ultimo_estado = "Mensaje inválido recibido"


client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_start()

# ---------------------------------------------
# FUNCIÓN PARA ENVIAR COMANDOS MQTT
# ---------------------------------------------
def enviar_comando(action, value=0):
    payload = json.dumps({"action": action, "value": value})
    client.publish(TOPIC_CONTROL, payload)


# ---------------------------------------------
# UI STREAMLIT
# ---------------------------------------------
st.title("SmartEcoHome – Control por Botones")
st.subheader("Panel de control físico + sincronizado con ESP32")

st.markdown("### Estado del sistema:")
st.info(ultimo_estado)

st.markdown("---")
st.markdown("## 🔆 Control de Luz")

col1, col2 = st.columns(2)
if col1.button("Encender Luz"):
    enviar_comando("luz_on")
if col2.button("Apagar Luz"):
    enviar_comando("luz_off")

st.markdown("---")
st.markdown("## 🌬️ Control de Ventilador")

col3, col4 = st.columns(2)
if col3.button("Encender Ventilador"):
    enviar_comando("vent_on")
if col4.button("Apagar Ventilador"):
    enviar_comando("vent_off")

st.markdown("---")
st.markdown("## 🚪 Control de Puerta (Servo)")

col5, col6 = st.columns(2)
if col5.button("Abrir Puerta"):
    enviar_comando("puerta", 90)
if col6.button("Cerrar Puerta"):
    enviar_comando("puerta", 0)

st.markdown("---")
st.success("Conectado al broker MQTT y esperando eventos…")

