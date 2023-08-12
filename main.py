import os
import uuid
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from speech_recognition import Recognizer, AudioFile
import soundfile as sf
import numpy as np
from pydub import AudioSegment

UPLOAD_FOLDER = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
    return render_template('index.html', text="Transcription will be displayed here")


@app.route('/save-record', methods=['POST'])
def save_record():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    file_name = str(uuid.uuid4()) + '.wav'
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(full_file_name)
    
    pcm_file_name = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + '_pcm.wav')
    audio_segment = AudioSegment.from_file(full_file_name)
    audio_segment = audio_segment.set_channels(1)  # Convert to mono
    audio_segment.export(pcm_file_name, format="wav")

    os.remove(full_file_name)


    recognizer = Recognizer()
    with AudioFile(pcm_file_name) as source:
        audio_data = recognizer.record(source)
        print('Recognizing...')
        text = recognizer.recognize_google(audio_data)
        print(text)

        os.remove(pcm_file_name)
        return jsonify(text=text)
        
    
if __name__ == '__main__':
    app.run()