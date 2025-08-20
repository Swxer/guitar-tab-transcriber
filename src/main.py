from utils import (
    load_audio_file, 
    get_pitch, 
    get_detected_notes, 
    onset_detect, 
    note_to_tab,
    create_ascii_tabs
)
from basic_pitch.inference import (
    predict,
    Model,
    ICASSP_2022_MODEL_PATH
)
import librosa
import shlex

if __name__ == '__main__':
    
    # sr - sample rate
    # y - numpy array that represents amplitude of sound wave at each sample point
    # y, sr = load_audio_file()
    print('Converting...')
    # f0 - fundamental frequency, an array that contains estimated funamental pitch for each frame of the audio
    # voiced_flag is a boolean array that corresponds one-to-one with f0, 
    # indicates whether a fundamental frequency was detected
    # onsets_frame is an array that contains the time (in seconds) where a note begins
    # f0, voiced_flag = get_pitch(y,sr)
    # onsets_frame = onset_detect(y,sr)
    # detected_notes = get_detected_notes(y,sr,onsets_frame,f0,voiced_flag)


    file_path = input('Drag and drop your audio file here and press Enter: ').strip()

    # handles quotes and spaces
    cleaned_path = shlex.split(file_path)[1]

    basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)
    _,__,note_events = predict(cleaned_path,basic_pitch_model)
    detected_notes = []

    for note_event in note_events:
        start_time = note_event[0]
        end_time = note_event[1]
        duration = end_time - start_time
        midi_note = note_event[2]
        note_name = librosa.midi_to_note(midi_note)
        detected_notes.append((note_name,start_time,duration))

    print(detected_notes)
    # mapped_notes = note_to_tab(detected_notes)
    # create_ascii_tabs(mapped_notes)