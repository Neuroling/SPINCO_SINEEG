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

import LogReg_functions as functions
import LogReg_constants as const
LogRegManager = functions.LogRegManager()

#%%
# data_dict, condition_dict = LogRegManager.get_data(output = True, condition = "NV")
# LogRegManager.run_LogitRegression(equalise_accuracy = False, time_bins = 8)
 
#%%
# ## prepare the data
# tmp_dict = {}
# for subjID in const.subjIDs:    
#     tmp_dict[subjID] = condition_dict[subjID]
#     tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,0,0]
# df = pd.concat(tmp_dict.values(), axis=0, ignore_index=True)
# del tmp_dict

# # TODO : treat every electrode as predictor

# # run the model
# model = Lmer('accuracy ~ levels * eeg_data + wordPosition + (1|subjID)', data = df, family = 'binomial')
# mdf = model.fit()
# model.anova()


# # tmp = Lmer('accuracy ~ levels * eeg_data + wordPosition + (1|subjID)', data = df, family = 'binomial').fit()
# # tmp.shape

#%% whole regression (for debugging)

# formula = "accuracy ~ levels * eeg_data + wordPosition + (1|subjID)"
# family = 'binomial'
# n_iter = 500
# equalise_accuracy = True
# time_bins = 8

  
# if not equalise_accuracy: # do not iterate if no sub-sampling is performed
#     n_iter = 1
    
# # create bins for the times (if desired)
# if time_bins is not None:
#     data_dict = LogRegManager.binTimes(time_bins)
    
    
# #% Create arrays and lists
# channelsIdx = [i for i in range(data_dict['s001'].shape[1])] # list of channels
# timesIdx = [i for i in range(data_dict['s001'].shape[2])] #list of timepoints


# # This will run a first model which is only used to extract the number of p-Values
# # Which is needed to create an empty array for the p-Values
# tmp_dict = {}
# for subjID in const.subjIDs:    
#     tmp_dict[subjID] = condition_dict[subjID]
#     tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,0,0]
# df = pd.concat(tmp_dict.values(), axis=0)
# n_coef = Lmer(formula, data = df, family = family).fit().shape[0]


# # now we know the dimensions of the empty array we need to create to collect p_Values
# n_channels = len(channelsIdx)
# n_times = len(timesIdx)
# shape_1 = (n_channels, n_times, n_coef, n_iter)

# p_values = np.zeros(shape = shape_1)
# coefficients = np.zeros(shape = shape_1)
# z_values = np.zeros(shape = shape_1)
# coef_SD = np.zeros(shape = shape_1)
# OR = np.zeros(shape = shape_1)

# del tmp_dict, df


# for iteration in range(n_iter):
    
#     if equalise_accuracy:
#         # we sub-sample running the function below. which will give us a set of indices (idx)
#         # and later we subset the data by idx
#         idx = LogRegManager.random_subsample_accuracy()
#     else: # if no sub-sampling is asked for, just get every idx
#         idx = [i for i in range(len(pd.concat(condition_dict.values(), axis=0, ignore_index=True)))]
    
#     # And now we run the model for every channel and every timepoint
#     for thisChannel in channelsIdx:
#         print('>>>> running channel',thisChannel,'of', len(channelsIdx))
        
#         for tf in timesIdx:
               
#             # extract the data & trial information of each subject at a given timepoint and channel
#             tmp_dict = {}
#             for subjID in const.subjIDs:    
#                 tmp_dict[subjID] = condition_dict[subjID]
#                 tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,thisChannel,tf]

            
#             # Combine all subject's data into one dataframe so we can run the model on that
#             df = pd.concat(tmp_dict.values(), axis=0,ignore_index=True)
#             # re-Index because after combination the idx will be non-sequential
#             reIdx = pd.Series(range(len(df)))
#             df.set_index(reIdx, inplace = True)
#             df = df.iloc[idx]
#             del tmp_dict
            

#             # calculate Logit regression
#             md = Lmer(formula, data = df, family = family)
#             md.fit()
            
