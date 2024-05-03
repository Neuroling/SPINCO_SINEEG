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
import matplotlib.pyplot as plt
import seaborn as sns
import librosa
import numpy as np

#%%
thisDir = os.getcwd()
baseDir = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Stimuli', 'AudioGens','Experiment2','tts-golang-44100hz')
audiodir = os.path.join(baseDir, 'tts_golang') + os.sep
df = pd.read_csv(os.path.join(baseDir, 'word-times','Full_tts-golang_allTimes.csv'))
# df['stim_duration'] = df['lastSound_tmax'] - df['firstSound_tmin']
# df['token_1_duration'] = df['token_1_tmax'] - df['token_1_tmin']
# df['token_2_duration'] = df['token_2_tmax'] - df['token_2_tmin']
# df['token_3_duration'] = df['token_3_tmax'] - df['token_3_tmin']
# df['non_target_duration'] = df['stim_duration'] - df['token_1_duration'] - df['token_2_duration'] - df['token_3_duration']

# #%%
# mean_t1_duration = df['token_1_duration'].mean()
# mean_t2_duration = df['token_2_duration'].mean()
# mean_t3_duration = df['token_3_duration'].mean()
# mean_stim_duration = df['stim_duration'].mean()
# mean_nT_duration = df['non_target_duration'].mean()

# std_t1_duration = df['token_1_duration'].std()
# std_t2_duration = df['token_2_duration'].std()
# std_t3_duration = df['token_3_duration'].std()
# std_stim_duration = df['stim_duration'].std()
# std_nT_duration = df['non_target_duration'].std()

#%% to standardise duration, I need to stretch each segment by a factor of (mean - duration)/duration


# Load your dataframe with timestamps
# Example dataframe df
# df = pd.DataFrame({'filename': ['audio1.wav', 'audio2.wav'],
#                    's1_tmin': [0.5, 0.3], 's1_tmax': [1.5, 1.8],
#                    's2_tmin': [2.0, 1.9], 's2_tmax': [3.5, 3.8],
#                    's3_tmin': [4.0, 3.9], 's3_tmax': [5.0, 5.2]})


sentence = ['Start', 'Vorsicht', 'CallSign', 'Break', 'Geh', 'Sofort', 'Zum', 'Colour', 'Feld', 'Von', 'Der', 'Spalte', 'Number', 'End']

mean_segment = []
for segment in sentence:
    # Calculate mean duration of the segment
    mean_segment.append((df[segment + '_tmax'] - df[segment + '_tmin']).mean())
mean_durations = pd.DataFrame(mean_segment).transpose()
mean_durations.columns = sentence

#%% loop to process each audio file
for filename in df['file']:

    # Load audio file
    y, sr = librosa.load((audiodir + filename), sr=None)
    
    """
    Now I need to loop over segments... # TODO
    """
    segments = []
    for segment in sentence:
        segment_start = int(df.loc[df['filename'] == filename, segment + '_tmin'].values[0] * sr)
        segment_end = int(df.loc[df['filename'] == filename, segment + '_tmax'].values[0] * sr)
    # s2_start = int(df.loc[df['filename'] == filename, 's2_tmin'].values[0] * sr)
    # s2_end = int(df.loc[df['filename'] == filename, 's2_tmax'].values[0] * sr)
    # s3_start = int(df.loc[df['filename'] == filename, 's3_tmin'].values[0] * sr)
    # s3_end = int(df.loc[df['filename'] == filename, 's3_tmax'].values[0] * sr)
    
        # Adjust length of the segment
        segment_length = segment_end - segment_start
        y_segment_stretched = librosa.effects.time_stretch(y[segment_start:segment_end], mean_durations[segment] / segment_length)
        segments.append(y_segment_stretched)
    break
    # Concatenate segments
    # y_processed = np.concatenate((y_s1_stretched, y[s2_start:s2_end], y[s3_start:s3_end]))

    # librosa.output.write_wav('processed_' + filename, y_processed, sr)
    
    


#%%
# df.columns = df.columns[:2].tolist() + ['orig_' + col for col in df.columns[2:]]
