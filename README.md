# Guitar Tab Transcriber

## Project Goal
The goal of this project is to create a Python script that can automatically transcribe notes from an audio file into guitar tablature.

## Status: Work in Progress
This project is currently under active development. The core logic for transcribing simple, single-note melodies into guitar tablature has been successfully implemented. I am now working on improving the accuracy of note detection for fast melodies and incorporating note duration to create more complete and realistic tabs.

## Current Features
* **Audio Loading**: The script can process standard audio files (`.wav`, `.mp3`, etc.) and automatically extract relevant musical data for transcription.
* **Monophonic Note Transcription**: The script successfully transcribes simple monophonic melodies (one note at a time) from an audio file into a sequence of notes.
* **Pitch and Onset Detection**: It uses a machine learning model from the `basic-pitch` library to identify individual notes and their starting points.
* **Frequency-to-Tablature Mapping**: The detected notes are automatically converted into a standard musical note name (e.g., "A2") and then mapped to a specific string and fret position on a standard-tuned 6-string guitar.
* **ASCII Tablature Generation**: The project outputs a formatted .txt file containing a simple, readable guitar tablature of the transcribed melody.
* **Robust Error Handling**: Includes error handling for invalid audio file formats, providing a more user-friendly experience.

---

## Recommended Workflow

For the best results, it is highly recommended that you first use a third-party program to **isolate the musical component** you want to transcribe. The program works best on a clean audio file that contains only the melody line.

https://splitter.ai/ is a free tool that can separate a song into its individual musical components, allowing you to select the track with the melody you need.

* **Disclaimer**: This program is not 100% accurate. Due to the complexities of audio analysis, the transcriber might pick up very minor sounds, resulting in extra notes in the tablature. Please use the output as a guideline and use your own judgment to determine which notes are necessary and which are not.

---

## Planned Features
* **Fret Range Selection**: Allow the user to specify a preferred fret range to produce a more playable tablature.
* **Duration-Based Tablature**: Enhance the tablature output to include note duration, representing different note lengths (e.g., quarter notes, eighth notes) for more accurate transcriptions.
* **Polyphonic Handling**: Investigate and integrate advanced techniques to accurately transcribe chords and other polyphonic audio.

---

## Dependencies
* `librosa`
* `basic-pitch`

**A note for contributors:** If you plan to contribute to this project, please ensure you are using a compatible Python version. The `basic-pitch` library currently only supports Python versions **3.7, 3.8, 3.9, 3.10, and 3.11**.

---

## How to use
1. **Git Clone the Repo**:


**HTTPS**
```
git clone https://github.com/Swxer/guitar-tab-transcriber.git
```
**SSH**
```
git clone git@github.com:Swxer/guitar-tab-transcriber.git
```
**GitHub CLI**
```
gh repo clone Swxer/guitar-tab-transcriber
```

2.  **Install Dependencies**: First, ensure you have a compatible version of Python 3 installed. Then, install the required libraries using pip:
```
pip install -r requirements.txt
```
3. **Run the Script**: Navigate to the project's directory in your terminal and execute the main script:
```
python src/main.py
```

**Audio Input**  

To use the program, run the main script and wait until it prompts you to drag and drop your audio file into the terminal. After the file path is displayed, press Enter. The program will then ask if you want to adjust the octaves before generating the transcribed guitar tablature, which will be saved to a file named `output.txt` in the same directory.

