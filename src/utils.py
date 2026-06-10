import librosa
import statistics
from config import OPEN_STRINGS, guitar_string_index, MIN_AMPLITUDE, MAX_COLUMNS

def note_to_tab(note_events, octave_shift):

    MIN_DURATION = 0.2
    all_notes = []

    for note_event in note_events:

        if len(note_event) >= 4 and note_event[3] < MIN_AMPLITUDE:
            continue

        start_time = note_event[0]
        end_time = note_event[1]
        current_note_midi = note_event[2] + octave_shift
        duration = end_time - start_time

        if duration < MIN_DURATION:
            continue

        if current_note_midi < 40 or current_note_midi > 100:
            continue

        note_name = librosa.midi_to_note(current_note_midi)

        possible_fingerings = []

        for string in OPEN_STRINGS:
            open_midi = librosa.note_to_midi(string)
            fret = current_note_midi - open_midi
            
            if 0 <= fret <= 24: 
                possible_fingerings.append({
                    "note": note_name,
                    "string": string,
                    "fret": fret,
                    "start_time": start_time,
                    "duration": duration
                })

        if possible_fingerings:
            all_notes.append(possible_fingerings)

    if not all_notes:
        return {}, 0

    all_frets = [f['fret'] for note in all_notes for f in note]
    median_fret = statistics.median(all_frets)

    mapped_notes_by_time = {}
    song_length = 0

    for possible_fingerings in all_notes:
        best_fingering = min(possible_fingerings, key=lambda x: abs(x['fret'] - median_fret))

        start_time = best_fingering['start_time']
        duration = best_fingering['duration']
        song_length = max(song_length, start_time + duration)

        time_key = round(start_time, 2)

        if time_key not in mapped_notes_by_time:
            mapped_notes_by_time[time_key] = []

        mapped_notes_by_time[time_key].append(best_fingering)
  
    return mapped_notes_by_time, song_length

def create_ascii_tabs(mapped_notes, song_length):
    column_width = 2
    note_value = 0.125
    total_columns = round(song_length / note_value)

    tab = [['-' for _ in range(total_columns * column_width)] for _ in range(6)]

    sorted_times = sorted(mapped_notes.keys())

    for time_key in sorted_times:
        chord_notes = mapped_notes[time_key]

        for note in chord_notes:
            fret = str(note['fret'])
            string_name = note['string']

            padded_fret = fret.rjust(column_width, '-')
            string_index = guitar_string_index[string_name]
            fret_position = round(note['start_time'] / note_value)

            start_pos = fret_position * column_width

            for i, char in enumerate(padded_fret):
                tab[string_index][start_pos] = char

    header = ['e |','B |','G |','D |','A |','E |']
    row_length = len(tab[0])

    with open('output.txt','w') as f:
        for chunk_start in range(0, row_length, MAX_COLUMNS):
            chunk_end = min(chunk_start + MAX_COLUMNS, row_length)
            for i in range(6):
                row_chunk = ''.join(tab[i][chunk_start:chunk_end])
                f.write(header[i] + row_chunk + '|\n')
            f.write('\n')

    print('Done!')