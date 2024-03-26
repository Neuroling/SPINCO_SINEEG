#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SKETCH / TRIAL SCRIPT FOR PreStim
===============================================================================
Created on Fri Feb  2 09:01:21 2024
@author: samuemu

This script is for spaghetti code - it is for trying things out and preliminary 
debugging before putting it in the *_functions or *_runner scripts.

It is largely disorganised and messy. 
"""
#%% Imports

import PreStim_constants as const
import PreStim_functions as function
PreStimManager = function.PreStimManager()

import os
from glob import glob
# import mne
import pandas as pd
import random
import numpy as np
import pickle
from datetime import datetime
from multiprocessing import Pool

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.formula.api as smf

from sklearn.model_selection import KFold

#%% more imports
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn import metrics

# import pymer4 
# from pymer4 import models
# from pymer4.models import lmer

# from rpy2.robjects.packages import importr, data
# from rpy2 import robjects
# from rpy2.robjects import pandas2ri
# base = importr("base")
# utils = importr("utils")
# read_csv = importr("read.csv")
# # utils.install_packages('lme4') # Only need to run this the first time to install lme4 package
# lme4 = importr("lme4")
# Matrix = importr('Matrix')

# # utils.update_packages()
# oo = base.options(repos = "https://cran.r-project.org/")
# utils.install_packages('Matrix')
# utils.install_packages('lme4', type = 'source')
# base.options(oo)
tmp = np.zeros(shape = (10,286))
for iteration in range(10):
    idx = PreStimManager.random_subsample_accuracy(trial_info = condition_df)         
    df = condition_df
    df = df.iloc[idx] # subset the df by idx
    tmp[iteration,:] = idx
    print(len(df))
#%% filepaths
# subjID = 's001'
# epo_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.fifFileEnd)), recursive=True)[0]
# freq_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.freqPickleFileEnd)), recursive=True)[0]


#%% Opening pickles
filepath = "/mnt/smbdir/Projects/Spinco/SINEEG/Data/SiN/derivatives_SM/task-sin/s001/s001_Logit_SSN_sub-sampled_100iter_uncorrected_allValues.pkl"
# filepath = const.dirinput + "/s003/s003_Logit_SSN_sub-sampled_1000iter_uncorrected_allValues.pkl"
with open(filepath, 'rb') as f:
    some_pVals = pickle.load(f)

# with open(freq_path, 'rb') as f:
#     tfr_bands = pickle.load(f)

#%% old code
    
# else:
#     #%% Open p-Values & evokeds ###############################################################################################
#     # TODO I need to change this now that we separated NoiseType and have different filenames
#     with open(const.diroutput + const.pValsPickleFileEnd, 'rb') as f:
#         p_values_FDR = pickle.load(f)
    
#     with open(const.diroutput + const.evokedsPickleFileEnd, 'rb') as f:
#         evokeds = pickle.load(f)


#% do some plots =============================================================================================================
# if doPlots:

    # pVals = p_values_FDR['p_values']     
    
# # Heatmaps for the parameters
#     plt.figure()
#     f, axs = plt.subplots(3, 3, figsize=(10, 8))   
#     # Iterate over the subplots, plot the heatmaps, and set the titles
#     for i in range(3):
#         for j in range(3):
#             sns.heatmap(pVals[:, :, i * 3 + j], vmin=0, vmax=0.15, ax=axs[i, j])
#             axs[i, j].set_title(p_values_FDR['metadata']['p_Values_index'][i * 3 + j])  # Set the title
#             axs[i,j].set(xlabel="times", ylabel="electrodes")
#     plt.subplots_adjust(hspace=0.5, wspace=0.5)
#     plt.show()
#     # TODO change electrode numbers in y-axis to labels like Fpz, Oz, etc
#     # TODO change times to seconds instead of tf

    
#     # sns.lineplot(data=p_values_FDR[1:10,1:10,3])

# #%% Amplitude Comparison of Accuracy ===========================================================================
# ## see https://neuraldatascience.io/7-eeg/erp_group_viz.html
    
#     roi = ['C3', 'Cz', 'C4', 
#            'P3', 'Pz', 'P4']
    
#     # Create a 3x2 grid of subplots
#     plt.figure()
#     fig, axs = plt.subplots(2,3, figsize=(20, 12))
    
#     # Loop through each combination of degradation and noise
#     for i, n in enumerate(const.noise):
#         for j, d in enumerate(const.degradation):
#             conditions = [n + '/' + d + '/' + a for a in const.accuracy]
#             evokeds_to_plot = [evokeds[condition] for condition in conditions]
    
#             # Plot the evokeds in the corresponding subplot
#             mne.viz.plot_compare_evokeds(
#                 evokeds_to_plot,
#                 combine='mean',
#                 legend='lower right',
#                 picks=roi,
#                 show_sensors='upper right',
#                 title=f'ERP ({n}/{d})',
#                 show = False, #If plotting multiple figures in one plot with MNE, set show = False and call plt.show() at the end
#                 axes=axs[i, j]  # Specify the subplot to use
#             )
    
#     # Adjust layout
#     # plt.tight_layout()
#     plt.show()



# #%% This section would run the above plots for every single electrode ============================================

# # for thisChannel in p_values_FDR['metadata']['ch_names']:
    
# #     # Create a 3x2 grid of subplots
# #     plt.figure()
# #     fig, axs = plt.subplots(2,3, figsize=(20, 12))
    
# #     # Loop through each combination of degradation and noise
# #     for i, n in enumerate(const.noise):
# #         for j, d in enumerate(const.degradation):
# #             conditions = [n + '/' + d + '/' + a for a in const.accuracy]
# #             evokeds_to_plot = [evokeds[condition] for condition in conditions]
    
# #             # Plot the evokeds in the corresponding subplot
# #             mne.viz.plot_compare_evokeds(
# #                 evokeds_to_plot,
# #                 combine='mean',
# #                 legend='lower right',
# #                 picks=thisChannel,
# #                 show_sensors='upper right',
# #                 title=f'{thisChannel} ({n}/{d})',
# #                 show = False, 
# #                 axes=axs[i, j]  # Specify the subplot to use
# #             )
    
# #     # Adjust layout
# #     # plt.tight_layout()
# #     plt.show()
    
# #%% topomap
#     evokeds_gAvg = PreStimManager.grandaverage_evokeds(evokeds)
    
#     # times_array = [-0.5, -0.4,-0.3,-0.2,-0.1,0]
    
#     for condition in const.conditions:
#         #f, axs = plt.subplots(1,10, figsize=(10, 8
#         # plt.figure()
#         fig = mne.viz.plot_evoked_topomap(
#             evokeds_gAvg[condition],
#             # times = times_array
#             )
#         # fig.suptitle(f'Topomaps for {condition}')
#         # plt.show()
     
#     for condition in const.conditions:
#         #f, axs = plt.subplots(1,10, figsize=(10, 8
#         # plt.figure()
#         fig = mne.viz.plot_evoked_topo(
#             evokeds_gAvg[condition],
#             title=f'{condition}'
#             )
#         # fig.suptitle(f'Topomaps for {condition}')
#         # plt.shSow()    


#%% logit regression preparation
# subjID = 's001'
# noise = 'NV'
# data_array, condition_df = PreStimManager.get_epoData_singleSubj(subjID, condition = noise, output=True)
# formula = "accuracy ~ levels * eeg_data + C(wordPosition)"
# # n_iter = 1
# # sub_sample = True

# # # #% Create arrays and lists
# # channelsIdx = [i for i in range(data_array.shape[1])] # list of channels
# # timesIdx = [i for i in range(data_array.shape[2])] #list of timepoints


# # # This will run a preliminary model, which is only used to extract the number of p-Values
# # # Which is needed to create an empty array for the p-Values

# # tmp_df = condition_df
# # tmp_df['eeg_data'] = data_array[:,0,0]
# # pVals_n = len(smf.logit(formula, tmp_df).fit().pvalues.index)
# # # del tmp_df

# # # now we know the dimensions of the empty array we need to create to collect p_Values
# # p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n))
# thisChannel = 0
# tf = 0
# df = condition_df
# df['eeg_data'] = data_array[:,thisChannel,tf]

#%% logistic regression with statsmodels

# # results = []

# formula = "accuracy ~ levels * eeg_data + noiseType + wordPosition "
# # # groups = 'subjID'

# md = smf.logit(formula, df)
# mdf = md.fit()
# mdf.summary()
# p_values = mdf.pvalues
# predicted = md.predict(mdf.params)

# pred_table = mdf.pred_table() 
# # # pred_table[i,j] refers to the number of times "i" was observed and the model predicted "j". 
# # # Correct predictions are along the diagonal.
# # results.append(formula)
# # results.append(mdf.prsquared)

#%% Most recent reproducible logistic regression (20.03.24)

# subjID = 's001'
# noise = 'NV'
# data_array, condition_df = PreStimManager.get_epoData_singleSubj(subjID, condition = noise, output=True)
# formula = "accuracy ~ levels * eeg_data + wordPosition" 
# n_iter = 3 
# N_chansTfs = 3

# #% Create arrays and lists
# channelsIdx = [i for i in range(data_array.shape[1])] # list of channels
# timesIdx = [i for i in range(data_array.shape[2])] #list of timepoints
# channelsIdx = channelsIdx[0:N_chansTfs]
# timesIdx = timesIdx[0:N_chansTfs]

# # This will run a preliminary model, which is only used to extract the number of p-Values
# # Which is needed to create an empty array for the p-Values
# tmp_df = pd.DataFrame()
  
# tmp_df = condition_df
# tmp_df['eeg_data'] = data_array[:,0,0]
# pVals_n = len(smf.logit(formula, 
#                         tmp_df
#                         ).fit().pvalues.index)
# del tmp_df

# # now we know the dimensions of the empty array we need to create to collect p_Values
# p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n,n_iter))
# coefficients = np.zeros(shape=p_values.shape)
# z_values = np.zeros(shape=p_values.shape)
# coef_CI = np.zeros(shape=p_values.shape)

# for iteration in range(n_iter):

#     idx = PreStimManager.random_subsample_accuracy()

#     # And now we run the model for every channel and every timepoint
#     for thisChannel in channelsIdx:

#         for tf in timesIdx:

#             # extract the data & trial information at a given timepoint and channel              
#             df = condition_df
#             df['eeg_data'] = data_array[:,thisChannel,tf]
#             df = df.iloc[idx] # subset the df by idx
                    
#             # calculate Logit regression
#             md = smf.logit(formula, 
#                            df, 
#                            )  
            
#             mdf = md.fit() # ??? Convergence warning
#             ## https://www.statsmodels.org/stable/generated/statsmodels.formula.api.logit.html
            
#             # record p-Values, z-Values and coefficients
#             p_values[thisChannel,tf,:, iteration] = mdf.pvalues
#             coefficients[thisChannel,tf,:, iteration] = mdf.params
#             coef_CI[thisChannel,tf,:, iteration] = mdf.conf_int()[1] - mdf.params
#             z_values[thisChannel,tf,:, iteration] = mdf.tvalues
 

# p_values_mean = p_values.mean(axis = 3)
# p_values_SD = p_values.std(axis = 3)


#%% k-fold crossvalidation -- unused, finished

# # Folds number
# n_splits = 5
# kf = KFold(n_splits=n_splits)

# # List of accuracy in a specific fold
# cv_scores = []

# # re-index df_nv because the indices are non-sequential
# reIdx = pd.Series(range(len(df)))
# df.set_index(reIdx, inplace = True)

# # Splitting data 
# for train_index, test_index in kf.split(df):
    
#     train_df = df.iloc[train_index]
#     test_df = df.iloc[test_index]
#     test_df_x = df.loc[test_index,['levels','eeg_data','wordPosition']]
#     # test_df_y = df.loc[test_index,['accuracy']]
    
#     md_split = smf.logit(formula, train_df)
#     mdf_split = md_split.fit()

#     # Forecasting on test data
#     y_pred = mdf_split.predict(exog=test_df_x)

#     # Quality of model assessment
#     # Determination coefficient R^2 is used
#     r_squared = np.corrcoef(test_df['accuracy'], y_pred)[0, 1] ** 2
#     cv_scores.append(r_squared)

# # Cross-validation results printing
# print("Cross-Validation Scores:", cv_scores)

#%% pool multiprocessing example -- for quick reference
# N = 5000
# import math

# def cube(x):
#     return math.sqrt(x)

# if __name__ == "__main__":
#     with Pool() as pool:
#       result = pool.map(cube, range(10,N))
#     print("Program finished!")
#%% parallel processing trial -- inefficient
# class Task:
#     def __init__(self, condition_df, data_array):
#         self.condition_df = condition_df
#         self.data_array = data_array
#         self.formula = "accuracy ~ levels * eeg_data + C(wordPosition)"
#         self.n_iter = 1

        
#     def doTask(self, tf):
#         df = self.condition_df  
#         # extract the data & trial information at a given timepoint and channel              
#         df['eeg_data'] = self.data_array[:,self.thisChannel,tf]
#         df = df.iloc[self.idx]
 
#         # calculate Logit regression
#         md = smf.logit(self.formula, df)  
        
#         mdf = md.fit()
#         return mdf.pvalues
    
#     def something(self):           
#         for iteration in range(self.n_iter):

#             self.idx = PreStimManager.random_subsample_accuracy()
#             # And now we run the model for every channel and every timepoint
#             for self.thisChannel in channelsIdx:
#                 # Task = Task(condition_df, data_array,idx, formula, thisChannel)
#                 if __name__ == "__main__":
#                     with Pool() as pool:
#                         p_values = pool.map(Task.doTask, timesIdx)
#         return p_values

# Task = Task(condition_df, data_array)  
# result = Task.something()      

            # record p-Values 
            # This adds the p-values to the values already present in the array at the specified location
            # for the first iteration, the array only contains 0s. Then, with every iteration, 
            # the array contains the sum of p-values of each channel and tf
            # and later we will get the mean by dividing by n_iter
            # p_values[thisChannel,tf,:] += mdf.pvalues


        

#%% heatmap plot
# pVals = some_pVals['p_values_mean']  
# index = some_pVals['metadata']['p_Values_index']
    
# # Heatmaps for the parameters
# plt.figure()
# f, axs = plt.subplots(3, 3, figsize=(10, 8))   
# # Iterate over the subplots, plot the heatmaps, and set the titles
# for i in range(3):
#     for j in range(3):
#         sns.heatmap(pVals[:, :, i * 3 + j], vmin=0, vmax=0.3, ax=axs[i, j])
#         axs[i, j].set_title(index[i * 3 + j])  # Set the title
#         axs[i,j].set(xlabel="times", ylabel="electrodes")
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()
    
    
    
#%% let's try the pymer4 logistic regression! -- Does not work.

# # run the model
# model = pymer4.models.lmer.lmer('accuracy ~ levels * eeg_data + wordPosition (1|subjID)', data = df, family = 'binomial')
# ## ImportError: cannot import name 'lmer' from 'pymer4.models' >:(
# # I don't know why it doesn't work. Circular dependency?
# # I am going to cry :(


#%% Try using rpy2 to use r code in python. Wish me luck. And strength. -- Does not work.


# ## Below: does not work :(
# # robjects.r('''glmer(accuracy ~ levels * eeg_data + wordPosition + (1|subjID), data = df, family = binomial)''')

# ## Issue: passing a pandas df directly to R's lme4 gives an error. I first need to convert it into an robjects.vectors.DataFrame
# with (robjects.default_converter + pandas2ri.converter).context():
#   df_r = robjects.conversion.get_conversion().py2rpy(df)

# with (robjects.default_converter + pandas2ri.converter).context():
#   df_summary = base.summary(df_r)
# print(df_summary)

# ## next issue: now I will need to recode the factors from chr to factor
# for col_name in const.factor_variables:
#     col_index = list(df_r.colnames).index(col_name)
#     col = robjects.vectors.FactorVector(df_r.rx2(col_name))
#     df_r[col_index] = col
    
# with (robjects.default_converter + pandas2ri.converter).context():
#   df_summary = base.summary(df_r)
# print(df_summary)


# model = lme4.glmer('accuracy ~ levels * eeg_data + wordPosition + (1|subjID)', data = df_r, family = 'binomial')
# # RRuntimeError: Error in initializePtr() :   function 'chm_factor_ldetL2' not provided by package 'Matrix'
# # apparently, the Matrix package does not support binary data.
# # usually, updating lme4 to the newest version would help, but using 
# # `utils.update_packages()` does not work (see screenshot 7.3.24 10.47)
# # https://stackoverflow.com/questions/77481539/error-in-initializeptr-function-cholmod-factor-ldeta-not-provided-by-pack
# # The solution here did not help
# # I also tried to 

# something = robjects.r(
#     """
#     head(df_r)
#     df_r$accuracy <- factor(df_r$accuracy)
#     df_r$levels <- factor(df_r$levels)
#     df_r$noiseType <- factor(df_r$noiseType)
#     df_r$wordPosition <- factor(df_r$wordPosition)
#     df_r$subjID <- factor(df_r$subjID)
    
