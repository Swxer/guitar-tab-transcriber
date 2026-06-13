import shlex
import os

SUPPORTED_EXTENSIONS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']

def parse_file_path(raw_input):
    parts = shlex.split(raw_input)
    if parts[0] == '&':
        return parts[1]
    return parts[0]

def validate_audio_file(file_path):
    final_path = os.path.normpath(file_path)
    file_extension = os.path.splitext(final_path)[1].lower()

    if file_extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file format. Please use a supported audio format (e.g., .mp3, .wav).")

    if not os.path.isfile(final_path):
        raise FileNotFoundError("The file does not exist. Please check the path and try again.")

    return final_path

def load_audio_file():
    while True:
        try:
            raw_input = input('Drag and drop your audio file here and press Enter: ').strip()
            file_path = parse_file_path(raw_input)
            validated_path = validate_audio_file(file_path)
            return validated_path
        except (ValueError, FileNotFoundError) as e:
            print(f"\nError: Could not load the file. Please ensure it is a valid audio format (e.g., .wav, .mp3).")
            print(f"Details: {e}\n")

def get_octave_shift():
    while True:
        try:
            shift_direction = input('Do you want to shift the melody higher or lower? (higher/lower/none): ').strip().lower()

            if shift_direction == 'none':
                return 0

            num_octaves = get_number_of_octaves(shift_direction)
            return calculate_semitone_shift(shift_direction, num_octaves)

        except ValueError:
            print("\nInvalid input. Please enter a whole number.")

def get_number_of_octaves(shift_direction):
    num_octaves_str = input(f'How many octaves do you want to shift {shift_direction}? ').strip()
    num_octaves = int(num_octaves_str)

    if num_octaves <= 0:
        raise ValueError("Octaves must be a positive number")

    return num_octaves

def calculate_semitone_shift(shift_direction, num_octaves):
    if shift_direction == 'higher':
        return num_octaves * 12
    elif shift_direction == 'lower':
        return num_octaves * -12
    else:
        raise ValueError("Invalid direction. Please type 'higher', 'lower', or 'none'.")
