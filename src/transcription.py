import librosa
import statistics
from config import (
    OPEN_STRINGS,
    MIN_AMPLITUDE,
    MIN_DURATION,
    MIN_MIDI,
    MAX_MIDI,
    MAX_FRET
)

def is_valid_note(note_event, octave_shift):
    if len(note_event) >= 4 and note_event[3] < MIN_AMPLITUDE:
        return False, None, None, None

    start_time = note_event[0]
    end_time = note_event[1]
    current_note_midi = note_event[2] + octave_shift
    duration = end_time - start_time

    if duration < MIN_DURATION:
        return False, None, None, None

    if current_note_midi < MIN_MIDI or current_note_midi > MAX_MIDI:
        return False, None, None, None

    return True, current_note_midi, start_time, duration

def get_possible_fingerings(midi_note, start_time, duration):
    note_name = librosa.midi_to_note(midi_note)
    possible_fingerings = []

    for string_name in OPEN_STRINGS:
        open_midi = librosa.note_to_midi(string_name)
        fret = midi_note - open_midi

        if 0 <= fret <= MAX_FRET:
            possible_fingerings.append({
                "note": note_name,
                "string": string_name,
                "fret": fret,
                "start_time": start_time,
                "duration": duration
            })

    return possible_fingerings

def select_best_fingering(fingerings, median_fret):
    return min(fingerings, key=lambda x: abs(x['fret'] - median_fret))

def calculate_median_fret(all_notes):
    all_frets = [fingering['fret'] for note in all_notes for fingering in note]
    return statistics.median(all_frets)

def collect_valid_notes(note_events, octave_shift):
    all_notes = []

    for note_event in note_events:
        is_valid, midi_note, start_time, duration = is_valid_note(note_event, octave_shift)

        if not is_valid:
            continue

        fingerings = get_possible_fingerings(midi_note, start_time, duration)

        if fingerings:
            all_notes.append(fingerings)

    return all_notes

def build_mapped_notes(all_notes, median_fret):
    mapped_notes_by_time = {}
    song_length = 0

    for possible_fingerings in all_notes:
        best_fingering = select_best_fingering(possible_fingerings, median_fret)

        start_time = best_fingering['start_time']
        duration = best_fingering['duration']
        song_length = max(song_length, start_time + duration)

        time_key = round(start_time, 2)

        if time_key not in mapped_notes_by_time:
            mapped_notes_by_time[time_key] = []

        mapped_notes_by_time[time_key].append(best_fingering)

    return mapped_notes_by_time, song_length

def note_to_tab(note_events, octave_shift):
    all_notes = collect_valid_notes(note_events, octave_shift)

    if not all_notes:
        return {}, 0

    median_fret = calculate_median_fret(all_notes)
    mapped_notes, song_length = build_mapped_notes(all_notes, median_fret)

    return mapped_notes, song_length