#     model <- glmer(accuracy ~ levels * eeg_data + wordPosition + (1|subjID), data = df_r, family = binomial)
#     summary(model)
#     """)

# ## This works with no problems in R
# """
# library(lme4)
# setwd("Y:/Projects/Spinco/SINEEG/Data/SiN/derivatives_SM/task-sin/PreStim")
# df_r<-read.csv("testing_df.csv",header=T, sep=',')
# head(df_r)
# str(df_r)
# df_r$accuracy <- factor(df_r$accuracy)
# df_r$levels <- factor(df_r$levels)
# df_r$noiseType <- factor(df_r$noiseType)
# df_r$wordPosition <- factor(df_r$wordPosition)
# df_r$subjID <- factor(df_r$subjID)

# model <- glmer(accuracy ~ levels * eeg_data + wordPosition + (1|subjID), data = df_r, family = binomial)
# summary(model)
# """

#%% Random/ jackknife resample -- Incorporated as PreStimManager.random_subsample_accuracy()
# # n_iter = 10

# stacked_cond_df = pd.concat(condition_df.values(), axis=0, ignore_index=True)
# # counting total correct and incorrect
# count_cor = stacked_cond_df['accuracy'].value_counts()[1]
# count_inc = stacked_cond_df['accuracy'].value_counts()[0]

