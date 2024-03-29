from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
# Import the document processing module
import utils
from dotenv import load_dotenv
import prompts
import openai
import OpenAIHandler
from graph import save_graph
import logging
import zipfile
import constants

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure necessary directories exist
for folder in [constants.UPLOAD_FOLDER, constants.EXTRACTED_TEXT_FOLDER, constants.CAPABILITY_TEXT_FOLDER]:
    os.makedirs(folder, exist_ok=True)


@app.route('/')
def index():
    return render_template(
        'index.html'
        )

@app.route('/upload', methods=['POST'])
def upload_file():

    utils.delete_files_in_folder(constants.UPLOAD_FOLDER)
    utils.delete_files_in_folder(constants.EXTRACTED_TEXT_FOLDER)
    utils.delete_files_in_folder(constants.CAPABILITY_TEXT_FOLDER)


    logging.info("Received a file upload request.")
    files = request.files.getlist('document')

    if not files:
        logging.warning("No files uploaded in the request.")
        return jsonify({'error': 'No files uploaded'}), 400
    

    # Check the number of files
    if len(files) > 3:
        return jsonify({'error': 'Maximum of 3 files can be uploaded'}), 400

    for file in files:
        if file.filename == '':
            logging.warning("File upload attempted with no file selected.")
            return jsonify({'error': 'No selected file'}), 400
        
        if file and not utils.allowed_file(file.filename, constants.ALLOWED_EXTENSIONS):
            return jsonify({'error': 'File type not allowed'}), 400
        
        if file and file.content_length > 5242880:  # 5 MB in bytes
            return jsonify({'error': 'File size exceeds limit'}), 400
        
        if file and utils.allowed_file(file.filename, constants.ALLOWED_EXTENSIONS):
            # Generate a timestamp format like '2023_01_01_12_00_00'
            timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            # Secure the filename and append the timestamp before the file extension
            filename_base, filename_ext = os.path.splitext(secure_filename(file.filename))
            filename = f"{filename_base}_{timestamp}{filename_ext}"
            file_path = os.path.join(constants.UPLOAD_FOLDER, filename)

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
            txt_path = os.path.join(constants.EXTRACTED_TEXT_FOLDER, txt_filename)
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                ##Extracted Text will be cleaned
                extracted_text = utils.clean_text(extracted_text)
                #corrected_text = OpenAIHandler.send_prompt("check_text_grammar_and_spelling", extracted_text)
                #txt_file.write(corrected_text)
                txt_file.write(extracted_text)
            logging.info(f"Extracted and saved text from {filename} to {txt_filename}")
        else:
            logging.warning(f"Uploaded file has a disallowed extension: {file.filename}")

    try:
        extracted_texts = utils.read_and_concat_text_files(constants.EXTRACTED_TEXT_FOLDER)
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
        extract_capabilities_from_text_chunk = utils.clean_text(prompts.extract_capabilities_from_text_chunk)
        if not extract_capabilities_from_text_chunk:
            raise ValueError("Extract capabilities from text chunk prompt is empty.")
    except Exception as e:
        print(f"Error cleaning 'extract_capabilities_from_text_chunk' prompt: {e}")
        extract_capabilities_from_text_chunk = ""  # Setting to a default empty string

    try:
        create_capability_map = utils.clean_text(prompts.create_capability_map)
        if not create_capability_map:
            raise ValueError("Create capability map prompt is empty.")
    except Exception as e:
        print(f"Error cleaning 'create_capability_map' prompt: {e}")
        create_capability_map = ""  # Setting to a default empty string

    capabilities = []


    logging.info("Processing text chunks for capability extraction.")

    for chunk in text_chunks:
        combined_capability = []
        for _ in range(3):  # Loop three times
            try:
                capability = OpenAIHandler.send_prompt(extract_capabilities_from_text_chunk, chunk)
                if capability:
                    combined_capability.append(capability)
            except Exception as e:
                logging.error(f"Error processing chunk: {e}")
        
        # Combine the results from the three iterations
        if combined_capability:
            combined_capability_str = ' '.join(combined_capability)
            capabilities.append(combined_capability_str)


    logging.info("All capabilities have been processed and saved.")
    # Filter out None or empty values from capabilities
    filtered_capabilities = [cap for cap in capabilities if cap]

    # Join all capabilities into a single string
    all_capabilities_text = '\n'.join(filtered_capabilities)

    capability_map = OpenAIHandler.send_prompt("create capability map", all_capabilities_text)

    #Add description to each capability
    capability_map_with_description = OpenAIHandler.send_prompt("add description", capability_map)

    utils.save_as_json_file(capability_map_with_description, constants.CAPABILITY_TEXT_FOLDER)

    return jsonify({'message': 'Files successfully uploaded'}), 200
    

@app.route('/download')
def download_graph():

    # Generate a timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Paths with timestamps to the JSON, PDF, and CSV files
    json_file_path = f'capabilities/data.json'
    pdf_file_path = f"static/capabilities_{timestamp}.pdf"
    csv_file_path = f"static/capabilities_{timestamp}.csv"

    # Read and parse the JSON file
    json_data = utils.read_json_from_file(json_file_path)
    save_graph(json_data, pdf_file_path)

    # Convert JSON data to CSV format
    utils.convert_json_to_csv(json_data, csv_file_path)

    # Create a zip file with the same timestamp
    zip_file_path = f"static/capabilities_{timestamp}.zip"
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(pdf_file_path, os.path.basename(pdf_file_path))
        zipf.write(csv_file_path, os.path.basename(csv_file_path))

    # Send zip file as attachment with the timestamp in the download name
    return send_file(zip_file_path, as_attachment=True, download_name=f'capabilities_{timestamp}.zip')


if __name__ == '__main__':
    app.run(debug=True)
