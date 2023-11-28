
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

from gpiozero import Button
button = Button(16)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("wt/server", 1)
    client.message_callback_add("wt/server", server_callback)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def server_callback(client, userdata, msg):
    transcript = msg.payload.decode()
    setText_norefresh(transcript)
    

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
            
            if button.is_pressed:
    
                time.sleep(.2)
                    
                speak_on = True
                mic_readings = []
                print("Speak Now")
                setText_norefresh("Speak Now")
                # button_stat = 0
        else:

            # append 8 bit with reading
            mic_readings.append(mcp.read_adc(0) >> 2)

            count += 1  
            if count == 25000:
                print(mic_readings)
                msg = ''.join([chr(x) for x in mic_readings])
                
                client.publish("wt/client", msg)
                print("Message over")
                setText_norefresh("Message over")
            
                speak_on = False
                count = 0
        
        
        time.sleep(20/1000000.0)
