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
import jiwer

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")

SAMPLE_FILES = [
    "gs://dev-resauto-transcriber/sample_data/sample-audio-1.wav",
    "gs://dev-resauto-transcriber/sample_data/sample-audio-2.wav",
    "gs://dev-resauto-transcriber/sample_data/sample-audio-3.wav"
]

REFERENCES = [
    "./references/sample_data_sample-audio-1_naked.txt",
    "./references/sample_data_sample-audio-2_naked.txt",
    "./references/sample_data_sample-audio-3_naked.txt"
]

REFERENCES_SPEECHMATICS_NORMALIZE = [
    "./speechmatics/speechmatics-1-normalization.txt",
    "./speechmatics/speechmatics-2-normalization.txt",
    "./speechmatics/speechmatics-3-normalization.txt",
]

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

def transcript_deepgram(gcs_uri: str):
    try:
        deepgram: DeepgramClient = DeepgramClient()
        options: PrerecordedOptions = PrerecordedOptions(
            model="nova-2",
            language="id",
            smart_format=True,
            diarize=True,
            paragraphs=True,
        )
        response = deepgram.listen.rest.v("1").transcribe_url({ "url" : gcs_uri }, options)
        transcript = [ { "transcript": t.alternatives[0].transcript, 
                        "confidence": t.alternatives[0].confidence ,
                        "words": t.alternatives[0].words } for t in response.results.channels ]
        
        return { "raw" : response, "result": transcript }

    except Exception as e:
        print(f"Exception: {e}")

def extract_text(transcripts: List):
    texts = [t["transcript"] for t in transcripts]
    return str.join(" ", texts)

def normalize(text: str):
    rex = re.compile(r'\W+')
    return rex.sub(' ', text).translate(str.maketrans("", "", string.punctuation)).lower().replace("\n", "")

target_file_index = 2

print(f"=== DEEPGRAM {SAMPLE_FILES[target_file_index]} ===")
reference = Path(REFERENCES[target_file_index]).read_text()
signed_uri = get_cloud_storage_signed_uri(SAMPLE_FILES[target_file_index])
output = transcript_deepgram(signed_uri)

extracted_text = extract_text(output["result"])
# print(extracted_text)

normalized_text = normalize(extracted_text)
print("=== Normalized Deepgram START ===")
print(normalized_text)
print(f"=== Normalized Deepgram END ===\n\n")

normalized_reference = normalize(reference)
print("=== Normalized Reference START ===")
print(normalized_reference)
print(f"=== Normalized Reference END ===\n\n")

jiwer_out = jiwer.process_words(normalized_reference, normalized_text)
print(jiwer.visualize_alignment(jiwer_out))
print(f"wer={jiwer.wer(normalized_reference, normalized_text)}")

speechmatics_reference = Path(REFERENCES_SPEECHMATICS[2]).read_text()
norm1 = normalize(reference)
norm2 = normalize(speechmatics_reference)
jiwer_out = jiwer.process_words(norm1, norm2)
print(jiwer.visualize_alignment(jiwer_out))
print(f"wer={jiwer.wer(norm1, norm2)}")