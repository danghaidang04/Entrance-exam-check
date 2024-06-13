import pytesseract
from PIL import Image

# Set the tesseract path in the script
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # replace with your own path

def convert(image_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
    return text

# Example usage
captcha_image_path = 'captcha.png'
captcha = convert(captcha_image_path)
print(captcha)