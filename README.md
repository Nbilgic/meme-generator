# Meme Generator Project

## Overview
The Meme Generator module is a Flask-based web application that allows users to generate memes by overlaying quotes onto images.
This project can create random memes by randomly selecting images and quotes under _data folder or can create user-defined memes using images and quotes passed as parameters by users.

## Project Structure
- `MemeEngine`: A class responsible for overlaying text on images and saving the generated meme.
- `QuoteEngine`: Handles the ingestion of quotes from different file formats (TXT, PDF, CSV, DOCX).
- `app.py`: The main Flask application that provides a web interface for generating memes.
  - `/` Route: Generates a random meme from available images and quotes.
  - `/create` (GET): Displays a form for user input.
  - `/create` (POST): Accepts user input and generates a custom meme.
- `meme.py`: Module to create memes using command line interface.

## Dependencies
- `Flask`: For running the web application.
- `requests`: For downloading images from user-provided URLs.
- `Pillow`: For image processing.
- `python-docx`: For processing DOCX files.
- `XpdfReader`: Required for PDF parsing (ensure `pdftotext` is installed).

## Usage
### Running the Application
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the application:
   ```sh
   python app.py
   ```
3. Open `http://127.0.0.1:5000/` in a web browser.

### Generating a Meme
- Visit the homepage to generate a random meme.
- Use the `/create` page to upload an image URL and input a custom quote.


# Quote Engine Module

## Overview
This module is designed to handle quotes from different types of resources such as TXT, PDF, CSV, and DOCX files. It provides an abstract interface for parsing files and extracting quote data, which includes the quote body and the author's name.

## Project Structure
- `QuoteModel`: A class representing a single quote, consisting of a body and an author.
- `IngestorInterface`: An abstract base class defining a contract for all ingestor classes.
- `TxtIngestor`: A class for parsing TXT files and extracting quotes.
- `DocxIngestor`: A class for parsing DOCX files and extracting quotes.
- `PDFIngestor`: A class for parsing PDF files using XpdfReader's `pdftotext` tool and extracting quotes.
- `CsvIngestor`: A class for parsing CSV files and extracting quotes.
- `Ingestor`: A class that determines the correct ingestor to use based on file type.

## Dependencies
- `python-docx`: Required for processing DOCX files.
- `XpdfReader`: Required for processing PDF files. Ensure `pdftotext` is installed and available in the system PATH.

## Installation
1. Install required dependencies:
   ```sh
   pip install python-docx
   ```
2. Install `pdftotext` from XpdfReader PDF parsing.

Download the Xpdf command line tools: which will contain several command line utilities as listed here and `pdftotext` will be one of them.

Note - Make sure bin64 directory of XpdfReader is added to your PATH.

After installing `XpdfReader`, test whether `pdftotext` is working as expected or not form your Terminal or Command Prompt by running below command -

pdftotext <sample_input_file.pdf> <destination_file.txt>



**HOW TO RUN THE PROGRAM FOR CLI EXECUTION**

python meme.py --body "Life is what happens" --author "John Lennon" --path "tmpn8fpzqap.jpg"


**HOW TO RUN THE PROGRAM ON WEB INTERFACE**

Run app.py. Open the link displayed in terminal. Create either a random meme or give an image url, body and author as a parameter to create a new meme.

