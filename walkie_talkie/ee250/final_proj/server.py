from flask import Flask, jsonify, render_template, redirect
import requests
import time
import openai
from pydub import AudioSegment
import io
import wave

app = Flask('final_proj')

openai.api_key= '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'
# import grovepi

transcript = ''

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
    

@app.route('/')
def index():
    global TRANSCRIPT
    return render_template('index.html', user_input=transcript)


@app.route('/callback', methods=['POST'])
def callback():
    byte_string = request.get_json()
    transcript = process_audio(byte_string)
    res = jsonify({})
    res.status_code = 201 # Status code for "created"
    redirect(url_for('index'))
    return res


if __name__ == "__main__":
    app.run(host='10.0.2.15', port=5000, debug=True)

