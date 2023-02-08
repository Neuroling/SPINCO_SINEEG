# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:44:31 2023

@author: gfraga
"""

import matplotlib.pyplot as plt
import numpy as np
import wave
import io
import scipy.signal as sig

# Load the speech signal from wave file
speech_file = "V:/spinco_data/AudioRecs/LIRI_voice_DF/segments/Take1_all_trimmed/trim_loudNorm-23LUFS_SiSSN/SiSSN_Absatz_norm-10db.wav"
speech_file = "V:/spinco_data/AudioRecs/LIRI_voice_DF/segments/Take1_all_trimmed/trim_loudNorm/Affe_trim_norm.wav"
with wave.open(speech_file, "rb") as wave_file:
    fs = wave_file.getframerate()
    n_samples = wave_file.getnframes()
    speech = np.frombuffer(wave_file.readframes(n_samples), dtype=np.int16)
    
# White noise signal
noise = np.random.normal(0, 1, len(speech)) # White noise signal


# Plotting
plt.figure(figsize=(12, 10))

plt.subplot(321)
plt.plot(speech)
plt.title("Speech signal")
plt.xlabel("Sample")
plt.ylabel("Amplitude")

plt.subplot(322)
f, t, Sxx = sig.spectrogram(speech, fs=fs)
plt.pcolormesh(t, f, Sxx)
plt.title("Speech signal spectrogram")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")

plt.subplot(323)
plt.plot(noise)
plt.title("White noise signal")
plt.xlabel("Sample")
plt.ylabel("Amplitude")

plt.subplot(324)
f, t, Sxx = sig.spectrogram(noise, fs=fs)
plt.pcolormesh(t, f, Sxx)
plt.title("White noise signal spectrogram")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")

plt.show()


# %%
# Plotting
plt.figure(figsize=(12, 5))

plt.subplot(121)
f, Pxx = sig.welch(speech, fs=fs)
plt.plot(f, Pxx)
plt.title("Speech signal power spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")

plt.subplot(122)
f, Pxx = sig.welch(noise, fs=fs)
plt.plot(f, Pxx)
plt.title("White noise signal power spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")

plt.show()