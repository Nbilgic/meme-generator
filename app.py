"""Module to create or generate meme using user interface ob web."""
import random
import os

import requests
from flask import Flask, render_template, abort, request

from src.MemeEngine import MemeEngine
from src.QuoteEngine import Ingestor


app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    # Use os to find all image files in the images_path directory
    imgs = [os.path.join(images_path, f) for f in os.listdir(images_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)  # Select a random image
    quote = random.choice(quotes)  # Select a random quote
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    image_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']

    # Ensure the 'tmp' directory exists
    tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)

    # Create a temporary file path in the tmp directory
    temp_img_path = os.path.join(tmp_dir, 'temp_output.jpg')

    response = requests.get(image_url)
    if response.status_code == 200:
        # Write the content of the image to the temporary file
        with open(temp_img_path, 'wb') as file:
            file.write(response.content)

        # Use the meme object to generate a meme using the temporary saved image
        path = meme.make_meme(temp_img_path, body, author)

        # Remove the temporary saved image
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)

        return render_template('meme.html', path=path)
    else:
        abort(400, 'Failed to retrieve image')


if __name__ == "__main__":
    app.run(debug=True)
