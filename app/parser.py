import pdfplumber
from typing import List

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts clean text from a PDF file.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_multiple_pdfs(pdf_paths: List[str]) -> dict:
    """
    Extracts clean text from multiple PDF files.
    Return a dictionary (file_name: text).
    """
    result = {}
    for path in pdf_paths:
        result[path] = extract_text_from_pdf(path)
    return result
