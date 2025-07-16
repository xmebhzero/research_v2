import os

from dotenv import load_dotenv
from google.cloud import storage
from datetime import timedelta
from typing import List
from pathlib import Path
import string
import re
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
)
from whisper_normalizer.basic import BasicTextNormalizer
import re

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")

GCS_FILES = [
    "gs://dev-resauto-transcriber/sample_data/sample-audio-1.wav",
    "gs://dev-resauto-transcriber/sample_data/sample-audio-2.wav",
    "gs://dev-resauto-transcriber/sample_data/sample-audio-3.wav"
]

REFERENCES = [
    "./references/sample_data_sample-audio-1_naked.txt",
    "./references/sample_data_sample-audio-2_naked.txt",
    "./references/sample_data_sample-audio-3_naked.txt"
]

SPEECHMATICS_NORMALIZE = [
    "./speechmatics/speechmatics-1-normalization.txt",
    "./speechmatics/speechmatics-2-normalization.txt",
    "./speechmatics/speechmatics-3-normalization.txt",
]

SPEECHMATICS_DIARIZATIONS = [
    "./speechmatics/speechmatics-diarization-1.txt",
    "./speechmatics/speechmatics-diarization-2.txt",
    "./speechmatics/speechmatics-diarization-3.txt"
]

DEEPGRAM_NORMALIZE = [
    "./deepgram/deepgram-1-normal.txt",
    "./deepgram/deepgram-2-normal.txt",
    "./deepgram/deepgram-3-normal.txt",
]

DEEPGAM_DIARIZATIONS = [
    "./deepgram/deepgram-1-diarization.txt",
    "./deepgram/deepgram-2-diarization.txt",
    "./deepgram/deepgram-3-diarization.txt",
]

DEEPGRAM_RAW = [
    "./deepgram/deepgram-1-raw.json",
    "./deepgram/deepgram-2-raw.json",
    "./deepgram/deepgram-3-raw.json",
]

MANUAL_NORMALIZE = [
    "./manual/manual-1-normal.txt",
    "./manual/manual-2-normal.txt",
    "./manual/manual-3-normal.txt",
]

MANUAL_DIARIZATIONS = [
    "./manual/manual-1-diarization.txt",
    "./manual/manual-2-diarization.txt",
    "./manual/manual-3-diarization.txt"
]

MANUAL_PATRONUS = [
    "./manual-patronus/idi-5.txt",
    "./manual-patronus/idi-2.txt",
    "./manual-patronus/dakar-fgd-2.txt"
]

ELEVENLABS_PATRONUS = [
    # "./elevenlabs/idi-5-diarization.txt",
    # "./elevenlabs/idi-2-diarization.txt",
    "patronus-no-punctuation/elevenlabs-idi-5.txt",
    "patronus-no-punctuation/elevenlabs-idi-2.txt",
    "patronus-no-punctuation/elevenlabs-dakar-fgd-2.txt",
]

DEEPGRAM_PATRONUS = [
    # "./deepgram/idi-5-diarization.txt",
    # "./deepgram/idi-2-diarization.txt",
    "patronus-no-punctuation/deepgram-idi-5.txt",
    "patronus-no-punctuation/deepgram-idi-2.txt",
    "patronus-no-punctuation/deepgram-dakar-fgd-2.txt",
]

normalizer = BasicTextNormalizer()

def extract_text(transcripts: List):
    texts = [t["transcript"] for t in transcripts]
    return str.join(" ", texts)

def normalize(text: str):
    rex = re.compile(r'\W+')
    return rex.sub(' ', text).translate(str.maketrans("", "", string.punctuation)).lower().replace("\n", "")

def pick_name_from_gcs_uri(gcs_uri: str):
    extract = gcs_uri.split(sep="/")[3:]
    return str.join("/", extract)

def get_cloud_storage_signed_uri(file_location: str) -> str:
    client = storage.Client()
    bucket = client.bucket("dev-resauto-transcriber")
    name = pick_name_from_gcs_uri(file_location)
    blob = bucket.blob(name)
    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=60),
        method="GET",
    )

def read_file(file_location: str):
    return Path(file_location).read_text()

def write_text_to_file(text: str, file_path: str):
    with open(file_path, 'w') as file:
        file.write(text)



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