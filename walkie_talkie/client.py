
import paho.mqtt.client as mqtt
import time
import grovepi
from grove_rgb_lcd import *

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

import os

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

button_speak = 1
button_hear = 2

GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(button_speak, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(button_hear, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

values = []


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("wt/server", 1)
    client.message_callback_add("wt/server", server_callback)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def server_callback(client, userdata, msg):
    for num in msg.payload:
        
        time.sleep(20/1000000.0)
    

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    speak_on = False
    hear_on = False
    mic_readings = []

    while True:

        if GPIO.input(button_speak) == GPIO.HIGH m:

            if speak_on == True:
                client.publish("wt/client1", mic_readings)
                mic_readings = []
                speak_on = False

            else:
                speak_on = True

        if speak_on == True:
            mic_readings.append(mcp.read_adc(0))

        time.sleep(20/1000000.0)
