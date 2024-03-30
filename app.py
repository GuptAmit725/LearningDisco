from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import json
from PyPDF2 import PdfReader
from scripts import extract_pdf
from AI_module.video_urls import ai_in_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

SAVE_PATH = './outputs'
text = """
The behavior of all objects can be described by saying that objects tend to "keep on doing what they're doing" (unless acted upon by an unbalanced force). If at rest, they will continue in this same state of rest. If in motion with an eastward velocity of 5 m/s, they will continue in this same state of motion (5 m/s, East). If in motion with a leftward velocity of 2 m/s, they will continue in this same state of motion (2 m/s, left). The state of motion of an object is maintained as long as the object is not acted upon by an unbalanced force. All objects resist changes in their state of motion - they tend to "keep on doing what they're doing."
"""
video_urls = ai_in_video()
video_links = video_urls.fetch_urls(text)
#print(video_links)

def extract_text_from_pdf(pdf_path):
    textContentDict = {}
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            text = ""
            textContentDict = extract_pdf.main(pdf_path)
            print(textContentDict.keys())
            with open("outputs\out_text.txt", 'r') as f:
                text = f.read()
            os.remove("outputs\out_text.txt")
            # for page in reader.pages:
            #     text += page.extract_text().replace('\n',' ')  # Add a line break after each page's text
            return text, textContentDict
    except Exception as e:
        return str(e), ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read')
def read():
    return render_template('read.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global textContentDict
    global file_path
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(SAVE_PATH, filename)#(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        extracted_text, textContentDict = extract_text_from_pdf(file_path)
        return render_template('display_text.html', textContentDict =  textContentDict, initial_video = video_links[0], video_links = video_links)# render_template('book.html', text=extracted_text)

@app.route('/proread')
def proread():
    return render_template('proread.html')

@app.route('/texfile')
def display_text():
    with open('outputs\out_text.txt', 'r') as file:
        text_content = file.read()
    return render_template('display_text.html', text_content=text_content)

@app.route('/process_doubt', methods=['POST'])
def process_doubt():
    doubt_text = request.json.get('doubt')  # Get the doubt text from the request
    # Process the doubt text here (e.g., perform some analysis or save it to a database)
    print("Received doubt text:", doubt_text)
    video_links = video_urls.fetch_urls(doubt_text)
    print(video_links)
    # extracted_text, textContentDict = extract_text_from_pdf(file_path)
    return jsonify({"video_urls": video_links})

if __name__ == '__main__':
    app.run(debug=True)
