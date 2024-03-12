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
from multiprocessing import Pool

import matplotlib.pyplot as plt

import statsmodels.formula.api as smf

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

#%% filepaths
# subjID = 's001'

# epo_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.fifFileEnd)), recursive=True)[0]

# pickle_path_in = os.path.join(dirinput[:dirinput.find(
#     'derivatives/')] + 'analysis', 'eeg', const.taskID,'features',subjID,subjID + const.inputPickleFileEnd)

#%% Old LMM on tfr_band
# print('opening dict:',pickle_path_in)
# with open(pickle_path_in, 'rb') as f:
#     tfr_bands = pickle.load(f)
    



# #%% create frequency dataset to run the LMM on
# df = tfr_bands['epoch_metadata'] # get trial information 
# df['data'] = tfr_bands['Alpha_data'][:,0,0] # get data of all trials, at electrode 0, and at timepoint 0
# df['subjID'] = [subjID for i in range(len(df))] # Put in a column with the subject ID


# #%%
# """
# Okay so this is a first draft. A bad one.

# It takes a long time to open the pickled dict. Every single analysis takes a full minute to run
# because it takes so long to open the dict.

# We need to run this analysis for every electrode and every timepoint.
# The Theta band has the lowest number of timepoints, 136.
# For only the theta band, this script would be complete in 145 hours (6 days).
# And we would need to run this for every single freq band.

# Which means that this script is so ridiculously badly optimised, that it is almost funny.

# #%% Create arrays and lists
# thisBand = 'Theta'
# channels = [i for i in range(64)]
# times = [i for i in range(len(tfr_bands[str(thisBand+"_COI_times")]))]

# p_values = np.zeros(shape=(len(channels),len(times),9))

# #%% And now the big loop...

# for thisChannel in channels:
#     for tf in times:
           
#         # Create df with the relevant data
#         tmp = {}
#         for subjID in const.subjIDs:
#             pickle_path_in = os.path.join(const.thisDir[:const.thisDir.find(
#                 'Scripts')] + 'Data', 'SiN','analysis', 'eeg', const.taskID,'features',subjID,subjID + const.inputPickleFileEnd)
            
#             print('opening dict:',pickle_path_in)
#             with open(pickle_path_in, 'rb') as f:
#                 tfr_bands = pickle.load(f)
                
#             df = tfr_bands['epoch_metadata']
#             df['data'] = tfr_bands[str(thisBand+'_data')][:,thisChannel,tf]
        
#             del tfr_bands
            
#             # re-code and delete unneeded data
#             df['subjID'] = [subjID for i in range(len(df))]
#             df['levels'].replace('Lv1', 1, inplace=True)
#             df['levels'].replace('Lv2', 2, inplace=True)
#             df['levels'].replace('Lv3', 3, inplace=True)
#             df['accuracy'].replace('inc', 0, inplace=True)
#             df['accuracy'].replace('cor', 1, inplace=True)
#             df['block'].replace('NV', 0, inplace=True)
#             df['block'].replace('SSN', 1, inplace=True)
#             df.drop(labels=['tf','stim_code','stimtype','stimulus','voice'], axis = 1, inplace = True)
            
#             tmp[subjID]=df
#             del df
        
#         # Combine all subject's data to one df
#         df = pd.concat(tmp.values(), axis=0)
#         del tmp
        
#         # calculate LMM
#         md = smf.mixedlm("accuracy ~ levels * data * block", df, groups = df["subjID"]) 
#         del df
        
#         # record p-Values
#         p_values[thisChannel,tf,:] = md.fit().pvalues
#         del md
  
# """

# #%% Alright! Let's optimise!

# #%% Create arrays and lists
# thisBand = 'Theta'
# channels = [i for i in range(64)] # list of channels
# times = [i for i in range(len(tfr_bands[str(thisBand+"_COI_times")]))] #list of timepoints

# p_values = np.zeros(shape=(len(channels),len(times),9)) # empty array for the p_values

# #%% First, create a dict of all subj data of thisBand to store in the memory
# data_dict = {}
# metadata_dict = {}

