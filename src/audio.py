import shlex
import os

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