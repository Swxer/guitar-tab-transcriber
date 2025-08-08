import numpy as np
import sounddevice as sd
from utils import (
    load_audio_file, 
    get_pitch, 
    get_detected_notes, 
    onset_detect, 
    note_to_tab
)
# import scipy
# import pydub

if __name__ == '__main__':
    
    # sr - sample rate
    # y - numpy array that represents amplitude of sound wave at each sample point
    y, sr = load_audio_file()

    # f0 - fundamental frequency, an array that contains estimated funamental pitch for each frame of the audio
    # voiced_flag is a boolean array that corresponds one-to-one with f0, 
    # indicates whether a fundamental frequency was detected
    # onsets_frame is an array that contains the time (in seconds) where a note begins
    f0, voiced_flag = get_pitch(y,sr)
    onsets_frame = onset_detect(y,sr)

    # print(f'Detected onsets (in seconds): {onsets_frame}')

    detected_notes = get_detected_notes(y,sr,onsets_frame,f0,voiced_flag)
    print(detected_notes)

    mapped_notes = note_to_tab(detected_notes)
    print(mapped_notes)
    
    # visualize(y, sr, f0, onsets)