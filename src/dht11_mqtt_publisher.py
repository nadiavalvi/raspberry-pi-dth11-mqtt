"""
Publica temperatura y humedad del DHT11 en un broker MQTT (Mosquitto).

Configuración por variables de entorno (valores por defecto entre paréntesis):
  MQTT_BROKER   (localhost)   IP o hostname del broker
  MQTT_PORT     (1883)
  MQTT_TOPIC_T  (casa/habitacion1/temperatura)
  MQTT_TOPIC_H  (casa/habitacion1/humedad)
  INTERVALO     (5)           segundos entre lecturas
"""
import os
import time

import dht11
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC_T = os.getenv("MQTT_TOPIC_T", "casa/habitacion1/temperatura")
TOPIC_H = os.getenv("MQTT_TOPIC_H", "casa/habitacion1/humedad")
INTERVALO = int(os.getenv("INTERVALO", "5"))
REINTENTOS = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
sensor = dht11.DHT11(pin=18)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Me he conectado al broker MQTT!")
    else:
        print(f"Error en la conexión MQTT: {reason_code}")


def leer_sensor():
    """Lee el DHT11 con reintentos (el sensor falla de forma puntual por timing)."""
    for _ in range(REINTENTOS):
        result = sensor.read()
        if result.is_valid():
            return result.temperature, result.humidity
        time.sleep(2)
    return None


# paho-mqtt 2.x: se usa la Callback API v2 (evita el DeprecationWarning de la v1)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        lectura = leer_sensor()
        if lectura:
            temperatura, humedad = lectura
            print(f"Temperatura: {temperatura} grados | Humedad: {humedad} %")
            client.publish(TOPIC_T, str(temperatura))
            client.publish(TOPIC_H, str(humedad))
        else:
            print("Error al leer el sensor")
        time.sleep(INTERVALO)
except KeyboardInterrupt:
    print("Desconectando del broker")
finally:
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()
    print("Desconectado")
