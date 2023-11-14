import requests
import grovepi
import time

import os

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# URL of the server endpoint you want to send data to
url = 'http://<Your_Server_IP>:5000/submit'

# Sensor connected to port D4 (for example, a temperature sensor)
sensor_port = 4
grovepi.pinMode(sensor_port, "INPUT")

while True:
    try:
        
        values[i] = mcp.read_adc(i)

        # Read from the sensor (this function will depend on your sensor type)
        sensor_value = grovepi.analogRead(sensor_port)

        # audio_file = open("/audio.mp3", "rb")
        # transcript = openai.Audio.transcribe("whisper-1", audio_file)
        # print(transcript)

        # Here we're just sending the raw value, but you might want to
        # apply some conversion to get meaningful data from your sensor
        data = {'sensor_value': sensor_value}

        # Send the data as a POST request to the server
        response = requests.post(url, json=data)

        # Check the response from the server
        if response.status_code == 200:
            print('Data sent successfully')
        else:
            print('Failed to send data: ', response.text)

        # Wait for a while before sending the next reading
        time.sleep(10)

    except IOError:
        print("Error reading from the sensor")
    except requests.RequestException as e:
        print("Error sending request to the server: ", e)
