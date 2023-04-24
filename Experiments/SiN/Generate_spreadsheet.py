# -*- coding: utf-8 -*-
""" GENERATE SPREADSHEETS FOR PSYCHOPY WITH LISTS OF TRIALS
---------------------------------------------------------------------

- Extract info from wav filename (tokens in sentence, voice, type of noise)
- Read wav durations
- Gather onset and offset of targets (inspected with Praat & Webmaus)
- Assign blocks splitting noise type: NV1, NV2, SiSSN1,SiSSN2:
- Select 2 voices and 3 degradation levels
- Voices  mixed (50% in trials within block)
- Equal number of trials for each level per voice 
- 32 trials x 2 voices x 3 levels = 192 trials per block (~20 min)
- Save the full table and a table per block   

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

diroutput = basedir + 'spinco_data/AudioGens/flow/'

# Dictionaries with trigger codes: 1st digit = noise, 2nd digit=position (1-call,2-col,3-num), 3rd digit = item (see below)
triggerDict_noise = {'NV':1,'SiSSN':2}
triggerDict_call = {'Ad':1,'Dr':2,'Kr':3,'Ti':4}
triggerDict_col = {'ge':1,'gr':2,'ro':3,'we':4}
triggerDict_num = {'Ei':1,'Zw':2,'Dr':3,'Vi':4}



# gather info in file 
fullTab= pd.DataFrame() 
#Loop thru directories for each noise (NV, SiSSN files separate folders)
for countdir, dirinput in enumerate(dirs2search):   
    
    praatSummaryFile = basedir + 'spinco_data/AudioGens/word_times/MEAN_tts-golang-selected_wordTimes.csv'
    
    os.chdir(dirinput)
    os.getcwd()
    # Find files 
    files = glob.glob('*.wav')
    praatTimes = pd.read_csv(praatSummaryFile) 
    
    # Create dict summarizing files, add times from praat 
    #Loop thru .wav files 
    fileDict = {'audiofile':[],'duration':[],'noise':[],'voice':[],'words':[],'callSign':[],'colour':[],'number':[],'levels':[],\
                'trigger_start':[],'trigger_end':[],'trigger_call':[],'trigger_col':[],'trigger_num':[]}
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
             
        #add file duration         
        with wave.open(fileinput, 'r') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            length = np.round(frames / float(rate), 4)
            
        fileDict['duration'].append(length)
        
        # Add trigger codes 
        tmpcode  = [triggerDict_noise[fileinput.split('_')[0]], 0, 0]
        fileDict['trigger_start'].append(''.join(map(str,tmpcode)))
        
        tmpcode  = [triggerDict_noise[fileinput.split('_')[0]], 0, 1]
        fileDict['trigger_end'].append(''.join(map(str,tmpcode)))
        
        tmpcode  = [triggerDict_noise[fileinput.split('_')[0]], 1, triggerDict_call[fileinput.split('_')[3].split('-')[0]]]
        fileDict['trigger_call'].append(''.join(map(str,tmpcode)))
        
        tmpcode  = [triggerDict_noise[fileinput.split('_')[0]], 2,triggerDict_col[fileinput.split('_')[3].split('-')[1]]]
        fileDict['trigger_col'].append(''.join(map(str,tmpcode)))
        
        tmpcode  = [triggerDict_noise[fileinput.split('_')[0]], 3, triggerDict_num[fileinput.split('_')[3].split('-')[2]]]
        fileDict['trigger_num'].append(''.join(map(str,tmpcode)))
        
        
        
        #Get praat info of onsets/offsets
        praatTimes.file = praatTimes.file.str.replace('-man.','.')
        names2match = praatTimes['file'].str.split('.TextGrid').str[0]
        rowidx= np.where('_'.join(fileinput.split('_')[1:4])==names2match)[0]
        times = times.append(praatTimes.iloc[rowidx],ignore_index=True)       
        
    
    # merge data frames with trial info and timtes
    tab = pd.DataFrame.from_dict(fileDict)
    if len(files) == len(times):
        tab = tab.join(times)
    else:
        print('~~~~~~~~~~~~ d[O_o]b. Could not find times for all files. Revise your praat summary!')
    
    # % Merge to main dataframe 
    fullTab = fullTab.append(tab)     
    
    # % Add block info 
    # Select only levels of interest
    vals = ['0.6p','0.7p','0.8p','-7db','-6db','-5db']
    fullTab = fullTab[fullTab['levels'].isin(vals)]
    # %%    
    # Add index by noise , voice and Level (to use for block assignment)
    fullTab2save = fullTab.groupby(['noise','voice','levels']).sample(frac=1)
    #fullTab2save = fullTab.groupby(['noise','voice','levels'])
    #fullTab2save['newidx'] = fullTab2save.groupby(['noise','voice','levels']).cumcount(ascending=True)
    fullTab2save['newidx'] = fullTab2save.groupby(['noise','voice','levels']).cumcount(ascending=True)
    
    # assign blocks: only 16 trials per Level are taken 
    fullTab2save['block'] = 0
    fullTab2save.block[(fullTab2save['noise']=='SiSSN') & (fullTab2save['newidx'].between(0, 15, inclusive=True))] = 'SSN1' 
    fullTab2save.block[(fullTab2save['noise']=='SiSSN') & (fullTab2save['newidx'].between(16, 31, inclusive=True))] = 'SSN2'
    fullTab2save.block[(fullTab2save['noise']=='NV') & (fullTab2save['newidx'].between(0, 15, inclusive=True))] = 'NV1'
    fullTab2save.block[(fullTab2save['noise']=='NV') & (fullTab2save['newidx'].between(16, 31, inclusive=True))] = 'NV2'
    fullTab2save = fullTab2save.groupby('block').sample(frac=1)
    
    # Discard excess trials
    fullTab2save = fullTab2save[fullTab2save['block']!= 0];
    
    #overview 
    print(fullTab2save.groupby(['noise','block','voice','levels'])['block'].count())
    overview = fullTab2save.groupby(['noise','block','voice','levels'])['words'].count().reset_index()
    
    stimOverview = pd.concat([fullTab2save.groupby(['noise','block','voice','levels'])['words'].count().reset_index(),\
                              fullTab2save.groupby(['noise','block','voice','levels'])['callSign'].count().reset_index(),\
                                  fullTab2save.groupby(['noise','block','voice','levels'])['colour'].count().reset_index(),\
                                      fullTab2save.groupby(['noise','block','voice','levels'])['number'].count().reset_index()])

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

#%%

with open(diroutput + 'tts-golang-selected_stimOverview.csv','w', newline='') as csvfile:
        stimOverview.to_csv(csvfile,index=False)
                
  

