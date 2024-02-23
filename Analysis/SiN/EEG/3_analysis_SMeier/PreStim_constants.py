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

thisDir = os.getcwd()
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data', 'SiN', 'derivatives_SM', taskID)
diroutput = dirinput + '/ERP/'

fifFileEnd = 'resampled_ICA_rej_epo.fif'
pValsPickleFileEnd = 'LMM_p_Values_FDR.pkl'
evokedsPickleFileEnd = 'evokeds.pkl'


subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]




accuracy = ['Cor','Inc']
degradation = ['Lv1','Lv2','Lv3']
noise = ['NV','SSN']


# List all possible combinations of noise degradation and accuracy
conditions = [x + '/' + y + '/' + z for x in noise for y in degradation for z in accuracy]
