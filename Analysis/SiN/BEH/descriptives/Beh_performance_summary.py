#!/usr/bin/env python3

""" Gather Behavioral Performance 
===============================================
Created on Tue Apr 25 10:56:48 2023
- Sentence-in-noise task in EEG experiment
- Read trial info with performance 
- Summarize 

@author: gfraga
"""
import os 
import shutil
import pandas as pd 

# User inputs
copyraw = 0;
subID = 's001'
taskID = 'task-sin'

# PATHS
thisDir = os.path.dirname(os.path.abspath(__file__))
rawdir = os.path.join(thisDir[:thisDir.find('scripts')] + 'Data','SiN','rawdata', subID,taskID, 'beh')
diroutput = os.path.join(thisDir[:thisDir.find('scripts')] + 'Data','SiN','rawdata',subID,taskID, 'beh','summary')
os.makedirs(diroutput, exist_ok=True)

# %% Get raw data into the analysis folder 
rawcsv = os.listdir(rawdir)
for file in rawcsv:
    if file.endswith(".csv") and file[-5].isdigit():
        # The file is a CSV file, copy it to the output directory
        filepath = os.path.join(rawdir, file)        
                
 
# %% read data frame 
df = pd.read_csv(filepath)     
   

# %% Summarize accuracy
# call or callSign  = is the animal ; col = color and num = number 
# 'uniqueTrials' is the number of target items per level, noise type and block (replace by infering this from data) 
uniqueTrials = 32     
(df.groupby(['noise', 'block', 'levels'])[['callSignCorrect', 'colourCorrect','numberCorrect']].sum())*100/uniqueTrials
 
   

# Save excel 
    
# Performance plot








# %% 
