import os
import uuid
from flask import Flask, flash, request, redirect, render_template, jsonify
from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment
from dotenv import load_dotenv
from openai import OpenAI

UPLOAD_FOLDER = 'files'
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
client = OpenAI(
    api_key=os.getenv('CHATGPT_API_KEY')
)

# save the user chat into a list of tuples.

chat = []


@app.route('/')
def root():
    return render_template('index.html', text="Transcription will be displayed here")

@app.route('/history')
def history():
    return render_template('historyindex.html')

@app.route('/chats')
def chats():
    return chat



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
        chat.append(('other', text))
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are helping a deaf person, to whom people talk using text. You need to give suggestions to respond to the text. Don't respond back with anything except for the Text Suggestions. Give a single Response without Quotation marks or numbering"},
                {"role": "user", "content": text}
            ],
            n=3  # Requesting 3 completions
        )
        os.remove(pcm_file_name)
        predictions = [ x.message.content for x in response.choices ]
        jsonify(text=text, predict=predictions)
        print(response)
        return jsonify(text=text, predict=predictions)
    
@app.route('/chat', methods=['POST'])
def chatadd():
    if 'text' not in request.form:
        flash('No text')
        return redirect(request.url)
    text = request.form['text']
    chat.append(('user', text))
    print(chat)
    return jsonify(text=text)
        
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=31337, debug=False)
