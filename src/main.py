from utils import (
    load_audio_file, 
    get_pitch, 
    get_detected_notes, 
    onset_detect, 
    note_to_tab,
    create_ascii_tabs
)

if __name__ == '__main__':
    
    # sr - sample rate
    # y - numpy array that represents amplitude of sound wave at each sample point
    y, sr = load_audio_file()
    print('Converting...')
    # f0 - fundamental frequency, an array that contains estimated funamental pitch for each frame of the audio
    # voiced_flag is a boolean array that corresponds one-to-one with f0, 
    # indicates whether a fundamental frequency was detected
    # onsets_frame is an array that contains the time (in seconds) where a note begins
    f0, voiced_flag = get_pitch(y,sr)
    onsets_frame = onset_detect(y,sr)
    detected_notes = get_detected_notes(y,sr,onsets_frame,f0,voiced_flag)
    mapped_notes = note_to_tab(detected_notes)
    create_ascii_tabs(mapped_notes)