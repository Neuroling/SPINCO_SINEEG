#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:39:09 2024

@author: testuser
"""
import mne
from glob import glob
import os 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# User inputs
taskID = 'task-sin'
subjID = 's202'

# PATHS
thisDir = os.getcwd()
# subIDs= [item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','sourcedata')) if item[-3] == '2']

eeg_fp = glob(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','sourcedata', subjID, '*.bdf'))[0]

EEG = mne.io.read_raw_bdf(eeg_fp, eog = ['EXG3', 'EXG4', 'EXG5', 'EXG6'], misc = ['EXG1', 'EXG2'])
events = mne.find_events(EEG, 'Status')

#%% Recoding event triggers to correct bit-overflow
# Because event triggers are for some reason stored as a single byte,
# numbers above 256 overflow back to 1. So triggers 300-339 (which we use
# for clear trials) are now coded as 44-83. This means that triggers
# 55 (end of instruction screen) and 60 (end of block) are now the same as
# the codes that originally were 311 and 316
#
# This loop recodes triggers that should be 300-339 by adding +256 to 
# the triggers between 44 and 83. For codes 55 and 60, it will only recode
# them to 311 and 316 if they were immediately preceded by code 300.
# Since 311 and 316 refer to onset of callSign (token_1_tmin), they always 
# have to follow 300, which refers to audio onset (firstSound_tmin)
for i in range(len(events)):
    if events[i,2] <= 83 and events[i,2]>= 44:
        if (events[i,2] == 55 and events[i-1,2] == 300) or events[i,2] != 55 :
            if (events[i,2] == 60 and events[i-1,2] == 300) or events[i,2] != 60  :
                events[i,2] = events[i,2] + 256
                


#%% Check in which trials the trigger code 1 is missing.
for i in range(len(events)):
    if events[i,2] == 100 or events[i,2] == 200 or events[i,2] == 300:
        if events[i-1,2] != 1:
            print('idx',i, ': preceding event', events[i-1,2])

#%% check how much difference (in samples) there is between the audio onset triggers and trigger code 1
diff_1_onset = [events[i,0] - events[i-1,0] for i in range(len(events)) if (events[i,2] == 100 or events[i,2] == 200 or events[i,2] == 300) and events[i-1,2] == 1]
print(np.std(diff_1_onset))
print(np.mean(diff_1_onset))
print(np.min(diff_1_onset))
print(np.max(diff_1_onset))
sns.violinplot(diff_1_onset, orient = 'h')

#%% Check how large the difference between two triggers are compared to what they should be (excel file)

times = [0.163854167,0.702291667,1.256333333,2.368270833,2.7699375,3.9993125,4.470875]
times = [int(i *2048) for i in times]
# This is the onset and offset times of the audio triggers from the excel in samples
# firstSound_tmin, token_1_tmin, token_1_tmax, token_2_tmin, token_2_tmax, token_3_tmin, lastSound_tmax
X = 0 # Compare difference of X and Y. These are the indexes of the list commented one line above.
Y = 1
        
for i in range(len(events)):
    if events[i,2] == 100 or events[i,2] == 200 or events[i,2] == 300:
        origin_diff = times[Y] - times[X]
        diff = events[i+Y,0] - events[i+X,0]
        diff2origin = origin_diff - diff
        print('idx',i, ": events", events[i+X,2], '&', events[i+Y,2], 'difference to standard:', diff2origin, 'difference', diff)
        
"""
Those trials where the 1 is missing is where the differnce between audio onset and callSign onset is larger than +/- 30 samples (14ms) compared to what it should be (origin_diff)
"""
            
#%%    
# # EEG.plot(events=events)              
# # EEG.load_data()
# # EEG.add_events(events, 'Status')

# #%%
# # picks = mne.pick_types(EEG.info, meg=False, eeg=True, stim=False, eog=True)
# # tmin, tmax = -0.5, 0.5
# event_ids = {str(i) : i for i in set(events[:,2])}
# # epochs = mne.Epochs(EEG, events, event_ids, tmin, tmax, picks=picks)
