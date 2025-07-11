import re

def read_file_clean_transcript(filepath):
    """
    Reads a text file and removes timestamp and speaker labels from each line.
    Example line: [00:02:03] Person 2: Sekarang saya bekerja di bidang travel consultant, tourism, industri seperti itu.
    Returns only the transcript text.
    """
    cleaned_lines = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Remove [timestamp] Person X: at the start of the line
            cleaned = re.sub(r'^\[\d{2}:\d{2}:\d{2}\]\s+Person\s+\d+:\s+', '', line)
            cleaned_lines.append(cleaned)
    return ''.join(cleaned_lines)