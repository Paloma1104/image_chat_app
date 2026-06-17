import os

import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_image_caption(image_path):

    image = Image.open(image_path)

    response = model.generate_content(
        [
            "Describe this image in detail.",
            image
        ]
    )

    return response.text