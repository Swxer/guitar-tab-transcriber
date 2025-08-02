import librosa
import numpy as np
import matplotlib.pyplot as plt

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