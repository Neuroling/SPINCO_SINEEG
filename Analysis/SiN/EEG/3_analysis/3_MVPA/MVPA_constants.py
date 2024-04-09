#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTANTS FOR MVPA SCRIPTS
===============================================================================
@author: samuemu
Created on Fri Dec  8 12:23:55 2023

This script contains constants that are used across functions and scripts.
It is called by MVPA_functions and MVPA_runner

"""

import os
# from glob import glob
# import pandas as pd
# import numpy as np

taskID = 'task-sin'
pipeID = 'pipeline-01'
fifFileEnd = '_avg-epo.fif'
setFileEnd = '_epoched_2.set'
inputPickleFileEnd = '_tfr_freqbands.pkl'
outputPickleFileEnd = '_tfr_freqbands_crossval.pkl'


thisDir = os.getcwd()
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]

n_jobs = -1
#% Number of jobs to run in parallel. 
#% n_jobs = None means sequential processing. 
#% n_jobs = -1 means using all processors (so n_jobs is = number of processors)

freqbands = dict(#Delta = [1,4], # Our TFR covers frequencies from 6-48
                 Theta = [4,8],
                 Alpha=[8,13], 
                 Beta= [13,25],
                 Gamma =[25,48])

degradationType = ['NV', 'SSN']
degradationLevel = ['Lv1', 'Lv2', 'Lv3']
wordPosition = ['Call', 'Col', 'Num']

# TODO update
codebook={'*_COI_times':'timepoints inside the COI in frequency band *',
          '*_crossval_FullEpoch':'The crossvalidation scrores on the whole epoch for frequency band *. There are 5 because the crossvalidation is repeated 5 times',
          '*_crossval_timewise_mean':'The mean of the 5 crossvalidation scores for each timepoint in frequency band *',
          '*_crossval_timewise_std':'The standard deviation of the 5 crossvalidation scores for each timepoint in frequency band *',
          '*_data': 'the data of all electrodes for every epoch in the frequency band *. Should be of size n_epochs x n_electrodes x n_COI_times',
          'epoch_conditions':'the conditions of each epoch in str, taken from the epoched .fif file',
          'epoch_eventIDs':'the event IDs as int, taken from the epoched .fif file',
          'epoch_metadata':'the metadata from the epoched .fif file',
          'metadata.ch_names':'channel names',
          'metadata.COI_extraction': 'method with which the COI boundaries were calculated',
          'metadata.conditionExclude': 'Epochs in these conditions are excluded from the MVPA',
          'metadata.conditionInclude': 'Epochs NOT in these conditions are excluded from the MVPA',
          'metadata.date_TFR_extraction':'date when the TFR was derived from the epoched .fif file',
          'metadata.decimation_factor': 'the number of the decim variable used for the TFR extraction. Decimates sampling rate by this factor',
          'metadata.epoch_path':'path of the epoched .fif file from which this dict is derived',
          'metadata.freqbands':'the freqbands into which the data is divided after TFR',
          'metadata.freqs':'the actual frequencies for which the TFR was performed',
          'metadata.freqs_code':'how the freqs were selected',
          'metadata.n_cycles': 'how many cycles of a given frequency are within a standard deviation of the wavelet envelope. Also determines COI boundaries.',
          'metadata.response_variable' : 'the variable the MVPA is trying to predict'}
