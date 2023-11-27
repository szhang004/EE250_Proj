import paho.mqtt.client as mqtt
import time
import openai
from pydub import AudioSegment
import io

openai.api_key= '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'
# import grovepi




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
    byte_string = msg.payload

    audio_bytes = bytearray(byte_string)
    print(audio_bytes)

    # The format will depend on the format of your raw audio data
    audio_segment = AudioSegment.from_raw(io.BytesIO(audio_bytes), sample_width=2, frame_rate=44100, channels=2)

    # Export to an MP3 file
    audio_segment.export("output.mp3", format="mp3")

    audio_file = open("output.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    client.publish("wt/server", str(transcript['text'].decode()))
    print(transcript['text'])


def client2_callback(client, userdata, msg):
    byte_string = msg.payload

    audio_bytes = bytearray(byte_string)
    print(audio_bytes)


    # The format will depend on the format of your raw audio data
    audio_segment = AudioSegment.from_raw(io.BytesIO(audio_bytes), sample_width=2, frame_rate=44100, channels=2)

    # Export to an MP3 file
    audio_segment.export("output.mp3", format="mp3")

    audio_file = open("output.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    client.publish("wt/server", transcript['text'])
    print(transcript['text'])


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(.1)
