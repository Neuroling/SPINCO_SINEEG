#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 07:57:50 2023

@author: samuemu
"""


import os
from glob import glob
thisDir = os.getcwd()

import mne
from mne.time_frequency import tfr_morlet
import matplotlib.pyplot as plt
import numpy as np

import FeatureExtraction_constants as const
import FeatureExtraction_helper as helper

#%% User inputs ###########################################################################################################
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', 
                        const.pipeID, const.taskID + '_preproc_epoched',subjID)
epo_path = glob(os.path.join(dirinput, str("*"+ const.fifFileEnd)), recursive=True)[0]



#%% Read epoched data #####################################################################################################
epo = mne.read_epochs(epo_path)

#%%
TFRManager = helper.TFRManager()
features_dict=TFRManager.EEG_extract_feat(epo)
tfr=features_dict['TFR']

tfr_df = TFRManager.extractCOI(tfr)
tfr_bands = TFRManager.extractFreqBands(tfr_df)
