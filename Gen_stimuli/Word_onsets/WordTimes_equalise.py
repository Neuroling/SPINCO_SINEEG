#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EQUALISE TARGET WORD DURIATION
===============================================================================
Created on Fri May  3 07:59:15 2024
@author: samuemu
"""

#%% imports
import os as os
from glob import glob
import pandas as pd
import textgrids
from scipy.io import wavfile
import librosa
import numpy as np
import shutil

#%% filepaths
thisDir = os.getcwd()
baseDir = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Stimuli', 'AudioGens','Experiment2','tts-golang-44100hz')
audiodir = os.path.join(baseDir, 'tts-golang')
diroutput = os.path.join(baseDir, 'tts-golang-equalisedDuration')

#%% Get word onset time dataframe
df = pd.read_csv(os.path.join(baseDir, 'word-times','Full_tts-golang_allTimes.csv'))


#%% get mean & std of durations of each segment
sentence = ['Start', 'Vorsicht', 'CallSign', 'Break', 'Geh', 'Sofort', 'Zum', 'Colour', 'Feld', 'Von', 'Der', 'Spalte', 'Number', 'End']

mean_segment = []
std_segment = []
for segment in sentence:
    mean_segment.append((df[segment + '_tmax'] - df[segment + '_tmin']).mean())
    std_segment.append((df[segment + '_tmax'] - df[segment + '_tmin']).std())
mean_durations = pd.DataFrame(mean_segment).transpose()
mean_durations.columns = sentence

std_durations = pd.DataFrame(std_segment).transpose()
std_durations.columns = sentence

    
#%% standardise duration - loop to process each audio file

for filename in df['file']:
    
    # get actual filepath (without file extension)
    filepath = os.path.join(audiodir, filename)
    
    
    # copy .txt file to the new folder and rename it to start with "equalised_"
    shutil.copy(filepath + '.txt', os.path.join(diroutput, filename + '.txt'))
    os.rename(os.path.join(diroutput, filename + '.txt'), os.path.join(diroutput,'equalised_' + filename + '.txt'))

    # Load audio file
    y, sr = librosa.load(filepath + '.wav', sr=None)

    segments = []
    for segment in sentence:
        segment_start = int(df.loc[df['file'] == filename, segment + '_tmin'].values[0] * sr)
        segment_end = int(df.loc[df['file'] == filename, segment + '_tmax'].values[0] * sr)

        # Adjust length of the segment
        segment_length = segment_end - segment_start
        
        segment_mean = mean_durations[segment][0]*sr
        rate = (segment_length/segment_mean)
        
        y_segment_stretched = librosa.effects.time_stretch(y[segment_start:segment_end], rate = rate )
        
        segments.append(y_segment_stretched)
        if len(y_segment_stretched) != round(segment_mean):
            raise ValueError('WARNING! Segment length could not be equalised. This could be due to a change in how librosa uses rate to calculate the length of the new segment. ')
        
    # Concatenate segments
    y_processed = np.concatenate(segments)

    
    output_file = os.path.join(diroutput, 'equalised_' + filename + '.wav')
    wavfile.write(output_file, sr, y_processed)
