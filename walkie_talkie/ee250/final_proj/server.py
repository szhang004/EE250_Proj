# from flask import Flask, jsonify, render_template, redirect, url_for

import paho.mqtt.client as mqtt
import time
import openai
from pydub import AudioSegment
import io
import wave

# app = Flask('final_proj')

openai.api_key= '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'
# import grovepi

TRANSCRIPT = ''

def process_audio(analog_data, filename="output.wav", sample_rate=50000):
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
        
    audio_segment = AudioSegment.from_wav("output.wav")

    # Export to an MP3 file
    audio_segment.export("output.mp3", format="mp3")

    audio_file = open("output.mp3", "rb")

    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']
        

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("wt/client", 1)
    client.message_callback_add("wt/client", client_callback)


# @app.route('/')
# def index():
#     global TRANSCRIPT
#     return render_template('index.html', user_input=TRANSCRIPT)


@app.route('/client_callback')
def client_callback(client, userdata, msg):
    
    byte_string = msg.payload
    
    global TRANSCRIPT
    TRANSCRIPT = process_audio(byte_string)

    client.publish("wt/server", TRANSCRIPT)

    print(TRANSCRIPT)

    # return redirect(url_for('index'))
    
 
client = mqtt.Client()
client.on_connect = on_connect
client.connect(host="test.mosquitto.org", port=1883, keepalive=60)




if __name__ == '__main__':
    client.loop_start()
    # app.run(debug=False)
