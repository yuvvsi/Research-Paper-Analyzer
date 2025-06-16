import fitz  # PyMuPDF
import docx
import io

def extract_text_from_pdf(file):
    text = ""
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        text = f"Error extracting text from PDF: {str(e)}"
    return text

def extract_text_from_docx(file):
    text = ""
    try:
        doc = docx.Document(io.BytesIO(file.read()))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        text = f"Error extracting text from DOCX: {str(e)}"
    return text