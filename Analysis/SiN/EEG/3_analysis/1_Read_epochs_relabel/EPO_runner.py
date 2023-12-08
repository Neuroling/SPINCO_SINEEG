# -*- coding: utf-8 -*-
"""
This script is for handling all the epoching with MNE

It takes the constants, such as subject ID, from EPO_constants,
and the functions from EPO_helper


Created on Fri Nov 10 14:59:24 2023

@author: samuemu
"""


import os
# from glob import glob
# import scipy.io as sio
thisDir = os.getcwd()
# import numpy as np
# import mne 
# import pandas as pd
import EPO_helper as helper
import EPO_constants as const

#%% ============== EEGLAB .set TO MNE .fif =============================================================================
# Looping over subj, will read epoched .set files, add metadata, and then save them to .fif files

for subjID in const.subjIDs:
    EpoManager = helper.EpochManager(subjID)
    EpoManager.set2fif(addMetadata=True,relabelEvents=True)

# To do: average reference epochs. Put in a note saying "average reference was done after interpolating channels"
    
#%% ============== CREATE EVENT FREQUENCY TABLE ========================================================================
# Will create a frequency of occurrence table for the event_ids - NOT SAVED
frequencyTable = const.freqTableEmpty
for subjID in const.subjIDs:
    EpoManager = helper.EpochManager(subjID)
    df=EpoManager.countEventFrequency()
    frequencyTable[subjID] = df['frequency']

    
