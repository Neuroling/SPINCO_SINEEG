#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RUNNER SCRIPT FOR PreStim
===============================================================================
Created on Fri Feb  2 09:01:21 2024
@author: samuemu

This is the runner script for the Pre-Stimulus analyses.

It calls the functions from PreStim_functions. To do this, it is necessary to
first initialize the class by calling `PreStimManager = PreStimManager()`

This script and the functions script requires the PreStim_constants script,
which contains variables used across scripts and functions, such as filepath chunks
or condition labels.

Input files:
    - epoched data from MNE *epo.fif
        - Handled entirely by PreStimManager
        - The filepaths are in PreStim_constants and adpted to each subject by PreStimManager.
        
Output files:
    - p-Values array as .pkl
        - A dict containing the array of p-Values as well as the metadata. 
        - The metadata contains information on how the p-Values were computed, including the
          type of regression (logit or LMM), regression formula, FDR-correction, etc.
        - p-Values are saved by calling PreStimManager.save_pValues()
        - This can be done regardless of regression type (logit or LMM) or FDR-correction.
        - The output filepath is in PreStim_constants and adapted to each case by PreStimManager.
        
    - evokeds dict as .pkl
        - A dict which has all possible combinations of accuracy, noiseType & degradation
          as keys, which each have the corresponding value of a list containing the evoked arrays
          of every subject. 
        - In other words: A dict of evoked arrays for every combination of subjID, accuracy, noiseType & degradation
        - They are created and saved by calling PreStimManager.get_evokeds().
        - The output filepath is in PreStim_constants.
        

"""


#%% Imports ###################################################################################################################
import os
from glob import glob
import mne

import statsmodels.formula.api as smf
import statsmodels.stats.multitest as ssm
import statsmodels.base.optimizer as smo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from datetime import datetime

import PreStim_constants as const
from PreStim_functions import PreStimManager
PreStimManager = PreStimManager(warnings=True) #initiate PreStimManager (collection of functions)

start_time = datetime.now() # recording the time when the script starts running (helpful for debugging, optimisation and control)

#%% Run regression and save Output #############################################################################################
time_control = []

for noise in const.noise: # separately for each noiseType
# for noise in ['SSN']: # for debugging, only run one condition
    for subjID in const.subjIDs:
        time_control.append("start " + subjID + ": " + str(datetime.now()))
        
        PreStimManager.get_epoData_singleSubj(subjID, condition = noise) # Get epoched data in a format usable for regression
        PreStimManager.run_LogitRegression_withinSubj() # run the regression separately for each timepoint & channel  
        # PreStimManager.FDR_correction() # FDR correct the p-Values (separately for each channel & parameter)
        PreStimManager.save_results() # save the output dict and return it

#%% get evoked objects for every subj of every possible combination of accuracy, noiseType & degradation
# evokeds = PreStimManager.get_evokeds()


end_time = datetime.now()    # To record the time of when the script finishes running
    

