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

dirinput = os.path.join(const.thisDir[:const.thisDir.find(
    'Scripts')] + 'Data', 'SiN', 'derivatives_SM', const.taskID)

#%% First, create a dict of all subj data to store in the memory
data_dict = {}
metadata_dict = {}

for subjID in const.subjIDs:
    
    # get filepath
    epo_path = glob(os.path.join(dirinput, subjID, str(subjID + '_' + const.taskID + "*" + const.fifFileEnd)), recursive=True)[0]
    epo = mne.read_epochs(epo_path)

    
    data_dict[subjID] = epo._get_data(tmax = 0) # get data
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
    
    del epo
    
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
        mdf = md.fit()
        
        # record p-Values
        p_values[thisChannel,tf,:] = mdf.pvalues
        
index_p_values = mdf.pvalues.index
formula_LMM = md.formula

#%% Now for the FDR correction...
print('Time for the FDR.................................................................')
p_values_1dim = p_values.flatten()
rej, p_values_FDR = ssm.fdrcorrection(p_values_1dim)

p_values_FDR = p_values_FDR.reshape(p_values.shape)
