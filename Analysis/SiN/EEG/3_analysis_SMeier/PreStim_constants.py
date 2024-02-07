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
setFileEnd = '_avgRef_epo.set'
fifFileEnd = '_avgRef_epo.fif'
freqTableEnd = 'event_group_frequencies.csv'
inputPickleFileEnd = '_tfr_freqbands.pkl'


thisDir = os.getcwd()
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]
