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
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

response_variable = 'stimtype'
timewindow = "_poststim" # other option : '_poststim'
scoretype =  [
    'accuracy', 
    'balanced_accuracy', 
    # 'roc_auc'
    ]
# separate = {'degradationType' : const.degradationType, 'degradationLevel' : const.degradationLevel, 'wordPosition' : const.wordPosition}
subjID = 's003'
verbose = True

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

#%% create empty dicts and lists to collect data
crossval_mean_dict = {}
full_epoch_crossval_mean = {}
for thisBand in const.freqbands:
    crossval_mean_dict[thisBand] = []
    full_epoch_crossval_mean[thisBand] = []
true_accuracy_list = []
all_results_dicts = {}

# TODO use the combine_lists function to separate conditions
column_idx = ['degradationType', 'degradationLevel', 'freqband', 'score']


#%% start with the loops - we run an MVPA for every combination of degradationType and degradationLevel

for degradationType in const.degradationType:
    for degradationLevel in const.degradationLevel:

            conditionInclude = [degradationType, degradationLevel] 
            conditionExculde = []
            
            #%% Filter conditions for each loop
            idx = list(MVPAManager.getSubsetIdx(
                tfr_bands['epoch_conditions'], 
                conditionInclude=conditionInclude, 
                conditionExclude=conditionExculde))
            
            #%% Get true accuracy
            y = tfr_bands['epoch_metadata'][response_variable][idx] # What variable we want to predict (set in the user inputs) - these are the class labels
            
            if response_variable == 'accuracy': # TODO option for this for other response_variables?
                n_cor = y.value_counts().iloc[0]
                n_inc = y.value_counts().iloc[1]
                true_accuracy = y.value_counts().iloc[0]/len(y)
                accu_df_tmp = pd.DataFrame({(degradationType, degradationLevel):  [n_inc, n_cor, true_accuracy]}, index=['n_inc', 'n_cor', 'true_accuracy'])            
                true_accuracy_list.append(accu_df_tmp)
            
            list_tmp = []
            for thisBand in const.freqbands: # loop over all frequency bands # TODO use metadata instead of constants
                if verbose: print('--> now performing crossvalidation for', thisBand)
                X = tfr_bands[str(thisBand +'_data')][idx,:,:] # Get only the trials that are in the specified conditions (user inputs)
                
                # Get scores and add to the dict collecting all outputs
                output_dict = MVPAManager.get_crossval_scores(X = X, y = y, scoretype = scoretype) 
                all_results_dicts[thisBand, degradationType, degradationLevel] = output_dict
                
                # Create dataframe
                columns = (degradationType, degradationLevel,  thisBand) 
                df_tmp = pd.DataFrame({columns + (key,): output_dict['crossval_scores_timewise'][key] for key in output_dict['crossval_scores_timewise'] if key.endswith('mean')})
                # The line above means: get every array whose key is ending in '_mean' from the 'timewise' dict of the output_dict
                # and put the values in a dataframe. The column indexes of the dataframe should be 'columns' and the key (=what score)
                # ... hence the `columns + (key,)` - the key is transformed into tuple and added to columns
                crossval_mean_dict[thisBand].append(df_tmp)
                
                columns = (degradationType, degradationLevel) 
                df_tmp = pd.DataFrame({columns + (key,): output_dict['crossval_score_FullEpoch'][key] for key in output_dict['crossval_score_FullEpoch'] if key.endswith('mean')}, index = [thisBand])
                full_epoch_crossval_mean[thisBand].append(df_tmp)
                del df_tmp
                     
            # # TODO save this somehow
            # tfr_bands['metadata']['response_variable']=response_variable
            # tfr_bands['metadata']['sklearn_version']= sklearn_version
            # tfr_bands['metadata']['codebook']=const.codebook   

"""
# TODO - Hm. all [band]_crossval_fullepoch are the same value. Check if there's an error somewhere

(18.01.24)
Not anymore  even though I didn't change anything but the filtering. Best to pay attention.

(01.02.24)
Huh. As of now they are once again the same. 
conditionExclude Call, conditionInclude Lv3, prediciton accuracy. 
See screenshot (@samuemu)
    
(02.04.24)
Solved: If the classifier ALWAYS predicts "cor", it will be right in exactly as 
many trials as there are trials marked "cor".

So if the classifier always predicts "cor" for every freqband, it will always 
have the same score in every freqband, and that score will always be equal to
the true accuracy of responses.

It seems that having [n_times * n_channels] features is just too much (overfitting).
The timewise classification (which only has [n_channels] features) actually differs 
between freqbands - so it probably doesn't simply predict "cor" across the board.

(18.04.24)        
Either way, with unbalanced data like this it actually makes way more sense to use
the balanced_accuracy. It is defined as [ (TPR + TNR) / 2 ]
Where TPR is the True Positive Rate, synonymous with Sensitivity, Recall, Hit Rate, Power,
and is defined as [ n_truePositives / (n_truePositives + n_falseNegatives)].
And where TNR is the True Negative Rate, synonymous with Specificity, Selectivity, and
is defined as [ n_trueNegatives / (n_trueNegatives + n_falsePositives)]
"""

            


