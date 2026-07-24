# Guitar settings
OPEN_STRINGS = ['E4','B3','G3','D3','A2','E2']
guitar_string_index = {note: i for i, note in enumerate(OPEN_STRINGS)}

# Note filtering
MIN_AMPLITUDE = 0.05
MIN_DURATION = 0.2
MIN_MIDI = 40
MAX_MIDI = 100
MAX_FRET = 24

# Tab display
MAX_COLUMNS = 80
COLUMN_WIDTH = 2
NOTE_VALUE = 0.125
STRING_HEADERS = ['e |', 'B |', 'G |', 'D |', 'A |', 'E |']

# Audio input
SUPPORTED_EXTENSIONS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']

MAX_FILE_SIZE = 10 * 1024 * 1024