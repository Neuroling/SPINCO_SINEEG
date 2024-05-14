# -*- coding: utf-8 -*-
"""
GATHER ALL TIMES FROM TEXTGRIDS INTO A CSV FILE
===============================================================================
Created on Fri 03.05.2024
@author: samuemu, adapted from gfraga

This dataframe contains the onset and offset times for each segment identified
by webmaus.

It will be used to equalise the duration of each segment across audiofiles.
"""
#%% Imports
import os as os
import sys as sys
from glob import glob
import pandas as pd
import textgrids
# To install, run the following line from the terminal:
    # python -m pip install praat-textgrids


#%% directories
thisDir = os.getcwd()
scripts_index = thisDir.find('Scripts')

dirinput = os.path.join(thisDir[:scripts_index] + 'Stimuli', 'AudioGens','Experiment2','tts-golang-44100hz','tts-golang')

diroutput = os.path.join(thisDir[:scripts_index] + 'Stimuli', 'AudioGens','Experiment2','tts-golang-44100hz','word-times')

#%% get files
files = glob(os.path.join(dirinput, '*.TextGrid'))

# %%  Praat files
sentence = ['Start', 'Vorsicht', 'CallSign', 'Break', 'Geh', 'Sofort', 'Zum', 'Colour', 'Feld', 'Von', 'Der', 'Spalte', 'Number', 'End']
sentence_tmin = [item + '_tmin' for item in sentence]
sentence_tmax = [item + '_tmax' for item in sentence]
header = ['file'] + [item for pair in zip(sentence_tmin, sentence_tmax) for item in pair] + ['CallSign', 'Colour', 'Number']

# header = ['file', 'start', 'Vorsicht_tmin', 'lastSound_tmax', 'token_1_tmin', 'token_1_tmax', 'token_2_tmin',' token_2_tmax', 'token_3_tmin', 'token_3_tmax']

#%% get dataframe
gathertimes = []

for fileinput in files:
    praatDict = textgrids.TextGrid(fileinput)    
    filename = fileinput[fileinput.rfind(os.sep)+1:fileinput.rfind('.')]
    times_tmin = [item.xmin for item in praatDict['ORT-MAU']]
    times_tmax = [item.xmax for item in praatDict['ORT-MAU']]
    callSign = praatDict['ORT-MAU'][2].text
    colour = praatDict['ORT-MAU'][7].text
    number = praatDict['ORT-MAU'][12].text

    times = [filename] + [item for pair in zip(times_tmin, times_tmax) for item in pair] + [callSign, colour, number]

    # Add to list 
    gathertimes.append(times)
    
# create dataframe
gathertimes = pd.DataFrame(gathertimes, columns = header)
# If you get an error of like "X columns passed, passed data has x columns" then the textgrid files have different numbers of segments
# find out which one by looking at the `gathertimes` list and sort it by size. You'll find the ones that deviate that way.
# Then edit the textGrid files in praat. 


# get all unique callSigns, colours and numbers
callSigns = list(set([item for item in gathertimes['CallSign']]))

colours = list(set([item for item in gathertimes['Colour']]))

numbers = list(set([item for item in gathertimes['Number']]))

stimType = ['CallSign', 'Colour', 'Number']

for i in stimType:
    gathertimes[i + '_duration'] = (gathertimes[i + '_tmax'] - gathertimes[i + '_tmin'])


gathertimes.to_csv(os.path.join(diroutput, 'Full_tts-golang_allTimes.csv'), index= False)
