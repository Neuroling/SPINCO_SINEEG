# -*- coding: utf-8 -*-
"""
IMPORT EPOCHS INTO MNE, RELABEL EVENTS, GROUP-SUMMARY OF EVENT FREQUENCIES
===============================================================================
Created on Fri Nov 10 14:59:24 2023
@author: samuemu

This script reads eeglab epochs and handles them with MNE

It takes the constants, such as subject ID, from EPO_constants,
and the functions from EPO_functions

"""


import os
# from glob import glob
# import scipy.io as sio
thisDir = os.getcwd()
# import numpy as np
# import mne 
# import pandas as pd
import EPO_functions as functions
import EPO_constants as const

CreateFreqTable = False

#%% ============== EEGLAB .set TO MNE .fif =============================================================================
# Looping over subj, will read epoched .set files, add metadata, and then save them to .fif files

for subjID in const.subjIDs:
    EpoManager = functions.EpochManager(subjID)
    EpoManager.set2fif()
    
#%% ============== CREATE EVENT FREQUENCY TABLE ========================================================================
if CreateFreqTable == True:
    # Will create a frequency of occurrence table for the event_ids
    frequencyTable = const.freqTableEmpty
    for subjID in const.subjIDs:
        EpoManager = functions.EpochManager(subjID)
        df=EpoManager.countEventFrequency()
        frequencyTable[subjID] = df['frequency']
    frequencyTable.to_csv(EpoManager.freqTable_path)
    print("saved frequency table to" + EpoManager.freqTable_path)