# idx_cor = stacked_cond_df.index[stacked_cond_df['accuracy'] == 1]
# idx_inc = stacked_cond_df.index[stacked_cond_df['accuracy'] == 0]

# minimum = min(count_cor, count_inc)
# tmp_idx = random.sample(list(idx_cor), minimum) + random.sample(list(idx_inc), minimum)

# subsampled_df = stacked_cond_df.iloc[tmp_idx]

#%% Account for uneven trial numbers of levels, wordPosition, subjID in random subsample -- Inefficient, with comment
# stacked_cond_df = pd.concat(condition_dict.values(), axis=0, ignore_index=True)

# # get all column names
# col_names = list(stacked_cond_df.columns)

# # this gives us the indexes of each condition
# indexes={} # empty dict
# for col in col_names: # for every column name
#     # indexes[col] = {} # create an empty dict within the indexes-dict
#     for UniqueVal in list(stacked_cond_df[col].unique()): # For each unique value, get the indexes of all trials with that value
#         indexes[str(col+ '_' + str(UniqueVal))] = list(stacked_cond_df[col].index[stacked_cond_df[col]==UniqueVal])

"""  
next we would need to get the minimum number of cor & inc of each combination of subjID, levels, wordPosition
and then select that many trials from every combination of accuracy, subjID, levels and wordPosition.
But that's not possible since some subj are 100% correct on some of those combinations.
Even when not accounting for word position, and only for subjID and levels - roughly a fourth of combinations are >90% correct,
meaning that accounting for accuracy, subjID and levels for the sub-sampling will give us only about 10% of the data for each sample
"""

