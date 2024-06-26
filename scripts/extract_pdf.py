# Requires Python 3.6 or higher due to f-strings

# Import libraries
import platform
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

if platform.system() == "Windows":
	# We may need to do some additional downloading and setup...
	# Windows needs a PyTesseract Download
	# https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine

    pytesseract.pytesseract.tesseract_cmd = (
		r"C:/Program Files/Tesseract-OCR/tesseract.exe"
	)

	# Windows also needs poppler_exe
    path_to_poppler_exe = Path(r"C:/Users/amiti/anaconda3/pkgs/poppler-24.03.0-hc2f3c52_0/Library/bin")
	# Put our output files in a sane place...
    out_directory = Path(r"~/Desktop/BookRead/outputs").expanduser()
else:
    out_directory = Path("~").expanduser()
# Path of the Input pdf

# Store all the pages of the PDF in a variable
image_file_list = []

text_file = out_directory / Path("out_text.txt")

def main(pdf_path:str):
    ''' 
    Main execution point of the program
    '''
    pdf_file = Path(pdf_path)
    textContentDict = {}
    with TemporaryDirectory() as tempdir:
        if platform.system() == "Windows":
            pdf_pages = convert_from_path(
                pdf_file, 500, poppler_path=path_to_poppler_exe
            )
        else:
            pdf_pages = convert_from_path(pdf_file, 500)

        for page_enumeration, page in enumerate(pdf_pages, start=1):
            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            image_file_list.append(filename)

        with open(text_file, "a") as output_file:
            for page_num, image_file in enumerate(image_file_list):
                # Recognize the text as string in image using pytesserct
                text = str(((pytesseract.image_to_string(Image.open(image_file)))))
                text = text.replace("-\n", "")
                textContentDict[page_num] = text

                # Finally, write the processed text to the file.
                output_file.write(text)

    return textContentDict

# main("C:/Users/amiti/Desktop/BookRead/uploads/book1.pdf")
