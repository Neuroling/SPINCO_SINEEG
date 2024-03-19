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

SM_fifFileEnd = 'resampled_ICA_rej_epo.fif'


#%% Getting a list of subject IDs
thisDir = os.getcwd()
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]


n_jobs = None
#% Number of jobs to run in parallel. 
#% n_jobs = None means sequential processing (takes longer, but requires less RAM)
#% n_jobs = -1 means using all processors (so n_jobs is = number of processors)

decim = 1 # When doing the TFR, decimates sampling rate by this factor 
# If RAM is an issue: choose 2 or higher to avoid freezing the kernel

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

In other words:
    (2 * np.pi * freqs) = one completed sine-wave of freqs (= one cycle)
    Therefore: n_cycles determines how many cycles are in a standard deviation of the gaussian envelope
    Higher n_cycles will give a higher sigma and therefore a broader wavelet


if << n_cycles = freqs / 2 >> then sigma will always be = 1 / (4 * np.pi) = 0.079577
--> and that is why you don't want to make n_cycles dependent on freqs


===== CONE OF INFLUENCE =====
For the Cone of Influence, we use the full width at half maximum (FWHM).
It is defined as the window between when the gaussian envelope is at 50% before and after the peak.

The full-width half-maximum (FWHM) can be determined by:
    >>> fwhm = sigma * 2 * np.sqrt(2 * np.log(2))
    or 
    >>> fwhm = n_cycles * np.sqrt(2 * np.log(2))/(np.pi * freqs)
    
Consequently, the FWHM is approximately 2.355 * sigma
We use half of that for the COI on either side, so 1.173 * sigma
This is also called the half width at half maximum (HWHM)

Therefore:
With the COI, we want to exclude data outside of the HWHM on the first and last wavelet.
Our wavelets extend to +/- 5 sigma on either side of the peak.
So we need to exclude values before << time[0] + ((5 - 1.173) * sigma) >> and after << time[-1] - ((5 - 1.173) * sigma) >>
(Where sigma is dependent on the frequency and n_cycles)
    
In other words:
    n_cycles determines how many complete cycles in a given frequency, multiplied by 3.27 (= 5 - 1.173)
    are at the boundary of the COI.
"""

freqs = np.logspace(*np.log10([6, 48]), num=56) # define frequencies of interest
n_cycles = 3 
sigma = n_cycles/(2 * np.pi * freqs)
fwhm = sigma * 2 * np.sqrt(2 * np.log(2))
hwhm_const = 5 - np.sqrt(2 * np.log(2))

comment_COI_extraction = ["Half width at half maximum - time window of size << (n_cycles/(2 * np.pi * freqs[i])) * 5 - np.sqrt(2 * np.log(2)) >> at beginnng and end of epoch"]

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