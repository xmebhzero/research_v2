import pdfplumber

def extract_text_from_pdf(pdf_path):
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text += text
                    if page_number < len(pdf.pages) - 1:
                        full_text += "\n"
        return full_text.strip()
    except Exception as e:
        return f"Error processing PDF: {e}"

if __name__ == '__main__':
    pdf_file_path = './Transcript - P. Acceptance - IDI 2.docx.pdf'
    # pdf_file_path = './Result-transcribe-using-internal-tools.docx.pdf'

    extracted_content = extract_text_from_pdf(pdf_file_path)
    print(extracted_content)