# for subjID in const.subjIDs:
#     pickle_path_in = os.path.join(const.thisDir[:const.thisDir.find(
#         'Scripts')] + 'Data', 'SiN','analysis', 'eeg', const.taskID,'features',subjID,subjID + const.inputPickleFileEnd)
    
#     print('opening dict:',pickle_path_in)
#     with open(pickle_path_in, 'rb') as f:
#         tfr_bands = pickle.load(f)
    
#     data_dict[subjID]=tfr_bands[str(thisBand+'_data')]
#     metadata_dict[subjID] = tfr_bands['epoch_metadata']
    
#     # re-code and delete unneeded data
#     metadata_dict[subjID]['subjID'] = [subjID for i in range(len(metadata_dict[subjID]))]
#     metadata_dict[subjID]['levels'].replace('Lv1', 1, inplace=True)
#     metadata_dict[subjID]['levels'].replace('Lv2', 2, inplace=True)
#     metadata_dict[subjID]['levels'].replace('Lv3', 3, inplace=True)
#     metadata_dict[subjID]['accuracy'].replace('inc', 0, inplace=True)
#     metadata_dict[subjID]['accuracy'].replace('cor', 1, inplace=True)
#     metadata_dict[subjID]['block'].replace('NV', 0, inplace=True)
#     metadata_dict[subjID]['block'].replace('SSN', 1, inplace=True)
#     metadata_dict[subjID].drop(labels=['tf','stim_code','stimtype','stimulus','voice'], axis = 1, inplace = True)
    
#     del tfr_bands



# #%% And now loop over that...

# for thisChannel in channels:
#     print('running channel',thisChannel,'of', len(channels))
    
#     for tf in times:
           
#         # the data & trial information of each subject at a given timepoint and channel
#         tmp_dict = {}
#         for subjID in const.subjIDs:    
#             tmp_dict[subjID] = metadata_dict[subjID]
#             tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,thisChannel,tf]

        
#         # Combine all subject's data into one dataframe so we can run the LMM on that
#         df = pd.concat(tmp_dict.values(), axis=0)
#         del tmp_dict
        
#         # calculate LMM
#         md = smf.mixedlm("accuracy ~ levels * eeg_data * block", df, groups = df["subjID"])        
#         mdf = md.fit()
        
#         # record p-Values
#         p_values[thisChannel,tf,:] = mdf.pvalues
        
# index_p_values = mdf.pvalues.index
# formula_LMM = md.formula


# #%%
# md = smf.mixedlm("accuracy ~ levels + eeg_data + block", df, groups = df["subjID"]) 
# mdf = md.fit()
# print(mdf.summary())
# print(mdf.pvalues)
# pvals = mdf.pvalues.index

# #%%

# md2 = smf.mixedlm('accuracy ~ eeg_data + levels * block', groups = 'subjID', data = df)
# mdf2 = md2.fit()
# print(mdf2.summary())


#%%###################################################################################################################
# data_dict, condition_dict = PreStimManager.get_data(output = True, condition = "NV")

# ## prepare the data
# tmp_dict = {}
# for subjID in const.subjIDs:    
#     tmp_dict[subjID] = condition_dict[subjID]
#     tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,0,0]
# df = pd.concat(tmp_dict.values(), axis=0, ignore_index=True)
# del tmp_dict

#%%
N = 5000
import math

def cube(x):
    return math.sqrt(x)

if __name__ == "__main__":
    with Pool() as pool:
      result = pool.map(cube, range(10,N))
    print("Program finished!")
#%%
subjID = 's001'
noise = 'NV'
data_array, condition_df = PreStimManager.get_data_singleSubj(subjID, condition = noise, output=True)
formula = "accuracy ~ levels * eeg_data + C(wordPosition)"
n_iter = 1
sub_sample = True

reIdx = pd.Series(range(len(condition_df)))
condition_df.set_index(reIdx, inplace = True)

# #% Create arrays and lists
channelsIdx = [i for i in range(data_array.shape[1])] # list of channels
timesIdx = [i for i in range(data_array.shape[2])] #list of timepoints


