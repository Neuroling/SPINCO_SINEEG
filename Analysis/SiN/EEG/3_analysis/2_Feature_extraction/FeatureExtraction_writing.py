#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:18:39 2023

@author: samuemu

Yet another largely undocumented script meant to try code in, which will then be put into a "*_helper.py" and "*_runner.py" script

list of abbreviations:
    epo = epoch
    const = constants
    freqs = frequencies
    psd = power spectrum density
    itc = inter-trial coherence
    tfr = time frequency representation
    
"""

import os
from glob import glob
thisDir = os.getcwd()
import mne
from mne.time_frequency import tfr_morlet
import matplotlib.pyplot as plt
import numpy as np

import FeatureExtraction_constants as const

#%% User inputs
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', const.pipeID, const.taskID + '_preproc_epoched',subjID)
epo_path = glob(os.path.join(dirinput, str("*"+ const.fifFileEnd)), recursive=True)[0]
set_path = glob(os.path.join(dirinput, str("*"+ const.setFileEnd)), recursive=True)[0]

#%% Read epoched data
epo = mne.read_epochs(epo_path)

#%% Plot Power Spectrum densities
epo.compute_psd(exclude=const.excludeElectrodes).plot() # We exclude electrode Cz (const.excludeElectrodes) because it is 0
epo.compute_psd(exclude=const.excludeElectrodes).plot_topomap(ch_type="eeg", normalize=False, contours=0)

#%% Now let's do the morlet time frequency representation (TFR)
incl_chans = epo.info.ch_names
incl_chans.remove(const.excludeElectrodes)

freqs = np.logspace(*np.log10([6, 35]), num=8) # define frequencies of interest
n_cycles = freqs / 2.0  # different number of cycle per frequency
power, itc = tfr_morlet(
    epo,
    freqs=freqs,
    n_cycles=n_cycles,
    use_fft=True,
    decim=3, # reduces data by this factor after convolution to reduce memory usage. May create aliasing artefacts
    n_jobs=None, # sequential execution (less memory usage)
)

power.plot_joint(
    baseline=(-0.5, 0), mode="mean", tmin=-0.5, tmax=2, timefreqs=[(0.5, 10), (1.3, 8)]
)