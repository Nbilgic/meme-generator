"""Module to make meme using given parameters."""
import os
import random

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Class to create image-related methods."""

    def __init__(self, output_dir: str):
        """Create path to save meme if not exist."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """Create meme from image and quote."""
        # Open the image
        img = Image.open(img_path)

        # Resize the image to the required width while maintaining the aspect ratio
        img = self.resize_image(img, width)

        # Add the quote text (body + author) to the image
        img = self.add_caption(img, text, author)

        # Save the generated meme
        output_path = os.path.join(self.output_dir, f'{random.randint(0, 10000)}.png')
        img.save(output_path)
        return output_path

    @staticmethod
    def resize_image(img: Image, width: int) -> Image:
        """Resize the image while maintaining aspect ratio."""
        aspect_ratio = img.height / img.width
        new_height = int(width * aspect_ratio)
        img = img.resize((width, new_height))
        return img

    @staticmethod
    def add_caption(img: Image, text: str, author: str) -> Image:
        """Add the text and author as a caption on the image."""
        # Combine the text and author into one string
        full_text = f'"{text}"\n  - {author}'

        print(full_text)
        # Create a drawing context
        draw = ImageDraw.Draw(img)

        # Choose a font and size
        try:
            font = ImageFont.truetype("arial.ttf", size=30)  # Replace with a font path if necessary
        except IOError:
            font = ImageFont.load_default()

        # Calculate text size and position to place it in a random location
        bbox = draw.textbbox((0, 0), full_text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        img_width, img_height = img.size

        # Randomize the position for the caption
        x = random.randint(1, img_width - text_width - 10)
        y = random.randint(1, img_height - text_height - 10)

        # Add the text to the image at the random position
        draw.text((x, y), full_text, font=font, fill="white")

        return img
