# document_processing.py
import os
import PyPDF2
from docx import Document
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        images = convert_from_path(pdf_path)
        extracted_texts = [pytesseract.image_to_string(image) for image in images]
        return ' '.join(extracted_texts)

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





    
