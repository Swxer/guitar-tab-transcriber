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
    return librosa.onset.onset_detect(y=y, sr=sr, units='time')


if __name__ == '__main__':
    print('hello world')

    # sr - sample rate
    # y - numpy array that represents amplitude of sound wave at each sample point
    y, sr = load_audio_file('./data/A2.wav')

    # f0 - fundamental frequency, an array that contains estimated funamental pitch for each frame of the audio
    # voiced_flag is a boolean array that corresponds one-to-one with f0, 
    # indicates whether a fundamental frequency was detected
    # onsets_frame is an array that contains the time (in seconds) where a note begins
    f0, voiced_flag = get_pitch(y,sr)
    onsets_frame = onset_detect(y,sr)

    print(f'Detected pitch: {f0}')
    print(f'Detected onsets (in seconds): {onsets_frame}')


    # create a new array with only the pitches we are confident about 
    confident_f0 = f0[voiced_flag]

    # get the start tiem of the first note
    if len(onsets_frame) > 0:
        first_onset_time = onsets_frame[0]

        frames = librosa.time_to_frames(first_onset_time,sr=sr)

        # create a new array that only contains the pitch data from the onset onwards
        note_pitches = confident_f0[frames:]

        # calculate the final representative pitch for the note
        final_pitch = np.median(note_pitches)
        final_note = librosa.hz_to_note(final_pitch)
        print(f"Final detected pitch (median): {final_pitch} Hz")
        print(f'frames: {frames}')
        print(f'note_pitches: {note_pitches}')
        print(f'final note: {final_note}')


    
    # visualize(y, sr, f0, onsets)