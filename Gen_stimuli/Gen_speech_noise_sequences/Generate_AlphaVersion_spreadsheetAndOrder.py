#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 06:47:27 2024

@author: samuemu

This is copied and adapted from Generate_spreadsheet_Exp2.py
"""
import os
from glob import glob
import pandas as pd
import numpy as np
import random
import itertools
import shutil


# %% paths 
thisDir = os.getcwd()

baseDir = os.path.join(thisDir[:thisDir.find('Gen_stimuli')], 'Experiments','SiN','Experiment2')

dirinput = os.path.join(baseDir, 'SiN_task')
diroutput = os.path.join(baseDir, 'SiN_alphaVersion')

# get files_csv
files_csv = glob(os.path.join(dirinput,'flow','tts-golang-selected_PsyPySEQ_*0.csv'))
files_csv = [item for item in files_csv if '10.csv' not in item]

#%% create flow spreadsheet with fewer trials
outputnames = []
for file in files_csv:
    df = pd.read_csv(file) 
    tmp = []
    for i in set(df['allocation_list']):
        tmp_df = df.loc[df['allocation_list']== i]
        tmp_df = tmp_df.loc[random.sample(list(tmp_df.index), len(tmp_df)//2)]
        tmp.append(tmp_df)
    df_new = pd.concat(tmp)

    # save flow spreadsheet
    block_designation = list(set(df['block']))[0]
    outputname = 'flow' + os.sep + 'tts-golang-selected_PsyPySEQ_' + block_designation + '.csv'
    with open(os.path.join(diroutput, outputname),'w', newline='') as csvfile:
        df_new.to_csv(csvfile,index=False)   
    outputnames.append(outputname)
    
    # copy needed audiofiles
    for audiofile in df_new['audiofile']:
        origin = os.path.join(dirinput, audiofile)
        destination = os.path.join(diroutput, audiofile)
        shutil.copy(origin, destination)

    
orderTab = pd.DataFrame({'condsFile':outputnames}, index = [0,1])
orderTab.to_csv(os.path.join(diroutput,'order1.csv'),index=False)
