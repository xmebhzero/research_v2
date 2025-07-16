from adu_utils import MANUAL_PATRONUS, ELEVENLABS_PATRONUS, DEEPGRAM_PATRONUS
from pathlib import Path
import re
from pyannote.core import Annotation, Segment
from pyannote.metrics.diarization import DiarizationErrorRate
from pyannote.core import Timeline

def time_str_to_seconds(time_str: str) -> float:
    minutes, seconds = map(int, time_str.split(':'))
    return float(minutes * 60 + seconds)

def parse_diarization_file(file_path: str):
    content = Path(file_path).read_text()
    lines = content.strip().split('\n')
    
    pattern = re.compile(r"\[(\d{2}:\d{2}:\d{2})\] (Person \d+): (.*)")
    
    anno = Annotation()
    
    last_speaker = None
    segment_start = 0.0
    
    for i, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
            
        time_str, speaker, text = match.groups()
        
        h, m, s = map(int, time_str.split(':'))
        current_time = float(h * 3600 + m * 60 + s)

        if last_speaker is not None and speaker != last_speaker:
            anno[Segment(segment_start, current_time)] = last_speaker
            segment_start = current_time
        
        if last_speaker is None:
            segment_start = current_time

        last_speaker = speaker

        if i == len(lines) - 1 and last_speaker is not None:
            anno[Segment(segment_start, current_time)] = last_speaker

    return anno

# Initialize DER
metric = DiarizationErrorRate()

for loop in range(3):
    print(f"*****************************************************************")
    print(f"File: {MANUAL_PATRONUS[loop]}")
    print(f"*****************************************************************")

    manual_annotation = parse_diarization_file(MANUAL_PATRONUS[loop])
    elevenlabs_annotation = parse_diarization_file(ELEVENLABS_PATRONUS[loop])
    deepgram_annotation = parse_diarization_file(DEEPGRAM_PATRONUS[loop])

    # Compute union of segments for UEM
    uem = Timeline(manual_annotation.get_timeline() | elevenlabs_annotation.get_timeline() | deepgram_annotation.get_timeline())

    print(f"### Manual vs Deepgram")
    der_deepgram = metric(manual_annotation, deepgram_annotation)
    print(f"DER: {der_deepgram}\n")

    print(f"### Manual vs ElevenLabs")
    der_elevenlabs = metric(manual_annotation, elevenlabs_annotation)
    print(f"DER: {der_elevenlabs}\n\n")