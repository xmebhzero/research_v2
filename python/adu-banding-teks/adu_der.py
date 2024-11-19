from typing import List
from adu_utils import MANUAL_NORMALIZE, MANUAL_DIARIZATIONS, DEEPGRAM_NORMALIZE, DEEPGAM_DIARIZATIONS, DEEPGRAM_RAW, SPEECHMATICS_NORMALIZE, SPEECHMATICS_DIARIZATIONS, GCS_FILES
from adu_utils import normalizer, extract_text, read_file, write_text_to_file
from pathlib import Path
import jiwer
import re
import json
from pyannote.core import Annotation, Segment
from pyannote.metrics.diarization import DiarizationErrorRate
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    Utterance
)
from math import inf,floor
from statistics import mean

def time_str_to_seconds(time_str: str) -> float:
    minutes, seconds = map(int, time_str.split(':'))
    return float(minutes * 60 + seconds)

def parse_diarization_file(file_path: str):
    content = Path(file_path).read_text()
    pattern = re.compile(r"Speaker (\d+):\n\[(.*?)\]\n(.*?)(?=\nSpeaker \d+:|\Z)", re.DOTALL)
    matches = pattern.findall(content)

    anno = Annotation()
    
    result = []
    for match in matches:
        speaker, time_str, text = match

        # start_time_str, end_time_str = time_str.split(', ')

        time_parts = time_str.split(', ')
        start_time_str = time_parts[0]
        end_time_str = time_parts[1]
        
        start_time_seconds = time_str_to_seconds(start_time_str)
        end_time_seconds = time_str_to_seconds(end_time_str)

        anno[Segment(start_time_seconds, end_time_seconds)] = f"Speaker {speaker}"

        result.append({
            "speaker": int(speaker),
            "time_str": time_str,
            "text": text.strip().replace("\n", " "),
            "start_time_seconds": start_time_seconds,
            "end_time_seconds": end_time_seconds,
        })
    
    return anno

def process_utterances(utts: List[Utterance]):
    data = {
            "speaker": inf,
            "start": [],
            "end": [],
            "transcript": [],
            "confidence": [],
        }

    transcriptions = []
    for idx, utterance in enumerate(utts):
        prev: Utterance = data if idx == 0 else utts[idx - 1]
        current: Utterance = utterance
        next: Utterance = None if idx == len(utts) - 1 else utts[idx + 1]

        if prev["speaker"] == current["speaker"]:
            data["speaker"] = current["speaker"]
            data["start"].append(current["start"])
            data["end"].append(current["end"])
            data["transcript"].append(current["transcript"])
            data["confidence"].append(current["confidence"])
        else:
            data["speaker"] = current["speaker"]
            data["start"] = [current["start"]]
            data["end"] = [current["end"]]
            data["transcript"] = [current["transcript"]]
            data["confidence"] = [current["confidence"]]
            
        if next is None or next["speaker"] != current["speaker"]:
            transcriptions.append(
                {
                    "speaker": data["speaker"],
                    "start": min(data["start"]),
                    "end": max(data["end"]),
                    "transcript": " ".join(data["transcript"]),
                    "confidence": mean(data["confidence"]),
                }
            )
                    
    return transcriptions

def extract_dia(utterances):
    return [(str(u["speaker"]), float(floor(u["start"])), float(floor(u["end"])))  for u in utterances]

def read_deepgram_diarization(file_path: str):
    file_content = read_file(file_path)
    json_content = json.loads(file_content)

    utterances = json_content.get("results", {}).get("utterances", None)

    if not utterances:
        raise Exception("No utterances found in the file")
    
    diarizations = extract_dia(process_utterances(utterances))
    anno = Annotation()

    for [speaker, time_start, time_end] in diarizations:
        anno[Segment(time_start, time_end)] = f"Speaker {speaker}"

    return anno
    

# reference = parse_diarization_file(MANUAL_DIARIZATIONS[0])
# hypothesis = parse_diarization_file(SPEECHMATICS_DIARIZATIONS[0])

# Initialize DER
metric = DiarizationErrorRate()

# Compute DER
# der = metric(reference, hypothesis)
# print(f"DER: {der:.2f}")

for loop in range(3):
    manual_annotation = parse_diarization_file(MANUAL_DIARIZATIONS[loop])
    deepgram_annotation = read_deepgram_diarization(DEEPGRAM_RAW[loop])
    speechmatics_annotation = parse_diarization_file(SPEECHMATICS_DIARIZATIONS[loop])

    print(f"*****************************************************************")
    print(f"File: {GCS_FILES[loop]}")
    print(f"*****************************************************************")

    print(f"### Manual vs Deepgram")
    der_speechmatics = metric(manual_annotation, deepgram_annotation)
    print(f"DER: {der_speechmatics}\n")

    print(f"### Manual vs Speechmatics")
    der_speechmatics = metric(manual_annotation, speechmatics_annotation)
    print(f"DER: {der_speechmatics}\n\n")