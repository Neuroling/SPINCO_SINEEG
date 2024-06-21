#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHECKING FOR MISSING TRIGGER 1, CHECKING TIME BETWEEN TRIGGERS
==============================================================
Created on Tue Jun  4 11:39:09 2024
@author: samuemu

- first loads the raw data
- extracts events from last channel
- corrects event codes above 256
- checks and reports in which trials trigger code 1 is missing
- summarises how many samples are between trigger code 1 and the following audio onset trigger
- reports the difference in samples between two audio trigger codes and the standardised time taken from the excel
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
subjID = 's006'

# PATHS
thisDir = os.getcwd()
# subIDs= [item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','sourcedata')) if item[-3] == '2']

eeg_fp = glob(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','sourcedata', subjID, '*.bdf'))[0]
csv_fp = [item for item in glob(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','sourcedata', subjID, '*.csv')) if item[-5].isdigit()][0]

print('>>>  Reading subject', subjID, ' <<<')


#%% read csv
df = pd.read_csv(csv_fp)

#%% Reading EEG data and getting events
EEG = mne.io.read_raw_bdf(eeg_fp, eog = ['EXG3', 'EXG4', 'EXG5', 'EXG6'], misc = ['EXG1', 'EXG2', 'erg1'])
events = mne.find_events(EEG, 'Status')

#%% Recoding event triggers to correct bit-overflow

"""
Recoding event triggers to correct bit-overflow
===========================================================================
Because event triggers are stored as a single bit, numbers above 256 overflow 
back to 1. I forgot that. Now, triggers 300-339 (which we use for clear trials) 
are coded as 44-83. This means that triggers 55 (end of instruction screen) 
and 60 (end of block) are now the same as the codes that originally were 311 and 316

This loop recodes triggers that should be 300-339 by adding +256 to 
the triggers between 44 and 83. For codes 55 and 60, it will only recode
them to 311 and 316 if they were immediately preceded by code 300.
Since 311 and 316 refer to onset of callSign (token_1_tmin), they always 
have to follow 300, which refers to audio onset (firstSound_tmin)
"""

for i in range(len(events)):
    if events[i,2] <= 83 and events[i,2]>= 44:
        if (events[i,2] == 55 and events[i-1,2] == 300) or events[i,2] != 55 :
            if (events[i,2] == 60 and events[i-1,2] == 300) or events[i,2] != 60  :
                events[i,2] = events[i,2] + 256
                
idx_firstSound_tmin = [i for i in range(len(events)) if events[i,2] == 100 or events[i,2] == 200 or events[i,2] == 300]

#%% Check in which trials the trigger code 1 is missing.
print(' ')
print('=========================================================================')
print("--> Checking for missing trigger 1")
for i, idx in enumerate(idx_firstSound_tmin):
    if events[idx-1,2] != 1:
        print('missing in trial',i,'index',idx, '- preceding event', events[idx-1,2])
        

#%% check how much difference (in samples) there is between the audio onset triggers and trigger code 1
print(' ')
print('=========================================================================')
print("--> Summary of samples between trigger code 1 and audio onset trigger")
diff_1_onset = [events[i,0] - events[i-1,0] for i in idx_firstSound_tmin if events[i-1,2] == 1]
print('mean:', np.mean(diff_1_onset))
print('std :', np.std(diff_1_onset))
print('min :', np.min(diff_1_onset))
print('max :', np.max(diff_1_onset))

plt.figure()
sns.violinplot(diff_1_onset, orient = 'h')
plt.show()
plt.close()


#%%
firstSound_tmin = df['firstSound_tmin'][4:-1]
diff_1_onset_csv = pd.Series([i/2048 for i in diff_1_onset])
diff_1_onset_csv = firstSound_tmin - diff_1_onset_csv


plt.figure()
sns.violinplot(diff_1_onset_csv, orient = 'h', color = '#C5CAE9', linewidth= 0)         
sns.stripplot(diff_1_onset_csv, orient = 'h',linewidth=0.5, size = 3, color = '#303F9F', jitter = 0.2)
plt.title(('deviation of time between trigger 1 and audio onset in seconds, '+subjID))    
plt.show()
plt.close()

"""
Using the code from [datachecks_eventcodes.py](url), I looked at the time between trigger code 1 and the first word onset trigger (100, 200) in the first experiment. If trigger code 1 were reliable as a trigger for the audio onset (and therefore the click), then it should always be exactly 0.1571, 0.1671 or 0.1771 seconds before trigger 100 or 200. 
"""

#%% Check how large the difference between two triggers are compared to what they should be (excel file)
print(' ')
print('=========================================================================')
print("--> Checking how many samples are between two triggers, compared to the times in the excel sheet")

# This is the onset and offset times of the audio triggers from the excel in seconds
times = [0.1638541, # idx 0 : firstSound_tmin
         0.7022916, # idx 1 : token_1_tmin
         1.2563333, # idx 2 : token_1_tmax 
         2.3682708, # idx 3 : token_2_tmin
         2.7699375, # idx 4 : token_2_tmax
         3.9993125, # idx 5 : token_3_tmin
         4.470875   # idx 6 : lastSound_tmax (is equal to token_3_tmax)
         ]

times = [int(i *2048) for i in times] # transform to samples

# firstSound_tmin, token_1_tmin, token_1_tmax, token_2_tmin, token_2_tmax, token_3_tmin, lastSound_tmax
# Compare difference of firstEvent and secondEvent. These are the indexes of the list commented one line above.
firstEvent = 0
secondEvent = 1

excel_diff = times[secondEvent] - times[firstEvent]

# print only if the difference between the excel and the triggers is outside of +/- `print_if_diff_larger_than`
print_if_diff_larger_than = 20
print('--> Only reporting if the difference between the excel times and the events is outside +/-', print_if_diff_larger_than, 'samples')


diff = [events[i+secondEvent,0] - events[i+firstEvent,0] for i in idx_firstSound_tmin ]
diff2excel = [excel_diff - i for i in diff]
   
for i, idx in enumerate(idx_firstSound_tmin):
        if max([diff2excel[i], -diff2excel[i]]) >= print_if_diff_larger_than:
            # max([num, -num]) will always return a positive number
            
            print('trial',i,'idx',idx, "; events", events[idx+firstEvent,2], '&', events[idx+secondEvent,2], '; difference between events', diff[i], '; difference to excel:', diff2excel[i])
        
"""
Those trials where the 1 is missing is where the difference between audio onset and callSign onset is larger than +/- 30 samples (14ms) compared to what it should be (excel_diff)
"""

plt.figure()
sns.violinplot(diff2excel, orient = 'h', color = '#C5CAE9', linewidth= 0)         
sns.stripplot(diff2excel, orient = 'h',linewidth=0.5, size = 3, color = '#303F9F', jitter = 0.2)    
plt.show()
plt.close()

#%% check the difference between recorded trigger 1 and audio onset trigger
# Technically: (first word onset - click timing) - (recorded first word onset trigger - recorded trigger 1)
# But the click timing should be at 0, so we don't have that in there.
check = (df['firstSound_tmin']) -  (df['pp_t0_start.started'] - df['pp_start.started'])
plt.figure()
sns.stripplot(check, orient = 'h',linewidth=0.5, size = 3, color = '#303F9F')
sns.violinplot(check, orient = 'h', color = '#C5CAE9', linewidth= 0)
plt.show()
plt.close()

"""
The trials where trigger 1 is missing in the EEG are the ones that differ exactly 0.16384 - meaning the trigger code 1 and first sound trigger are sent at the same time
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

#%% check time between when trigger 1 is sent and when the sound file starts
check = df['pp_start.started']- df['sound_1.started']
plt.figure()
sns.stripplot(check, orient = 'h',linewidth=0.5, size = 3, color = '#303F9F')
sns.violinplot(check, orient = 'h', color = '#C5CAE9', linewidth= 0)
plt.show()
plt.close()

#%%
check = df['pp_t0_start.started'] - df['sound_1.started']
plt.figure()
sns.stripplot(check, orient = 'h',linewidth=0.5, size = 3, color = '#303F9F')
sns.violinplot(check, orient = 'h', color = '#C5CAE9', linewidth= 0)
plt.show()
plt.close()

#%%
check = (df['firstSound_tmin']) -  (df['pp_t0_start.started'] - df['pp_start.started'])
plt.figure()
sns.stripplot(check, orient = 'h',linewidth=0.5, size = 3, color = '#303F9F')
sns.violinplot(check, orient = 'h', color = '#C5CAE9', linewidth= 0)
plt.show()
plt.close()

#%%
check = (df['token_1_tmin'] - df['firstSound_tmin']) - (df['pp_t1_start.started'] - df['pp_t0_start.started'])
plt.figure()
sns.stripplot(check, orient = 'h',linewidth=0.5, size = 3, color = '#303F9F')
sns.violinplot(check, orient = 'h', color = '#C5CAE9', linewidth= 0)
plt.show()
plt.close()

#%%
check = (df['token_1_tmax'] - df['token_1_tmin']) - (df['pp_t1_end.started'] - df['pp_t1_start.started'])
plt.figure()
sns.stripplot(check, orient = 'h',linewidth=0.5, size = 3, color = '#303F9F')
sns.violinplot(check, orient = 'h', color = '#C5CAE9', linewidth= 0)
plt.show()
plt.close()
