import streamlit as st
import paho.mqtt.client as mqtt
import json

st.title("🔧 SmartEcoHome – Control Manual")

# ---- MQTT Config ----
BROKER = "broker.mqttdashboard.com"
TOPIC_PUBLISH = "SmartEcoHome/Actions"

client = mqtt.Client(client_id="control_streamlit")
client.connect(BROKER, 1883, 60)

def send_command(command, value=None):
    payload = {"Act1": command}
    if value is not None:
        payload["Analog"] = value
    client.publish(TOPIC_PUBLISH, json.dumps(payload))

# ---- UI ----
st.subheader("💡 Control de Luces")
col1, col2 = st.columns(2)
with col1:
    if st.button("Encender Luz"):
        send_command("ON")
with col2:
    if st.button("Apagar Luz"):
        send_command("OFF")

st.divider()

st.subheader("🪟 Control de Escotilla")
col3, col4 = st.columns(2)
with col3:
    if st.button("Abrir Escotilla"):
        send_command("Abre la escotilla")
with col4:
    if st.button("Cerrar Escotilla"):
        send_command("Cierra la escotilla")

st.divider()

st.subheader("🔧 Servo Manual")
angulo = st.slider("Ángulo del servo", 0, 100, 0)
if st.button("Enviar"):
    send_command("SET_SERVO", angulo)

