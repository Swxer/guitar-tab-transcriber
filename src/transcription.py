import librosa
import statistics
from config import OPEN_STRINGS, MIN_AMPLITUDE

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