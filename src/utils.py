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

    mapped_notes_by_time = {}
    song_length = 0
    for note_event in reversed(note_events):

        start_time = note_event[0]
        end_time = note_event[1]
        current_note_midi = note_event[2] + octave_shift
        duration = end_time - start_time

        MIN_DURATION = 0.2
        if duration < MIN_DURATION:
            continue

        song_length = max(song_length, start_time + duration)
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

            time_key = round(start_time, 2)

            if time_key not in mapped_notes_by_time:
                mapped_notes_by_time[time_key] = []

            best_fingering['duration'] = duration
            best_fingering['start_time'] = start_time


            mapped_notes_by_time[time_key].append(best_fingering)
 
    return  mapped_notes_by_time, song_length

def create_ascii_tabs(mapped_notes, song_length):
    column_width = 2
    note_value = 0.125
    total_columns = round(song_length / note_value)

    tab = [['-' for _ in range(total_columns * column_width)] for _ in range(6)]

    sorted_times = sorted(mapped_notes.keys())

    for time_key in sorted_times:
        chord_notes = mapped_notes[time_key]
        fret_position = round(time_key / note_value)


    
        # loop through the mapped notes and build the tab
        for note in chord_notes:
            fret = str(note['fret'])
            string_name = note['string']

            padded_fret = fret.rjust(column_width, '-')
            string_index = guitar_string_index[string_name]
            fret_position = round(note['start_time'] / note_value)

            start_pos = fret_position * column_width

            for i, char in enumerate(padded_fret):
                tab[string_index][start_pos] = char

        # tab[string_index][fret_position] = padded_fret

    header = ['e |','B |','G |','D |','A |','E |']
    final_tab = []

    for i in range(len(tab)):
        row = header[i] + ''.join(tab[i]) + '|'
        final_tab.append(row)

    # output txt file 
    with open('output.txt','w') as f:
        for string in final_tab:
            f.write(''.join(string) + '\n')

    print('Done!')