from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
from docx import Document
from datetime import datetime
from openai import OpenAI

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
EXTRACTED_TEXT_FOLDER = 'extracted_text'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

# Stellen Sie sicher, dass der Upload-Ordner existiert
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(EXTRACTED_TEXT_FOLDER):
    os.makedirs(EXTRACTED_TEXT_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # Generate a timestamp format like '2023_01_01_12_00_00'
        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        # Secure the filename and append the timestamp before the file extension
        filename_base, filename_ext = os.path.splitext(secure_filename(file.filename))
        filename = f"{filename_base}_{timestamp}{filename_ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extrahieren Sie den Text aus der Datei basierend auf dem Dateityp
        extracted_text = ""
        if filename.lower().endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        elif filename.lower().endswith('.docx'):
            extracted_text = extract_text_from_docx(file_path)
        else:
            return jsonify({'error': 'File format not supported for text extraction'}), 400

        # Speichern Sie den extrahierten Text in einer .txt-Datei
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(EXTRACTED_TEXT_FOLDER, txt_filename)
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(extracted_text)

        return jsonify({'message': 'File successfully uploaded'}), 200
    

@app.route('/analyze', methods=['POST'])
def analyze_files():
    texts = []
    files = os.listdir(EXTRACTED_TEXT_FOLDER)

    # Concatenate all texts from .txt files
    for file_name in files:
        if file_name.endswith('.txt'):
            file_path = os.path.join(EXTRACTED_TEXT_FOLDER, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                texts.append(file.read())

    # Combine all texts into a single string (if needed)
    combined_text = " ".join(texts)

    # Here you would call the ChatGPT API
    client = OpenAI(
        api_key = os.environ.get("OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages={

        },
        response_format= "json_format"

    )


    if response.status_code == 200:
        # Process the response and extract capabilities
        capabilities = response.json()['choices'][0]['text']
    else:
        capabilities = "Error: Could not process the document."

    # Return the capabilities in the response, or save them as needed
    return jsonify({'capabilities': capabilities})

if __name__ == '__main__':
    app.run(debug=True)
