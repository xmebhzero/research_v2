import soundfile as sf
import noisereduce as nr
from pydub import AudioSegment
import io
import numpy as np
import os

file_path = "interview_indo.mp3"

# Reduce the noise
# rate, data = sf.read('interview_indo.mp3')
# reduced_noise_data = nr.reduce_noise(y=data, sr=rate)

# Save the reduced noise audio
# sf.write('interview_indo_reduced_noise.mp3', reduced_noise_data, rate)

# Send to deepgram

# Save the result


# Reduce the noise using noisereducee
def reduce_noise(input_filepath):
    output_dir = ""
    filename, extension = os.path.splitext(input_filepath)

    audio = AudioSegment.from_file(input_filepath)

    # Standardize for speech recognition:
    # - 16000 Hz sample rate
    # - Mono (single channel)
    audio = audio.set_frame_rate(16000).set_channels(1)

    wav_buffer = io.BytesIO()
    audio.export(wav_buffer, format="wav")
    wav_buffer.seek(0)

    data, rate = sf.read(wav_buffer)

    # if data.ndim > 1:
    #     data = np.mean(data, axis=1)

    if data.size > 0:
        reduced_noise_data = nr.reduce_noise(y=data, sr=rate)
    else:
        reduced_noise_data = data

    base_filename = os.path.basename(filename)
    output_filepath = os.path.join(output_dir, f"cleaned_{base_filename}.wav")

    sf.write(output_filepath, reduced_noise_data, rate)

    return output_filepath


reduced_noise_file = reduce_noise(file_path)
print(f"Reduced noise audio saved to: {reduced_noise_file}")