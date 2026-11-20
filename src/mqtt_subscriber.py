"""Suscriptor MQTT para PC: muestra por pantalla las lecturas recibidas."""
import os

import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "casa/habitacion1/#")  # '#' = todos los subtopics


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado al broker {BROKER}:{PORT} ({reason_code})")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()
