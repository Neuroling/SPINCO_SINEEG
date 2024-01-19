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
# import MVPA_functions as functions

#%% filepaths 
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                        const.taskID,'features',subjID)
pickle_path = os.path.join(dirinput, subjID + const.pickleFileEnd)

#%% Unpickle the dict
with open(pickle_path, 'rb') as f:
    tfr_bands = pickle.load(f)

#%% ===========================================================================

#%% filter the dict for conditions before doing the crossvalidation
""" Notes: How to filter the dict [17.01.23]

probably best to do a function like 
 def filterConditions(self, accuracy=none, block=none, stimType=none, etc)
where each condition can be specified, and the default for each is None (= not filtered)
And that function will then filter the data to the speficied filters,
using either the metadata, event-codes or event-labels

But then, how do I actually apply that to the data, which is a different entry in the dict?

like this:
    # idx = filtered epoch indexes (from the function described above)
    # filtered dataset = tfr_bands['*_data'][idx,:,:]
        

Idea:
    Add another dimension to the data. 
    Right now it is (n_samples * n_epochs * n_electrodes)
    I could make it into (n_samples * n_epochs * n_electrodes * n_freqbands)
    And then first filter the data by getting the idx of the epochs of the conditions we want
    from the metadata, and removing all data in [n_epochs] that are not these idxs
    Then, do a loop: for each freqband, reduce dimensionality by removing all other freqbands,
    and then do the crossvalidation
    

Considerations:
    - It might be hard to think about and grasp 4-dimensional data, making it hard for any 
    3rd party to follow the logic of the code
    - What is more error-prone: filtering for each band or across the 4-dimensional array?
    - What is less resource-heavy?

Hm. Let's throw some spaghetti at the wall and see what sticks.

"""

# First let's get the lists out of the dict so I don't have to type the whole thing every time
event_label = tfr_bands['all_epoch_conditions']
event_id = tfr_bands['all_epoch_eventIDs']

# This is how you get all indices of a specific value in a list
# because list.index() will only return the index of the first item
indices = [i for i, x in enumerate(event_label) if x == "NV/Call/Stim1/Lv1/Cor/F" ]
indices = [i for i, x in enumerate(event_label) if x == 'NV/Call/Stim1/Lv1/Cor/M']

# Next step: get the indices of multiple values
indices = [i for i, x in enumerate(event_label) if x == "NV/Call/Stim1/Lv1/Cor/F" or x == 'NV/Call/Stim1/Lv1/Cor/M']
# There has to be an easier way to do this...

# there we go: this gives all indices of values that contain a specific string
indices = [i for i, x in enumerate(event_label) if "NV/Call/Stim1/Lv1/Cor" in x]
indices = [i for i, x in enumerate(event_label) if "Lv3/Cor"  and "NV" in x]

# and to get the indices of all items that are NOT in that condition:
indices = [i for i, x in enumerate(event_label) if "Lv1"  not in x]

# and we filter the dataset by:
filtered_dataset = tfr_bands['Beta_data'][indices,:,:]
    
#%% Now: how to put it in a function

# First we do the pre-sets
NoiseType = 'NV'
StimulusType = None
Stimulus = None
Degradation = 'Lv3'
Accuracy = None
Voice = None

# Put all of the conditions & parameters into a dict
newDict = {'NoiseType' : NoiseType, 
           'StimulusType' : StimulusType,
           'Stimulus' : Stimulus,
           'Degradation' : Degradation,
           'Accuracy' : Accuracy,
           'Voice' : Voice}

# Create a set of all indexes. Items that are not in the desired conditions will be removed
filt_idx = set(range(len(event_label)))

# For each parameter, if it is not None, get the indices of the desired condition
# and then compare them to filt_idx. From filt_idx, remove all elements not in the desired condition
for key in newDict.keys():
    if newDict[key] is not None:
        idx = [i for i, x in enumerate(event_label) if newDict[key] in x]
        filt_idx = filt_idx & set(idx) # Keep only the common elements

#%%
"""
I need an option to keep multiple conditions of each variable instead of just one.
What if someone wants to filter the data into Degradation Lv2 and Lv3, but does not
need the data for Lv1 ?

With the function above, it is only possible to filter into EITHER Lv2 OR Lv3.
I need to make an option to remove a single condition instead of only being able
to keep a single condition.

Idea: For the parameters, have both the (Condition = None) but also (ConditionExclude = None)
Pass a list of variables to ConditionExclude, and for these variables, the 
condition specified will be excluded rather than included


Then, how to put it in a function?
Make separate functions. 
The first function is to exclude (if any) and return the filtered idx.
The second will take the filt_idx and include the desired conditions.

Or:
    If ConditionExclude is not None, Function1 will call Function2.
    Function2 will exlude the specified condition and return filt_idx.
    Function1 will then filter (include) the rest of the conditions using filt_idx
"""

conditionExclude = ['Degradation']

if conditionExclude is not None:
    for cond in conditionExclude:
        idx = [i for i, x in enumerate(event_label) if newDict[cond] not in x]
        filt_idx = filt_idx & set(idx)



#%% Get crossvalidation scores
# y = epo.metadata['accuracy'] # What variable we want to predict

# for thisBand in const.freqbands:
#     all_scores_full, scores, std_scores = TFRManager.get_crossval_scores(X=tfr_bands[thisBand], y = y)
#     tfr_bands[thisBand+'_crossval_FullEpoch'] = all_scores_full
#     tfr_bands[thisBand+'_crossval_timewise_mean'] = scores
#     tfr_bands[thisBand+'_crossval_timewise_std'] = std_scores
# # TODO - Hm. all [band]_timewise_mean and all [band]_timewise_std are the same value. Check if there's an error somewhere
