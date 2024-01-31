# -*- coding: utf-8 -*-
"""
RUNNER SCRIPT FOR THE MVPA AND CROSS-VALIDATION
===============================================================================
@author: sameumu
Created on Tue Jan 16 16:07:49 2024


This script runs the MVPA and crossvalidation.
Functions are called from MVPA_functions.
Constants such as filepath-endings and frequency bands are called from MVPA_constants.
Conditions can be filtered using the User Inputs.


Prerequisites:
    - The dicts created by the Feature Extraction scripts
    - The MVPA_constants.py script
    - The MVPA_functions.py script
    
TO DO:
    - Check if the output is correct
    - Loop over subjects

"""

import os
import pickle
thisDir = os.path.dirname(__file__)

import MVPA_constants as const
import MVPA_functions as functions

MVPAManager = functions.MVPAManager()

#%% 
""" USER INPUTS
===============================================================================

conditionInclude : list of str or None
    Only trials in these conditions will be included.
    Example : conditionInclude = ['Lv3'] will perform the analysis only on 
        trials with degradation Lv3
    
conditionExclude : list of str or None
    All trials in these conditions will be excluded.
    Example : conditionExclude = ['Call'] will perform the analysis only on
        trials with StimulusType Col or Num
        
prediction : str --- must be a column name from tfr_bands['epoch_metadata']
    The variable we are interested in. 
    Options : accuracy, block, stimtype, stimulus, levels, voice
    Example : prediction = 'accuracy' will do the cross-validation on how well 
        the frequency power encodes whether the response was correct or not
    

"""
conditionInclude = ['Lv3'] 
conditionExculde = ['Call']
prediction = 'accuracy'

#%% setting filepaths 
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                        const.taskID,'features',subjID)
pickle_path_in = os.path.join(dirinput, subjID + const.inputPickleFileEnd)
pickle_path_out = os.path.join(dirinput, subjID + const.outputPickleFileEnd)

#%% Open the dict 
print('opening dict:',pickle_path_in)
with open(pickle_path_in, 'rb') as f:
    tfr_bands = pickle.load(f)
    
# #%% Filter conditions using the user inputs
# idx = list(MVPAManager.getFilteredIdx(
#     tfr_bands['epoch_conditions'], conditionInclude=conditionInclude, conditionExclude=conditionExculde))

# #%% Get crossvalidation scores
# y = tfr_bands['metadata'][prediction][idx] # What variable we want to predict (set in the user inputs)

# for thisBand in const.freqbands: # loop over all frequency bands
#     print('--> now performing crossvalidation for', thisBand)
#     X=tfr_bands[str(thisBand +'_data')][idx,:,:] # Get only the trials that are in the specified conditions (user inputs)
    
#     all_scores_full, scores, std_scores = MVPAManager.get_crossval_scores(X = X, y = y) # Get scores and add to the dict
#     tfr_bands[thisBand+'_crossval_FullEpoch'] = all_scores_full['test_score']
#     tfr_bands[thisBand+'_crossval_timewise_mean'] = scores
#     tfr_bands[thisBand+'_crossval_timewise_std'] = std_scores
# # TODO - Hm. all [band]_crossval_fullepoch  are the same value. Check if there's an error somewhere
# # Not anymore (as of 18.01.24) even though I didn't change anything but the filtering. Best to pay attention.

# # #%% Saving the dict
# # print("pickling the dictionary to: /n"+pickle_path_out)
# # with open(pickle_path_out, 'wb') as f:
# #     pickle.dump(tfr_bands, f)
