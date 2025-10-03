import docx  # For DOCX files
import PyPDF2  # For PDF files
import re    #for regex

def extract_conversation(file_path):
    """
    Extracts the conversation from a file, supporting DOCX, PDF, and TXT formats.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: A string containing the extracted conversation, or None on error.
    """
    conversation_text = ""
    try:
        if file_path.lower().endswith(".docx"):
            document = docx.Document(file_path)
            for paragraph in document.paragraphs:
                if re.match(r'^[MR]\t', paragraph.text):
                    conversation_text += paragraph.text + "\n"

        elif file_path.lower().endswith(".pdf"):
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        for line in text.splitlines():
                            if re.match(r'^[MR]\t', line):
                                conversation_text += line + "\n"

        elif file_path.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    if re.match(r'^[MR]\t', line):
                        conversation_text += line + "\n"
        else:
            raise ValueError("Unsupported file format. Please use .docx, .pdf, or .txt.")
        return conversation_text

    except Exception as e:
        print(f"Error: An error occurred while extracting conversation from {file_path}: {e}")
        return None


def main():
    """
    Main function to execute the conversation extraction.
    """
    file_path_docx = "Transcript - P. Acceptance - IDI 2.docx"  #example
    file_path_pdf = "example.pdf" #change with your pdf file
    file_path_txt = "example.txt" #change with your txt file

    #example usage
    conversation_docx = extract_conversation(file_path_docx)
    conversation_pdf = extract_conversation(file_path_pdf)
    conversation_txt = extract_conversation(file_path_txt)

    if conversation_docx:
        print(f"Extracted Conversation from {file_path_docx}:\n")
        print(conversation_docx)
    if conversation_pdf:
        print(f"Extracted Conversation from {file_path_pdf}:\n")
        print(conversation_pdf)

    if conversation_txt:
        print(f"Extracted Conversation from {file_path_txt}:\n")
        print(conversation_txt)
    else:
        print("Failed to extract conversation.")



if __name__ == "__main__":
    main()