# This will run a preliminary model, which is only used to extract the number of p-Values
# Which is needed to create an empty array for the p-Values

tmp_df = condition_df
tmp_df['eeg_data'] = data_array[:,0,0]
pVals_n = len(smf.logit(formula, tmp_df).fit().pvalues.index)
# del tmp_df

# now we know the dimensions of the empty array we need to create to collect p_Values
p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n))

#%%
class Task:
    def __init__(self, condition_df, data_array):
        self.condition_df = condition_df
        self.data_array = data_array
        self.formula = "accuracy ~ levels * eeg_data + C(wordPosition)"
        self.n_iter = 1

        
    def doTask(self, tf):
        df = self.condition_df  
        # extract the data & trial information at a given timepoint and channel              
        df['eeg_data'] = self.data_array[:,self.thisChannel,tf]
        df = df.iloc[self.idx]
 
        # calculate Logit regression
        md = smf.logit(self.formula, df)  
        
        mdf = md.fit()
        return mdf.pvalues
    
    def something(self):           
        for iteration in range(self.n_iter):

            self.idx = PreStimManager.random_subsample_accuracy()
            # And now we run the model for every channel and every timepoint
            for self.thisChannel in channelsIdx:
                # Task = Task(condition_df, data_array,idx, formula, thisChannel)
                if __name__ == "__main__":
                    with Pool() as pool:
                        p_values = pool.map(Task.doTask, timesIdx)
        return p_values

Task = Task(condition_df, data_array)  
result = Task.something()      

            # record p-Values 
            # This adds the p-values to the values already present in the array at the specified location
            # for the first iteration, the array only contains 0s. Then, with every iteration, 
            # the array contains the sum of p-values of each channel and tf
            # and later we will get the mean by dividing by n_iter
            # p_values[thisChannel,tf,:] += mdf.pvalues


        
#%% TRASH
#         for iteration in range(n_iter):
#             # print(str(iteration) + "---------------------------------------------")
            
#             if sub_sample:
#                 # we sub-sample running the function below. which will give us a set of indices (idx)
#                 # and later we subset the data by idx
#                 self.idx = self.random_subsample_accuracy()
#             else: # if no sub-sampling is asked for, just get every idx
#                 self.idx = [ids for ids in range(len(condition_df))]
            
#             # And now we run the model for every channel and every timepoint
#             for self.thisChannel in channelsIdx:
                
#                 for tf in timesIdx:
                    
#                     def do_regression_timewise(self,tf):
#                         # extract the data & trial information at a given timepoint and channel              
#                         df = self.condition_df # TODO need to change this in case condition_df is provided
#                         df['eeg_data'] = self.data_array[:,self.thisChannel,tf]
    
#                         df = df.iloc[self.idx] # subset the df by idx
    
                        
                        
#                         # calculate Logit regression
#                         md = smf.logit(formula, 
#                                        df, 
#                                        )  
                        
#                         mdf = md.fit() # ??? Convergence warning
#                         ## https://www.statsmodels.org/stable/generated/statsmodels.formula.api.logit.html
                    
#                     # record p-Values 
#                     # This adds the p-values to the values already present in the array at the specified location
#                     # for the first iteration, the array only contains 0s. Then, with every iteration, 
#                     # the array contains the sum of p-values of each channel and tf
#                     # and later we will get the mean by dividing by n_iter
#                     p_values[self.thisChannel,tf,:] += mdf.pvalues
 
        
#         if sub_sample: # get mean and sd of the p-Values across iterations
#             p_values_mean = p_values / n_iter
#             self.p_values_SD = np.sqrt(p_values_mean - np.square(p_values_mean))
#             self.p_values = p_values_mean

#         else:
#             self.p_values = p_values

        
        
#         self.metadata['p_Values_index'] = mdf.pvalues.index
#         self.metadata['regression_formula'] = self.formula
#         self.metadata['regression_groups'] = "NONE" 
#         self.metadata['regression_type'] = str(mdf.model)
#         self.metadata['FDR_correction'] = False # This will change to True once the FDR is run
#         self.metadata['axes'] = ['channel, timeframe, p-Value']
#         self.metadata['iterations'] = n_iter
#         self.metadata['equalized_accuracy_sample'] = sub_sample
        
