import librosa
import numpy as np
import matplotlib.pyplot as plt
import shlex
import os

guitar_string_midi = {
    'E4': librosa.note_to_midi('E4'),
    'B3': librosa.note_to_midi('B3'),
    'G3': librosa.note_to_midi('G3'),
    'D3': librosa.note_to_midi('D3'),
    'A2': librosa.note_to_midi('A2'),
    'E2': librosa.note_to_midi('E2'),
}

guitar_string_number = {
    'E4': 0,
    'B3': 1,
    'G3': 2,
    'D3': 3,
    'A2': 4,
    'E2': 6,
}

SAMPLE_RATE = 44100

def load_audio_file():
    while True:
        try:
            file_path = input('Drag and drop your audio file here and press Enter: ').strip()

            # handles quotes and spaces
            # revert the index to 0 when project is done
            cleaned_path = shlex.split(file_path)[1]

            return librosa.load(os.path.normpath(cleaned_path))
        except Exception as e:
            print(f"\nError: Could not load the file. Please ensure it is a valid audio format (e.g., .wav, .mp3).")
            print(f"Details: {e}\n")

def get_pitch(y,sr):
    
    # lowest note range for EADGBe tuning
    fmin = librosa.note_to_hz('E2')
    fmax = librosa.note_to_hz('C7')
    
    f0, voiced_flag, voiced_prob = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=sr)
    return f0, voiced_flag

def onset_detect(y,sr):
    return librosa.onset.onset_detect(y=y, sr=sr, units='time')

def get_detected_notes(y,sr,onsets_frame, f0, voiced_flag):
    detected_notes = []
    if len(onsets_frame) > 0:

        # get the starting frame of each note
        for i in range(len(onsets_frame)):

            # get the frame where the note starts
            onset_time = onsets_frame[i]

            # the start time of the note
            start_frame = librosa.time_to_frames(onset_time,sr=sr)

            # the end time of the note
            if i < len(onsets_frame) - 1:
                end_time = onsets_frame[i+1]
            else:
                end_time = librosa.get_duration(y=y,sr=sr)
            end_frame = librosa.time_to_frames(end_time,sr=sr)

            f0_segment = f0[start_frame:end_frame]
            voiced_flag_segment = voiced_flag[start_frame:end_frame]

            # create a new array with only the pitches we are confident about 
            confident_f0 = f0_segment[voiced_flag_segment]

            if len(confident_f0) > 0:
                # calculate the final representative pitch for the note
                final_pitch = np.median(confident_f0)
                # print(f'note_pitches: {final_pitch}')
                final_note = librosa.hz_to_note(final_pitch)
                # print(f"Final detected pitch (median): {final_pitch} Hz")
                # print(f'frames: {frames}')
                
                # print(f'final note: {final_note}')
                detected_notes.append(final_note)
            else:
                detected_notes.append('Rest')
            

    return detected_notes

def note_to_tab(detected_notes):

    mapped_notes = []

    for note in detected_notes:
        current_note_midi = librosa.note_to_midi(note)
        found_position = False

        # loop through each open string's midi value
        for string_name, open_midi in guitar_string_midi.items():
            fret = current_note_midi - open_midi
            
            # check if this is a valid fret on the guitar
            if 0 <= fret <= 24: 
                mapped_notes.append({
                    "note": note,
                    "string": string_name,
                    "fret": fret
                })
                found_position = True
                break # remove this when you want to look at other possible position 

        if not found_position:
            mapped_notes.append({
                "note": note,
                "string": "Unknown",
                "fret": "Unknown"
            })
                
    return mapped_notes

def create_ascii_tabs(mapped_notes):
    tab = [['e |'],['B |'],['G |'],['D |'],['A |'],['E |']]

    # loop through the mapped notes and build the tab
    for note in mapped_notes:
        column = ['-'] * 6

        fret = str(note['fret'])
        string_name = note['string']

        if string_name in guitar_string_number:
            string_index = guitar_string_number[string_name]
            column[string_index] = fret

        # append the entire column to the tab
        for i in range(len(tab)):
            tab[i].append(column[i])

    # indicate the end of the tab
    end = ['|'] * 6
    for i in range(len(tab)):
        tab[i].append(end[i])

    # output txt file 
    with open('output.txt','w') as f:
        for string in tab:
            f.write(''.join(string) + '\n')