# newdf = stacked_cond_df.drop(labels=['wordPosition','noiseType', 'levels'], axis = 1, inplace = False)
# tmp = newdf.groupby(['subjID']).sum() # when only accounting for subjID
# max(tmp['accuracy']) 
"""
530 correct out of 576. Which would mean we would sub-sample 46 correct and incorrect trials of every subj
for a total of 1288 (46*2*14) trials per sub-sample. We would reduce the dataset by a sixth of its size.
Only accounting for accuracy results in a sub-sample of 2924 trials - reducing the dataset by a third of its size
"""

#%% Creating a dict of dicts to store the mdf -- Unfinished
# result_dict = {key1: {key2: None for key2 in metadata['ch_names']} for key1 in metadata['times']}




#%% CREATING EVOKEDS -- Incorporated as PreStimManager.get_evokeds() - with comment
# """
# But we need the evoked separately for each condition we want to include.
# For example, if we want to look at how degradation levels affect accuracy, 
# we would need to create 3*2 evoked arrays. Doing this manually is a lot of work.

# epochs.average(by_event_type) would create evoked arrays for every event type
# but we have 288 event types and some of them don't matter, so that is not feasible.
# (I.e. we do not need to create separate evoked objects for male/female voices right now)

# But! Here is the source code for that: 
#     https://github.com/mne-tools/mne-python/blob/maint/1.6/mne/epochs.py#L1060-L1110
 
