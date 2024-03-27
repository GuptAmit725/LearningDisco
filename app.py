from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
from PyPDF2 import PdfReader
from scripts import extract_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

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
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        extracted_text, textContentDict = extract_text_from_pdf(file_path)
        return render_template('display_text.html', textContentDict =  textContentDict)# render_template('book.html', text=extracted_text)

@app.route('/proread')
def proread():
    return render_template('proread.html')

@app.route('/texfile')
def display_text():
    with open('outputs\out_text.txt', 'r') as file:
        text_content = file.read()
    return render_template('display_text.html', text_content=text_content)

if __name__ == '__main__':
    app.run(debug=True)