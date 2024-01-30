#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTANTS FOR MVPA SCRIPTS
===============================================================================
@author: samuemu
Created on Fri Dec  8 12:23:55 2023

This script contains constants that are used across functions and scripts.
It is called by MVPA_functions and MVèA_runner



"""

import os
# from glob import glob
# import pandas as pd
# import numpy as np

taskID = 'task-sin'
pipeID = 'pipeline-01'
fifFileEnd = '_avg-epo.fif'
setFileEnd = '_epoched_2.set'
inputPickleFileEnd = '_tfr_freqbands.pkl'
outputPickleFileEnd = '_tfr_freqbands_crossval.pkl'


thisDir = os.getcwd()
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]

n_jobs = -1
#% Number of jobs to run in parallel. 
#% n_jobs = None means sequential processing. 
#% n_jobs = -1 means using all processors (so n_jobs is = number of processors)

freqbands = dict(#Delta = [1,4], # Our TFR covers frequencies from 6-48
                 Theta = [4,8],
                 Alpha=[8,13], 
                 Beta= [13,25],
                 Gamma =[25,48])
