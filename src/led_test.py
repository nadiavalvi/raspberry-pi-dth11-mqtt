"""Prueba inicial de GPIO: enciende y apaga un LED conectado a GPIO18 (pin físico 12)."""
import time
import RPi.GPIO as GPIO

LED = 18  # Numeración BCM

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)


def encender_led(pin, encendido, apagado):
    GPIO.output(pin, True)
    time.sleep(encendido)
    GPIO.output(pin, False)
    time.sleep(apagado)


try:
    for _ in range(3):
        encender_led(LED, 3, 1)  # 3 s encendido, 1 s apagado
finally:
    GPIO.cleanup()
