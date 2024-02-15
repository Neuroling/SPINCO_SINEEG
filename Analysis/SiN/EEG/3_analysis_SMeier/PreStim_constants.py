#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 09:01:21 2024

@author: samuemu
"""

import os
# from glob import glob
import pandas as pd

taskID = 'task-sin'
pipeID = 'pipeline-01'

fifFileEnd = 'resampled_ICA_rej_epo.fif'
freqTableEnd = 'event_group_frequencies.csv'
inputPickleFileEnd = '_tfr_freqbands.pkl'


thisDir = os.getcwd()
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]



## this list is copy-pasted from epo.ch_names of s009, who has all 64 channels, so it should be complete
ch_names = ['Fp1', 'AF7', 'AF3', 'F1', 'F3', 'F5', 'F7', 'FT7', 'FC5', 'FC3', 'FC1', 'C1', 'C3', 'C5', 'T7', 'TP7', 'CP5',
            'CP3', 'CP1', 'P1', 'P3', 'P5', 'P7', 'P9', 'PO7', 'PO3', 'O1', 'Iz', 'Oz', 'POz', 'Pz', 'CPz', 'Fpz', 'Fp2',
            'AF8', 'AF4', 'Afz', 'Fz', 'F2', 'F4', 'F6', 'F8', 'FT8', 'FC6', 'FC4', 'FC2', 'FCz', 'Cz', 'C2', 'C4', 'C6',
            'T8', 'TP8', 'CP6', 'CP4', 'CP2', 'P2', 'P4', 'P6', 'P8', 'P10', 'PO8', 'PO4', 'O2']
