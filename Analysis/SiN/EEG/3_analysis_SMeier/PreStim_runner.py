#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 09:01:21 2024

@author: samuemu
"""
#%% Imports
import os
from glob import glob
import mne
import PreStim_constants as const
import statsmodels.formula.api as smf
import statsmodels.stats.multitest as ssm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

dirinput = os.path.join(const.thisDir[:const.thisDir.find(
    'Scripts')] + 'Data', 'SiN', 'derivatives_SM', const.taskID)

#%% First, create a dict of all subj data to store in the memory
data_dict = {}
metadata_dict = {}

for subjID in const.subjIDs:
    
    # get filepath
    epo_path = glob(os.path.join(dirinput, subjID, str(subjID + '_' + const.taskID + "*" + const.fifFileEnd)), recursive=True)[0]
    epo = mne.read_epochs(epo_path)

    
    data_dict[subjID] = epo.get_data(tmax = 0) # get data as array of shape [n_epochs, n_channels, n_times]
    metadata_dict[subjID] = epo.metadata # get trial information
    
    # re-code and delete unneeded data
    metadata_dict[subjID]['noiseType'] = metadata_dict[subjID]['block'] 
    metadata_dict[subjID]['subjID'] = [subjID for i in range(len(metadata_dict[subjID]))]
    metadata_dict[subjID]['levels'].replace('Lv1', 1, inplace=True)
    metadata_dict[subjID]['levels'].replace('Lv2', 2, inplace=True)
    metadata_dict[subjID]['levels'].replace('Lv3', 3, inplace=True)
    metadata_dict[subjID]['accuracy'].replace('inc', 0, inplace=True)
    metadata_dict[subjID]['accuracy'].replace('cor', 1, inplace=True)
    metadata_dict[subjID]['noiseType'].replace('NV', 0, inplace=True)
    metadata_dict[subjID]['noiseType'].replace('SSN', 1, inplace=True)
    metadata_dict[subjID].drop(labels=['tf','stim_code','stimtype','stimulus','voice','block'], axis = 1, inplace = True)
    
    #del epo
    
"""
HOLD ON!

Not all subjects have 64 electrodes. The matlab script rejects some channels but does not interpolate them.
Which leads to unequal numbers of channels.

This means we cannot simply compare the n-th channel of each subject because the n-th channel
might not be the same across subjects, if any channel between 1 and n has been removed.

So we need to first check each subj channels (epo.ch_names) against a list of all 64 channels
to figure out which ones are missing, and insert a...

Or: create an array of shape [n_channels, n_subjects] filled with boolean values.
Then only incl channels if True
"""
    
#%% Create arrays and lists
channels = [i for i in range(data_dict[subjID].shape[1])] # list of channels
times = [i for i in range(data_dict[subjID].shape[2])] #list of timepoints

p_values = np.zeros(shape=(len(channels),len(times),9)) # empty array for the p_values

#%% And now the big loop

for thisChannel in channels:
    print('>>>> running channel',thisChannel,'of', len(channels))
    
    for tf in times:
           
        # the data & trial information of each subject at a given timepoint and channel
        tmp_dict = {}
        for subjID in const.subjIDs:    
            tmp_dict[subjID] = metadata_dict[subjID]
            tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,thisChannel,tf]

        
        # Combine all subject's data into one dataframe so we can run the LMM on that
        df = pd.concat(tmp_dict.values(), axis=0)
        del tmp_dict
        
        # calculate LMM
        md = smf.mixedlm("accuracy ~ levels * eeg_data * noiseType", df, groups = "subjID")        
        mdf = md.fit() # This gives the convergence warning # TODO
        
        # record p-Values
        p_values[thisChannel,tf,:] = mdf.pvalues
        
index_p_values = mdf.pvalues.index
formula_LMM = md.formula

#%% Now for the FDR correction...
print('Time for the FDR.................................................................')
p_values_1dim = p_values.flatten() #transforms the array into a one-dimensional array (needed for the FDR)
rej, p_values_FDR = ssm.fdrcorrection(p_values_1dim) # get FDR corrected p-Values

p_values_FDR = p_values_FDR.reshape(p_values.shape) # transform 1D array back to 3D array of shape [channel, timeframe, p-Value]

print('done! ...........................................................................')

#%% do some plots
run = True
if run == True:
    f,ax = plt.subplots(figsize=(10,8))
    sns.heatmap(p_values_FDR[:,:,8], vmin = 0, vmax = 0.05)
    ax.set(xlabel="times", ylabel="electrodes")
