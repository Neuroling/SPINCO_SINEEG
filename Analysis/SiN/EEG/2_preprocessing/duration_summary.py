# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 15:05:37 2023
Script to create a .csv file with recording durations of all subjects

- Reads the duration and sampling rate from the json file of each subject
- Reads the number of events/triggers and the number of samples (= time frame 
    of the last trigger, which is the end of block 4) 
    from the s0NN_task-sin_events_accu.tsv file of each subject
- Divides the number of samples (from the tsv file) by the sampling frequency (from the json file)
    to receive recording duration in seconds (allows comparison to json file)
- Saves to csv file

@author: samuemu
"""

import os 
import pandas as pd 
import json

#%% User inputs
taskID = 'task-sin'
save = 1 # if = 1 it will save csv file

#%% PATHS
thisDir = os.path.dirname(os.path.abspath(__file__))
diroutput= os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')
## below: Don't save subjIDs of the pilots or discarded subj
subIDs= [item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]

#%% Create empty lists
filepaths_json = list()
durations_json = list()
filepaths_tsv  = list()
durations_tsv  = list()
samples_tsv   =  list()
n_events_tsv  =  list()

#%% loop over all subj: first read json files and append duration to list, then do the same for tsv files
for subID in subIDs:   
    dirinput=os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subID,taskID, 'eeg')
    rawdata = os.listdir(dirinput)
    
    ## open json files, read duration, append it to list
    for file in rawdata:
        if file.endswith("eeg.json") and file[3].isdigit():
            # If the file is a json file, get its filepath
            fp = os.path.join(dirinput, file)
            filepaths_json.append(fp)
            with open(fp, 'r') as f:
                data = json.load(f)
            durations_json.append(data['RecordingDurationSec'])
            SamplingFrequencyHz= data['SamplingFrequencyHz']
    
    ## open tsv files, read duration, divide duration by sampling frequency, append to list
    dirinput=os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives_SM',taskID,subID)
    rawdata = os.listdir(dirinput)
    for file in rawdata:
        if file.endswith("accu.tsv") and file[3].isdigit():
            # If the file is a tsv file, get its filepath
            fp = os.path.join(dirinput, file)
            filepaths_tsv.append(fp)
            data_tsv = pd.read_csv(fp,sep='\t')
            temp = data_tsv.iloc[-1:]['SAMPLES'] # Read n of samples (last row)
            samples = int(temp.iloc[0]) # Get value as int instead of pd series
            samples_tsv.append(samples)
            durations_tsv.append(samples/SamplingFrequencyHz)
            n_events_tsv.append(len(data_tsv))
            
#%% Create dataframe from the lists
df = pd.DataFrame(list(zip(subIDs, durations_json, filepaths_json, 
                           durations_tsv, samples_tsv, n_events_tsv, filepaths_tsv)), 
                  columns =['subjID', 'duration_json', 'filepath_json', 
                            'duration_tsv', 'n_samples_tsv', 'n_events_tsv',
                            'filepath_tsv'])

#%% save dataframe
if save == 1:
    df.to_csv(diroutput+'\\'+'recording_durations.csv')
    print('saved to '+diroutput+'\\'+'recording_durations.csv')
