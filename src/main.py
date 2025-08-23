from utils import (
    note_to_tab,
    create_ascii_tabs,
    load_audio_file,
    get_octave_shift
)
from basic_pitch.inference import (
    predict,
    Model,
    ICASSP_2022_MODEL_PATH
)

def main():
    cleaned_path = load_audio_file()
    octave_shift = get_octave_shift()

    print('Converting...')
    basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)
    _,__,note_events = predict(cleaned_path, basic_pitch_model)

    mapped_notes = note_to_tab(note_events, octave_shift)
    create_ascii_tabs(mapped_notes)

if __name__ == '__main__':
    main()
