#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Search for some files and copy them elsewhere
==========================================================
Created on Tue Nov  8 10:18:34 2022

@author: gfraga
"""
import os 
import glob
import re 
import shutil 


thisDir = os.getcwd()
# baseDir = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2')
# dirinput = os.path.join(baseDir, 'tts-golang-44100hz', 'tts-golang-equalisedDuration-selected-click')
# diroutput = os.path.join(baseDir, 'selected_audio_psychoPy_click')

baseDir = os.path.join(thisDir[:thisDir.find('Scripts')], )
dirinput = os.path.join(baseDir,'Stimuli','AudioGens','Experiment2','flow')
diroutput = os.path.join(baseDir,'Scripts', 'Experiments','SiN','Experiment2','SiN_task','flow')

if not os.path.exists(diroutput):
    os.mkdir(diroutput)


#%% find target files
#files = [files for files in glob.glob(os.path.join(dirinput,'*wav'), recursive=True) if re.findall(r"-11db\b|\b-9db",files)]
# files = [files for files in glob.glob(os.path.join(dirinput,'*wav'), recursive=True) if re.findall("0.2p|0.4p|0.6p",files)]
# files = [files for files in glob.glob(os.path.join(dirinput,'*'), recursive=True) if re.findall('Ham|Sch|Tel|Loe',files)]
files = glob.glob(os.path.join(dirinput,'*'), recursive=True)

#%% Retrieve list of subjects name from folder structure
#subjects =  [[item for item in currpart if 'SUBJECT' in item] 
  #            for currpart in [fullpath.split('/')
  #                            for fullpath in files]] 

#%% copy files to diroutput
print("Copied files:")
for file in files:
    file_name = os.path.basename(file)
    # HINT if you want to rename the files in the new directory, change file_name here!
    destination = os.path.join(diroutput, file_name)
    shutil.copy(file, destination)
    print(file)