#     evokeds = list()
#     for event_type in epochs.event_id.keys():
#             ev = epochs[event_type]._compute_aggregate(picks=picks, mode=method)
#             ev.comment = event_type
#             evokeds.append(ev)
    
#     Meaning basically, if I create a dict of what conditions I want to split the data into,
#     and then use that in place of epochs.event_id.keys() - that would work.
#     I can put that into a function.

# """
# accuracy = ['Cor','Inc']
# degradation = ['Lv1','Lv2','Lv3']
# noise = ['NV','SSN']

# # creating a list of every possible combination of accuracy, noise & degradation, separated by /
# conditions = [x + '/' + y + '/' + z for x in noise for y in degradation for z in accuracy]

# # This gives us a dict containing a lists for every condition, which contain evoked arrays for every subject
# evokeds = {condition : [] for condition in conditions}
# for subjID in const.subjIDs:
#     epo_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.fifFileEnd)), recursive=True)[0]
#     epo = mne.read_epochs(epo_path)
#     for event_type in conditions:
#             evokeds[event_type].append(epo[event_type]._compute_aggregate(picks=None))


# with open(const.diroutput + const.evokedsPickleFileEnd, 'wb') as f:
#     pickle.dump(evokeds, f)
# print("saving...........................................................................")

# Below: not working yet # TODO
# n_trial_per_condition = pd.DataFrame([[i , evokeds[i].nave] for i in evokeds ])

