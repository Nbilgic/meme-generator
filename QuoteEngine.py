"""Module to handle quotes from different type of resources."""
import os
import subprocess
from abc import ABC, abstractmethod


class QuoteModel:
    """Model to store body and author of the meme."""

    def __init__(self, body, author):
        """Initialize body and author."""
        self.body = body
        self.author = author

    def __repr__(self):
        """Representation of model with body and author."""
        return f'{self.body} - {self.author}'


class IngestorInterface(ABC):
    """Abstract class to guide implementation of other ingestor classes."""

    allowed_extensions = ['txt', 'pdf', 'csv', 'docx']

    @abstractmethod
    def parse(self, path):
        """Abstract method to parse a file."""
        raise NotImplementedError("Subclasses should implement this method")

    @classmethod
    def can_ingest(cls, file_type):
        """Class method method to verify if the file type is compatible with the ingestor class."""
        return file_type in cls.allowed_extensions


class TxtIngestor(IngestorInterface):
    """Subclass to handle txt files."""

    @classmethod
    def parse(cls, path):
        """Read the content of the txt files."""
        quotes = []
        with open(path, 'r') as file:
            for line in file:
                body, author = line.strip().split('-')
                quotes.append(QuoteModel(body.strip(), author.strip()))
        return quotes


class DocxIngestor(IngestorInterface):
    """Subclass to handle docx files."""

    @classmethod
    def parse(cls, path):
        """Read the content of the docx files."""
        from docx import Document
        quotes = []
        doc = Document(path)
        for para in doc.paragraphs:
            if para.text.strip():
                body, author = para.text.strip().split('-')
                quotes.append(QuoteModel(body.strip(), author.strip()))
        return quotes


class PDFIngestor(IngestorInterface):
    """Subclass to handle pdf files."""

    @classmethod
    def parse(cls, path):
        """Read the content of the pdf files."""
        quotes = []

        # Ensure the 'tmp' directory exists
        tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)

        # Create a temporary file path in the tmp directory
        temp_text_path = os.path.join(tmp_dir, 'temp_output.txt')

        try:
            # Step 2: Use the XpdfReader pdftotext command to extract text from PDF
            # `pdftotext` from XpdfReader is installed and in the PATH
            subprocess.run(['pdftotext', path, temp_text_path], check=True)

            # Step 3: Read the text from the temporary file
            with open(temp_text_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Step 4: Parse each line and create QuoteModel instances
            for line in lines:
                parts = line.strip().split(' - ')
                if len(parts) == 2:
                    body, author = parts
                    quotes.append(QuoteModel(body, author))

        except subprocess.CalledProcessError as e:
            print(f"Error occurred while converting PDF to text using XpdfReader: {e}")
        except FileNotFoundError:
            print(
                "XpdfReader's pdftotext tool not found. Please ensure it's installed and available in the system PATH.")
        except Exception as e:
            print(f"Unexpected error: {e}")

        # Remove temp txt file
        if os.path.exists(temp_text_path):
            os.remove(temp_text_path)
        return quotes


class CsvIngestor(IngestorInterface):
    """Subclass for parsing csv files."""

    @classmethod
    def parse(cls, path):
        """Read the content of the csv files."""
        import csv
        quotes = []
        with open(path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                body, author = row
                quotes.append(QuoteModel(body.strip(), author.strip()))
        return quotes


class Ingestor(IngestorInterface):
    """Main ingestor class that selects the appropriate file parser."""

    ingestors = {
        "txt": TxtIngestor,
        "docx": DocxIngestor,
        "pdf": PDFIngestor,
        "csv": CsvIngestor,
    }

    @classmethod
    def parse(cls, path: str):
        """Select the appropriate ingestor based on file extension."""
        file_extension = path.split('.')[-1].lower()
        if not cls.can_ingest(file_extension):
            raise ValueError(f"Unsupported file type: {file_extension}")

        ingestor_class = cls.ingestors.get(file_extension)
        if ingestor_class:
            return ingestor_class.parse(path)
        else:
            raise ValueError(f"No ingestor found for file type: {file_extension}")
