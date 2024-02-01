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

from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold, cross_validate  
from sklearn import metrics
from sklearn import svm
import numpy as np

import MVPA_constants as const
import MVPA_functions as functions
MVPAManager = functions.MVPAManager()

#%% filepaths 
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                        const.taskID,'features',subjID)
pickle_path = os.path.join(dirinput, subjID + const.inputPickleFileEnd)

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

#%%
conditionInclude = ['Lv3'] 
conditionExculde = []
prediction = 'accuracy'

idx = list(MVPAManager.getFilteredIdx(
    tfr_bands['epoch_conditions'], conditionInclude=conditionInclude, conditionExclude=conditionExculde))
#%%
def get_crossval_scores(X,y,clf=svm.SVC(C=1, kernel='linear'),cv=None,scoretype=('accuracy')):    
    """ Get classification scores with a scikit classifier 
    =================================================================
    Created on Thu Dec 22 13:44:33 2022
    @author: gfraga & samuemu
    Ref: visit documentation in https://scikit-learn.org/stable/modules/classes.html
    https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
    https://scikit-learn.org/stable/modules/svm.html
    
    Parameters
    ----------
    X: array of shape (n_epochs, n_channels, n_timepoints)
       feature vector (e.g., epochs x [channels x times]) 
    
    y: array-like of shape (n_samples,) or (n_samples, n_outputs)
        The target variable to try to predict in the case of supervised learning.
        For instance, the accuracy labels of the epochs (y = epo.metadata['accuracy'])
        # TODO I need to include an error if the 
    
    clf: str 
       Define classifier, i.e. the object to use to fit the data. 
       Default: clf = svm.SVC(C=1, kernel='linear')
    
    cv: int | cross-validation generator or an iterable | Default=None
        cross validation choice. 
        - int to specify the number of folds.
        - None will use default 5-fold cross validation.
        - iterable yielding (train, test) splits as arrays of indices
        - A CV splitter, such as KFold or StratifiedKFold, ShuffleSplit.
          example: cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        - If int/None input, and if clf is a classifier and y is either binary or multiclass,
          then StratifiedKFold is used. Otherwise, KFold is used. Both will be instantiated with
          shuffle=False, so splits will be the same across class.
        
    scoretype: str | callable | list | tuple | dict
        the type of score (e.g., 'roc_auc','accuracy','f1')
        see https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
        Default= ('accuracy')
    
    
    Returns
    -------       
    scores_full: classification score for the whole epoch
    
    scores: classification scores for each time point (time-resolved mvpa)
    
    std_scores: std of scores
    
    """  
    
    
    # #[MVPA] Decoding based on entire epoch
    # ---------------------------------------------
    if len(X.shape) != 3:
        raise ValueError(f'Array X needs to be 3-dimensional, not {len(X.shape)}')
    X_2d = X.reshape(len(X), -1) # Now it is epochs x [channels x times]   
    # self.X_2d = X_2d
    
    #% see https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
    all_scores_full = cross_validate(estimator = clf,
                                     X = X_2d, # the data to fit the model
                                     y= y,  # target variable to predict
                                     cv=cv, # cross-validation splitting strategy
                                     n_jobs=const.n_jobs,
                                     scoring=scoretype,
                                     return_estimator=True,
                                     return_indices=True)
    
    #all_scores_full = {key: all_scores_full[key] for key in all_scores_full if key.startswith('test')} #get only the scores from output (also contains times)
    # TODO get only mean and std instead of all 5 (ask Gorka if he wants all 5)
    print('---> run classification on the full epoch')
    
    
    
    # #[MVPA] Time-resolved decoding 
    # # ---------------------------------------------
    # n_times = X.shape[2] # get number of timepoints
    
    # #Use dictionaries to store values for each score type
    # if type(scoretype) is str:
    #     scores = np.zeros(shape=(n_times,1))
    #     std_scores = np.zeros(shape=(n_times,1))
    # else:
    #     scores = {name: np.zeros(shape=(n_times,1)) for name in scoretype}
    #     std_scores = {name: np.zeros(shape=(n_times,1)) for name in scoretype}
    
    # print('----> starting classification per time point....')
    # for t in range(n_times): # for each timepoint...
    #     Xt = X[:, :, t] # get array of shape (n_epochs, n_channels) for this timepoint
        
    #     # Standardize features
    #     Xt -= Xt.mean(axis=0) # subtracts the mean of the row from each value
    #     Xt /= Xt.std(axis=0) # divides each value by the SD of the row
        
    #     #[O_O] Run cross-validation for each timepoint
    #     scores_t = cross_validate(estimator=clf, 
    #                               X=Xt, 
    #                               y=y, 
    #                               cv=cv, 
    #                               n_jobs=const.n_jobs,
    #                               scoring=scoretype)     
        
    #     #Add CV mean and std of this time point to my output dict 
    #     if type(scoretype) is str:
    #         scores[t]=scores_t['test_score'].mean()
    #         std_scores[t]=scores_t['test_score'].std()

            
    #     else:
    #         for name in scoretype:
    #             scores[name][t]=scores_t['test_' + name].mean()
    #             std_scores[name][t]=scores_t['test_' + name].std()
    
    # #from lists to arrays 
    # if type(scoretype) is not str:
    #     scores = {key: np.array(value) for key, value in scores.items()}
    #     std_scores = {key: np.array(value) for key, value in std_scores.items()}
      
    # print('-----> Done.')
    return all_scores_full #, scores, std_scores 




#%% Get crossvalidation scores
y = tfr_bands['epoch_metadata'][prediction][idx] # What variable we want to predict (set in the user inputs)

thisBand = 'Alpha'
# for thisBand in const.freqbands: # loop over all frequency bands # TODO use metadata instead of constants
print('--> now performing crossvalidation for', thisBand)
X=tfr_bands[str(thisBand +'_data')][idx,:,:] # Get only the trials that are in the specified conditions (user inputs)

all_scores_full = get_crossval_scores(X = X, y = y) # Get scores and add to the dict
tfr_bands[thisBand+'_crossval_FullEpoch'] = all_scores_full['test_score']
# tfr_bands[thisBand+'_crossval_timewise_mean'] = scores
# tfr_bands[thisBand+'_crossval_timewise_std'] = std_scores

#%%
n_test = sum(len(sub_array) for sub_array in all_scores_full['indices']['test'])/len(all_scores_full['indices']['test'])
n_train = sum(len(sub_array) for sub_array in all_scores_full['indices']['train'])/len(all_scores_full['indices']['train'])