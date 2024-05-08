#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:10:47 2024

@author: samuemu

This will give you various tables of mean durations of segments (segmented by webmaus)


"""
import numpy as np

import pandas as pd
import os

#%%
thisDir = os.getcwd()
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz')



#%% Get word onset time dataframe
df = pd.read_csv(os.path.join(dirinput, 'word-times','Full_tts-golang_allTimes.csv'))


#%% 
sentence = ['Start', 'Vorsicht', 'CallSign', 'Break', 'Geh', 'Sofort', 'Zum', 
            'Colour', 'Feld', 'Von', 'Der', 'Spalte', 'Number', 'End']

# get all unique callSigns, colours and numbers
callSigns = list(set([item for item in df['CallSign']]))

colours = list(set([item for item in df['Colour']]))

numbers = list(set([item for item in df['Number']]))

stimuli = callSigns + colours + numbers

#%% get mean & std of durations of each segment
# mean_segment = []
# std_segment = []
# for segment in sentence:
#     mean_segment.append((df[segment + '_tmax'] - df[segment + '_tmin']).mean())
#     std_segment.append((df[segment + '_tmax'] - df[segment + '_tmin']).std())
# mean_durations = pd.DataFrame(mean_segment).transpose()
# mean_durations.columns = sentence

# std_durations = pd.DataFrame(std_segment).transpose()
# std_durations.columns = sentence

#%% get mean & std of durations of each segment within target words

# rownames_mean = ['overall_mean']
# rownames_std = ['overall_std']
# duration_info_mean = [mean_durations]
# duration_info_std =  [std_durations]

# for stim in stimuli:
#     tmp_df = df[df['file'].str.contains(stim[:3])]
#     rownames_mean.append(stim + '_mean')
#     rownames_std.append(stim + '_std')
    
#     mean_segment = []
#     std_segment = []
#     for segment in sentence:
#         mean_segment.append((tmp_df[segment + '_tmax'] - tmp_df[segment + '_tmin']).mean())
#         std_segment.append((tmp_df[segment + '_tmax'] - tmp_df[segment + '_tmin']).std())
#     mean_durations = pd.DataFrame(mean_segment).transpose()
#     mean_durations.columns = sentence
#     std_durations = pd.DataFrame(std_segment).transpose()
#     std_durations.columns = sentence
    
#     duration_info_mean.append(mean_durations)
#     duration_info_std.append(std_durations)
    
# duration_info_mean = pd.concat(duration_info_mean)
# duration_info_std = pd.concat(duration_info_std)   

# duration_info_mean.index = rownames_mean
# duration_info_std.index = rownames_std

#%%
maxLen = max([len(callSigns),len(colours),len(numbers)])

wordOrder = ['CallSign', 'Colour', 'Number']
stimLists = [callSigns] + [colours] + [numbers]

mean_targetWord = []
std_targetWord = []
rownames = list(range(maxLen))
# iterate over the three lists
for i, targetList in enumerate(stimLists):
    
    mean = []
    std = []
    # iterate over stimuli within lists
    for ii, stim in enumerate(targetList):
        tmp_df = df[df['file'].str.contains(stim[:3])]
        
        rownames[ii] = str(rownames[ii]) +'-'+ stim[:3]
        targetWord = wordOrder[i]
        mean.append( (tmp_df[targetWord + '_tmax'] - tmp_df[targetWord + '_tmin']).mean())
        std.append( (tmp_df[targetWord + '_tmax'] - tmp_df[targetWord + '_tmin']).std())
        
    mean_targetWord.append(pd.Series(mean))
    std_targetWord.append(pd.Series(std))
    

mean_targetWord = pd.DataFrame(mean_targetWord).transpose()
std_targetWord = pd.DataFrame(std_targetWord).transpose()
mean_targetWord.index = rownames
std_targetWord.index = rownames 
