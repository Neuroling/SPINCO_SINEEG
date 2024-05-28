#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DELETE FILES FROM DIRECTORY
===============================================================================
Created on 08.05.2024
@author: samuemu

This script will delete files from a directory.

If you instead want to move files into another directory, use files_move.py
If you instead want to copy files into another directory, use files_copy.py

The script will ask you to confirm to delete files.

"""

create_backup = True

import os 
from glob import glob
import re 
import shutil 
from datetime import datetime



thisDir = os.getcwd()
baseDir = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz')

dirinput = os.path.join(baseDir,'tts-golang-textGrid')
backupDir = os.path.join(baseDir, '_delete', str(datetime.now())[:-10].replace(':',''))

# make directory if it doesn't exist yet
if not os.path.isdir(backupDir):
    os.makedirs(backupDir)

#%% find target files
files = [files for files in glob(os.path.join(dirinput,'*'), recursive=True) if re.findall('Ham|Sch|Tel|Loe',files)]
# files = glob(os.path.join(dirinput,'*.TextGrid'), recursive=True)


#%%
msg = '--> are you sure you want to delete ' + str(len(files)) + ' files? [y/n]'

if input(msg) == 'y':      
    for file in files:
        if create_backup:
            file_name = os.path.basename(file)
            destination = os.path.join(backupDir, file_name)
            shutil.move(file, destination)
        else:
            os.remove(file)
        print(file)
        
    if create_backup:
        print('above files have been moved to ', backupDir)
        print('to fully delete files, delete the above directory.')
    else:
        print('above files have been deleted')
