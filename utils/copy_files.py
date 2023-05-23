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

# paths - Use current script path as reference 
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
scripts_index = thisScriptDir.find('scripts')

dirinput = os.path.join(thisScriptDir[:scripts_index],'Stimuli','AudioGens','tts-golang-44100hz','tts-golang-selected-SiSSN')
dirinput = os.path.join(thisScriptDir[:scripts_index],'Stimuli','AudioGens','tts-golang-44100hz','tts-golang-selected-NV_v1')
diroutput = os.path.join(thisScriptDir[:scripts_index],'Stimuli','AudioGens','selected_audio_psychoPy')


# find target files
#files = glob.glob(os.path.join(dirinput,'*wav'), recursive=True)b
#files = [files for files in glob.glob(os.path.join(dirinput,'*wav'), recursive=True) if re.findall(r"-11db\b|\b-9db",files)]
files = [files for files in glob.glob(os.path.join(dirinput,'*wav'), recursive=True) if re.findall("0.2p|0.4p|0.6p",files)]
files

#%%
# Retrieve list of subjects name from folder structure
#subjects =  [[item for item in currpart if 'SUBJECT' in item] 
 #            for currpart in [fullpath.split('/')
  #                            for fullpath in files]] 
 # copy files to diroutput
for file in files:
    file_name = os.path.basename(file)
    destination = os.path.join(diroutput, file_name)
    shutil.copy(file, destination)

# print the list of copied files
print("Copied files:")
for file in files:
    print(file)