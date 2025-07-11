from pathlib import Path
import jiwer
from adu_utils import MANUAL_PATRONUS, ELEVENLABS_PATRONUS, DEEPGRAM_PATRONUS
from adu_utils import read_file_clean_transcript, normalizer

for loop in range(2):
    print(f"*****************************************************************")
    print(f"File: {loop+1}")
    print(f"*****************************************************************")
    
    manual_text = read_file_clean_transcript(MANUAL_PATRONUS[loop])
    deepgram_text = read_file_clean_transcript(DEEPGRAM_PATRONUS[loop])
    elevenlabs_text = read_file_clean_transcript(ELEVENLABS_PATRONUS[loop])

    # print(f"Manual Text: {manual_text}")

    normalized_manual_text = normalizer(manual_text)
    normalized_deepgram_text = normalizer(deepgram_text)
    normalized_elevenlabs_text = normalizer(elevenlabs_text)

    print(f"### Manual vs Deepgram")
    jiwer_out_deepgram = jiwer.process_words(normalized_manual_text, normalized_deepgram_text)
    # print(jiwer.visualize_alignment(jiwer_out_deepgram))
    print(f"WER: {jiwer.wer(normalized_manual_text, normalized_deepgram_text)}\n")
    
    print(f"### Manual vs ElevenLabs")
    jiwer_out_elevenlabs = jiwer.process_words(normalized_manual_text, normalized_elevenlabs_text)
    print(jiwer.visualize_alignment(jiwer_out_elevenlabs))
    print(f"WER: {jiwer.wer(normalized_manual_text, normalized_elevenlabs_text)}\n\n")