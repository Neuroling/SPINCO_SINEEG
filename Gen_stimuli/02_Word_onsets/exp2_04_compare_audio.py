#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:29:26 2024

@author: samuelmull
"""
#%% User inputs

lang_voice_speaker = 'DE_Neural2-F'

# Only for the overlay plots: Specify which target stimuli to plot or use '*' to plot every stimulus
callSign = '*'
colour   = '*'
number   = '*'

allCallSign = ['Adl', 'Eul', 'Rat', 'Tig', 'Vel', 'Aut', 'Mes', 'Gab']
allColour = ['gel', 'gru', 'rot', 'wei', 'bla', 'bra', 'pin', 'sch']
allNumber = ['Ein', 'Zwe', 'Dre', 'Vie', 'Fue', 'Sec', 'Neu', 'Nul']

save_plots = True


#%% Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hilbert
import pandas as pd
import os
from glob import glob


#%% Filepaths
thisDir = os.getcwd()
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz')
diroutput = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz', 'word-times')

designation = callSign[:3] + '-' + colour[:3] + '-' + number[:3]
sentence = str("Vorsicht " + callSign + '. Gehe sofort zum ' + colour + ' Feld der Spalte ' + number)

audiofiles = glob(os.path.join(dirinput,'tts-golang-equalisedDuration', ('*' +'.wav')))
praatSummaryFile = os.path.join(dirinput, 'word-times','equalised_tts-golang_wordTimes.csv')

praatTimes = pd.read_csv(praatSummaryFile)
praatTimes = praatTimes.iloc[0]

#%% plot just the audiofiles as overlay
selected_audiofiles = audiofiles
for target in [callSign, colour, number]:
    if target != '*':
        selected_audiofiles = [item for item in selected_audiofiles if target in item]


opacity = 1/len(selected_audiofiles)
if opacity <= 0.01: opacity = 0.005

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 4), sharex=True)

for i, audiofile  in enumerate(selected_audiofiles):
    print(audiofile[audiofile.rfind(os.sep):])
    samplFreq, signal = wavfile.read(audiofile)
    time = np.arange(len(signal)) / samplFreq
    
    axes.plot(time, signal, label='signal', alpha = opacity, color = 'black')
    
    # # For the amplitude envelope (don't run this for all files because it is computationally intense)
    # # https://stackoverflow.com/a/53470301
    # # The amplitude envelope is given by magnitude of the analytic signal.
    # analytic_signal = hilbert(signal)
    # amplitude_envelope = np.abs(analytic_signal)
    # axes.plot(amplitude_envelope, label='envelope', linewidth = 0.1, alpha = 0.1, color = 'black')   
plt.title(sentence)
plt.show()
if save_plots: plt.savefig((diroutput + os.sep + 'plot_amplitudeOverlay_equalisedDuration.png'), bbox_inches = "tight")


#%% plot amplitude of all target words in a 8x3 grid (averaged within word)
nrows = max(len(allCallSign), len(allColour), len(allNumber))


fig, axes = plt.subplots(nrows=nrows, ncols=3, figsize=(20,20), sharex=True)

for col, allTarget in enumerate([allCallSign, allColour, allNumber]):
    # get onset and offset times
    tmin = int(praatTimes[('token_' + str(col +1)+ '_tmin')] * 48000)
    tmax = int(praatTimes[('token_' + str(col +1)+ '_tmax')] * 48000)
    
    for row, stimulus in enumerate(allTarget):
        ax = axes[row, col]
        selected_audiofiles = [item for item in audiofiles if stimulus in item[-20:]]
        
        for i, audiofile  in enumerate(selected_audiofiles):
            
            print(audiofile[audiofile.rfind(os.sep):])
            samplFreq, signal = wavfile.read(audiofile)
            
            # tmin = int(tmin * samplFreq)
            # tmax = int(tmax * samplFreq)

            time = np.arange((tmax-tmin)) / samplFreq
            
            ax.plot(time, signal[tmin:tmax], label='signal', alpha = 0.02, color = 'black')
            ax.set_ylim(0.75, -0.75)
            ax.text(x=0.5, y=0.5, s = stimulus)
            
if save_plots: plt.savefig((diroutput + os.sep + 'plot_amplitudeOverlay_perTarget_equalisedDuration.png'), bbox_inches = "tight")

    
