#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 06:47:27 2024

@author: samuemu

This script will update files in SiN_practise to reflect changes in the SiN_task.
The practise has the same response selection screen as the task, but only 8 stimuli,
all of which are non-degraded ('clear').

This script first deletes all previous audiofiles, flow spreadsheets, block order tables
and images from SiN_practise, to ensure they are all the same as the current versions in to SiN_task.

Then it creates a new flow table (based on 'SiN_task/flow/tts-golang-selected_PsyPySEQ.csv')
and then the block order table.

Then, it will copy the needed audiofiles from SiN_task/audio into SiN_practise/audio
and the response screen images from SiN_task/images to SiN_practise/images.

"""
import os
from glob import glob
import shutil
import pandas as pd

import random



# %% paths 
thisDir = os.getcwd()

baseDir   = os.path.join(thisDir[:thisDir.find('Gen_stimuli')], 'Experiments','SiN','Experiment2')
dirinput  = os.path.join(baseDir, 'SiN_task')
diroutput = os.path.join(baseDir, 'SiN_practice')

#%% delete old files in SiN_practise
delFiles = glob(os.path.join(diroutput,'audio','*.wav'), recursive=True) # audiofiles
delFiles += glob(os.path.join(diroutput,'flow','*.csv'), recursive=True) # flow table
delFiles += glob(os.path.join(diroutput,'order*.csv'), recursive=True) # block order
delFiles += glob(os.path.join(diroutput, 'images', '*.png'), recursive=True) # block order

for file in delFiles:
    os.remove(file)
    print('deleted:', os.path.relpath(file, start = baseDir))


#%% get flow spreadsheet from SiN_task
praatTimes = pd.read_csv(os.path.join(dirinput, 'flow', 'tts-golang-selected_PsyPySEQ.csv'))

# remove NV and SSN rows, as well as allocation_list and block columns
praatTimes = praatTimes.loc[praatTimes['noise'] == 'clear']
praatTimes = praatTimes.drop(['allocation_list', 'block'], axis = 1)

# %%  
ls1 = list(set(praatTimes['callSign']))
ls2 = list(set(praatTimes['colour']))
ls3 = list(set(praatTimes['number']))
random.shuffle(ls1)
random.shuffle(ls2)
random.shuffle(ls3)

# Since we don't need more than 8 trials in the practise task, just combine the i-th item of every list
# Since the lists are randomised, every item will occur exactly once in a random combination
designation_list = ['-'.join(j) for j in [(ls1[i], ls2[i], ls3[i]) for i in range(8)]]

#%% subset the praatTimes dataframe by the 8 stimuli we actually have
tab = praatTimes.loc[[idx for idx in praatTimes.index if praatTimes['words'][idx] in designation_list]]

tab['block'] = ['block1'] * 8 # add block designation (just 'block1' for every item)

#%% save flow table and block order table
outputname = 'flow' + os.sep + 'tts-golang-selected_PsyPySEQ.csv'
with open(os.path.join(diroutput,outputname),'w', newline='') as csvfile:
    tab.to_csv(csvfile,index=False)
   
orderTab = pd.DataFrame({'condsFile':outputname}, index = [0])
orderTab.to_csv(os.path.join(diroutput,'order1.csv'),index=False)

#%% copy needed audiofiles from SiN_task
for audiofile in tab['audiofile']:
    origin = os.path.join(dirinput, audiofile)
    destination = os.path.join(diroutput, audiofile)
    shutil.copy(origin, destination)
    print('copied to', os.path.relpath(destination, start = baseDir))

#%% copy needed images from SiN_task
for file in glob(os.path.join(dirinput, 'images', '*.png'), recursive=True)   :
    file_name = os.path.basename(file)
    destination = os.path.join(diroutput, 'images', file_name)
    shutil.copy(file, destination)
    print('copied to', os.path.relpath(destination, start = baseDir))

    
