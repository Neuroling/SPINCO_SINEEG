#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EQUALISE WORD DURIATION
===============================================================================
Created on Fri May  3 07:59:15 2024
@author: samuelmull

This script will use the .csv file of gathered webmaus word times of each stimuli
and calculate the mean and std of the duration of each identified segment.

It will then loop over audiofiles, and over each segment within each audiofile.
Each segment is stretched/squeezed to have a duration equal to the mean duration
of that segment. This is done without changing the pitch. To remove impulse bursts,
each segment is fading in and out by `crossfade_duration` seconds (adjust below).
Then, the segments are joined back together and saved as .wav file with the prefix
'equalised_'

After all audiofiles are processed, the new word onset times are saved as .csv file.
This .csv file is needed to generate the flow spreadsheets.

"""
crossfade_duration = 0.01 # in seconds

#%% imports
import os as os
from glob import glob
import pandas as pd

from scipy.io import wavfile
import librosa
import numpy as np
import shutil
from itertools import accumulate


#%% filepaths
thisDir = os.getcwd()
baseDir = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Stimuli', 'AudioGens','Experiment2','tts-golang-44100hz')
audiodir = os.path.join(baseDir, 'tts-golang')
diroutput = os.path.join(baseDir, 'tts-golang-equalisedDuration')

if not os.path.exists(diroutput):
    os.mkdir(diroutput)



#%% Get word onset time dataframe
df = pd.read_csv(os.path.join(baseDir, 'word-times','Full_tts-golang_allTimes.csv'))
original_columns = df.columns

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

df_summary = pd.concat([mean_durations, std_durations])
df_summary.index = ['mean_durations','std_durations']
df_summary.to_csv(os.path.join(baseDir, 'word-times', 'summary_equalised_tts-golang_wordTimes.csv'), index= True)
 
  
#%% standardise duration - loop to process each audio file
df_segment_tmax = [] # collect tmax of every segment for every audiofile

for filename in df['file']:
    
    # get actual filepath (without file extension)
    filepath = os.path.join(audiodir, filename)
    print(filepath)
    
    # copy .txt file to the new folder and rename it to start with "equalised_"
    shutil.copy(filepath + '.txt', os.path.join(diroutput, filename + '.txt'))
    os.rename(os.path.join(diroutput, filename + '.txt'), os.path.join(diroutput,'equalised_' + filename + '.txt'))

    # Load audio file
    y, sr = librosa.load(filepath + '.wav', sr=None)
    
    fade_length = int(sr * crossfade_duration)
    fade_out = np.linspace(1,0, fade_length) 
    fade_in = np.linspace(0,1, fade_length) 
    
    segments = [] # collect segments to later concatenate again into a full audifile
    all_segment_len = [] # collect segment lengths for this file
    for segment in sentence:
        #
        segment_start = int(df.loc[df['file'] == filename, segment + '_tmin'].values[0] * sr)
        segment_end = int(df.loc[df['file'] == filename, segment + '_tmax'].values[0] * sr)

        # Adjust length of the segment
        segment_length = segment_end - segment_start
        
        segment_mean = mean_durations[segment][0]*sr
        rate = (segment_length/segment_mean)
        
        y_segment_stretched = librosa.effects.time_stretch(y[segment_start:segment_end], rate = rate )
        
        # fading in and out to avoid the impulse bursts
        y_segment_stretched[:fade_length] = y_segment_stretched[:fade_length] * fade_in
        y_segment_stretched[-fade_length:] = y_segment_stretched[-fade_length:] * fade_out
        
        segments.append(y_segment_stretched)
        all_segment_len.append(len(y_segment_stretched))
        

        if len(y_segment_stretched) != round(segment_mean):
            raise ValueError('WARNING! Segment length could not be equalised. May be due to changes in how librosa uses `rate` to calculate new segment length.') 
            # e.g. previous versions of the package seemed to have calculated the new length by multiplying with `rate`, 
            # whereas the version I'm using (v0.10.2) divides by `rate`. 
            # Look at the source code of the function to make sure: `./site-packages/librosa/effects.py in time_stretch` 
            # It should be something like `len_stretch = int(round(y.shape[-1] / rate))`
      

    
    # Concatenate segments & save new .wav file
    y_processed = np.concatenate(segments)
    output_file = os.path.join(diroutput, 'equalised_' + filename + '.wav')
    wavfile.write(output_file, sr, y_processed)
    
    # collect tmax for each segment in a list of df to later create the new wordTimes df
    all_tmax_sr = list(accumulate(all_segment_len)) # cumulative sums of segment durations to get tmax
    all_tmax = [x / sr for x in all_tmax_sr] # from samples to seconds
    all_tmax = pd.DataFrame([[filename]+all_tmax])
    all_tmax.columns = ['file']+ sentence
    
    df_segment_tmax.append(all_tmax)
    

#%% concatenate dfs for every file into one big df
# there should be the same numbers for every row (every audiofile), because the segments are now equalised
df_segment_tmax = pd.concat(df_segment_tmax)

df_segment_tmax['firstSound_tmin'] = df_segment_tmax['Start']
df_segment_tmax['lastSound_tmax'] = df_segment_tmax['Number']
df_segment_tmax['token_1_tmin'] = df_segment_tmax['Vorsicht']
df_segment_tmax['token_1_tmax'] = df_segment_tmax['CallSign']
df_segment_tmax['token_2_tmin'] = df_segment_tmax['Zum']
df_segment_tmax['token_2_tmax'] = df_segment_tmax['Colour']
df_segment_tmax['token_3_tmin'] = df_segment_tmax['Spalte']
df_segment_tmax['token_3_tmax'] = df_segment_tmax['Number']

df_segment_tmax.drop(sentence, axis = 1, inplace = True)
df_segment_tmax.to_csv(os.path.join(baseDir, 'word-times', 'equalised_tts-golang_wordTimes.csv'), index= True)
