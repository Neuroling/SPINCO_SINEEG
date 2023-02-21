# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:37:20 2023

@author: gfraga
"""
import os as os
import sys as sys
import glob as glob
import pandas as pd
import textgrids


if sys.platform=='linux':  basedir  = '/home/d.uzh.ch/gfraga/smbmount/'
else:  basedir ='V:/'

dirinput = basedir + 'spinco_data/AudioGens/tts-golang-selected' # folder with .wav files
diroutput = basedir + 'spinco_data/AudioGens/'

os.chdir(dirinput)
os.getcwd()

# %%  Praat files
files = glob.glob('*.textGrid')
gathertimes = pd.DataFrame()
for fileinput in files:
    praatDict = textgrids.TextGrid(fileinput)    
    
    times= \
    [fileinput] + \
    [str(praatDict['ORT-MAU'][1].xmin)] + \
    [str(praatDict['ORT-MAU'][-1].xmin)]  + \
    [str(praatDict['ORT-MAU'][2].xmin)]+ [str(praatDict['ORT-MAU'][2].xmax)] + \
    [str(praatDict['ORT-MAU'][6].xmin)]+ [str(praatDict['ORT-MAU'][6].xmax)] +\
    [str(praatDict['ORT-MAU'][11].xmin)]+ [str(praatDict['ORT-MAU'][11].xmax)]
    
    # Add to large array    
    gathertimes = gathertimes.append([times], ignore_index=True)
    
# add header
header = ['file','firstSound_tmin','lastSound_tmax','token_1_tmin','token_1_tmax','token_2_tmin','token_2_tmax','token_3_tmin','token_3_tmax']
gathertimes.columns=header

gathertimes.to_csv(diroutput+'tts-golang-selected_wordTimes.csv')

