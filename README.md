# Guitar Tab Transcriber

## Project Goal
The goal of this project is to create a Python script that can automatically transcribe notes from a monophonic audio file into guitar tablature.

## Status: Work in Progress
This project is currently under active development. The core logic for transcribing simple, single-note melodies into guitar tablature has been successfully implemented. I am now working on improving the accuracy of note detection for fast melodies and incorporating note duration to create more complete and realistic tabs.

## Current Features
* **Audio Loading**: The script can load and process standard audio files (`.wav`, `.mp3`) using the librosa library.
* **Monophonic Note Transcription**: The script successfully transcribes simple monophonic melodies (one note at a time) from an audio file into a sequence of notes.
* **Pitch and Onset Detection**: It uses a combination of librosa's pitch and onset detection algorithms to identify individual notes and their starting points.
* **Frequency-to-Tablature Mapping**: The detected notes are automatically converted into a standard musical note name (e.g., "A2") and then mapped to a specific string and fret position on a standard-tuned 6-string guitar.
* **ASCII Tablature Generation**: The project outputs a formatted .txt file containing a simple, readable guitar tablature of the transcribed melody.
* **Robust Error Handling**: Includes error handling for invalid audio file formats, providing a more user-friendly experience.

## Planned Features
* **Duration-Based Tablature**: Enhance the tablature output to include note duration, representing different note lengths (e.g., quarter notes, eighth notes) for more accurate transcriptions.
* **Improved Fast Melody Detection**: Implement more robust algorithms to handle quick successions of notes, improving the overall accuracy of the transcription.
* **Multi-Note (Polyphonic) Handling**: Investigate and integrate advanced techniques, such as machine learning models, to accurately transcribe chords and other polyphonic audio.

## Dependencies
* `librosa`
* `numpy`

## How to use
This program can be used in two ways: by running a standalone executable (for Windows users) or by running the Python script directly (for all operating systems).

**Option 1: For Windows Users (Executable)**  
For a simple, no-setup-required experience, you can download a standalone executable.
1. **Download the Executable:** Click the link below to download the latest Windows executable.
[Download Guitar Tab Transcriber.exe](https://drive.google.com/file/d/19gpGk9zqjeZMpnT53HvRgmE8cnatmzu6/view?usp=drive_link)

2. **Run the Application**: Double-click the `.exe` file to launch the application.

**Option 2: For All Users (Python Script)**  
If you prefer to run the script directly, or are on a Mac or Linux machine, follow these steps.

1. **Install Dependencies**: First, ensure you have Python 3 installed. Then, install the required libraries using pip:
```
pip install -r requirements.txt
```
2. **Run the Script**: Navigate to the project's directory in your terminal and execute the main script:
```
python src/main.py
```

**Audio Input**  
In both cases, the program will prompt you to drag and drop your audio file into the terminal window. After the file path is displayed, press Enter. The transcribed guitar tablature will be saved to a file named `output.txt` in the same directory.