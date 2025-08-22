import librosa
import numpy as np
import shlex
import os

OPEN_STRINGS = ['E4','B3','G3','D3','A2','E2']
guitar_string_index = {note: i for i, note in enumerate(OPEN_STRINGS)}

def load_audio_file():
    while True:
        try:
            file_path = input('Drag and drop your audio file here and press Enter: ').strip()

            # handles quotes and spaces
            # (file_path)[1] if you drop the file into the terminal and & is added in front of the absolute directory
            # (file_path)[0] <- otherwise do this
            cleaned_path = shlex.split(file_path)[1]

            return cleaned_path
        except Exception as e:
            print(f"\nError: Could not load the file. Please ensure it is a valid audio format (e.g., .wav, .mp3).")
            print(f"Details: {e}\n")

def note_to_tab(note_events):

    mapped_notes = []
    for note_event in reversed(note_events):

        start_time = note_event[0]
        end_time = note_event[1]
        current_note_midi = note_event[2]
        found_position = False
        
        duration = end_time - start_time
        MIN_DURATION = 0.2
        if duration < MIN_DURATION:
            continue
        note_name = librosa.midi_to_note(current_note_midi) 

        # loop through each open string's midi value
        for string in OPEN_STRINGS:
            open_midi = librosa.note_to_midi(string)
            fret = current_note_midi - open_midi
            
            # check if this is a valid fret on the guitar
            if 0 <= fret <= 24: 
                mapped_notes.append({
                    "note": note_name,
                    "string": string,
                    "fret": fret,
                    "start_time": start_time,
                    "duration": duration
                })
                found_position = True
                break # remove this when you want to look at other possible position 
                
    return mapped_notes

def create_ascii_tabs(mapped_notes):
    tab = [['e |'],['B |'],['G |'],['D |'],['A |'],['E |']]

    # loop through the mapped notes and build the tab
    for note in mapped_notes:
        column = ['--'] * 6

        if note['fret'] != 'Unknown' and note['string'] != 'Unknown':
            fret = str(note['fret'])
            string_name = note['string']

            if string_name in guitar_string_index:
                string_index = guitar_string_index[string_name]
                column[string_index] = f'{fret}-' if len(fret) < 2 else fret

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
            f.write('-'.join(string) + '\n')

    print('Done!')