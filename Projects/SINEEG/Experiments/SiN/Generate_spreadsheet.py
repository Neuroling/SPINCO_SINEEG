# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:37:20 2023

@author: gfraga
"""
import os as os
import sys as sys
import glob as glob
import pandas as pd
import numpy as np
import wave


if sys.platform=='linux':  basedir  = '/home/d.uzh.ch/gfraga/smbmount/'
else:  basedir ='V:/'





dirs2search = [basedir + 'spinco_data/AudioGens/tts-golang-selected-NV' ,
               basedir + 'spinco_data/AudioGens/tts-golang-selected-SiSSN']

tab2save= pd.DataFrame() 
for dirinput in dirs2search:   
    diroutput = basedir + 'spinco_data/AudioGens/'
    praatSummaryFile = basedir + 'spinco_data/AudioGens/tts-golang-selected_wordTimes.csv'
    
    os.chdir(dirinput)
    os.getcwd()
    # Find files 
    files = glob.glob('*.wav')
    praatTimes = pd.read_csv(praatSummaryFile) 
    praatTimes = praatTimes.iloc[:, 1:] # delete fist column (row labels)
    
    # Create dict summarizing files, add times from praat 
    fileDict = {'audiofile':[],'duration':[],'noise':[],'voice':[],'words':[],'callSign':[],'colour':[],'number':[],'level':[]}
    times=pd.DataFrame()
    for i,fileinput in enumerate(files):           
        # Extract file info
        fileDict['audiofile'].append(fileinput)
        fileDict['noise'].append(fileinput.split('_')[0])
        fileDict['voice'].append(fileinput.split('_')[2])
        # info about sentence content
        fileDict['words'].append(fileinput.split('_')[3])
        fileDict['callSign'].append(fileinput.split('_')[3].split('-')[0])
        fileDict['colour'].append(fileinput.split('_')[3].split('-')[1])
        fileDict['number'].append(fileinput.split('_')[3].split('-')[2])
        # degradation/noise levels
        fileDict['level'].append(fileinput.split('_')[-1].split('.wav')[0])
        
        # file duration         
        with wave.open(fileinput, 'r') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            length = np.round(frames / float(rate), 4)
            
        fileDict['duration'].append(length)
        
        #get praat info
        names2match = praatTimes['file'].str.split('.TextGrid').str[0]
        rowidx= np.where('_'.join(fileinput.split('_')[1:4])==names2match)[0]
        times = times.append(praatTimes.iloc[rowidx],ignore_index=True)
        
    
    # merge data frames
    tab = pd.DataFrame.from_dict(fileDict)
    if len(files) == len(times):
        tab = tab.join(times)
    else:
        print('O_o. Could not find times for all files. Revise your praat summary!')

    #merge to main dataframe 
    tab2save = tab2save.append(tab)


# save to file
tab2save.to_csv(diroutput + 'tts-golang-selected_list.csv', index=False )
