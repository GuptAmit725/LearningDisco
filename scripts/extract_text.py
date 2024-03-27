import PyPDF2

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + '\n'  # Add a line break after each page's text
            return text
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    pdf_path = input("Enter the path to the PDF file: ")
    extracted_text = extract_text_from_pdf(pdf_path)
    if extracted_text:
        print(extracted_text)
    else:
        print("Failed to extract text from the PDF file.")
