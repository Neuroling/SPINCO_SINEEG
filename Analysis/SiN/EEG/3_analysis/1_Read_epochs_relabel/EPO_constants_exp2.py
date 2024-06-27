#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTANTS FOR EPO SCRIPTS (Experiment2)
===============================================================================
@author: samuelmull
Created on 26.06.2024

This script contains constants: variables that are used across functions and scripts, 
such as filepath-chunks, subject_IDs, and event_ids

These variables are called by EPO_functions and EPO_runner

since experiment 1 and experiment 2 have slightly different constants, there is 
a constants-script for each. This is the script for experiment 2

"""

import os

import pandas as pd

#%% filepath chunks
taskID = 'task-sin'

pipeID = 'pipeline-automagic-01-unalignedTriggers'

derivativesFolder = 'derivatives_exp2-unalignedTriggers'

setFileEnd = '_avgRef_epo.set'

fifFileEnd = '_avgRef_epo.fif'

freqTableEnd = 'event_group_frequencies.csv'

#%% get list of subjectIDs

thisDir = os.getcwd()
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN', derivativesFolder, pipeID, taskID + '_preproc_epoched')) if item[-1].isdigit()]


#%%
"""
CREATE EVENT IDs AND EVENT LABELS

These are the event labels:
    NoiseType / StimulusType /  Accuracy 
    
    X___ NoiseType: NV = 1, SSN = 2, clear = 3
    _X__ Stimulus Type: Call = 1, Colour = 2, Number = 3
    __X_ Stimulus: 'Stim1', 'Stim2', 'Stim3', 'Stim4', 'Stim5', 'Stim6', 'Stim7', 'Stim8'
    ___X Accuracy: Incorrect = 0, Correct = 1

Where the Stim* stands for the following:
| | CallSign | Colour | Number |
| Stim1 | Adler | gelb | eins |
| Stim2 | Eule | gruen | zwei |
| Stim3 | Ratte | rot | drei|
| Stim4 | Tiger | weiss | vier|
| Stim5 | Velo | blau | fuenf|
| Stim6 | Auto | braun | sechs|
| Stim7 | Messer | pink | neun|
| Stim8 | Gabel | schwarz | null|

    
This allows you to filter the epochs using the event labels, i.e. by:
    epochs.__getitem__('NV') --------> will return all epochs with NV
    epochs['NV'] --------------------> will return all epochs with NV

    
    
"""
NoiseType = {'NV':1, 'SSN':2, 'clear':3}
StimulusType = {'Call':1, 'Col':2,'Num':3}
Stimulus = {'Stim1':1, 'Stim2':2, 'Stim3':3, 'Stim4':4, 'Stim5':5, 'Stim6':6, 'Stim7':7, 'Stim8':8}
Accuracy = {'Inc':0, 'Cor':1}
event_id = {}

for noise_key, noise_value in NoiseType.items():
    for stimulus_type_key, stimulus_type_value in StimulusType.items():
        for stimulus_key, stimulus_value in Stimulus.items():
            for accuracy_key, accuracy_value in Accuracy.items():
                # Create the combined key using a backslash as a separator
                combined_key = f"{noise_key}/{stimulus_type_key}/{stimulus_key}/{accuracy_key}"

                # Create a six-number sequence of the corresponding values
                combined_value = (noise_value*1000+ stimulus_type_value*100+ stimulus_value*10+ accuracy_value)

                # Add the key-value pair to the combined dictionary
                event_id[combined_key] = combined_value

#%% Creating an empty frequency of occurrence table
all_event_ids = list(event_id.values())
all_event_labels = list(event_id.keys())
freqTableEmpty = pd.DataFrame([all_event_labels,all_event_ids],index=['events','event_codes']).T

freqCountEmpty = dict()
for i in range(len(all_event_ids)):
    freqCountEmpty[all_event_ids[i]] = 0
