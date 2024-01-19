# -*- coding: utf-8 -*-
"""
RUNNER SCRIPT FOR THE MVPA AND CROSS-VALIDATION
===============================================================================
@author: sameumu
Created on Tue Jan 16 16:07:49 2024


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
        
prediction : str
    The variable we are interested in. 
    Example : prediction = 'accuracy' will do the cross-validation on how well 
        the frequency power encodes whether the response was accurate or not

"""
conditionInclude = ['Lv3'] 
conditionExculde = None
prediction = 'accuracy'

#%% filepaths 
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                        const.taskID,'features',subjID)
pickle_path_in = os.path.join(dirinput, subjID + const.inputPickleFileEnd)
pickle_path_out = os.path.join(dirinput, subjID + const.outputPickleFileEnd)

#%% Unpickle the dict
with open(pickle_path_in, 'rb') as f:
    tfr_bands = pickle.load(f)
    
#%% Filter conditions
idx = list(MVPAManager.getFilteredIdx(
    tfr_bands['all_epoch_conditions'], conditionInclude=conditionInclude, conditionExclude=conditionExculde))

#%% Get crossvalidation scores
y = tfr_bands['metadata'][prediction][idx] # What variable we want to predict

for thisBand in const.freqbands:
    
    X=tfr_bands[str(thisBand +'_data')][idx,:,:]
    
    all_scores_full, scores, std_scores = MVPAManager.get_crossval_scores(X = X, y = y)
    tfr_bands[thisBand+'_crossval_FullEpoch'] = all_scores_full['test_score']
    tfr_bands[thisBand+'_crossval_timewise_mean'] = scores
    tfr_bands[thisBand+'_crossval_timewise_std'] = std_scores
# TODO - Hm. all [band]_crossval_fullepoch  are the same value. Check if there's an error somewhere
# Not anymore (as of 18.01.24) even though I didn't change anything but the filtering. Best to pay attention.

with open(pickle_path_out, 'wb') as f:
    pickle.dump(tfr_bands, f)
print("pickling the dictionary")