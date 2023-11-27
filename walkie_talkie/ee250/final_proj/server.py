from flask import Flask, jsonify, render_template

import paho.mqtt.client as mqtt
import time
import openai
from pydub import AudioSegment
import io
import wave

app = Flask('final_proj')

openai.api_key= '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'
# import grovepi

transcript = None
message_lock = threading.Lock()

def create_wav_from_analog(analog_data, filename="output.wav", sample_rate=50000):
    with wave.open(filename, "wb") as wav_file:
        nchannels = 1
        sampwidth = 1  # 1 byte for 8 bit
        framerate = sample_rate
        nframes = len(analog_data)
        comptype = "NONE"
        compname = "not compressed"

        # Set parameters
        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        
        # Write raw data
        wav_file.writeframes(analog_data)


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

    # audio_bytes = bytearray(byte_string)
    create_wav_from_analog(byte_string)
    # print(audio_bytes)

    # The format will depend on the format of your raw audio data
    # audio_segment = AudioSegment.from_raw(io.BytesIO(audio_bytes), sample_width=2, frame_rate=44100, channels=2)

    audio_segment = AudioSegment.from_wav("output.wav")

    # Export to an MP3 file
    audio_segment.export("output.mp3", format="mp3")

    audio_file = open("output.mp3", "rb")

    global transcript
    with message_lock:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
        client.publish("wt/server", transcript['text'])
        print(transcript['text'])
    publish()


def client2_callback(client, userdata, msg):
    byte_string = msg.payload

    # audio_bytes = bytearray(byte_string)
    create_wav_from_analog(byte_string)
    # print(audio_bytes)

    # The format will depend on the format of your raw audio data
    # audio_segment = AudioSegment.from_raw(io.BytesIO(audio_bytes), sample_width=2, frame_rate=44100, channels=2)

    audio_segment = AudioSegment.from_wav("output.wav")

    # Export to an MP3 file
    audio_segment.export("output.mp3", format="mp3")

    audio_file = open("output.mp3", "rb")

    global transcript
    with message_lock:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
        client.publish("wt/server", transcript['text'])
        print(transcript['text'])
    publish()
    
    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/publish/message')
def publish():
    with message_lock: 
        return render_template('display.html', user_input=transcript['text'])

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="test.mosquitto.org", port=1883, keepalive=60)




if __name__ == '__main__':

    mqtt_thread = threading.Thread(target=client.loop_forever)
    mqtt_thread.start()
    app.run(debug=False)

    while True:
        time.sleep(.1)
