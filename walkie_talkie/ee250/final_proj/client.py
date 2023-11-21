
import paho.mqtt.client as mqtt
import time
import sys
import RPi.GPIO as GPIO

# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')


import grovepi
from grove_rgb_lcd import *
import smbus

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# GPIO.setmode(GPIO.BOARD)

button_speak = 3
grovepi.pinMode(button_speak,"INPUT")

# GPIO.setup(button_speak, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
    mic_readings = []
    count = 0

    
    setText_norefresh("hello")
    while True:

        if not speak_on:
            button_stat = grovepi.digitalRead(button_speak)
            # button_stat = GPIO.input(button_speak)
            # print(button_stat)
            if not button_stat:
    
                time.sleep(.2)
                    
                speak_on = True
                mic_readings = []
                print("Speak")
        else:
            
            mic_readings.append(mcp.read_adc(0))
            # print(mic_readings)
            count += 1   
            print(count)
            if count == 25000:
                msg = ''.join([chr(x) for x in mic_readings])
                client.publish("wt/client1", msg)
                print("Message over")
            
                speak_on = False
                count = 0
        
        
        time.sleep(20/1000000.0)
