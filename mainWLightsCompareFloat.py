import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# --- PIN-KONFIGURATION ---
led_rot = Pin(14, Pin.OUT)
led_gruen = Pin(18, Pin.OUT)
sensor = dht.DHT22(Pin(4))

# MQTT Parameter
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.f4.htw-berlin.de"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "f4/bis/byte-bank"

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()
print("Connected!")

prev_temp = None
prev_humidity = None

while True:
    print("Measuring weather conditions... ", end="")
    sensor.measure()

    temp = sensor.temperature()
    humidity = sensor.humidity()

    # --- LAMPEN STEUERN ---
    if temp > 30:
        led_rot.value(1)
        led_gruen.value(0)
    else:
        led_rot.value(0)
        led_gruen.value(1)

    # --- VERGLEICH VOR TRANSFORMATION ---
    if temp != prev_temp or humidity != prev_humidity:
        print("Updated!")
        message = ujson.dumps({
            "temp": temp,
            "humidity": humidity,
        })
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)
        prev_temp = temp
        prev_humidity = humidity
    else:
        print("No change")

    time.sleep(1)
