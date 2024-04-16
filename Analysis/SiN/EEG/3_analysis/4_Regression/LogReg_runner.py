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
import pickle
from datetime import datetime

import LogReg_functions as functions
import LogReg_constants as const
LogRegManager = functions.LogRegManager()

#%% User Inputs
n_bins = 8
subsample = False

#%% get data 
LogRegManager.get_data(condition = "NV")

#%% check complete separation, place random 0 if 100% correct
# LogRegManager.FixCompleteSeparation()

#%% get condition_df
try:
    condition_df = LogRegManager.condition_df
except AttributeError:
    LogRegManager.get_condition_df()
    condition_df = LogRegManager.condition_df

#%% And this will aggregate the df with time and electrode as a variables
data_dict = LogRegManager.binTimes(n_bins = n_bins)
ch_names = LogRegManager.metadata['ch_names']
dfs = []
idx = []

    
for subjID in const.subjIDs:
    
    # get data
    eeg_data = data_dict[subjID]
    condition_data = condition_df[condition_df['subjID'] == subjID]
    
    # re-index
    reIdx = pd.Series(range(len(condition_data)))
    condition_data.set_index(reIdx, inplace = True)
    
    if subsample: 
        # we subsample running the function below. which will give us a set of indices (idx)
        # and later we subset the data by idx
        idx = (LogRegManager.random_subsample_accuracy_decimate(trial_info=condition_data))
    else: # if no subsampling is asked for, just get every idx
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

#%% Formulas to run
formulas = [
    'accuracy ~ 1 + (1|timeBin:channel)  + (1|subjID)',
    'accuracy ~ eeg_data + (eeg_data|timeBin:channel)  + (1|subjID)',
    'accuracy ~ eeg_data + (eeg_data|timeBin/channel)  + (1|subjID)',
    'accuracy ~ eeg_data + (eeg_data|channel/timeBin)  + (1|subjID)',
    'accuracy ~ levels + wordPosition + eeg_data + (eeg_data|timeBin:channel) + (1|subjID)',
    'accuracy ~ levels + wordPosition + eeg_data + (eeg_data|timeBin/channel) + (1|subjID)',
    'accuracy ~ levels + wordPosition + eeg_data + (eeg_data|channel/timeBin) + (1|subjID)',    
    'accuracy ~ wordPosition + levels * eeg_data + (eeg_data|timeBin:channel) + (1|subjID)',
    'accuracy ~ wordPosition + levels * eeg_data + (eeg_data|timeBin/channel) + (1|subjID)',
    'accuracy ~ wordPosition + levels * eeg_data + (eeg_data|channel/timeBin) + (1|subjID)',    
    ]

saved_variables = ["AIC","coefs", "family", "fixef", "formula", "logLike", "ranef", "ranef_corr", "ranef_var", "sig_type", "warnings"]
pickle_path_out = const.diroutput + "_LogitRegression_noSubsample.pkl"

#%% 
timecontrol = []
start = datetime.now()
output_dict = {}
for formula in formulas:
    
    print(datetime.now(),' --- now starting model: ', formula, ' --- ><((((°> ')
    timecontrol.append((formula, str(datetime.now())))
    model = Lmer(formula, data = total_df, family = 'binomial')
    model.fit()
    
    tmp_dict = {}
    for variable in saved_variables:
        variable_value = getattr(model, variable)
        tmp_dict[variable] = variable_value
    output_dict[formula] = tmp_dict
    del model
    
    # We save this at every step so we don't lose everything when the kernel dies
    with open(pickle_path_out, 'wb') as f:
        pickle.dump(output_dict, f)
    
end = datetime.now()

output_dict['metadata'] = LogRegManager.metadata

with open(pickle_path_out, 'wb') as f:
    pickle.dump(output_dict, f)   

#%% Run the models with both time and electrode as predictors

# start = datetime.now()

# print('starting unconditional model now', start)
# # unconditional Means Model - model with no predictors, which shows amount of variation at each level
# # there should be 0 variation due to timeBin or channel
# # timeBin:channel means "Treat the combination of timeBin and channel as predictor" 
# model0 = Lmer('accuracy ~ 1 + (1|timeBin:channel) + (1|subjID)', data = total_df, family = 'binomial')
# model0.fit()
# # this will give us mean accuracy across trials, timeBin:channel, and sbujID
# # and variance over trials within timeBins & channels
# # and variance between timeBin:channel of same subjID
# # and variance between subjID

# print('starting model1 now', datetime.now())
# model1 = Lmer('accuracy ~ eeg_data + (eeg_data|timeBin:channel)  + (1|subjID)', data = total_df, family = 'binomial')
# model1.fit()
# # This model accounts for the fact that the data is nested in timeBin & channel
# # It also allows a random slope for timebin & channel - meaning the eeg_data may have a different slope depending on timeBin & channel
# # slope refers to the effect or the coefficient

# print('starting model2 now', datetime.now())
# model2 = Lmer('accuracy ~ levels + wordPosition + eeg_data + (eeg_data|timeBin:channel) + (1|subjID)', data = total_df, family = 'binomial')
# model2.fit()
# # same model as above but now with wordPosition and levels

# print('starting model3 now', datetime.now())
# model3 = Lmer('accuracy ~ wordPosition + levels * eeg_data + (eeg_data|timeBin:channel) + (1|subjID)', data = total_df, family = 'binomial')
# model3.fit()
# # same model as above but with an interaction of levels and eeg_data

# print('starting model4 now', datetime.now())
# model4 = Lmer('accuracy ~ wordPosition + levels * eeg_data + (eeg_data|timeBin/channel) + (1|subjID)', data = total_df, family = 'binomial')
# model4.fit()
# # same model as above but with an interaction of levels and eeg_data

# end = datetime.now()

#%% Get outputs
# saved_variables = ["AIC","coefs", "family", "fixef", "formula", "logLike", "ranef", "ranef_corr", "ranef_var", "sig_type", "warnings"]
# models = [model0, model1, model2, model3, model4]
# output_dict = {}
# for model in models:
#     tmp_dict = {}
#     for variable in saved_variables:
#         variable_value = getattr(model, variable)
#         tmp_dict[variable] = variable_value
#     output_dict[str(model)] = tmp_dict

#%% save dict
# pickle_path_out = const.diroutput + "Logistic_Regression_Test.pkl"
# with open(pickle_path_out, 'wb') as f:
#     pickle.dump(output_dict, f)
