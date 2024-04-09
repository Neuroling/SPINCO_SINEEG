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

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.formula.api as smf

from sklearn.model_selection import KFold

import pymer4 
from pymer4 import models
from pymer4.models import Lmer

#%% Run regression and save Output #############################################################################################
# """
# time_control = []
# for noise in const.noise: # separately for each noiseType
# # for noise in ['SSN']: # for debugging, only run one condition
#     for subjID in const.subjIDs:
#         time_control.append("start " + subjID + ": " + str(datetime.now()))
#         PreStimManager.run_LogitRegression_withinSubj(n_iter = 100, debug = False)
#         PreStimManager.run_LogitRegression_withinSubj() # run the regression separately for each timepoint & channel  
#         # PreStimManager.FDR_correction() # FDR correct the p-Values (separately for each channel & parameter)
#         PreStimManager.save_results() # save the output dict and return it
# """

noise = 'NV'
subjID = 's005'

data_array, condition_df = PreStimManager.get_epoData_singleSubj(subjID = subjID, condition = noise, output = True) # Get epoched data in a format usable for regression

# p_values = PreStimManager.run_LogitRegression_withinSubj(n_iter = 100, debug = True)
# p_values_mean = p_values.mean(axis = 3)
#%%

formula = "accuracy ~ levels * eeg_data + wordPosition"
n_iter = 3
subsample = True

#% Create arrays and lists
channelsIdx = [i for i in range(data_array.shape[1])] # list of channels
timesIdx = [i for i in range(data_array.shape[2])] #list of timepoints
channelsIdx = channelsIdx[0:3]
timesIdx = timesIdx[0:3]

# This will run a preliminary model, which is only used to extract the number of p-Values
# Which is needed to create an empty array for the p-Values
tmp_df = pd.DataFrame()
  
tmp_df = condition_df.copy()
tmp_df['eeg_data'] = data_array[:,0,0]
pVtmp = smf.logit(formula, tmp_df)
pVals_n = len(smf.logit(formula, 
                        tmp_df
                        ).fit().pvalues.index)
del tmp_df

# # now we know the dimensions of the empty array we need to create to collect p_Values
p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n,n_iter))
coefficients = np.zeros(shape=p_values.shape)
z_values = np.zeros(shape=p_values.shape)
coef_SD = np.zeros(shape=p_values.shape)
converged = np.zeros(shape=p_values.shape)


for iteration in range(n_iter):

    if subsample:
        # we sub-sample running the function below. which will give us a set of indices (idx)
        # and later we subset the data by idx
        idx = PreStimManager.random_subsample_accuracy()

    else: # if no sub-sampling is asked for, just get every idx
        idx = [ids for ids in range(len(condition_df))]


    # And now we run the model for every channel and every timepoint
    for thisChannel in channelsIdx:

        for tf in timesIdx:

            # extract the data & trial information at a given timepoint and channel              
            df = condition_df
            df['eeg_data'] = data_array[:,thisChannel,tf]
            df = df.iloc[idx] # subset the df by idx
            
            
            # calculate Logit regression
            md = smf.logit(formula, 
                            df, 
                            )


            
            mdf = md.fit() # ??? don't know what the correct solver is
            break # only run one iteration # !!!
            
#             # record p-Values, z-Values and coefficients
#             p_values[thisChannel,tf,:, iteration] = mdf.pvalues
#             coefficients[thisChannel,tf,:, iteration] = mdf.params
#             coef_SD[thisChannel,tf,:, iteration] = mdf.conf_int()[1] - mdf.params
#             z_values[thisChannel,tf,:, iteration] = mdf.tvalues
#             converged[thisChannel,tf,:, iteration] = mdf.converged
 

# if subsample: # get mean and sd of the p-Values across iterations
#     p_values_mean = p_values.mean(axis = 3)
#     p_values_SD = p_values.std(axis = 3)
# else:
#     pass
# mdf = md.fit(method = 'powell',maxiter = 1000)

#%% compare fitting methods

# methods = ['newton','nm','bfgs','lbfgs','cg','ncg','powell','basinhopping','minimize']
# index=list(mdf.pvalues.index)
# index.append('converged')
# temp_pVal_df = pd.DataFrame(index=index)
# temp_coef_df = temp_pVal_df.copy()
# temp_converged = []
# for method in methods:
#     mdf = md.fit(method = method, maxiter = 500)
#     pVals = list(mdf.pvalues)
#     coef = list(mdf.params)
#     pVals.append(int(mdf.converged))
#     coef.append(int(mdf.converged))
#     temp_pVal_df[method] = pVals
#     temp_coef_df[method] = coef
#     temp_converged.append(mdf.converged)
#     # print(method)
#     # mdf.summary()

#%% Opening pickles
# filepath = "/mnt/smbdir/Projects/Spinco/SINEEG/Data/SiN/derivatives_SM/task-sin/s001/s001_Logit_Alpha_SSN_sub-sampled_10iter_uncorrected_allValues.pkl"
# filepath = const.dirinput + "/s003/s003_Logit_Alpha_NV_FDR_allValues.pkl"
# with open(filepath, 'rb') as f:
#     some_pVals = pickle.load(f)

#%% filepaths
# subjID = 's001'
# epo_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.fifFileEnd)), recursive=True)[0]
# freq_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.freqPickleFileEnd)), recursive=True)[0]

