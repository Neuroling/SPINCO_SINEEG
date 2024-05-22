#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOVE FILES TO DIRECTORY
===============================================================================
Created on 22.05.2024
@author: samuemu

This script will move files from one directory to another.

If you instead want to copy files into another directory, use files_copy.py
If you instead want to delete files from a directory, use files_delete.py

The path of the original directory is dirinput.
The path of the destination directory is diroutput.
The path until dirinput and diroutput diverge is baseDir.

If the diroutput does not exist, the script will ask before creating it. Check
the console.
"""

#%% package imports
import os 
from glob import glob
import re 
import shutil 
import sys

#%% directories
thisDir = os.getcwd()



baseDir = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2')
dirinput = os.path.join(baseDir, 'tts-golang-44100hz', 'tts-golang-equalisedDuration-selected')
diroutput = os.path.join(baseDir, 'selected_audio_psychoPy')

#%% find target files
# files = [files for files in glob(os.path.join(dirinput,'*'), recursive=True) if re.findall('Ham|Sch|Tel|Loe',files)]
files = glob(os.path.join(dirinput,'*.wav'), recursive=True)



#%% Check if diroutput exists. If not, ask if it should be created.
print(diroutput)

# make directory if it doesn't exist yet
if not os.path.isdir(diroutput):
    if input("--> destination directory does not exist. Create the above directory? [y/n] ") == 'y':       
        os.makedirs(diroutput)
    else:
        print('----> please create destination directory and try again.')
        sys.exit()

#%% Move files.
for file in files:
    file_name = os.path.basename(file)
    destination = os.path.join(diroutput, file_name)
    shutil.move(file, destination)
    print(file)
    

print('--> above files have been moved to ', diroutput)
