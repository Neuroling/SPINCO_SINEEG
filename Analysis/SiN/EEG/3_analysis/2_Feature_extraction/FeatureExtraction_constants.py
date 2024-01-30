#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTANTS FOR FEATURE EXTRACTION SCRIPTS
===============================================================================
@author: samuemu
Created on Fri Dec  8 12:23:55 2023

This script contains constants that are used across functions and scripts
It is called by the FeatureExtraction_functions.py and the FeatureExtraction_runner.py scripts

"""

import os
# from glob import glob
# import pandas as pd
import numpy as np

#%% Building blocks for paths
taskID = 'task-sin'
pipeID = 'pipeline-01'
fifFileEnd = '_avgRef_epo.fif'
pickleFileEnd = '_tfr_freqbands.pkl'
AmplitudeExtractionFileEnd = '_amplitude-epo.fif'

#%% Getting a list of subject IDs
thisDir = os.getcwd()
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]


n_jobs = -1
#% Number of jobs to run in parallel. 
#% n_jobs = None means sequential processing (takes longer, but requires less RAM)
#% n_jobs = -1 means using all processors (so n_jobs is = number of processors)

decim = 1 # When doing the TFR, decimates sampling rate by this factor (to avoid freezing the kernel)

freqbands = dict(#Delta = [1,4], # Our TFR covers frequencies from 6-48
                 Theta = [4,8],
                 Alpha=[8,13], 
                 Beta= [13,25],
                 Gamma =[25,48])

"""
WAVELET WIDTH, CYCLES AND FREQUENCIES
===============================================================================

https://mne.tools/stable/generated/mne.time_frequency.morlet.html#mne.time_frequency.morlet

Paraphrased:
The width of a wavelet is determined by Sigma, which is the standard deviation of the Gaussian envelope.
The wavelet extends to +/-5 standard deviations, so the values at tail ends are close to 0.
Sigma is determined by freqs and n_cycles:
    >>> sigma = n_cycles/(2 * np.pi * freqs)

The full-width half-maximum (FWHM) can be determined by:
    >>> fwhm = sigma * 2 * np.sqrt(2 * np.log(2))
    or 
    >>> fwhm = n_cycles * np.sqrt(2 * np.log(2))/(np.pi * freqs)
    
if << n_cycles = freqs / 2 >> then sigma will always be = 1 / (4 * np.pi) = 0.079577
"""

freqs = np.logspace(*np.log10([6, 48]), num=56) # define frequencies of interest
n_cycles = 3# for a static width of the wavelets independent of frequency
sigma = n_cycles/(2 * np.pi * freqs)
fwhm = sigma * 2 * np.sqrt(2 * np.log(2))
