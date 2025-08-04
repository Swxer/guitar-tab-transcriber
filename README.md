# Guitar Tab Transcriber

## Project Goal
The goal of this project is to create a Python script that can automatically transcribe notes from an audio file into guitar tablature.

## Status: Work in Progress
This project is currently in the early stages of development. The core logic for detecting and processing single notes has been successfully implemented, and I am now working on expanding the functionality to handle multiple notes and translate them into guitar fret positions.

## Current Features
* **Audio Loading**: The script can load and process standard `.wav` audio files using the `librosa` library.
* **Pitch Detection**: The script can detect the fundamental frequency (pitch) of a sustained note.
* **Onset Detection**: The script can accurately identify the start time of a note in an audio file.
* **Data Aggregation**: The script can take a series of pitch detections for a single note and aggregate them into a single, representative frequency.
* **Data Visualization**: The script includes a visualization function that plots the audio waveform, detected pitches, and note onsets to verify the accuracy of the detection algorithms.

## Planned Features
* **Multi-Note Handling**: Modify the existing code to handle multiple notes within a single audio file.
* **Frequency-to-Note Conversion**: Convert the final detected frequency (e.g., 110 Hz) into a standard musical note name (e.g., "A2").
* **Tablature Mapping**: Map the detected notes to specific guitar strings and frets to generate a simple tablature.

## Dependencies
* `librosa`
* `numpy`
* `matplotlib` (for visualization)