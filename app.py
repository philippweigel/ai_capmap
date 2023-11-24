from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
# Import the document processing module
import utils
from dotenv import load_dotenv
import config
import openai
from OpenAIHandlerClass import OpenAIHandler
from config import (UPLOAD_FOLDER, EXTRACTED_TEXT_FOLDER,
                    ALLOWED_EXTENSIONS, CAPABILITY_TEXT_FOLDER)

from graph import save_graph

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
UPLOAD_FOLDER = config.UPLOAD_FOLDER
EXTRACTED_TEXT_FOLDER = config.EXTRACTED_TEXT_FOLDER
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS
CAPABILITY_TEXT_FOLDER = config.CAPABILITY_TEXT_FOLDER

openai.api_key = os.getenv("OPENAI_API_KEY")




app = Flask(__name__)


# Ensure necessary directories exist
for folder in [UPLOAD_FOLDER, EXTRACTED_TEXT_FOLDER, CAPABILITY_TEXT_FOLDER]:
    os.makedirs(folder, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('document')

    if not files:
        return jsonify({'error': 'No files uploaded'}), 400


    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and utils.allowed_file(file.filename, ALLOWED_EXTENSIONS):
            # Generate a timestamp format like '2023_01_01_12_00_00'
            timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            # Secure the filename and append the timestamp before the file extension
            filename_base, filename_ext = os.path.splitext(secure_filename(file.filename))
            filename = f"{filename_base}_{timestamp}{filename_ext}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Extrahieren Sie den Text aus der Datei basierend auf dem Dateityp
            extracted_text = ""
            if filename.lower().endswith('.pdf'):
                extracted_text = utils.extract_text_from_pdf(file_path)
            elif filename.lower().endswith('.docx'):
                extracted_text = utils.extract_text_from_docx(file_path)
            else:
                return jsonify({'error': 'File format not supported for text extraction'}), 400

            # Speichern Sie den extrahierten Text in einer .txt-Datei
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(EXTRACTED_TEXT_FOLDER, txt_filename)
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                ##Whitespaces und NewLines werden entfernt
                extracted_text = utils.clean_text(extracted_text)
                txt_file.write(extracted_text)


    extracted_texts = utils.read_and_concat_text_files(EXTRACTED_TEXT_FOLDER)
    openai_handler = OpenAIHandler(extracted_texts)
    capabilities = openai_handler.extract_capabilities_from_extracted_texts()

    utils.save_as_json_file(capabilities, CAPABILITY_TEXT_FOLDER)


    return jsonify({'message': 'File successfully uploaded'}), 200
    

@app.route('/download')
def download_graph():
    # Path to the JSON file
    json_file_path = 'capabilities/data.json'
    json_data = utils.read_json_from_file(json_file_path)

    pdf_file_path = "static/file.pdf"

    # Read and parse the JSON file
    save_graph(json_data, pdf_file_path)

    return send_file(pdf_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
