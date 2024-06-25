# -*- coding: utf-8 -*-
"""
GATHER ALL TIMES FROM TEXTGRIDS INTO A CSV FILE
===============================================================================
Created on Fri 03.05.2024
@author: samuelmull, adapted from gfraga

This script will use the textgrid files downloaded from webmaus to create a 
dataframe that contains the onset and offset times for each segment identified 
by webmaus.

It will be used to equalise the duration of each segment across audiofiles.

Webmaus link: https://clarin.phonetik.uni-muenchen.de/

Packages:
    textgrids : 
        - https://pypi.org/project/praat-textgrids/
        - install with `python -m pip install praat-textgrids`
        - Version I used: 1.4.0
        
        
"""
#%% Imports
import os
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

#%%  Create column names for the output df
sentence = ['Start', 'Vorsicht', 'CallSign', 'Break', 'Geh', 'Sofort', 'Zum', 'Colour', 'Feld', 'Von', 'Der', 'Spalte', 'Number', 'End']
sentence_tmin = [item + '_tmin' for item in sentence]
sentence_tmax = [item + '_tmax' for item in sentence]
header = ['file'] + [item for pair in zip(sentence_tmin, sentence_tmax) for item in pair] + ['CallSign', 'Colour', 'Number']


#%% get data from the textgrids
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
    
#%% create dataframe
gathertimes = pd.DataFrame(gathertimes, columns = header)
# If you get an error of like "X columns passed, passed data has x columns" then 
# the textgrid files have different numbers of segments find out which one by 
# looking at the `gathertimes` list, scroll all the way down and then sort it 
# by size. You'll find the ones that deviate that way.
# Then edit the textGrid files in praat. 


# get a list of all unique callSigns, colours and numbers
callSigns = list(set([item for item in gathertimes['CallSign']]))
colours = list(set([item for item in gathertimes['Colour']]))
numbers = list(set([item for item in gathertimes['Number']]))
print('all unique target stimuli:')
print(callSigns)
print(colours)
print(numbers)

stimType = ['CallSign', 'Colour', 'Number']

for i in stimType:
    gathertimes[i + '_duration'] = (gathertimes[i + '_tmax'] - gathertimes[i + '_tmin'])


# gathertimes.to_csv(os.path.join(diroutput, 'Full_tts-golang_allTimes.csv'), index= False)
