import io
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
from fastapi import UploadFile


# guess what this function does
# Extracts text from a PDF or DOCX file PFFFTTT
async def extract_text(file: UploadFile) -> str:
    contents = await file.read()

    if file.filename.lower().endswith(".pdf"):
        return extract_pdf_text(io.BytesIO(contents))
    elif file.filename.lower().endswith(".docx"):
        doc = Document(io.BytesIO(contents))
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return ""
