"""OCR extraction from PNG/image files using pytesseract"""
from PIL import Image
import pytesseract


def extract_text_from_image(file) -> str:
    """Extract text from an uploaded image file using OCR."""
    image = Image.open(file)
    # Convert to RGB to ensure compatibility (e.g. RGBA PNGs)
    image = image.convert("RGB")
    text = pytesseract.image_to_string(image)
    return text.strip()
