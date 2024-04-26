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


#%% User Inputs
n_bins = 8
subsample = False
FixCompleteSeparation = True
verbose = True

LogRegManager = functions.LogRegManager(verbose=verbose)

#%% get data 
LogRegManager.get_data(condition = "NV")

#%% check complete separation. If FixCompleteSeparation = True place random 0 if 100% correct
# for more information:
# help(LogRegManager.CheckCompleteSeparation)
# help(LogRegManager.FixCompleteSeparation)
if FixCompleteSeparation: 
    LogRegManager.FixCompleteSeparation()
else:
    LogRegManager.CheckCompleteSeparation()

#%% get condition_df from LogRegManager object. If needed, create condition_df first.
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

grps_new = {'timeBin': n_bins, 'channel': len(ch_names), 'subjID': len(const.subjIDs)}
del dfs, df_tmp, i, condition_data, reIdx, eeg_data, data_dict, idx 
del ch_names, timepoint, thisChannel, n_bins, subjID

#%% Formulas to run
formulas = [
    'accuracy ~ 1 + (1|timeBin:channel)  + (1|subjID)',
    'accuracy ~ eeg_data + (eeg_data|timeBin:channel)  + (1|subjID)',
    # 'accuracy ~ eeg_data + (eeg_data|timeBin/channel)  + (1|subjID)',
    # 'accuracy ~ eeg_data + (eeg_data|channel/timeBin)  + (1|subjID)',
    'accuracy ~ levels + wordPosition + eeg_data + (eeg_data|timeBin:channel) + (1|subjID)',
    # 'accuracy ~ levels + wordPosition + eeg_data + (eeg_data|timeBin/channel) + (1|subjID)',
    # 'accuracy ~ levels + wordPosition + eeg_data + (eeg_data|channel/timeBin) + (1|subjID)',    
    'accuracy ~ wordPosition + levels * eeg_data + (eeg_data|timeBin:channel) + (1|subjID)',
    # 'accuracy ~ wordPosition + levels * eeg_data + (eeg_data|timeBin/channel) + (1|subjID)',
    # 'accuracy ~ wordPosition + levels * eeg_data + (eeg_data|channel/timeBin) + (1|subjID)',    
    ]

saved_variables = ["AIC","coefs", "_conf_int", "family", "fixef", "formula", "logLike", "ranef", "ranef_corr", "ranef_var", "sig_type", "warnings"]
pickle_path_out = const.diroutput + "_LogitRegression_noSubsample.pkl"

#%%  run models and save output
timecontrol = []
start = datetime.now()
output_dict = {}
for formula in formulas:
    
    print(datetime.now(),' --- now starting model: ', formula, ' --- ><((((°> ')
    timecontrol.append([formula, str(datetime.now())])
    model = Lmer(formula, data = total_df, family = 'binomial')

    model.fit()
    
    tmp_dict = {}
    for variable in saved_variables:
        variable_value = getattr(model, variable)
        tmp_dict[variable] = variable_value
    output_dict[formula] = tmp_dict
    # del model

    
    # We save this at every step so we don't lose everything if/when the kernel dies
    with open(pickle_path_out, 'wb') as f:
        pickle.dump(output_dict, f)
    
end = datetime.now()

output_dict['metadata'] = LogRegManager.metadata

with open(pickle_path_out, 'wb') as f:
    pickle.dump(output_dict, f)   

#%% Print AIC for each model (for quick comparison)
for key in output_dict.keys():
    if '~' in key:
        print( "%.3f" % output_dict[key]['AIC'], 'for model', key)

#%%
# grp_vars = model.grps
# dv_var = formula.split("~")[0].strip()
# perm_dat = total_df.copy()
# tmp = perm_dat.groupby('subjID')[dv_var].transform(lambda x: x.sample(frac=1))
# # perm_dat[dv_var] = perm_dat.groupby(grp_vars)[dv_var].transform(lambda x: x.sample(frac=1))
