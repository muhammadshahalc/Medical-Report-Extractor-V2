
#extractor.py
from groq import Groq
import base64
import pdfplumber
from io import BytesIO
import json
import streamlit as st
from PIL import Image, ImageDraw, ImageFont


class MedicalPDFExtractor:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def pdf_to_images(self, pdf_path):
        """Convert each PDF page to a PIL image using pdfplumber (no poppler needed)."""
        pages = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    # Render page as image (bitmap)
                    pil_image = page.to_image(resolution=200).original
                    pages.append(pil_image)
        except Exception as e:
            st.error(f"PDF conversion error: {e}")
        return pages

    def encode_image(self, image):
        """Encode a PIL image to base64 string."""
        try:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
            if len(encoded) > 20 * 1024 * 1024:  # 20MB limit
                st.error("Page image too large (>20MB). Try lower DPI.")
                return None
            return encoded
        except Exception as e:
            st.error(f"Image encoding error: {e}")
            return None

    def extract_medical_data(self, base64_image):
        """Send image to Groq Vision model and return structured JSON."""
        try:
            response = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "You are an expert medical data extractor. "
                                    "Extract strictly in JSON with this schema:\n"
                                    "{\n"
                                    '  \"patient\": { \"name\": \"\", \"age\": \"\", \"gender\": \"\", \"date_of_report\": \"\" },\n'
                                    '  \"tests\": [ { \"test_name\": \"\", \"value\": \"\", \"unit\": \"\" } ],\n'
                                    '  \"diagnosis\": \"\"\n'
                                    "}"
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    }
                ],
                max_tokens=2048,
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"Groq API error: {e}")
            return None
