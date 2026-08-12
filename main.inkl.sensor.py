import time
from machine import Pin
from machine import Pin, ADC #Moisture Sensor
import dht
import ujson
from umqtt.simple import MQTTClient

# --- 1. PIN-KONFIGURATION ---
led_rot = Pin(14, Pin.OUT)     # D14 für Rot
led_gruen = Pin(18, Pin.OUT)   # D12 für Grün
sensor = dht.DHT22(Pin(4))     # D4 für den DHT22 Temperatur-Sensor

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.f4.htw-berlin.de"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "f4/bis/byte-bank"

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()
print("Connected!")

prev_weather = ""

while True:
    print("Measuring weather conditions... ", end="")
    sensor.measure()
    
    temp = sensor.temperature()
    humidity = sensor.humidity()

    # --- 2. LAMPEN STEUERN (> 30 Grad = Rot, sonst Grün) ---
    if temp > 30:
        led_rot.value(1)      # Rot AN
        led_gruen.value(0)    # Grün AUS
    else:
        led_rot.value(0)      # Rot AUS
        led_gruen.value(1)    # Grün AN
    
    message = ujson.dumps({
        "temp": temp,
        "humidity": humidity,
       # "time": time_str
    })

    if message != prev_weather:
        print("Updated!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)
        prev_weather = message
    else:
        print("No change")

    time.sleep(1)