#         if sub_sample:
#             self.metadata['sub_sample_dataframe_length'] = len(df)
        
        
#         return p_values
    
        
#     def do_regression_timewise(self,tf):
#         # extract the data & trial information at a given timepoint and channel              
#         df = self.condition_df # TODO need to change this in case condition_df is provided
#         df['eeg_data'] = self.data_array[:,self.thisChannel,tf]

#         df = df.iloc[self.idx] # subset the df by idx

        
        
#         # calculate Logit regression
#         md = smf.logit(formula, 
#                        df, 
#                        )  
        
#         mdf = md.fit() # ??? Convergence warning
#         ## https://www.statsmodels.org/stable/generated/statsmodels.formula.api.logit.html
#%% Opening a pickle
# filepath = "/mnt/smbdir/Projects/Spinco/SINEEG/Data/SiN/derivatives_SM/task-sin/s001/s001_Logit_NV_FDR_pValues.pkl"
# with open(filepath, 'rb') as f:
#     some_pVals = pickle.load(f)
    
#%% let's try the pymer4 logistic regression!

# # run the model
# model = pymer4.models.lmer.lmer('accuracy ~ levels * eeg_data + wordPosition (1|subjID)', data = df, family = 'binomial')
# ## ImportError: cannot import name 'lmer' from 'pymer4.models' >:(
# # I don't know why it doesn't work. Circular dependency?
# # I am going to cry :(


#%% Try using rpy2 to use r code in python. Wish me luck. And strength.


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

#%% Random/ jackknife resample
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

#%% How to account for uneven trial numbers of levels, wordPosition, subjID as a result of the above
# stacked_cond_df = pd.concat(condition_dict.values(), axis=0, ignore_index=True)

# # get all column names
# col_names = list(stacked_cond_df.columns)

# # this gives us the indexes of each condition
# indexes={} # empty dict
# for col in col_names: # for every column name
#     # indexes[col] = {} # create an empty dict within the indexes-dict
#     for UniqueVal in list(stacked_cond_df[col].unique()): # For each unique value, get the indexes of all trials with that value
#         indexes[str(col+ '_' + str(UniqueVal))] = list(stacked_cond_df[col].index[stacked_cond_df[col]==UniqueVal])
   
# # next we would need to get the minimum number of cor & inc of each combination of subjID, levels, wordPosition
# # and then select that many trials from every combination of accuracy, subjID, levels and wordPosition
# # but that's not possible since some subj are 100% correct on some of those combinations.
# # even when not accounting for word position, and only for subjID and levels - roughly a fourth of combinations are >90% correct
# # meaning that accounting for accuracy, subjID and levels for the sub-sampling will give us only about 10% of the data for each sample

# newdf = stacked_cond_df.drop(labels=['wordPosition','noiseType', 'levels'], axis = 1, inplace = False)
# tmp = newdf.groupby(['subjID']).sum() # when only accounting for subjID
# max(tmp['accuracy']) 
# # 530 correct out of 576. Which would mean we would sub-sample 46 correct and incorrect trials of every subj
# # for a total of 1288 trials per sub-sample. We would reduce the dataset by a sixth of its size.
# # Only accounting for accuracy results in a sub-sample of 2924 trials - reducing the dataset by a third of its size

#%% Creating a dict of dicts to store the mdf
# result_dict = {key1: {key2: None for key2 in metadata['ch_names']} for key1 in metadata['times']}


#%% Let's try the logistic regression with statsmodels

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

#%%  CREATING EVOKEDS #########################################################################################################
# """
# But we need the evoked separately for each condition we want to include.
# For example, if we want to look at how degradation levels affect accuracy, 
# we would need to create 3*2 evoked arrays. Doing this manually is a lot of work.

# epochs.average(by_event_type) would create evoked arrays for every event type
# but we have 288 event types and some of them don't matter, so that is not feasible.

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