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
    - Loop over subjects

"""

import os
import pickle
thisDir = os.path.dirname(__file__)
import pandas as pd

import MVPA_constants as const
import MVPA_functions as functions

MVPAManager = functions.MVPAManager()

#%% 
""" USER INPUTS
===============================================================================

conditionInclude : list of str or None
    Only trials in these conditions will be included.
    Example : conditionInclude = ['Lv3'] will perform the analysis only on 
        trials with degradation Lv3, and trials with degradation Lv2 and Lv1 are excluded
    
conditionExclude : list of str or None
    All trials in these conditions will be excluded.
    Example : conditionExclude = ['Call'] will perform the analysis only on
        trials with StimulusType Col or Num
        
response_variable : str --- must be a column name from tfr_bands['epoch_metadata']
    The variable we are interested in. 
    Options : accuracy, block, stimtype, stimulus, levels, voice
    Example : response_variable = 'accuracy' will do the cross-validation on how well 
        the frequency power encodes whether the response was correct or not
        
timewindow # TODO

  

"""
degradationType = 'NV'
degradationLevel = 'Lv3'
wordPosition = 'Call'
response_variable = 'accuracy'
timewindow = "_prestim" # other option : '_poststim'

#%% setting filepaths 
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                        const.taskID,'features',subjID)
pickle_path_in = os.path.join(dirinput, subjID + timewindow + const.inputPickleFileEnd)
pickle_path_out = os.path.join(dirinput, subjID + timewindow + const.outputPickleFileEnd)

#%% Open the dict 
print('--> opening dict:',pickle_path_in)
with open(pickle_path_in, 'rb') as f:
    tfr_bands = pickle.load(f)


#%% start with the loops

data_list = []
true_accuracy = []
column_idx = ['degradationType', 'degradationLevel', 'wordPosition', 'freqband', 'score']

for degradationType in const.degradationType:
    for degradationLevel in const.degradationLevel:
        for wordPosition in const.wordPosition:
            conditionInclude = [degradationType, degradationLevel, wordPosition] 
            conditionExculde = []
            #%% Filter conditions using the user inputs
            idx = list(MVPAManager.getSubsetIdx(
                tfr_bands['epoch_conditions'], 
                conditionInclude=conditionInclude, 
                conditionExclude=conditionExculde))
            
            #%% Get crossvalidation scores
            y = tfr_bands['epoch_metadata'][response_variable][idx] # What variable we want to predict (set in the user inputs) - these are the class labels
            
            n_cor = y.value_counts().iloc[0]
            n_inc = y.value_counts().iloc[1]
            true_response_accuracy = y.value_counts().iloc[0]/len(y)
            dict_tmp = {'n_cor':n_cor, 'n_inc' : n_inc, 'true_response_accuracy': true_response_accuracy}
            accu_data_tmp = pd.DataFrame({(degradationType, degradationLevel, wordPosition, key): dict_tmp[key] for key in dict_tmp}, index =[1])
            
            true_accuracy.append(accu_data_tmp)
            
            for thisBand in const.freqbands: # loop over all frequency bands # TODO use metadata instead of constants
                print('--> now performing crossvalidation for', thisBand)
                X = tfr_bands[str(thisBand +'_data')][idx,:,:] # Get only the trials that are in the specified conditions (user inputs)
                
                # Get scores and add to the dict 
                output_dict = MVPAManager.get_crossval_scores(X = X, y = y, scoretype = ['accuracy', 'balanced_accuracy', 'roc_auc']) 
                
                # Create dataframe
                columns = (degradationType, degradationLevel, wordPosition, thisBand) 
                data_tmp = pd.DataFrame({columns + (key,): output_dict['crossval_scores_timewise'][key] for key in output_dict['crossval_scores_timewise'] if key.endswith('mean')})
                # The line above means: get every array whose name is ending in '_mean' from the 'timewise' dict of the output_dict
                # and put the values in a dataframe. The column indexes of the dataframe should be 'columns' and the name of the array
                # ... hence the `columns + (key,)` - the key is transformed into tuple and added to columns
                data_list.append(data_tmp)
            
                # break
                # # TODO
                # tfr_bands[thisBand+'_crossval_FullEpoch'] = output_dict['crossval_score_FullEpoch']
                # tfr_bands[thisBand+'_crossval_timewise_mean'] = {key: output_dict['crossval_scores_timewise'][key] for key in output_dict['crossval_scores_timewise'] if key.endswith('mean')}
                # tfr_bands[thisBand+'_crossval_timewise_std'] = {key: output_dict['crossval_scores_timewise'][key] for key in output_dict['crossval_scores_timewise'] if key.endswith('std')}
            
            # df = pd.concat({columns : data_tmp}, axis = 1, names = column_idx)
            
            # # TODO - Hm. all [band]_crossval_fullepoch  are the same value. Check if there's an error somewhere
            # # Not anymore (as of 18.01.24) even though I didn't change anything but the filtering. Best to pay attention.
            # # Huh. As of now (01.02.24) they are once again the same. conditionExclude Call, conditionInclude Lv3, prediciton accuracy. See screenshot (@samuemu)
            # # Solved: If the classifier ALWAYS predicts "cor", it will be right in exactly as many trials as there are trials marked "cor"
            # # So if the classifier always predicts "cor" for every freqband, it will always have the same score.
            # # It seems that having [n_times * n_channels] features is just too much - the timewise classification (which only has [n_times] features)
            # # actually differs between freqbands - so it probably doesn't simply predict "cor" across the board
            
            # # TODO
            # tfr_bands['metadata']['response_variable']=response_variable
            # tfr_bands['metadata']['sklearn_version']= sklearn_version
            # tfr_bands['metadata']['codebook']=const.codebook

df = pd.concat(data_list, axis = 1, names = column_idx)
df_accuracy = pd.concat(true_accuracy, axis = 1, names = ['degradationType', 'degradationLevel', 'wordPosition'])
#%% Saving the dict

# print("pickling the dictionary to: /n"+pickle_path_out)
# with open(pickle_path_out, 'wb') as f:
#     pickle.dump(tfr_bands, f)
