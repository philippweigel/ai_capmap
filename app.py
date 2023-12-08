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
import zipfile

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
    return render_template(
        'index.html',
        extract_capabilities_from_text_chunk_prompt=utils.clean_text(config.extract_capabilities_from_text_chunk_prompt),
        create_capability_map_prompt=utils.clean_text(config.create_capability_map_prompt),
        divide_capabilities_prompt=utils.clean_text(config.divide_capabilities_prompt),
        check_naming_of_capabilities_prompt=utils.clean_text(config.check_naming_of_capabilities_prompt),
        aggregateSameTopicPrompt=utils.clean_text(config.aggregate_same_topic_prompt),
        )

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

            logging.info(f"Process Extracting text started")

            # Extrahieren Sie den Text aus der Datei basierend auf dem Dateityp
            extracted_text = ""
            if filename.lower().endswith('.pdf'):
                extracted_text = utils.extract_text_from_pdf(file_path)
                logging.info(f"Text from PDF extracted: {filename}")
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


    try:
        extracted_texts = utils.read_and_concat_text_files(EXTRACTED_TEXT_FOLDER)
        if not extracted_texts:
            raise ValueError("Extracted texts are empty.")
    except Exception as e:
        print(f"Error reading and concatenating text files: {e}")
        extracted_texts = ""  # Setting to a default empty string

    try:
        text_chunks = utils.get_text_chunks(extracted_texts)
        if not text_chunks:
            raise ValueError("Text chunks are empty.")
    except Exception as e:
        print(f"Error getting text chunks: {e}")
        text_chunks = []  # Setting to a default empty list

    try:
        extract_capabilities_from_text_chunk = utils.clean_text(config.extract_capabilities_from_text_chunk_prompt)
        if not extract_capabilities_from_text_chunk:
            raise ValueError("Extract capabilities from text chunk prompt is empty.")
    except Exception as e:
        print(f"Error cleaning 'extract_capabilities_from_text_chunk' prompt: {e}")
        extract_capabilities_from_text_chunk = ""  # Setting to a default empty string

    try:
        create_capability_map = utils.clean_text(config.create_capability_map_prompt)
        if not create_capability_map:
            raise ValueError("Create capability map prompt is empty.")
    except Exception as e:
        print(f"Error cleaning 'create_capability_map' prompt: {e}")
        create_capability_map = ""  # Setting to a default empty string

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
    # Paths to the JSON, PDF, and CSV files
    json_file_path = 'capabilities/data.json'
    pdf_file_path = "static/capabilities.pdf"
    csv_file_path = "static/capabilities.csv"

    # Read and parse the JSON file
    json_data = utils.read_json_from_file(json_file_path)
    save_graph(json_data, pdf_file_path)

    # Convert JSON data to CSV format
    utils.convert_json_to_csv(json_data, csv_file_path)

    # Create a zip file
    zip_file_path = "static/capabilities.zip"
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(pdf_file_path, os.path.basename(pdf_file_path))
        zipf.write(csv_file_path, os.path.basename(csv_file_path))

    # Send zip file as attachment
    return send_file(zip_file_path, as_attachment=True, download_name='capabilities.zip')
    #return send_file(csv_file_path, as_attachment=True, download_name='capabilities.csv')


if __name__ == '__main__':
    app.run(debug=True)