#             # TODO find out if I need anything else (i.e. random effects)
            
#             # record p-Values, z-Values and coefficients
#             p_values[thisChannel,tf,:, iteration] = md.coefs['P-val']
#             coefficients[thisChannel,tf,:, iteration] = md.coefs['Estimate']
#             coef_SD[thisChannel,tf,:, iteration] = md.coefs['SE']
#             z_values[thisChannel,tf,:, iteration] = md.coefs['Z-stat']
#             OR[thisChannel,tf,iteration] = md.coefs['OR']

            
#             currentChannelTimeIter = [thisChannel, tf, iteration]
#             idx = idx
            
# if n_iter == 1:  # reduce dimensions of output if no subsampling was performed
#     p_values = p_values[:,:,:,0]
#     coefficients = coefficients[:,:,:,0]
#     z_values = z_values[:,:,:,0]
#     coef_SD = coef_SD[:,:,:,0]
#     OR = OR[:,:,0]


# if equalise_accuracy: # get mean and sd of the p-Values across iterations
#     p_values_mean = p_values.mean(axis = 3)
#     p_values_SD = p_values.std(axis = 3)
# else:
#     pass

# count_cor = df['accuracy'].value_counts()[1]
# count_inc = df['accuracy'].value_counts()[0]
# metadata = {}
# metadata['n_correct/n_incorrect'] = (count_cor, count_inc)

# metadata['p_Values_index'] = md.coefs.index
# metadata['regression_formula'] = formula
# metadata['regression_type'] = family
# metadata['FDR_correction'] = False # This will change to True once the FDR is run
# metadata['axes'] = ['channel, timeframe, (coefficients), iteration']
# metadata['subsampling_iterations'] = n_iter
# metadata['subsampling_performed'] = equalise_accuracy
# metadata['degrees_of_freedom_Model'] = md.coefs.df_model
# # metadata['degrees_of_freedom_Residuals'] = mdf.coefs.df_resid # TODO
# metadata['n_observations_per_Regression'] = len(df)


# if equalise_accuracy:
#     metadata['subsample_length'] = len(df)

#%%

# idx = LogRegManager.random_subsample_accuracy()
# ch_names = LogRegManager.metadata['ch_names']
# data = data_dict['s001']

# reshaped_array = data.reshape(-1, data.shape[-1])
# reshaped_labels = np.repeat(ch_names, data.shape[0], axis=0)

# long_df = pd.DataFrame(reshaped_array)
# long_df.columns = [f'timeBin{i}' for i in range(reshaped_array.shape[-1])]
# long_df['label'] = reshaped_labels

#%% Run the model with
n_bins = 8
data_dict, condition_dict = LogRegManager.get_data(output = True, condition = "NV")
data_dict = LogRegManager.binTimes(n_bins = n_bins)

ch_names = LogRegManager.metadata['ch_names']

# And this will aggregate the df with time and electrode as a variable
dfs = []
for subjID in const.subjIDs:
    eeg_data = data_dict[subjID]
    condition_data = condition_dict[subjID].copy()
    reIdx = pd.Series(range(len(condition_data)))
    condition_data.set_index(reIdx, inplace = True)
    idx = LogRegManager.random_subsample_accuracy(trial_info=condition_data)
    for timepoint in range(n_bins):
        for i, thisChannel in enumerate(ch_names):
            df = condition_data.copy()
            df = df.iloc[idx]
            df['eeg_data'] = eeg_data[idx,i,timepoint]
            df['channel'] = thisChannel
            df['timeBin'] = str(timepoint)
            dfs.append(df)
aggregated_df = pd.concat(dfs, ignore_index=True)   

#To check if any combination of subjID, wordPosition and levels has 100% correct:
check_complete_separation = aggregated_df.groupby(['levels', 'subjID', 'wordPosition'])['accuracy'].mean().reset_index()

            
model = Lmer('accuracy ~ levels + eeg_data + (eeg_data|channel) + (eeg_data|timeBin) + wordPosition + (1|subjID)', data = aggregated_df, family = 'binomial')
model.fit()
