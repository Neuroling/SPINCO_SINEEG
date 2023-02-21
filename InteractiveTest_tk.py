# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:50:23 2023

@author: gfraga
"""

import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class WaveformPanel:
    def __init__(self, master):
        self.master = master
        master.title("Waveform Panel")

        # Create GUI elements
        self.filename_label = tk.Label(master, text="Select a .wav file")
        self.filename_label.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.plot_button = tk.Button(master, text="Plot", command=self.plot_waveform)
        self.plot_button.pack()

        # Initialize figure and axes for waveform and power spectrum plots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 6))

    def browse_file(self):
        # Open file dialog to select a .wav file
        self.filename = filedialog.askopenfilename(filetypes=(("WAV files", "*.wav"),))

        # Update label to display selected filename
        self.filename_label.config(text=self.filename)

    def plot_waveform(self):
        # Load waveform data from selected .wav file
        sample_rate, data = wavfile.read(self.filename)

        # Compute time vector from sample rate and data length
        duration = len(data) / sample_rate
        time = np.linspace(0, duration, len(data))

        # Compute power spectral density and power spectrum
        psd, freqs = plt.psd(data, Fs=sample_rate)
        power_spectrum = np.square(psd)

        # Plot waveform, PSD, and power spectrum
        self.ax1.clear()
        self.ax1.plot(time, data)
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Amplitude")
        self.ax1.set_title("Waveform")

        self.ax2.clear()
        self.ax2.plot(freqs, psd)
        self.ax2.set_xlabel("Frequency (Hz)")
        self.ax2.set_ylabel("Power Spectral Density (dB/Hz)")
        self.ax2.set_title("PSD")

        self.fig2, ax = plt.subplots(figsize=(6, 6))
        ax.plot(freqs, power_spectrum)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Power (dB)")
        ax.set_title("Power Spectrum")

        plt.show()

# Create and run the GUI
root = tk.Tk()
waveform_panel = WaveformPanel(root)
root.mainloop()
