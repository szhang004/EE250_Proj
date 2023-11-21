
import paho.mqtt.client as mqtt
import time
import sys
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

button_speak = 2
grovepi.pinMode(button_speak,"INPUT")


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

    
    setText_norefresh("hello")
    while True:

        if grovepi.digitalRead(button_speak):

            time.sleep(.5)

            print("PRESSED")
        
            if speak_on == True:
                msg = ''.join([chr(x) for x in mic_readings])
                client.publish("wt/client1", msg)
                print(msg)
                mic_readings = []

                print("Message Over")
                speak_on = False

            else:
                speak_on = True
                print("Speak")

        if speak_on == True:
            print("Listening")
            # mic_readings.append(mcp.read_adc(0))

        time.sleep(20/1000000.0)
