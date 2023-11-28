from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
# Import the document processing module
import utils
from dotenv import load_dotenv
import config
import openai
import OpenAIHandler
from config import (UPLOAD_FOLDER, EXTRACTED_TEXT_FOLDER,
                    ALLOWED_EXTENSIONS, CAPABILITY_TEXT_FOLDER)

from graph import save_graph
import logging

# Load environment variables from .env file
load_dotenv()




# Configuration from environment variables
UPLOAD_FOLDER = config.UPLOAD_FOLDER
EXTRACTED_TEXT_FOLDER = config.EXTRACTED_TEXT_FOLDER
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS
CAPABILITY_TEXT_FOLDER = config.CAPABILITY_TEXT_FOLDER

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure necessary directories exist
for folder in [UPLOAD_FOLDER, EXTRACTED_TEXT_FOLDER, CAPABILITY_TEXT_FOLDER]:
    os.makedirs(folder, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():

    utils.delete_files_in_folder(UPLOAD_FOLDER)
    utils.delete_files_in_folder(EXTRACTED_TEXT_FOLDER)
    utils.delete_files_in_folder(CAPABILITY_TEXT_FOLDER)


    logging.info("Received a file upload request.")
    files = request.files.getlist('document')

    if not files:
        logging.warning("No files uploaded in the request.")
        return jsonify({'error': 'No files uploaded'}), 400


    for file in files:
        if file.filename == '':
            logging.warning("File upload attempted with no file selected.")
            return jsonify({'error': 'No selected file'}), 400
        if file and utils.allowed_file(file.filename, ALLOWED_EXTENSIONS):
            # Generate a timestamp format like '2023_01_01_12_00_00'
            timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            # Secure the filename and append the timestamp before the file extension
            filename_base, filename_ext = os.path.splitext(secure_filename(file.filename))
            filename = f"{filename_base}_{timestamp}{filename_ext}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            logging.info(f"Saving uploaded file: {filename}")
            file.save(file_path)

            # Extrahieren Sie den Text aus der Datei basierend auf dem Dateityp
            extracted_text = ""
            if filename.lower().endswith('.pdf'):
                extracted_text = utils.extract_text_from_pdf(file_path)
            elif filename.lower().endswith('.docx'):
                extracted_text = utils.extract_text_from_docx(file_path)
            else:
                logging.error(f"Unsupported file format for text extraction: {filename_ext}")
                return jsonify({'error': 'File format not supported for text extraction'}), 400

            # Speichern Sie den extrahierten Text in einer .txt-Datei
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(EXTRACTED_TEXT_FOLDER, txt_filename)
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                ##Extracted Text will be cleaned
                extracted_text = utils.clean_text(extracted_text)
                txt_file.write(extracted_text)
            logging.info(f"Extracted and saved text from {filename} to {txt_filename}")
        else:
            logging.warning(f"Uploaded file has a disallowed extension: {file.filename}")


    extracted_texts = utils.read_and_concat_text_files(EXTRACTED_TEXT_FOLDER)

    text_chunks = utils.get_text_chunks(extracted_texts)

    extract_capabilities_from_text_chunk = utils.clean_text(config.extract_capabilities_from_text_chunk_prompt)
    create_capability_map= utils.clean_text(config.create_capability_map_prompt)

    capabilities = []

    logging.info("Processing text chunks for capability extraction.")

    for chunk in text_chunks:
        try:
            capability = OpenAIHandler.send_prompt(extract_capabilities_from_text_chunk, chunk)
            if capability:
                capabilities.append(capability)
        except Exception as e:
            logging.error(f"Error processing chunk: {e}")


    logging.info("All capabilities have been processed and saved.")
    # Filter out None or empty values from capabilities
    filtered_capabilities = [cap for cap in capabilities if cap]

    # Join all capabilities into a single string
    all_capabilities_text = '\n'.join(filtered_capabilities)

    capability_map = OpenAIHandler.send_prompt(create_capability_map, all_capabilities_text)

    utils.save_as_json_file(capability_map, CAPABILITY_TEXT_FOLDER)

    return jsonify({'message': 'Files successfully uploaded'}), 200
    

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
