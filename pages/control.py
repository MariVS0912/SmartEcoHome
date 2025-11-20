import streamlit as st
import paho.mqtt.client as mqtt
import json

BROKER = "broker.emqx.io"
TOPIC_CONTROL = "smarteco/control"
TOPIC_ESTADO = "smarteco/estado"

# Necesario por paho-mqtt v2
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="SmartEcoHome_ControlWeb")

estado_recibido = st.session_state.get("estado_recibido", "Esperando estado...")

# ---------- CALLBACK AL RECIBIR MENSAJE ----------
def on_message(client, userdata, message):
    payload = message.payload.decode()
    try:
        data = json.loads(payload)
        st.session_state["estado_recibido"] = f"{data['tipo']}: {data['detalle']}"
    except:
        st.session_state["estado_recibido"] = payload

client.on_message = on_message

# ---------- CONEXIÓN ----------
def conectar_mqtt():
    if not client.is_connected():
        client.connect(BROKER, 1883, 60)
        client.subscribe(TOPIC_ESTADO)
        client.loop_start()

conectar_mqtt()

# ---------- UI ----------
st.title("🔧 Control SmartEcoHome")

st.subheader("Estado del sistema")
st.info(st.session_state.get("estado_recibido", "Esperando datos..."))

col1, col2 = st.columns(2)

with col1:
    if st.button("💡 Encender luz"):
        client.publish(TOPIC_CONTROL, json.dumps({"action": "luz_on"}))
    if st.button("🌀 Encender ventilador"):
        client.publish(TOPIC_CONTROL, json.dumps({"action": "vent_on"}))
    if st.button("🔓 Abrir puerta"):
        client.publish(TOPIC_CONTROL, json.dumps({"action": "puerta", "value": 90}))

with col2:
    if st.button("💡 Apagar luz"):
        client.publish(TOPIC_CONTROL, json.dumps({"action": "luz_off"}))
    if st.button("🌀 Apagar ventilador"):
        client.publish(TOPIC_CONTROL, json.dumps({"action": "vent_off"}))
    if st.button("🔒 Cerrar puerta"):
        client.publish(TOPIC_CONTROL, json.dumps({"action": "puerta", "value": 0}))
