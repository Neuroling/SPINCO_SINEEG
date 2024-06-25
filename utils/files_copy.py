#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Search for some files and copy them elsewhere
==========================================================
Created on 08.11.2022, adjusted 22.05.2024
@author: gfraga & samuelmull

This script will copy files from one directory to another.

If you instead want to move files to another directory, use files_move.py
If you instead want to delete files from a directory, use files_delete.py


----- MANUAL -----

- thisDir is the path of the current file (`./Projects/Spinco/SINEEG/Scripts/utils`)
- dirinput is the path of the original directory
- diroutput is the path of the destination directory
- baseDir is the path until dirinput and diroutput diverge

The script will look for all files in dirinput following a specific pattern.
The character '*' is a so-called wild-card, which means that '*.wav' will get
every file in dirinput that ends in '.wav'

If the diroutput does not exist, the script will ask before creating it. 
Check the console and type y for yes and n for no

If you want to adjust the filename in the copied files, see the lines marked with
# HINT in the code below.

"""
#%% IMPORTS
import os 
from glob import glob
import re 
import shutil 
import sys

#%% USER INPUTS
thisDir = os.getcwd()
baseDir = os.path.join(thisDir[:thisDir.find('Scripts')])
dirinput = os.path.join(baseDir, 'Stimuli','AudioGens','Experiment2','selected_audio_psychoPy_click')
diroutput = os.path.join(baseDir,'Scripts', 'Experiments','SiN','Experiment2','SiN_task','audio')

# baseDir = os.path.join(thisDir[:thisDir.find('Scripts')], )
# dirinput = os.path.join(baseDir,'Scripts', 'Experiments','SiN','Experiment2','SiN_task','images')
# diroutput = os.path.join(baseDir,'Scripts', 'Experiments','SiN','Experiment2','SiN_practice','images')

#%% find target files
files = glob(os.path.join(dirinput,'*.wav'), recursive=True)
# files = [files for files in glob(os.path.join(dirinput,'*wav'), recursive=True) if re.findall(r"-11db\b|\b-9db",files)]
# files = [files for files in glob(os.path.join(dirinput,'*wav'), recursive=True) if re.findall("0.2p|0.4p|0.6p",files)]
# files = [files for files in glob(os.path.join(dirinput,'*'), recursive=True) if re.findall('Ham|Sch|Tel|Loe',files)]
# files = [files for files in glob(os.path.join(dirinput,'*.wav'), recursive=True) if '-9db' in files]

#%% Check if diroutput exists. If not, ask if it should be created.
print(diroutput)

# make directory if it doesn't exist yet
if not os.path.isdir(diroutput):
    if input("--> destination directory does not exist. Create the above directory? [y/n] ") == 'y':       
        os.makedirs(diroutput)
    else:
        print('----> please create destination directory and try again.')
        sys.exit()
        
#%% copy files to diroutput
print("Copied files:")
for file in files:
    file_name = os.path.basename(file)
    
    # # HINT : if you want to rename the files in the new directory, change file_name here!
    # # For instance, this will rename it from 'originalName.wav' to 'clear_originalName_clear.wav'
    # file_name = 'clear_' + file_name[:file_name.rfind('.wav')] + '_clear.wav'
    
    destination = os.path.join(diroutput, file_name)
    shutil.copy(file, destination)
    print('copied to', os.path.relpath(destination, start = baseDir))
