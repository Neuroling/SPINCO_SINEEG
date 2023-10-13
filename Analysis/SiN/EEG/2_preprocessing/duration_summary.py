# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 15:05:37 2023
Script to create a .csv file with all recording durations and number of events

@author: samuemu
"""

import os 
import pandas as pd 
import json

# User inputs
taskID = 'task-sin'
save = 0 # if = 1 it will save excel files and plots
subID= 's001'

# PATHS
thisDir = os.path.dirname(os.path.abspath(__file__))
subIDs= os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata'))
diroutput= os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')

# for subID in subIDs:
#     if subID=='pilots' or subID.endswith("discard"):
#         pass
#     else:
dirinput=os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subID,taskID, 'eeg')
rawdata = os.listdir(dirinput)
for file in rawdata:
    if file.endswith("eeg.json") and file[-5].isdigit():
        # The file is a CSV file, get its filepath
        filepath = os.path.join(dirinput, file)