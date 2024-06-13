import pytesseract
from PIL import Image

# Set the tesseract path in the script
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # replace with your own path

def convert(image_path):
    try:
        # Open an image file
        with Image.open(image_path) as img:
            print("Image opened successfully.")  # Debug print
            # Use Tesseract to do OCR on the image
            text = pytesseract.image_to_string(img)
            print("OCR completed.")  # Debug print
    except Exception as e:
        print(f"An error occurred: {e}")
        text = ""
    return text
# Usage example
#captcha_image_path = 'image.png'
#captcha = convert(captcha_image_path)
#print("Captcha text:", captcha)

