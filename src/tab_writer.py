from config import guitar_string_index, MAX_COLUMNS

COLUMN_WIDTH = 2
NOTE_VALUE = 0.125
STRING_HEADERS = ['e |', 'B |', 'G |', 'D |', 'A |', 'E |']

def build_tab_grid(song_length):
    total_columns = round(song_length / NOTE_VALUE)
    return [['-' for _ in range(total_columns * COLUMN_WIDTH)] for _ in range(6)]

def place_notes_on_grid(tab, mapped_notes):
    for time_key in sorted(mapped_notes.keys()):
        chord_notes = mapped_notes[time_key]

        for note in chord_notes:
            place_single_note(tab, note)

def place_single_note(tab, note):
    fret = str(note['fret'])
    string_name = note['string']

    padded_fret = fret.rjust(COLUMN_WIDTH, '-')
    string_index = guitar_string_index[string_name]
    fret_position = round(note['start_time'] / NOTE_VALUE)
    start_position = fret_position * COLUMN_WIDTH

    for i, char in enumerate(padded_fret):
        tab[string_index][start_position] = char

def write_tab_chunks(tab, output_path):
    row_length = len(tab[0])

    with open(output_path, 'w') as output_file:
        for chunk_start in range(0, row_length, MAX_COLUMNS):
            chunk_end = min(chunk_start + MAX_COLUMNS, row_length)
            write_tab_block(output_file, tab, chunk_end, chunk_start)

def write_tab_block(output_file, tab, chunk_end, chunk_start):
    for string_index in range(6):
        row_chunk = ''.join(tab[string_index][chunk_start:chunk_end])
        output_file.write(STRING_HEADERS[string_index] + row_chunk + '|\n')
    output_file.write('\n')

def create_ascii_tabs(mapped_notes, song_length):
    tab = build_tab_grid(song_length)
    place_notes_on_grid(tab, mapped_notes)
    write_tab_chunks(tab, 'output.txt')

    print('Done!')
