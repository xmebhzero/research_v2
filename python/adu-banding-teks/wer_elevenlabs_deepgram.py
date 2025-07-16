from pathlib import Path
import jiwer
from adu_utils import MANUAL_PATRONUS, ELEVENLABS_PATRONUS, DEEPGRAM_PATRONUS
from adu_utils import read_file_clean_transcript, normalizer

word_mapping = {
    "konfidensial": "confidential",
    "consultant": "konsultan",
    "behaviour": "behavior",
    "41": "empat puluh satu",
    "15": "lima belas",
    "10": "sepuluh",
    "500": "lima ratus",
    "100%": "seratus persen",
    "33": "tiga puluh tiga",
    "9 to 5": "nine to five",
    "1": "one",
    "5": "lima",
    "nggak": "enggak",
    "ga": "enggak",
    "ya": "iya",
    "kemaren": "kemarin",
    "dimana": "di mana",
    "lu": "lo",
    "kaya": "kayak",
    "make up": "makeup",
    "tau": "tahu",
    "ngefollow": "nge follow",
    "temen": "teman",
    "aja": "saja",
    "rilis": "release",
    "ngedesain": "mendesain",
    "klien": "client",
    "stres": "stress",
    "venuenya": "venue nya",
    "apalagi": "apa lagi",
    "mba": "mbak",
}

transformation = jiwer.Compose([
    jiwer.SubstituteWords(word_mapping),
    jiwer.ReduceToListOfListOfWords(word_delimiter=" "),
])

for loop in range(3):
    print(f"*****************************************************************")
    print(f"File: {MANUAL_PATRONUS[loop]}")
    print(f"*****************************************************************")
    
    manual_text = read_file_clean_transcript(MANUAL_PATRONUS[loop])
    deepgram_text = read_file_clean_transcript(DEEPGRAM_PATRONUS[loop])
    elevenlabs_text = read_file_clean_transcript(ELEVENLABS_PATRONUS[loop])

    # print(f"Manual Text: {manual_text}")

    normalized_manual_text = normalizer(manual_text)
    normalized_deepgram_text = normalizer(deepgram_text)
    normalized_elevenlabs_text = normalizer(elevenlabs_text)

    # print(f"### Manual vs Deepgram")
    # jiwer_out_deepgram = jiwer.process_words(reference=normalized_manual_text, hypothesis=normalized_deepgram_text, reference_transform=transformation, hypothesis_transform=transformation)
    # print(jiwer.visualize_alignment(jiwer_out_deepgram))
    # print(f"WER: {jiwer.wer(normalized_manual_text, normalized_deepgram_text)}\n")
    
    print(f"### Manual vs ElevenLabs")
    jiwer_out_elevenlabs = jiwer.process_words(reference=normalized_manual_text, hypothesis=normalized_elevenlabs_text, reference_transform=transformation, hypothesis_transform=transformation)
    print(jiwer.visualize_alignment(jiwer_out_elevenlabs))
    # print(f"WER: {jiwer.wer(reference=normalized_manual_text, hypothesis=normalized_elevenlabs_text, reference_transform=transformation, hypothesis_transform=transformation)}\n\n")