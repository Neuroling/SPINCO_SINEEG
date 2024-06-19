#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 06:55:14 2024
@author: Samuemu

This script is (/should be) a python-alternative to the matlab script `Import_01_importBDF_loadLocs_split.m`
Therefore, it will:
    - Import the bdf file
    - load channel locations
    - align triggers (actually we cannot do that for experiment 2, see github issue #7) #TODO
    - split resting state and task files # TODO
    - copy behavioural data file into rawdata folder # TODO
    - save accuracy tsv files # TODO
    
steps marked with TODO are a work in progress

---

Actually, this script is not used anymore, because it was simpler to just use the matlab script.
Still, I'm keeping it here for future reference
"""


import mne
from glob import glob
import os 
import pandas as pd 
# import seaborn as sns
# import matplotlib.pyplot as plt
import numpy as np

#%% User inputs
taskID = 'task-sin'
debug = False # If true, will only run one subject

#%% PATHS
_thisDir = os.getcwd()
_baseDir = os.path.join(_thisDir[:_thisDir.find('Scripts')] + 'Data','SiN')


subjIDs= [item for item in os.listdir(os.path.join(_thisDir[:_thisDir.find('Scripts')] + 'Data','SiN','sourcedata')) if item[-3] == '2']

#%% Get channel locations from file, import as MNE montage object, remove spaces from channel names
chanLocsFile = glob(os.path.join(_baseDir,'_acquisition','_electrodes','Biosemi_71ch_EEGlab_xyz.tsv'))[0]
chanLocs = mne.channels.read_custom_montage(chanLocsFile, head_size = None)
chanLocs.ch_names = [i.replace(' ', '') for i in chanLocs.ch_names]

#%%
for subjID in subjIDs:
    
    ## set paths
    dirinput = os.path.join(_baseDir,'sourcedata', subjID)
    diroutput = os.path.join(_baseDir,'rawdata', subjID, taskID)
    
    eeg_fp = glob(os.path.join(dirinput, '*.bdf'))[0]
    beh_csv_fp = [item for item in glob(os.path.join(dirinput, '*.csv')) if item[-5].isdigit()][0]
    events_fp = os.path.join(diroutput, 'eeg', subjID +  '_' + taskID + '_events.tsv')
    
    print('--> Reading subject', subjID, 'from file', eeg_fp)    
    
    #%% Opening the EEG
    rawEEG = mne.io.read_raw_bdf(eeg_fp, 
                                 eog = ['EXG3', 'EXG4', 'EXG5', 'EXG6'], 
                                 misc = ['EXG1', 'EXG2', 'erg1'], 
                                 exclude = ['EXG7', 'EXG8'])
    
    ## Get channel montage, save as tsv file
    rawEEG.set_montage(chanLocs)
    # TODO save as tsv file
    
    #%% Get events
    events = mne.find_events(rawEEG, 'Status')
    
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
    
    #%% save events as tsv file (for later import into mne)
    events_df = pd.DataFrame(events)
    events_df.to_csv(events_fp, sep='\t', index=False)
    
    #%% save events with accuracy
    events_df.columns = pd.Index(['SAMPLES', 'DURATION', 'VALUE'])
    
    beh_df = pd.read_csv(beh_csv_fp)
    
    #%%
    beh_df = beh_df[['callSign', 'colour', 'number', 'trigger_start','trigger_end',
                    'trigger_call','trigger_col','trigger_num','trigger_call_end','trigger_col_end','trigger_num_end',
                    'mouseClickOnCall.clicked_name', 'mouseClickOnColour.clicked_name', 'mouseClickOnNumber.clicked_name',
                    'callSignCorrect','colourCorrect','numberCorrect']]
    
    #% ensure 'correct' columns are read as text (it will read boolean if they are only True or False and have no NO_ANSW)
    beh_df[['callSignCorrect','colourCorrect','numberCorrect']] = beh_df[['callSignCorrect','colourCorrect','numberCorrect']].astype(str)
            
    # %% Recode to numerico to compute summary descriptives 
    beh_df['callSignCorrect'] = pd.to_numeric(beh_df['callSignCorrect'].map({'TRUE': 1, 'FALSE': 0, "NO_ANSW":''}))
    beh_df['colourCorrect'] =  pd.to_numeric(beh_df['colourCorrect'].map({'TRUE': 1, 'FALSE': 0, "NO_ANSW": ''}))
    beh_df['numberCorrect'] =  pd.to_numeric(beh_df['numberCorrect'].map({'TRUE': 1, 'FALSE': 0, "NO_ANSW": ''}))
    
    #%%
    # for trial in list(events_df['VALUE'])
    
    # for event in list(events_df['VALUE']):
    #     event = str(event)
    #     if len(event) == 3 and event[2] != '0' and event[1:3] != '01':
            
    
    # tsv_file_path = os.path.join(diroutput,subjID +  '_' + taskID + '_events.tsv')
    
    #%%
    if debug : break
