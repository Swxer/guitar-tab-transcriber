import librosa
import shlex
import os

OPEN_STRINGS = ['E4','B3','G3','D3','A2','E2']
guitar_string_index = {note: i for i, note in enumerate(OPEN_STRINGS)}

def load_audio_file():

    SUPPORTED_EXTENSIONS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']

    while True:
        try:
            file_path = input('Drag and drop your audio file here and press Enter: ').strip()

            # handles quotes and spaces
            parts = shlex.split(file_path)
            if parts[0] == '&':
                cleaned_path = parts[1]
            else:
                cleaned_path = parts[0]
            final_path = os.path.normpath(cleaned_path) # make file path consistent across different operating systems
            file_extension = os.path.splitext(final_path)[1].lower()

            if file_extension not in SUPPORTED_EXTENSIONS:
                raise ValueError("Unsupported file format. Please use a supported audio format (e.g., .mp3, .wav).")
            
            if not os.path.isfile(final_path):
                raise FileNotFoundError("The file does not exist. Please check the path and try again.")

            return final_path
        except (ValueError, FileNotFoundError) as e:
            print(f"\nError: Could not load the file. Please ensure it is a valid audio format (e.g., .wav, .mp3).")
            print(f"Details: {e}\n")

def get_octave_shift():
    while True:
        try:
            shift_direction = input('Do you want to shift the melody higher or lower? (higher/lower/none): ').strip().lower()
            if shift_direction == 'none':
                return 0
            
            num_octaves_str = input(f'How many octaves do you want to shift {shift_direction}? ').strip()
            num_octaves = int(num_octaves_str)

            if num_octaves <= 0:
                print("\nPlease enter a positive number of octaves")
                continue

            if shift_direction == 'higher':
                return num_octaves * 12
            elif shift_direction == 'lower':
                return num_octaves * -12
            else:
                print("\nInvalid direction. Please type 'higher', 'lower', or 'none'.")

        except ValueError:
            print("\nInvalid input. Please enter a whole number.")

def note_to_tab(note_events, octave_shift):

    mapped_notes = []
    for note_event in reversed(note_events):

        start_time = note_event[0]
        end_time = note_event[1]
        current_note_midi = note_event[2] + octave_shift
        
        duration = end_time - start_time
        MIN_DURATION = 0.2
        if duration < MIN_DURATION:
            continue

        note_name = librosa.midi_to_note(current_note_midi)

        # contains all valid fingering options for the current note
        possible_fingerings = []

        # loop through each open string's midi value
        for string in OPEN_STRINGS:
            open_midi = librosa.note_to_midi(string)
            fret = current_note_midi - open_midi
            
            # check if this is a valid fret on the guitar
            if 0 <= fret <= 24: 
                possible_fingerings.append({
                    "note": note_name,
                    "string": string,
                    "fret": fret,
                    "start_time": start_time,
                    "duration": duration
                })

        if possible_fingerings:
            best_fingering = min(possible_fingerings,key=lambda x: x['fret'])
            mapped_notes.append(best_fingering)
 
                
    return mapped_notes

def create_ascii_tabs(mapped_notes):
    tab = [['e |'],['B |'],['G |'],['D |'],['A |'],['E |']]

    COLUMN_WIDTH = 4

    # loop through the mapped notes and build the tab
    for note in mapped_notes:
        column = ['-' * (COLUMN_WIDTH - 1)] * 6

        fret = str(note['fret'])
        string_name = note['string']

        padded_fret = fret.rjust(COLUMN_WIDTH - 1, '-')

        if string_name in guitar_string_index:
            string_index = guitar_string_index[string_name]
            column[string_index] = padded_fret

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

    print('Done!')