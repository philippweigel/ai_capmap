import json
import os
from docx import Document
import pytesseract
from pdf2image import convert_from_path
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
import csv

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_text_from_pdf(pdf_path):
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    # Initialize an empty list to hold extracted text
    extracted_texts = []

    # Extract text from each image
    for image in images:
        text = pytesseract.image_to_string(image)
        extracted_texts.append(text)

    # Combine all extracted texts into a single string
    combined_text = ' '.join(extracted_texts)
    return combined_text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def read_and_concat_text_files(folder_path):
    """Reads all text files in a folder and concatenates their content."""
    texts = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                texts.append(file.read())
    return " ".join(texts)


def clean_text(text):
    # Zerlegt den Text in Zeilen und entfernt Newlines
    lines = text.split('\n')

    # Entfernt führende und nachfolgende Leerzeichen sowie Einrückungen in jeder Zeile
    cleaned_lines = [line.strip() for line in lines]

    # Fügt die bereinigten Zeilen wieder zu einem String zusammen
    cleaned_text = ' '.join(cleaned_lines)

    # Entfernt überflüssige Leerzeichen zwischen den Wörtern
    cleaned_text = ' '.join(cleaned_text.split())

    return cleaned_text

def save_as_json_file(data, file_path):
    file_name = "data.json"
    file_path = file_path + file_name

    try:
        # Check if data is a JSON string and parse it into a dictionary
        if isinstance(data, str):
            data = json.loads(data)

        # Write the data to a file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving JSON file: {e}")


# Function to read JSON from a file
def read_json_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=0,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def delete_files_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # Check if it's a file and not a directory
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")



def get_capabilities_from_sample_data_as_reference_by_level(level):
    file_path = 'data/RefCapMapTrans.xlsx'
    capability_mapping = get_capability_mapping()

    # Read the Excel file
    df = pd.read_excel(file_path,skiprows=1)

    # Replace values in the "Capability" column based on the provided capability_mapping
    df['Capability'] = df['Capability'].apply(lambda x: replace_substrings(x, capability_mapping))

    filtered_df = df[(df['Level'] == level)]

    return filtered_df["Capability"].values

def get_capabilities_from_sample_data_as_reference(tier, level):
    file_path = 'data/RefCapMapTrans.xlsx'

    # Read the Excel file
    df = pd.read_excel(file_path,skiprows=1)

    filtered_df = df[(df['Tier'] == tier) & (df['Level'] == level)]

    return filtered_df["Capability"].values


def convert_json_to_csv(json_data, csv_file_path):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=";")
        csv_writer.writerow(['Capability Name', 'Level', 'Tier', 'Description', 'Parent Capability'])

        def write_row(capability, level, tier, description, parent_name=None,):
            csv_writer.writerow([capability['name'], level, tier, description, parent_name])
            for sub_capability in capability.get('subCapabilities', []):
                write_row(sub_capability, str(int(level) + 1), tier, sub_capability['description'], capability['name'])

        for capability in json_data['capabilities']:
            write_row(capability, capability['level'], capability['tier'], capability['description'])



def get_capability_mapping():
    file_path = 'data/capabilitymapping.xlsx'

    # Read the Excel file
    df = pd.read_excel(file_path)

    capability_mapping = {row['Term']: row['Mapped term'] for _, row in df.iterrows()}

    return capability_mapping


def replace_substrings(s, mapping):
    for key, value in mapping.items():
        s = s.replace(key, value)
    return s



    
