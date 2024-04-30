#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:29:26 2024

@author: samuemu
"""

import numpy as np
import wave

import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hilbert
import os
from glob import glob
from random import shuffle

thisDir = os.getcwd()
# dirinput = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz','tts-golang_sentences')
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz','tts-golang')
lang_voice_speaker = 'DE_Neural2-F'

files = glob(os.path.join(dirinput, (lang_voice_speaker+'_'+'*'+'.wav')))
# shuffle(files)

# file = files[0]
for i, file  in enumerate(files):
    print(file[-15:])
    signal = wavfile.read(file)
    
    samplFreq = signal[0]
    
    # https://stackoverflow.com/a/53470301
    # The amplitude envelope is given by magnitude of the analytic signal.
    # analytic_signal = hilbert(signal[1])
    # amplitude_envelope = np.abs(analytic_signal)
    
    plt.plot(signal[1], label='signal', alpha = 0.01, color = 'black')
    # plt.plot(amplitude_envelope, label='envelope')
# plt.title('Vorsicht Adler. Gehe sofort zum * Feld der Spalte *')
plt.show()
