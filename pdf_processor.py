from PyPDF2 import PdfReader
import re
import logging

logging.basicConfig(level=logging.INFO)

class PDFProcessor:
    def __init__(self, paths):
        self.paths = paths

    def extract_text_from_pdf(self):
        text = ""
        for path in self.paths:
            with open(path, 'rb') as file:
                reader = PdfReader(file)
                for page in range(len(reader.pages)):
                    text += reader.pages[page].extract_text()
        return text

    def preprocess_text(self, text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = text.lower()
        sentences = text.split('.')
        return sentences
