import paho.mqtt.client as mqtt
import time
import openai
# import grovepi


openai.api_key = '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'

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("wt/client1", 1)
    client.message_callback_add("wt/client1", client1_callback)

    client.subscribe("wt/client2", 1)
    client.message_callback_add("wt/client2", client2_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def client1_callback(client, userdata, msg):
    print(msg.payload)
    audio_file = msg.payload
    transcript = client.Audio.transcribe("whisper-1", audio_file)
    client.publish("wt/server", transcript)


def client2_callback(client, userdata, msg):
    audio_file = msg.payload
    transcript = client.Audio.transcribe("whisper-1", audio_file)
    client.publish("wt/server", transcript)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(.1)
