#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:29:26 2024

@author: samuemu
"""
#%% User inputs

lang_voice_speaker = 'DE_Neural2-F'

# Specify which target stimulus to plot or use '*' to plot every stimulus
callSign = 'Flugzeug'
colour   = 'gelben'
number   = '*'

plot_audio_overlay = False
plot_webmaus_comparison = False

#%% Imports
import numpy as np

import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hilbert
import os
from glob import glob


import textgrids
# To install, run the following line from the terminal:
    # python -m pip install praat-textgrids

#%% Filepaths
thisDir = os.getcwd()
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz')

designation = callSign[:3] + '-' + colour[:3] + '-' + number[:3]
sentence = str("Vorsicht " + callSign + '. Gehe sofort zum ' + colour + ' Feld der Spalte ' + number)

textgridfiles = glob(os.path.join(dirinput,'tts-golang-textGrid', (lang_voice_speaker + '_' + designation + '.TextGrid')))
audiofiles = glob(os.path.join(dirinput,'tts-golang', (lang_voice_speaker + '_' + designation + '.wav')))


#%% plot just the audiofiles
if plot_audio_overlay:
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 4), sharex=True)
    for i, audiofile  in enumerate(audiofiles):
        print(audiofile[audiofile.rfind(lang_voice_speaker):])
        samplFreq, signal = wavfile.read(audiofile)
        time = np.arange(len(signal)) / samplFreq
        
        axes.plot(time, signal, label='signal', alpha = 0.01, color = 'black')
        
        # https://stackoverflow.com/a/53470301
        # The amplitude envelope is given by magnitude of the analytic signal.
        # analytic_signal = hilbert(signal)
        # amplitude_envelope = np.abs(analytic_signal)
        # axes.plot(amplitude_envelope, label='envelope', linewidth = 0.1, alpha = 0.1, color = 'black')
        
    plt.title(sentence)
    plt.show()

#%% and here to compare the webmaus metrics
if plot_webmaus_comparison:
    colormap= ['red','blue','green','black'] 
    for i, audiofile  in enumerate(audiofiles):
        title = audiofile[audiofile.rfind(lang_voice_speaker):]
        print(title)
        
        praatDict = textgrids.TextGrid(textgridfiles[i]) 
        
        samplFreq, signal = wavfile.read(audiofile)
        time = np.arange(len(signal)) / samplFreq
        fig, axes = plt.subplots(nrows=len(praatDict.keys()), ncols=1, figsize=(20, 4*len(praatDict.keys())), sharex=True)
        
        for i, key in enumerate(praatDict.keys()):
            ax = axes[i] 
            ax.plot(time, signal, label='signal', alpha = 0.1, color = 'black')
            
            for item in range(len(praatDict[key])):        
                ax.axvline(x= praatDict[key][item].xmin, color = colormap[i])
            ax.set_title(f'{title} metric {key}')
                
        # plt.title(title)
        plt.show()

#%% And this is just to plot the speech signal and the ORT-MAU segmentation times

for i, audiofile  in enumerate(audiofiles):

    title = audiofile[audiofile.rfind(lang_voice_speaker):audiofile.rfind('.wav')]   
    
    # get the texgrid file with the same 
    for fs in textgridfiles:
        if title in fs:
            textgridfile = textgridfiles[textgridfiles.index(fs)]
            
    print(audiofile[audiofile.rfind(lang_voice_speaker):])   
    print(textgridfile[textgridfile.rfind(lang_voice_speaker):])
    praatDict = textgrids.TextGrid(textgridfile)
    ort_mau = praatDict['ORT-MAU']
    
    samplFreq, signal = wavfile.read(audiofile)
    time = np.arange(len(signal)) / samplFreq
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 4), sharex=True)

    axes.plot(time, signal, label='signal', alpha = 0.1, color = 'black')
    
    for item in ort_mau:    
        # print(item.xmin)
        axes.axvline(x= item.xmin, color = 'lightgrey')
        axes.text(x = item.xmin, y = -10000, s = item.text)
    axes.set_title(f'{title} metric ORT_MAU')
        
    # plt.title(title)
    plt.show()   
