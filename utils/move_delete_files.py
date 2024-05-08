#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 09:59:37 2024

@author: samuemu
"""

create_backup = True

import os 
import glob
import re 
import shutil 
from datetime import datetime



thisDir = os.getcwd()
baseDir = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz')

dirinput = os.path.join(baseDir,'tts-golang-textGrid')
diroutput = os.path.join(baseDir, '_delete', str(datetime.now())[:-10].replace(':',''))

# make directory if it doesn't exist yet
if not os.path.isdir(diroutput):
    os.makedirs(diroutput)

#%% find target files
files = [files for files in glob.glob(os.path.join(dirinput,'*'), recursive=True) if re.findall('Ham|Sch|Tel|Loe',files)]
# files = glob.glob(os.path.join(dirinput,'*.TextGrid'), recursive=True)


#%%


for file in files:
    if create_backup:
        file_name = os.path.basename(file)
        destination = os.path.join(diroutput, file_name)
        shutil.move(file, destination)
    else:
        os.remove(file)
    print(file)
    
if create_backup:
    print('above files have been moved to ', diroutput)
    print('to fully delete files, delete the above directory.')
else:
    print('above files have been deleted')
