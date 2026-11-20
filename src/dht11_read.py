"""Lectura de temperatura y humedad del DHT11 (GPIO18) e impresión por consola cada 2 s."""
import time
import RPi.GPIO as GPIO
import dht11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
sensor = dht11.DHT11(pin=18)

try:
    while True:
        result = sensor.read()
        if result.is_valid():
            print(f"Temperatura: {result.temperature} grados")
            print(f"Humedad: {result.humidity} %")
        else:
            print("Error al leer el sensor")
        time.sleep(2)  # El DHT11 necesita >= 2 s entre lecturas
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