#%% some plots

# # Visualising global amplitude
# evo_inc.plot(gfp=True, spatial_colors=True)
# evo_cor.plot(gfp=True, spatial_colors=True)

# # Comparing amplitude between conditions
# evokeds=dict(cor=evo_cor, inc=evo_inc)
# picks = [1] #which electrode to compare - if None, will compare GFP
# mne.viz.plot_compare_evokeds(evokeds, picks=picks, combine="mean")

# # And here with confidence intervals
# evokeds = dict(
#     cor=list(epo["Cor"].iter_evoked()),
#     inc=list(epo["Inc"].iter_evoked()),
# )
# mne.viz.plot_compare_evokeds(evokeds, combine="mean", picks=None)
# ## Hm... that's interesting. For subj s001, the GFP before correct trials is way less varied / more stable.
# ## ... actually, that reflects the unequal number of trials per condition (918 correct, 234 incorrect)

# # We can also combine evokeds!
# inc_minus_cor = mne.combine_evoked([evo_inc, evo_cor], weights = [1, -1])
# inc_minus_cor.plot(gfp=True, spatial_colors=True)
# inc_minus_cor.plot_joint()




# #%% to dataframe
# epo_df = epo.to_data_frame(copy=False)


# #%%
# df_long # Should have the columns Accuracy, Noise, Degradation, [Every electrode] and the rows as timepoints (128 * 2 * 3 * 2)
# #md = smf.mixedlm("accu ~ noise * levels", df_long, groups = df_long["subj"]) 
# #md = smf.mixedlm("accu ~ noise * levels * itemType", df_long, groups = df_long["subj"]) 
# #mdf = md.fit()