#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test/writing Script for the MVPA
===============================================================================
author: samuemu
Created on Fri Jan 12 13:24:52 2024



"""
import os
import pickle
thisDir = os.path.dirname(__file__)

import MVPA_constants as const
import MVPA_functions as functions

#%% filepaths 
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                        const.taskID,'features',subjID)
pickle_path = os.path.join(dirinput, subjID + const.pickleFileEnd)

#%% Unpickle the dict
with open(pickle_path, 'rb') as f:
    tfr_bands = pickle.load(f)
    
#%% filter the dict for conditions before doing the crossvalidation
""" Notes: How to filter the dict [17.01.23]

probably best to do a function like 
 def filterConditions(self, accuracy=none, block=none, stimType=none, etc)
where each condition can be specified, and the default for each is None (= not filtered)
And that function will then filter the data to the speficied filters,
using either the metadata, event-codes or event-labels

But then, how do I actually apply that to the data, which is a different entry in the dict?

Idea 1:
    Add another dimension to the data. 
    Right now it is (n_samples * n_epochs * n_electrodes)
    I could make it into (n_samples * n_epochs * n_electrodes * n_freqbands)
    And then first filter the data by getting the idx of the epochs of the conditions we want
    from the metadata, and removing all data in [n_epochs] that are not these idxs
    Then, do a loop: for each freqband, reduce dimensionality by removing all other freqbands,
    and then do the crossvalidation
    
Idea 2: 
    Change the names of the epoch-columns/rows to the event-label. Then, use this to filter
    I'd need to change the name for every freqband in the dict (do this in the featureExtraction script)
    ... unless I do it in conjunction with Idea 1. In the feature extraction script, 
    increase the dimensionality, relabel epochs, then pickle. 
    
Considerations:
    - It might be hard to think about and grasp 4-dimensional data, making it hard for any 
    3rd party to follow the logic of the code
    - What is more error-prone: relabelling the columns/rows, or first getting the idx and then filtering?
    - What is less resource-heavy?

Hm. Let's throw some spaghetti at the wall and see what sticks.

"""
    

# #%% Get crossvalidation scores
# y = epo.metadata['accuracy'] # What variable we want to predict

# for thisBand in const.freqbands:
#     all_scores_full, scores, std_scores = TFRManager.get_crossval_scores(X=tfr_bands[thisBand], y = y)
#     tfr_bands[thisBand+'_crossval_FullEpoch'] = all_scores_full
#     tfr_bands[thisBand+'_crossval_timewise_mean'] = scores
#     tfr_bands[thisBand+'_crossval_timewise_std'] = std_scores
# # TODO - Hm. all [band]_timewise_mean and all [band]_timewise_std are the same value. Check if there's an error somewhere
