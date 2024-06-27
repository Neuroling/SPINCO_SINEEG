# -*- coding: utf-8 -*-
"""
IMPORT EPOCHS INTO MNE, RELABEL EVENTS, GROUP-SUMMARY OF EVENT FREQUENCIES
===============================================================================
Created on Fri Nov 10 14:59:24 2023
@author: samuelmull

This script reads eeglab epochs and handles them with MNE

It takes the constants, such as subject ID, from EPO_constants.

From EPO_functions, it initialises the EpochManager class. EpochManager is a 
collection of functions, which aggregate data as they are called.


USER INPUTS:
CreateFreqTable : bool
    If a table with the frequency of occurrence of each event_id should be created or not.
    
ExpID : str
    Determines which data is processed and which constants script is imported
    Options:
        'exp1': data from ./derivatives/pipeline-01/
        'SM'  : data from ./derivatives_SM/
        'exp2': data from ./derivatives_exp2-unalignedTriggers/pipeline-automagic-01-unalignedTriggers/

"""
CreateFreqTable = False
ExpID = 'exp2' 

import os
thisDir = os.getcwd()
import EPO_functions as functions


if ExpID == 'exp1' or ExpID == 'SM':
    import EPO_constants_exp1 as const
elif ExpID == 'exp2':
    import EPO_constants_exp2 as const
else:
    raise ValueError('Experiment ID not recognised. It must bei either `exp1` , `SM` or `exp2` ')

#%% ============== EEGLAB .set TO MNE .fif =============================================================================
# Looping over subj, will read epoched .set files, add metadata, and then save them to .fif files

for subjID in const.subjIDs:
    EpoManager = functions.EpochManager(subjID, ExpID )
    EpoManager.set2fif()
    
#%% ============== CREATE EVENT FREQUENCY TABLE ========================================================================
if CreateFreqTable == True:
    # Will create a frequency of occurrence table for the event_ids
    frequencyTable = const.freqTableEmpty
    for subjID in const.subjIDs:
        EpoManager = functions.EpochManager(subjID, ExpID)
        df=EpoManager.countEventFrequency()
        frequencyTable[subjID] = df['frequency']
    frequencyTable.to_csv(EpoManager.freqTable_path)
    print("saved frequency table to" + EpoManager.freqTable_path)
