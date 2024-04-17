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

     
response_variable : str --- must be a column name from tfr_bands['epoch_metadata']
    The variable we are interested in. 
    Options : accuracy, block, stimtype, stimulus, levels, voice
    Example : response_variable = 'accuracy' will do the cross-validation on how well 
        the frequency power encodes whether the response was correct or not
        
timewindow : either "_prestim" or "_poststim"
    This will affect which file will be opened to get the data. 
    
scoretype : # TODO
    
"""

response_variable = 'accuracy'
timewindow = "_prestim" # other option : '_poststim'
scoretype =  ['roc_auc'] # ['accuracy', 'balanced_accuracy', 'roc_auc']
# separate = {'degradationType' : const.degradationType, 'degradationLevel' : const.degradationLevel, 'wordPosition' : const.wordPosition}
subjID = 's003'

#%% setting filepaths 
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                        const.taskID,'features',subjID)
pickle_path_in = os.path.join(dirinput, subjID + timewindow + const.inputPickleFileEnd)
pickle_path_out = os.path.join(dirinput, subjID + timewindow + const.outputPickleFileEnd)

#%% Open the dict 
print('--> opening dict:',pickle_path_in)
with open(pickle_path_in, 'rb') as f:
    tfr_bands = pickle.load(f)
    
# TODO subsample data

#%% start with the loops - we run an MVPA for every combination of wordPosition, degradationType and degradationLevel

data_dict = {}
for thisBand in const.freqbands:
    data_dict[thisBand] = []
true_accuracy = []

# TODO use the combine_lists function to separate conditions
column_idx = ['degradationType', 'degradationLevel', 'wordPosition', 'freqband', 'score']

for degradationType in const.degradationType:
    for degradationLevel in const.degradationLevel:
        for wordPosition in const.wordPosition:
            conditionInclude = [degradationType, degradationLevel, wordPosition] 
            conditionExculde = []
            
            #%% Filter conditions for each loop
            idx = list(MVPAManager.getSubsetIdx(
                tfr_bands['epoch_conditions'], 
                conditionInclude=conditionInclude, 
                conditionExclude=conditionExculde))
            
            #%% Get true accuracy
            y = tfr_bands['epoch_metadata'][response_variable][idx] # What variable we want to predict (set in the user inputs) - these are the class labels
            
            n_cor = y.value_counts().iloc[0]
            n_inc = y.value_counts().iloc[1]
            true_response_accuracy = y.value_counts().iloc[0]/len(y)
            
            # TODO make this as rows instead of columns, set index as n_inc, n_cor, true_response_accuracy
            dict_tmp = {'n_cor':n_cor, 'n_inc' : n_inc, 'true_response_accuracy': true_response_accuracy}
            accu_data_tmp = pd.DataFrame({(degradationType, degradationLevel, wordPosition, key): dict_tmp[key] for key in dict_tmp}, index =[1])
            
            true_accuracy.append(accu_data_tmp)
            
            for thisBand in const.freqbands: # loop over all frequency bands # TODO use metadata instead of constants
                print('--> now performing crossvalidation for', thisBand)
                X = tfr_bands[str(thisBand +'_data')][idx,:,:] # Get only the trials that are in the specified conditions (user inputs)
                
                # Get scores and add to the dict 
                output_dict = MVPAManager.get_crossval_scores(X = X, y = y, scoretype = scoretype) 
                
                # Create dataframe
                columns = (degradationType, degradationLevel, wordPosition, thisBand) 
                data_tmp = pd.DataFrame({columns + (key,): output_dict['crossval_scores_timewise'][key] for key in output_dict['crossval_scores_timewise'] if key.endswith('mean')})
                # The line above means: get every array whose key is ending in '_mean' from the 'timewise' dict of the output_dict
                # and put the values in a dataframe. The column indexes of the dataframe should be 'columns' and the key (=what score)
                # ... hence the `columns + (key,)` - the key is transformed into tuple and added to columns
                
                data_dict[thisBand].append(data_tmp)
            

            
            # # TODO - Hm. all [band]_crossval_fullepoch  are the same value. Check if there's an error somewhere
            # # Not anymore (as of 18.01.24) even though I didn't change anything but the filtering. Best to pay attention.
            # # Huh. As of now (01.02.24) they are once again the same. conditionExclude Call, conditionInclude Lv3, prediciton accuracy. See screenshot (@samuemu)
            # # Solved: If the classifier ALWAYS predicts "cor", it will be right in exactly as many trials as there are trials marked "cor"
            # # So if the classifier always predicts "cor" for every freqband, it will always have the same score.
            # # It seems that having [n_times * n_channels] features is just too much - the timewise classification (which only has [n_times] features)
            # # actually differs between freqbands - so it probably doesn't simply predict "cor" across the board
            
            # # TODO save this somehow
            # tfr_bands['metadata']['response_variable']=response_variable
            # tfr_bands['metadata']['sklearn_version']= sklearn_version
            # tfr_bands['metadata']['codebook']=const.codebook


# create a df for each freqband            
for key, data_list in data_dict.items():
    concat_df = pd.concat(data_list, axis=1,  names = column_idx)
    index = tfr_bands[key+'_COI_times']
    concat_df.set_index(index, inplace = True)
    globals()['df_' + key] = concat_df
df_tmp = pd.MultiIndex.from_frame(concat_df)
df_accuracy = pd.concat(true_accuracy, axis = 1, names = ['degradationType', 'degradationLevel', 'wordPosition'])

# TODO save it
