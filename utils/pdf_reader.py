from pdfminer.high_level import extract_text


# Function to extract text from uploaded PDF
def extract_pdf_text(uploaded_file):
    try:
        extracted_text = extract_text(uploaded_file)
        return extracted_text or ""

    except Exception as e:
        raise RuntimeError(
            f"Could not extract text from the PDF: {str(e)}"
        ) from e
