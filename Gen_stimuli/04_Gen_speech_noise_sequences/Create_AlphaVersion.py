#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 06:47:27 2024

@author: samuemu



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

#%% rename previous alpha version to *_old and create new directory
if os.path.exists(diroutput):
    os.rename(diroutput, diroutput+'_old')
    
os.mkdir(diroutput)

#%% create directories in the SiN_alphaVersion
dirsToCreate = ['audio', 'flow', 'images']
for item in dirsToCreate:
    os.mkdir(os.path.join(diroutput, item))

#%% copy files from SiN_task to SiN_alphaVersion
files = glob(os.path.join(dirinput,'*'), recursive=True)

doNotCopy = ['.rtf', '.csv', 'old_']
for file in files:
    # do not copy directories, only files that do not contain the substr in doNotCopy
    if os.path.isfile(file) and not any(x in file for x in doNotCopy):
        file_name = os.path.basename(file)
        destination = os.path.join(diroutput, file_name)
        shutil.copy(file, destination)
        print('copied to', os.path.relpath(destination, start = baseDir))

#%% copy images for response screen from SiN_task
for file in glob(os.path.join(dirinput, 'images', '*.png'), recursive=True)   :
    file_name = os.path.basename(file)
    destination = os.path.join(diroutput, 'images', file_name)
    shutil.copy(file, destination)
    print('copied to', os.path.relpath(destination, start = baseDir))

    
#%% get flow spreadsheet for NV0 and SSN0
files_csv = glob(os.path.join(dirinput,'flow','tts-golang-selected_PsyPySEQ_*0.csv'))
files_csv = [item for item in files_csv if '10.csv' not in item]

#%% randomly choose half of the trials to discard to have shorter blocks
# (discard half of degraded and half of clear trials, so the ratio remains)

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
    
    # copy needed audiofiles from SiN_task
    for audiofile in df_new['audiofile']:
        origin = os.path.join(dirinput, audiofile)
        destination = os.path.join(diroutput, audiofile)
        shutil.copy(origin, destination)

# create block order table    
orderTab = pd.DataFrame({'condsFile':outputnames}, index = [0,1])
orderTab.to_csv(os.path.join(diroutput,'order1.csv'),index=False)

#%% copy click_beep.wav into SiN_alphaVersion/audio
for file in glob(os.path.join(dirinput, 'click_beep.wav'), recursive=True):
    file_name = os.path.basename(file)
    destination = os.path.join(diroutput,'audio', file_name)
    shutil.copy(file, destination)
    print('copied to', os.path.relpath(destination, start = baseDir))
