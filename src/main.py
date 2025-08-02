import librosa
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
# import scipy
# import pydub

SAMPLE_RATE = 44100

guitar_notes = {
    'E2': 82.41,
    'A2': 110,
    'D3': 146.83,
    'G3': 196,
    'B3': 246.94,
    'E4': 329.63
}

expected_ranges = {
    'E2': (75, 90),
    'A2': (100, 120),
    'D3': (140, 160),
    'G3': (190, 210),
    'B3': (240, 260),
    'E4': (320, 340)
}

def load_audio_file(filename):
    return librosa.load(filename)

def get_pitch(y,sr):
    
    fmin = librosa.note_to_hz('E2')
    fmax = librosa.note_to_hz('C7')
    
    f0, voiced_flag, voiced_prob = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=sr)
    return f0, voiced_flag

def onset_detect(y,sr):
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    return onset_frames

def visualize(y, sr, f0, onsets):
    # Create the plot
    fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(10, 6))

    # Plot the audio waveform
    librosa.display.waveshow(y, sr=sr, ax=ax[0])
    ax[0].set(title='Audio Waveform')
    ax[0].set_ylabel('Amplitude')

    # Plot the fundamental frequency (pitch)
    times = librosa.times_like(f0)
    ax[1].plot(times, f0, label='f0', color='r', linewidth=2)
    ax[1].set(title='Pitch Detection')
    ax[1].set_ylabel('Frequency (Hz)')
    ax[1].set_xlabel('Time (s)')
    ax[1].grid(True)
    
    # Overlay the onset times as vertical lines
    # This line now uses the full height of the plot for clarity
    ax[1].vlines(onsets, 0, ax[1].get_ylim()[1], color='g', linestyle='--', label='Onsets')
    
    ax[1].legend(loc='upper right')

    # Zoom in on the beginning of the audio to see the onset
    # ax[0].set_xlim(0, 1)
    # ax[1].set_xlim(0, 1)

    # Display the plot
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    print('hello world')
    y, sr = load_audio_file('./data/A2.wav')
    f0, voiced_flag = get_pitch(y,sr)
    onsets = onset_detect(y,sr)

    # Create a new array with only the pitches we are confident about 
    confident_f0 = f0[voiced_flag]
    print(f'Detected pitch: {f0}')
    print(f'Detected onsets (in seconds): {onsets}')

    visualize(y, sr, f0, onsets)