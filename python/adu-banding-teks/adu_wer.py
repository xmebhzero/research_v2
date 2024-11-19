from adu_utils import MANUAL_NORMALIZE, MANUAL_DIARIZATIONS, DEEPGRAM_NORMALIZE, DEEPGAM_DIARIZATIONS, SPEECHMATICS_NORMALIZE, SPEECHMATICS_DIARIZATIONS, GCS_FILES
from adu_utils import normalizer, extract_text, read_file, write_text_to_file
from pathlib import Path
import jiwer

for loop in range(3):
    manual_text = read_file(MANUAL_NORMALIZE[loop])
    deepgram_text = read_file(DEEPGRAM_NORMALIZE[loop])
    speechmatics_text = read_file(SPEECHMATICS_NORMALIZE[loop])

    normalized_manual_text = normalizer(manual_text)
    normalized_deepgram_text = normalizer(deepgram_text)
    normalized_speechmatics_text = normalizer(speechmatics_text)

    print(f"*****************************************************************")
    print(f"File: {GCS_FILES[loop]}")
    print(f"*****************************************************************")
    
    print(f"### Manual vs Deepgram")
    jiwer_out_deepgram = jiwer.process_words(normalized_manual_text, normalized_deepgram_text)
    print(jiwer.visualize_alignment(jiwer_out_deepgram))
    print(f"WER: {jiwer.wer(normalized_manual_text, normalized_deepgram_text)}\n")
    
    print(f"### Manual vs Speechmatics")
    jiwer_out_speechmatics = jiwer.process_words(normalized_manual_text, normalized_speechmatics_text)
    print(jiwer.visualize_alignment(jiwer_out_speechmatics))
    print(f"WER: {jiwer.wer(normalized_manual_text, normalized_speechmatics_text)}\n\n")
    