#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 07:42:19 2024

@author: testuser
"""


from pymer4.models import Lmer
import pandas as pd
import numpy as np
import random
from datetime import datetime

import LogReg_functions as functions
import LogReg_constants as const
LogRegManager = functions.LogRegManager()

#%%
# data_dict, condition_dict = LogRegManager.get_data(output = True, condition = "NV")
# LogRegManager.run_LogitRegression(equalise_accuracy = False, time_bins = 8)
 
#%% check complete separation, place random 0 if 100% correct
LogRegManager.get_data(condition = "NV")
# LogRegManager.FixCompleteSeparation()
try:
    condition_df = LogRegManager.condition_df
except AttributeError:
    LogRegManager.get_condition_df()
    condition_df = LogRegManager.condition_df
    
#%% Run the model with both time and electrode as predictors
n_bins = 8
data_dict = LogRegManager.binTimes(n_bins = n_bins)
ch_names = LogRegManager.metadata['ch_names']
equalise_accuracy = False



#%% And this will aggregate the df with time and electrode as a variable
dfs = []
idx = []

    
for subjID in const.subjIDs:
    
    # get data
    eeg_data = data_dict[subjID]
    condition_data = condition_df[condition_df['subjID'] == subjID]
    
    # re-index
    reIdx = pd.Series(range(len(condition_data)))
    condition_data.set_index(reIdx, inplace = True)
    
    if equalise_accuracy:
        # we sub-sample running the function below. which will give us a set of indices (idx)
        # and later we subset the data by idx
        idx = (LogRegManager.random_subsample_accuracy_decimate(trial_info=condition_data))
    else: # if no sub-sampling is asked for, just get every idx
        idx = [i for i in range(len(condition_data))]

    
    for timepoint in range(n_bins):
        for i, thisChannel in enumerate(ch_names):
            df_tmp = condition_data.copy()
            df_tmp = df_tmp.iloc[idx]
            df_tmp['eeg_data'] = eeg_data[idx,i,timepoint]
            df_tmp['channel'] = thisChannel
            df_tmp['timeBin'] = str(timepoint)
            dfs.append(df_tmp)
            
total_df = pd.concat(dfs, ignore_index=True)   
del dfs, df_tmp, i, condition_data, reIdx, eeg_data, data_dict, idx 
del ch_names, timepoint, thisChannel, n_bins, subjID


#%%
start = datetime.now()

# print('starting unconditional model now', start)
# # unconditional Means Model - model with no predictors, which shows amount of variation at each level
# # there should be 0 variation due to timeBin or channel
# model0 = Lmer('accuracy ~ 1 + (1|timeBin) + (1|channel) + (1|subjID)', data = total_df, family = 'binomial')
# model0.fit()
# # this will give us mean accuracy across trials, timeBin, channel, and sbujID
# # and variance over trials within timeBins
# # and variance between timeBin of same channel
# # and variance between channel of same subjID
# # and variance between subjID

print('starting model1 now', datetime.now())
model1 = Lmer('accuracy ~ eeg_data + (eeg_data|timeBin:channel)  + (1|subjID)', data = total_df, family = 'binomial')
model1.fit()
# This model accounts for the fact that the data is nested in timeBin & channel
# It also allows a random slope for timebin & channel - meaning the eeg_data may have a different slope depending on timeBin & channel

print('starting model2 now', datetime.now())
model2 = Lmer('accuracy ~ levels + wordPosition + eeg_data + (eeg_data|timeBin:channel) + (1|subjID)', data = total_df, family = 'binomial')
model2.fit()
# same model as above but now with wordPosition and levels

print('starting model3 now', datetime.now())
model3 = Lmer('accuracy ~ wordPosition + levels * eeg_data + (eeg_data|timeBin:channel) + (1|subjID)', data = total_df, family = 'binomial')
model3.fit()
# same model as above but now with wordPosition and levels

end = datetime.now()
