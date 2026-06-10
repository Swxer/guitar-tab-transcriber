
import statistics
from config import guitar_string_index, MAX_COLUMNS

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