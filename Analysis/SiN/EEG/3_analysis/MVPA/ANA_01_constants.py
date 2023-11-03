#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:47:21 2023

@author: samuemu
"""
import os
from glob import glob

taskID = 'task-sin'
pipeID = 'pipeline-01'
setFileEnd = '_epoched_2.set'

thisDir = os.path.dirname(os.path.abspath(__file__))
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]

# set_fp = glob(os.path.join(dirinput, str("*"+ setFileEnd)), recursive=True)[0]
# epo_fp = set_fp[:set_fp.find(setFileEnd)]+'-epo.fif'
# events_fp = glob(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', pipeID, taskID, subjID,"*accu.tsv"), recursive=True)[0]
# beh_fp = glob(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subjID, taskID, 'beh',"*.csv"), recursive=True)[0]