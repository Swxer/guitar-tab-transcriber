import librosa
import numpy as np
import sounddevice as sd
# import scipy
# import pydub

SAMPLE_RATE = 44100

def load_audio_file(filename):
    return librosa.load(filename)

def get_pitch(y,sr):
    
    fmin = librosa.note_to_hz('E2')
    fmax = librosa.note_to_hz('C7')
    
    f0, voiced_flag, voiced_prob = librosa.pyin(y,fmin=fmin,fmax=fmax, sr=sr)
    return f0


if __name__ == '__main__':
    print('hello world')
    y, sr = load_audio_file('./data/A2.wav')

    f0 = get_pitch(y,sr)
    print(f'Detected pitch: {f0}')