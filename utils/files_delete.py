#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DELETE FILES FROM DIRECTORY
===============================================================================
Created on 08.05.2024
@author: samuelmull

This script will delete files from a directory. It will not delete directories

If you instead want to move files into another directory, use files_move.py
If you instead want to copy files into another directory, use files_copy.py

----- MANUAL -----

- thisDir is the path of the current file (`./Projects/Spinco/SINEEG/Scripts/utils`)
- baseDir is the path of thisDir until `Scripts`, i.e. `./Projects/Spinco/SINEEG`
- dirinput is the path of the file directory


The script will look for all files in dirinput following a specific pattern.
The character '*' is a so-called wild-card, which means that '*.wav' will get
every file in dirinput that ends in '.wav'

I strongly suggest setting `create_backup` to True. 
This will create a directory named "_delete/<currentDate>" and move files there.
You then need to manually delete this directory (AFTER checking the contents)

If `create_backup` is set to False, this script will ask you to confirm that choice.

Regardless of backup-setting, this script will ask to confirm before deleting/removing files.

"""
#%% IMPORTS
import os 
from glob import glob
import re 
import shutil 
from datetime import datetime

#%% USER INPUTS
create_backup = True

## Adjust filepaths
thisDir = os.getcwd()
baseDir = os.path.join(thisDir[:thisDir.find('Scripts')])
dirinput = os.path.join(baseDir,'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz','tts-golang')

## find target files
# files = [files for files in glob(os.path.join(dirinput,'*'), recursive=True) if re.findall('Ham|Sch|Tel|Loe',files)]
files = glob(os.path.join(dirinput,'*.TextGrid'), recursive=True)



#%%
""" 
===============================================================================
                    NO USER INPUTS BEYOND THIS LINE 
===============================================================================
"""

#%% warning messages
msg_backup = '--> do you want to create a backup? [y/n] '
msg_RUSure = '--> are you sure you want to delete the above ' + str(len(files)) + ' files? [y/n] '

#%% confirm choice if no backup is asked for; 
if not create_backup:
    if input(msg_backup) == 'y':
        create_backup = True
        
#%% create backup directory if desired
if create_backup:
    backupDir = os.path.join(baseDir, '_delete', str(datetime.now())[:-10].replace(':',''))    
    msg_RUSure = '--> are you sure you want to move the above ' + str(len(files)) + ' files to', backupDir,'? [y/n] '
    # make directory if it doesn't exist yet
    if not os.path.isdir(backupDir):
        os.makedirs(backupDir)
        
#%% print all filenames
for file in files:
    print(os.path.basename(file))

#%% Confirm choice, then delete/remove files, then report back.
if input(msg_RUSure) == 'y':      
    for file in files:
        if create_backup:
            file_name = os.path.basename(file)
            destination = os.path.join(backupDir, file_name)
            shutil.move(file, destination)
        else:
            os.remove(file)
        
    if create_backup:
        print('--> files have been moved to ', backupDir)
        print('--> to fully delete files, delete the above directory.')
    else:
        print('--> files have been deleted')
