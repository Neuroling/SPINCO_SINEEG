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

diroutput = basedir + 'spinco_data/AudioGens/'

fullTab= pd.DataFrame() 
for countdir, dirinput in enumerate(dirs2search):   
    
    praatSummaryFile = basedir + 'spinco_data/AudioGens/word_times/Rahel_tts-golang-selected_wordTimes.csv'
    
    os.chdir(dirinput)
    os.getcwd()
    # Find files 
    files = glob.glob('*.wav')
    praatTimes = pd.read_csv(praatSummaryFile) 
    
    
    # Create dict summarizing files, add times from praat 
    fileDict = {'audiofile':[],'duration':[],'noise':[],'voice':[],'words':[],'callSign':[],'colour':[],'number':[],'levels':[]}
    times=pd.DataFrame()
    for i,fileinput in enumerate(files):           
        # Extract file info
        fileDict['audiofile'].append('audio/'+fileinput)
        fileDict['noise'].append(fileinput.split('_')[0])
        fileDict['voice'].append(fileinput.split('_')[2])
        # info about sentence content
        fileDict['words'].append(fileinput.split('_')[3])
        fileDict['callSign'].append(fileinput.split('_')[3].split('-')[0])
        fileDict['colour'].append(fileinput.split('_')[3].split('-')[1])
        fileDict['number'].append(fileinput.split('_')[3].split('-')[2])
        # degradation/noise levels
        fileDict['levels'].append(fileinput.split('_')[-1].split('.wav')[0])
        
        # file duration         
        with wave.open(fileinput, 'r') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            length = np.round(frames / float(rate), 4)
            
        fileDict['duration'].append(length)
        
        #get praat info
        praatTimes.file = praatTimes.file.str.replace('-man.','.')
        names2match = praatTimes['file'].str.split('.TextGrid').str[0]
        rowidx= np.where('_'.join(fileinput.split('_')[1:4])==names2match)[0]
        times = times.append(praatTimes.iloc[rowidx],ignore_index=True)
        
    
    # merge data frames
    tab = pd.DataFrame.from_dict(fileDict)
    if len(files) == len(times):
        tab = tab.join(times)
    else:
        print('~~~~~~~~~~~~ d[O_o]b. Could not find times for all files. Revise your praat summary!')

    #merge to main dataframe 
    fullTab = fullTab.append(tab)
    
    print(countdir)
    print(dirinput)
    # %% Add block info 
    # Shuffle
    
    vals = ['0.6p','0.75p','0.8p','-7.5db','-5db','0db']
    fullTab = fullTab[fullTab['levels'].isin(vals)]
    
    # 
    fullTab2save = fullTab.groupby(['noise','voice','levels']).sample(frac=1)
    fullTab2save['newidx'] = fullTab2save.groupby(['noise','voice','levels']).cumcount(ascending=True)
    
    # assign blocks
    fullTab2save['block'] = 0
    fullTab2save.block[(fullTab2save['noise']=='SiSSN') & (fullTab2save['newidx'] < 32)] = 'SSN1' 
    fullTab2save.block[(fullTab2save['noise']=='SiSSN') & (fullTab2save['newidx'] >= 32)] = 'SSN2'
    fullTab2save.block[(fullTab2save['noise']=='NV') & (fullTab2save['newidx'] < 32)] = 'NV1'
    fullTab2save.block[(fullTab2save['noise']=='NV') & (fullTab2save['newidx'] >= 32)] = 'NV2'
    fullTab2save = fullTab2save.groupby('block').sample(frac=1)
    
    print(fullTab2save.groupby(['noise','block','voice','levels'])['block'].count())
    overview = fullTab2save.groupby(['noise','block','voice','levels'])['words'].count().reset_index()
    
# %% save to file
with open(diroutput + 'tts-golang-selected_PsyPySEQ.csv','w', newline='') as csvfile:
    fullTab2save.to_csv(csvfile,index=False)
    
# %% save per block    
for block_value in fullTab2save['block'].unique():    
    block_df = fullTab2save[fullTab2save['block'] == block_value]    
    block_df.to_csv(diroutput + 'tts-golang-selected_PsyPySEQ_' + block_value + '.csv', index=False)

    

#%%
with open(diroutput + 'tts-golang-selected_seqOverview.csv','w', newline='') as csvfile:
        overview.to_csv(csvfile,index=False)

