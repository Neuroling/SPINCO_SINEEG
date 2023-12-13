#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:23:55 2023

@author: samuemu
"""

import os
from glob import glob
import pandas as pd

taskID = 'task-sin'
pipeID = 'pipeline-01'
fifFileEnd = '-epo.fif'
setFileEnd = '_epoched_2.set'

excludeElectrodes = ['Cz'] # Cz is the reference, so it is all 0
includedElectrodes = ['Fp1', 'AF7', 'AF3', 'F1', 'F3', 'F5', 'F7', 'FT7', 'FC5',
                      'FC3', 'FC1', 'C1', 'C3', 'C5', 'T7', 'TP7', 'CP5', 'CP3',
                      'CP1', 'P1', 'P3', 'P5', 'P7', 'P9', 'PO7', 'PO3', 'O1', 'Iz',
                      'Oz', 'POz', 'Pz', 'CPz', 'Fpz', 'Fp2', 'AF8', 'AF4', 'Afz',
                      'Fz', 'F2', 'F4', 'F6', 'F8', 'FT8', 'FC6', 'FC4', 'FC2', 'FCz',
                      'C2', 'C4', 'C6', 'T8', 'TP8', 'CP6', 'CP4', 'CP2', 'P2',
                      'P4', 'P6', 'P8', 'P10', 'PO8', 'PO4', 'O2']
# TEMPORARY!!! Either do a less error-prone approach, or do the average reference,
# so Cz doesn't need to be excluded
# You get the above list by copying epo.info.ch_names and manually removing channels

epo_duration= [-0.5, 0.49609375] # time window of the epoch (first and last idx of epo.times)


thisDir = os.getcwd()
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]


"""
These are the event labels:
    NoiseType / StimulusType / DegradationLevel / Accuracy / Voice
    
    X_____ NoiseType: NV = 1, SSN = 2
    _X____ Stimulus Type: Call = 1, Colour = 2, Number = 3
    __X___ Stimulus: Adler/Gelb/Eins = 1, Drossel/Grün/Zwei = 2, Kröte/Rot/Drei = 3, Tiger/Weiss/Vier = 4
    ___X__ Degradation Level: Lv1 = 1, Lv2 = 2, Lv3 = 3
    ____X_ Accuracy: Incorrect = 0, Correct = 1
    _____X Voice: Feminine (Neural2-F) = 1, Masculine (Neural2-D) = 2
    
This allows you to filter the epochs using the event labels, i.e. by:
    epochs.__getitem__('NV') --------> will return all epochs with NV
    epochs.__getitem__('Lv1/Call') --> will return all epochs with Lv1 degradation and CallSign
or even just by:
    epochs['Lv1/Call']
    
"""
NoiseType = {'NV':1, 'SSN':2}
StimulusType = {'Call':1, 'Col':2,'Num':3}
Stimulus = {'Stim1':1, 'Stim2':2, 'Stim3':3, 'Stim4':4}
Degradation = {'Lv1':1, 'Lv2':2, 'Lv3':3}
Accuracy = {'Inc':0, 'Cor':1}
Voice = {'F':1, 'M':2}
event_id = {}

for noise_key, noise_value in NoiseType.items():
    for stimulus_type_key, stimulus_type_value in StimulusType.items():
        for stimulus_key, stimulus_value in Stimulus.items():
            for degradation_key, degradation_value in Degradation.items():
                for accuracy_key, accuracy_value in Accuracy.items():
                    for voice_key, voice_value in Voice.items():
                        # Create the combined key using a backslash as a separator
                        combined_key = f"{noise_key}/{stimulus_type_key}/{stimulus_key}/{degradation_key}/{accuracy_key}/{voice_key}"

                        # Create a six-number sequence of the corresponding values
                        combined_value = (noise_value*100000+ stimulus_type_value*10000+ stimulus_value*1000+ degradation_value*100+ accuracy_value*10+ voice_value)

                        # Add the key-value pair to the combined dictionary
                        event_id[combined_key] = combined_value
