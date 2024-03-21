#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 08:42:13 2024

@author: testuser

This script contains variables that do not change across scripts, such as 
filepath-chunks, subject_IDs, and condition labels

These variables are called by Plotting_functions and Plotting_runner
"""

import os
# from glob import glob
# import pandas as pd

taskID = 'task-sin'
pipeID = 'pipeline-01'

thisDir = os.getcwd()
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data', 'SiN', 'derivatives_SM', taskID)
diroutput = dirinput 

fifFileEnd = 'resampled_ICA_rej_epo.fif'
freqPickleFileEnd = "_prestim_tfr_freqbands.pkl"
pValsPickleFileEnd = '.pkl'
evokedsPickleFileEnd = 'evokeds_allSubj_condition-separated.pkl'

# Get all subjIDs
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]


accuracy = ['Cor','Inc']
degradation = ['Lv1','Lv2','Lv3']
noise = ['SSN', 'NV']

# List all possible combinations of noise, degradation and accuracy, separated by /
conditions = [x + '/' + y + '/' + z for x in noise for y in degradation for z in accuracy]

factor_variables = ['accuracy', 'levels', 'noiseType', 'wordPosition', 'subjID']