#%% create a df for each freqband    
dfs_dict = {}
for key, data_list in crossval_mean_dict.items():
    concat_df = pd.concat(data_list, axis=1,  names = column_idx)
    index =  tfr_bands[key+'_COI_times']
    concat_df.set_index(index, inplace = True)
    # globals()['df_' + key] = concat_df # this creates a df for every freqband but 
    # # everytime the script references the dfs created this way, there will be a red X next to
    # # the line number, saying e.g. "undefined name 'df_Alpha'" - because it only checks the
    # # variables explicitly assigned in the script.
    # # So instead I am going with this, less cool solution:
    dfs_dict['df_' + key] = concat_df

if response_variable == 'accuracy':
    df_accuracy = pd.concat(true_accuracy_list, axis = 1, 
                            names = ['degradationType', 'degradationLevel'])

#%%
dfs_list_full = []
for key, data_list in full_epoch_crossval_mean.items():
    concat_df = pd.concat(data_list, axis=1,  names = column_idx)

    # globals()['df_' + key] = concat_df # this creates a df for every freqband but 
    # # everytime the script references the dfs created this way, there will be a red X next to
    # # the line number, saying e.g. "undefined name 'df_Alpha'" - because it only checks the
    # # variables explicitly assigned in the script.
    # # So instead I am going with this, less cool solution:
    dfs_list_full.append(concat_df)
full_epoch_crossval_mean = pd.concat(dfs_list_full, axis = 0)
    
# TODO save dfs as .csv
# TODO also put df_accuracy into dfs_dict and save as .pkl

#%% just to check for consistency in the time indexes (they should be the same but it's good to check)
# # TODO put in functions
# for thisBand in const.freqbands:
#     index =  tfr_bands[thisBand+'_COI_times']
#     globals()['times_' + thisBand] = set([float("%.3f" % x) for x in list(index)])

# freqbands_list = list(const.freqbands.keys())
# for i, thisBand in enumerate(freqbands_list[0:-1]):
#     length = len(globals()['times_' + thisBand])
#     overlap = len( (globals()['times_' + thisBand]) & (globals()['times_' + freqbands_list[i+1]]) )
#     if overlap != length:
#         raise ValueError('ERROR: not all timepoints of', thisBand, 'contained in', freqbands_list[i+1])
#     elif verbose:
#         print('--> all timepoints of', thisBand, 'contained in', freqbands_list[i+1])

#%% Lineplot of the mean score of each freqband across all conditions
y_lim = [0.2, 0.6]
horizontal_line = 0.33

for score in scoretype:
    score = score + '_mean'
    means_tmp = []
    for key in dfs_dict.keys():
        legend_str = str(key)[str(key).find('_')+1:]
        df_tmp = dfs_dict[key]
        df_tmp = df_tmp.xs(score,axis = 1, level = 3)
        tmp = pd.DataFrame({legend_str : df_tmp.mean(axis=1)})
        means_tmp.append(tmp)
    
    all_means = pd.concat(means_tmp, axis = 1)
    sns.lineplot(data = all_means, palette = const.palette[0:4], dashes=False)
    plt.ylim(y_lim)
    plt.axhline(y = horizontal_line, color = '#999999', linestyle = ':')
    plt.title(subjID + ' - ' + score + ' - mean across conditions')
    plt.show()
    
    #%% And now if I want the mean within degradationType...
    for degradationType in const.degradationType:
        means_tmp = []
        for key in dfs_dict.keys():
            legend_str = str(key)[str(key).find('_')+1:]
            df_tmp = dfs_dict[key]
            df_tmp = df_tmp.xs(score,axis = 1, level = 3)
            tmp = pd.DataFrame({legend_str : df_tmp[degradationType].mean(axis=1)})
            means_tmp.append(tmp)
        
        all_means = pd.concat(means_tmp, axis = 1)
        sns.lineplot(data = all_means, palette = const.palette[0:4], dashes=False)
        plt.ylim(y_lim)
        plt.axhline(y = horizontal_line, color = '#999999', linestyle = ':')
        plt.title(subjID + ' - ' + score + ' - mean of ' + degradationType)
        plt.show()
    
    #%% And now if I want the mean within degradationType...
    for degradationType in const.degradationType:
        for degradationLevel in const.degradationLevel:
            means_tmp = []
            for key in dfs_dict.keys():
                legend_str = str(key)[str(key).find('_')+1:]
                df_tmp = dfs_dict[key]
                df_tmp = df_tmp.xs(score,axis = 1, level = 3)
                tmp = pd.DataFrame({legend_str : df_tmp[degradationType, degradationLevel].mean(axis=1)})
                means_tmp.append(tmp)
            
            all_means = pd.concat(means_tmp, axis = 1)
            sns.lineplot(data = all_means, palette = const.palette[0:4], dashes=False)
            plt.ylim(y_lim)
            plt.axhline(y = horizontal_line, color = '#999999', linestyle = ':')
            plt.title(subjID + ' - ' + score+ ' - ' + degradationType + '/' + degradationLevel)
            plt.show()
        
