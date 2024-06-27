#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTANTS FOR FEATURE EXTRACTION SCRIPTS
===============================================================================
@author: samuelmull
Created on Fri Dec  8 12:23:55 2023

This script contains constants: variables that are used across functions and scripts, 
such as filepath-chunks, subject_IDs, and variables determining frequency bands and 
TFR and COI, as well as a codebook that is saved along with the output of FeatureExtraction_runner

It is called by the FeatureExtraction_functions.py and the FeatureExtraction_runner.py scripts

"""

import os
import numpy as np
thisDir = os.getcwd()

#%% Building blocks for paths
taskID = 'task-sin'

pipeID = {
    'exp1':'pipeline-01', 
    'SM':'pipeline-01', 
    'exp2':'pipeline-automagic-01-unalignedTriggers'
    }



fifFileEnd = {
    'exp1':'_avgRef_epo.fif', 
    'SM':'resampled_ICA_rej_epo.fif', 
    'exp2':'_avgRef_epo.fif'
    }

pickleFileEnd = '_tfr_freqbands.pkl'

derivativesFolder = {
    'exp1':'derivatives', 
    'SM':'derivatives_SM', 
    'exp2':'derivatives_exp2-unalignedTriggers'
    }

analysisFolder = {
    'exp1':'analysis', 
    'SM':'', 
    'exp2':'analysis_exp2-unalignedTriggers'
    }


baseDir = {
    'exp1':os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN', derivativesFolder['exp1'], pipeID['exp1'], taskID + '_preproc_epoched'), 
    'SM':os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN', derivativesFolder['SM'], taskID), 
    'exp2':os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN', derivativesFolder['exp2'], pipeID['exp2'], taskID + '_preproc_epoched')
    }


#%% Getting a list of subject IDs

subjIDs = {
    'exp1':[item for item in os.listdir(baseDir['exp1']) if item[-1].isdigit()], 
    'SM':[item for item in os.listdir(baseDir['SM']) if item[-1].isdigit()], 
    'exp2':[item for item in os.listdir(baseDir['exp2']) if item[-1].isdigit()]
    }




n_jobs = -1
#% Number of jobs to run in parallel. 
#% n_jobs = None means sequential processing (takes longer, but requires less RAM)
#% n_jobs = -1 means using all processors (so n_jobs is = number of processors)

decim = 1 # When doing the TFR, decimates sampling rate by this factor 
# If RAM is an issue: choose 2 or higher to avoid freezing the kernel

# Define frequency bands 
freqbands = dict(#Delta = [1,4], # Our TFR covers frequencies from 6-48 Hz, so no delta
                 Theta = [4,8],
                 Alpha=[8,13], 
                 Beta= [13,25],
                 Gamma =[25,48])

"""
Note: an explanation of how wavelets and cone of influences work can be found in the README.md file.
The variables below this line should make more sense then.
"""

freqs = np.logspace(*np.log10([6, 48]), num=56) # define frequencies of interest
n_cycles = 3 # define how broad the wavelet should be (see README file)

sigma = n_cycles/(2 * np.pi * freqs)
fwhm = sigma * 2 * np.sqrt(2 * np.log(2))
hwhm_const = 5 - np.sqrt(2 * np.log(2))

comment_COI_extraction = ["Half width at half maximum - time window of size << (n_cycles/(2 * np.pi * freqs[i])) * 5 - np.sqrt(2 * np.log(2)) >> at beginnng and end of epoch"]

# TODO find a better way to do this - what if I change a variable name in the script but forget to change it here?
codebook={'*_COI_times':'timepoints inside the COI in frequency band *',
          '*_data': 'the data of all electrodes for every epoch in the frequency band *. Should be of size n_epochs x n_electrodes x n_COI_times',
          'epoch_conditions':'the conditions of each epoch in str, taken from the epoched .fif file',
          'epoch_eventIDs':'the event IDs as int, taken from the epoched .fif file',
          'epoch_metadata':'the metadata from the epoched .fif file',
          'metadata.ch_names':'channel names',
          'metadata.COI_extraction': 'method with which the COI boundaries were calculated',
          'metadata.date_TFR_extraction':'date when the TFR was derived from the epoched .fif file',
          'metadata.decimation_factor': 'the number of the decim variable used for the TFR extraction. Decimates sampling rate by this factor',
          'metadata.epoch_path':'path of the epoched .fif file from which this dict is derived',
          'metadata.freqbands':'the freqbands into which the data is divided after TFR',
          'metadata.freqs':'the actual frequencies for which the TFR was performed',
          'metadata.freqs_code':'how the freqs were selected',
          'metadata.n_cycles': 'how many cycles of a given frequency are within a standard deviation of the wavelet envelope. Also determines COI boundaries.'}
