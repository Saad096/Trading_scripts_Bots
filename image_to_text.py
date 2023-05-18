import pytesseract
from PIL import Image

# Open the image file
image = Image.open('image.jpg')

# Use pytesseract to convert the image to text
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
