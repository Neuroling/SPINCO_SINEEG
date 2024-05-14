#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:10:47 2024

@author: samuemu

This will give you various tables of mean durations of segments (segmented by webmaus)


"""

save_plots = False
inlcuding_old = False

#%% imports
import numpy as np

import pandas as pd
import os

import seaborn as sns
import matplotlib.pyplot as plt 
from datetime import datetime

#%%
thisDir = os.getcwd()
baseDir = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz','word-times')



#%% Get word onset time dataframe
df = pd.read_csv(os.path.join(baseDir, 'Full_tts-golang_allTimes.csv'))

if inlcuding_old: df = pd.concat([df,pd.read_csv(os.path.join(baseDir, 'old_Full_tts-golang_allTimes.csv'))])

#%% 
sentence = ['Start', 'Vorsicht', 'CallSign', 'Break', 'Geh', 'Sofort', 'Zum', 
            'Colour', 'Feld', 'Von', 'Der', 'Spalte', 'Number', 'End']

# get all unique callSigns, colours and numbers
callSigns = list(set([item for item in df['CallSign']]))

colours = list(set([item for item in df['Colour']]))

numbers = list(set([item for item in df['Number']]))

stimType = ['CallSign', 'Colour', 'Number']
stimAll = callSigns + colours + numbers
stimLists = [callSigns] + [colours] + [numbers]


#%% get mean & std of durations of each segment

mean_segment = []
std_segment = []
for segment in sentence:
    mean_segment.append((df[segment + '_tmax'] - df[segment + '_tmin']).mean())
    std_segment.append((df[segment + '_tmax'] - df[segment + '_tmin']).std())
mean_durations = pd.DataFrame(mean_segment).transpose()
mean_durations.columns = sentence

std_durations = pd.DataFrame(std_segment).transpose()
std_durations.columns = sentence

del segment, std_segment, mean_segment

#%% get mean & std of durations of each segment within target words

rownames_mean = ['overall_mean']
rownames_std = ['overall_std']
duration_info_mean = [mean_durations]
duration_info_std =  [std_durations]

for stim in stimAll:
    tmp_df = df[df['file'].str.contains(stim[:3])]
    rownames_mean.append(stim + '_mean')
    rownames_std.append(stim + '_std')
    
    mean_segment = []
    std_segment = []
    for segment in sentence:
        mean_segment.append((tmp_df[segment + '_tmax'] - tmp_df[segment + '_tmin']).mean())
        std_segment.append((tmp_df[segment + '_tmax'] - tmp_df[segment + '_tmin']).std())
    mean_durations = pd.DataFrame(mean_segment).transpose()
    mean_durations.columns = sentence
    std_durations = pd.DataFrame(std_segment).transpose()
    std_durations.columns = sentence
    
    duration_info_mean.append(mean_durations)
    duration_info_std.append(std_durations)
    
duration_info_mean = pd.concat(duration_info_mean)
duration_info_std = pd.concat(duration_info_std)   

duration_info_mean.index = rownames_mean
duration_info_std.index = rownames_std

del rownames_mean, rownames_std, tmp_df, mean_durations, std_durations
del segment, std_segment, mean_segment

#%%
maxLen = max([len(callSigns),len(colours),len(numbers)])

mean_targetWord = []
std_targetWord = []
rownames = list(range(maxLen))

# iterate over the three lists
for i, targetList in enumerate(stimLists):
    targetWord = stimType[i]
    mean = []
    std = []
    
    # iterate over Stimuli within lists
    for ii, stim in enumerate(targetList):
        tmp_df = df[df['file'].str.contains(stim[:3])]
        
        rownames[ii] = str(rownames[ii]) +'-'+ stim[:3]
        
        mean.append( tmp_df[targetWord + '_duration'].mean())
        std.append( tmp_df[targetWord + '_duration'].std())
        
    mean_targetWord.append(pd.Series(mean))
    std_targetWord.append(pd.Series(std))
    

mean_targetWord = pd.DataFrame(mean_targetWord).transpose()
std_targetWord = pd.DataFrame(std_targetWord).transpose()
mean_targetWord.index = rownames
std_targetWord.index = rownames 

# del rownames, maxLen, targetList, targetWord, i, ii, stim, mean, std, tmp_df

#%%

output_path = baseDir + os.sep + 'plot_wordDuration_'
output_end = '_' + str(datetime.now())[:-10].replace(':','') + '.png'
df_lf = []
for i in stimType:
    df_tmp = pd.melt(df, id_vars=[i], value_vars=[i + '_duration'])
    df_tmp.columns = ['Stimulus', 'variable','value']
    
    plt.figure()
    ax=sns.stripplot(data=df_tmp, x='value', y='variable', hue = 'Stimulus',linewidth=(0.5), dodge = True)
    ax=sns.violinplot(data=df_tmp, x='value', y='variable', hue = 'Stimulus',linewidth=(0), dodge = True, saturation = 0.3, palette = ['lightgrey'], legend = False)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.xlabel('original duration of word')
    if save_plots: plt.savefig((output_path + i + output_end), bbox_inches = "tight")
    
    df_lf.append(df_tmp)
df_lf = pd.concat(df_lf)
del df_tmp

plt.figure(figsize=[10,7])
ax=sns.stripplot(data=df_lf, x='value', y='variable', hue = 'Stimulus',linewidth=(0.5))
ax=sns.violinplot(data=df_lf, x='value', y='variable',linewidth=(0), saturation = 0.3, color = 'lightgrey')
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
plt.xlabel('original duration of word')
if save_plots: plt.savefig((output_path + 'allTargets' + output_end), bbox_inches = "tight")
