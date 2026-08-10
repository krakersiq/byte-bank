"""
MicroPython IoT Weather Station Example for Wokwi.com

To view the data:

1. Go to http://www.hivemq.com/demos/websocket-client/
2. Click "Connect"
3. Under Subscriptions, click "Add New Topic Subscription"
4. In the Topic field, type "wokwi-weather" then click "Subscribe"

Now click on the DHT22 sensor in the simulation,
change the temperature/humidity, and you should see
the message appear on the MQTT Broker, in the "Messages" pane.

Copyright (C) 2022, Uri Shaked

https://wokwi.com/arduino/projects/322577683855704658
"""

import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient




# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.f4.htw-berlin.de"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "f4/bis/byte-bank"


sensor = dht.DHT22(Pin(4))

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")


prev_weather = ""
while True:
  print("Measuring weather conditions... ", end="")
  sensor.measure()
  
  t = time.localtime()
  time_str = "{:02d}:{:02d}:{:02d}".format(t[3],t[4],t[5])
  
  message = ujson.dumps({
    "temp": sensor.temperature(),
    "humidity": sensor.humidity(),
    "time": time_str
  })
  if message != prev_weather:
    print("Updated!")
    print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
    client.publish(MQTT_TOPIC, message)
    prev_weather = message
  else:
    print("No change")
  time.sleep(1)



