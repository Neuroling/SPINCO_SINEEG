# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:37:20 2023

@author: gfraga
"""
import os as os
import sys as sys
from glob import glob
import pandas as pd
import textgrids
# To install, run the following line from the terminal:
    # python -m pip install praat-textgrids



thisDir = os.getcwd()
scripts_index = thisDir.find('Scripts')

dirinput = os.path.join(thisDir[:scripts_index] + 'Stimuli', 'AudioGens','Experiment2','tts-golang-44100hz','tts-golang-textGrid')

# dirinput = basedir + 'spinco_data/AudioGens/tts-golang-selected' # folder with .wav files
# diroutput = basedir + 'spinco_data/AudioGens/'

diroutput = os.path.join(thisDir[:scripts_index] + 'Stimuli', 'AudioGens','Experiment2','tts-golang-44100hz','word-times')
ratername= 'automatic'


# %%  Praat files
header = ['file','rater','firstSound_tmin','lastSound_tmax','token_1_tmin','token_1_tmax','token_2_tmin','token_2_tmax','token_3_tmin','token_3_tmax']

files = glob(os.path.join(dirinput, '*.TextGrid'))
gathertimes = []

for fileinput in files:
    praatDict = textgrids.TextGrid(fileinput)    
    filename = fileinput[fileinput.rfind(os.sep)+1:]
    if len(praatDict['ORT-MAU']) != 14:
        raise ValueError(f'Error! {filename} has different number of segments than the rest')
        
    times= \
    [filename] + \
    [ratername] + \
    [str(praatDict['ORT-MAU'][1].xmin)] + \
    [str(praatDict['ORT-MAU'][-1].xmin)]  + \
    [str(praatDict['ORT-MAU'][2].xmin)]+ [str(praatDict['ORT-MAU'][2].xmax)] + \
    [str(praatDict['ORT-MAU'][7].xmin)]+ [str(praatDict['ORT-MAU'][7].xmax)] +\
    [str(praatDict['ORT-MAU'][12].xmin)]+ [str(praatDict['ORT-MAU'][12].xmax)]
    times = pd.DataFrame(times).transpose()
    times.columns = header
    # Add to large array    
    gathertimes.append(times)
    
# add header
gathertimes = pd.concat(gathertimes)


gathertimes.to_csv(os.path.join(diroutput, ratername + '_tts-golang_wordTimes.csv'), index= False)
