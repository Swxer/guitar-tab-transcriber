import librosa
import numpy as np
import sounddevice as sd
from utils import visualize
# import scipy
# import pydub

SAMPLE_RATE = 44100

guitar_notes = {
    'E2': 82.41,
    'A2': 110,
    'D3': 146.83,
    'G3': 196,
    'B3': 246.94,
    'E4': 329.63
}

expected_ranges = {
    'E2': (75, 90),
    'A2': (100, 120),
    'D3': (140, 160),
    'G3': (190, 210),
    'B3': (240, 260),
    'E4': (320, 340)
}


def load_audio_file(filename):
    return librosa.load(filename)

def get_pitch(y,sr):
    
    fmin = librosa.note_to_hz('E2')
    fmax = librosa.note_to_hz('C7')
    
    f0, voiced_flag, voiced_prob = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=sr)
    return f0, voiced_flag

def onset_detect(y,sr):
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    return onset_frames

if __name__ == '__main__':
    print('hello world')
    y, sr = load_audio_file('./data/A2.wav')
    f0, voiced_flag = get_pitch(y,sr)
    onsets = onset_detect(y,sr)

    print(f'Detected pitch: {f0}')
    print(f'Detected onsets (in seconds): {onsets}')


    # Create a new array with only the pitches we are confident about 
    confident_f0 = f0[voiced_flag]

    # get the start tiem of the first note
    if len(onsets) > 0:
        first_onset_time = onsets[0]

        frames = librosa.time_to_frames(first_onset_time,sr=sr)

        # create a new array that only contains the pitch data from the onset onwards
        note_pitches = confident_f0[frames:]

        # Calculate the final representative pitch for the note
        final_pitch = np.median(note_pitches)
        print(f"Final detected pitch (median): {final_pitch} Hz")
        print(f'frames: {frames}')
        print(f'note_pitches: {note_pitches}')


    
    # visualize(y, sr, f0, onsets)