#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 08:09:32 2024

@author: testuser
"""

import os


taskID = 'task-sin'

thisDir = os.getcwd()
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data', 'SiN', 'derivatives_SM', taskID)
diroutput = dirinput

# Get file ends
fifFileEnd = 'resampled_ICA_rej_epo.fif'
freqPickleFileEnd = "_prestim_tfr_freqbands.pkl"
pValsPickleFileEnd = '.pkl'
evokedsPickleFileEnd = 'evokeds_allSubj_condition-separated.pkl'

# Get all subjIDs
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]

accuracy = ['Cor','Inc']
levels = ['Lv1','Lv2','Lv3']
noiseType = ['SSN', 'NV']
wordPosition = ['CallSign', 'Colour', 'Number']


freqbands = ['Alpha', 'Beta', 'Gamma', 'Theta']
