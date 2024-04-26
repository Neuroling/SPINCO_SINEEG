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

#%% User Inputs
# Dictionaries with trigger codes: 1st digit = noise, 2nd digit=position (1-call,2-col,3-num), 3rd digit = item (see below)
triggerDict_noise = {'NV':1, 
                     #'SiSSN':2
                     }

triggerDict_call = {'Ad':1,'Dr':2,'Kr':3,'Ti':4}
triggerDict_col = {'ge':1,'gr':2,'ro':3,'we':4}
triggerDict_num = {'Ei':1,'Zw':2,'Dr':3,'Vi':4}

# which degradation levels should be included? If empty, will include all.
degradation_levels = []

# %% paths 
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
scripts_index = thisScriptDir.find('Scripts')

dirs2search = [#os.path.join(thisScriptDir[:scripts_index] + 'Stimuli', 'AudioGens','tts-golang-44100hz','tts-golang-selected-SiSSN'),
               os.path.join(thisScriptDir[:scripts_index] + 'Stimuli', 'AudioGens','tts-golang-44100hz','tts-golang-selected-NV_Experiment2')]

diroutput = os.path.join(thisScriptDir[:scripts_index] + 'Stimuli', 'AudioGens','flow_Experiment2')

praatSummaryFile = os.path.join(thisScriptDir[:scripts_index] + 'Stimuli', 'AudioGens','tts-golang-44100hz','word_times','MEAN_tts-golang-selected_wordTimes.csv')



# gather info in file 
fullTab = pd.DataFrame() 
#Loop through directories for each noise (NV, SiSSN files separate folders)
for countdir, dirinput in enumerate(dirs2search):     
    
    os.chdir(dirinput)
    os.getcwd()
    # Find files 
    files = glob.glob('*.wav')
    praatTimes = pd.read_csv(praatSummaryFile) 
    
    # Create dict summarizing files, add times from praat 
    #Loop thru .wav files 
    fileDict = {'audiofile':[],'duration':[],'noise':[],'voice':[],'words':[],'callSign':[],'colour':[],'number':[],'levels':[],\
                'NV_nChannels':[],'trigger_start':[],'trigger_end':[],'trigger_call':[],'trigger_col':[],'trigger_num':[],\
                    'trigger_call_end': [],'trigger_col_end':[],'trigger_num_end':[]}
        
    times=[] # appending to list and then concatenating to a df is always cheaper
    for i,fileinput in enumerate(files): 
        
        # for readability and convenience, we do this here instead of repeating the fileinput.split('_')[n] over and over
        _noise_ = fileinput.split('_')[0]
        _voice_ = fileinput.split('_')[2]
        _words_ = fileinput.split('_')[3]
        _callSign_ = _words_.split('-')[0]
        _colour_ = _words_.split('-')[1]
        _number_ = _words_.split('-')[2]
        _level_ = fileinput.split('_')[4] 
        _nCh_ = fileinput.split('_')[5].split('.wav')[0]
        
        #if degradation_levels is not empty, only include files in with specified levels
        if degradation_levels: # lists are implicitly boolean: they are False if empty and True if not empty           
            if not any(_level_ in x  for x in degradation_levels):
                continue # Will skip this iteration and continue with next file

            
        # Extract file info
        fileDict['audiofile'].append('audio/'+fileinput)
        fileDict['noise'].append(_noise_)
        fileDict['voice'].append(_voice_)
        # info about sentence content
        fileDict['words'].append(_words_)
        fileDict['callSign'].append(_callSign_)
        fileDict['colour'].append(_colour_)
        fileDict['number'].append(_number_)
        # degradation/noise levels
        fileDict['levels'].append(_level_)
        # number of channels
        fileDict['NV_nChannels'].append(_nCh_)
             
        #add file duration         
        with wave.open(fileinput, 'r') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            length = np.round(frames / float(rate), 4)
            
        fileDict['duration'].append(length)
        
        # Add trigger codes, defined by parts in the filename 
        tmpcode  = [triggerDict_noise[_noise_], 0, 0]
        fileDict['trigger_start'].append(''.join(map(str,tmpcode)))
        
        tmpcode  = [triggerDict_noise[_noise_], 0, 1]
        fileDict['trigger_end'].append(''.join(map(str,tmpcode)))
        
        tmpcode  = [triggerDict_noise[_noise_], 1, triggerDict_call[_callSign_]]
        fileDict['trigger_call'].append(''.join(map(str,tmpcode)))
        fileDict['trigger_call_end'].append(''.join(map(str,tmpcode[0:2])) + '0')
        
        tmpcode  = [triggerDict_noise[_noise_], 2,triggerDict_col[_colour_]]
        fileDict['trigger_col'].append(''.join(map(str,tmpcode)))
        fileDict['trigger_col_end'].append(''.join(map(str,tmpcode[0:2])) + '0')
        
        tmpcode  = [triggerDict_noise[_noise_], 3, triggerDict_num[_number_]]
        fileDict['trigger_num'].append(''.join(map(str,tmpcode)))
        fileDict['trigger_num_end'].append(''.join(map(str,tmpcode[0:2])) + '0')
        
        
        
        #Get praat info of onsets/offsets
        praatTimes.file = praatTimes.file.str.replace('-man.','.')
        names2match = praatTimes['file'].str.split('.TextGrid').str[0]
        rowidx = np.where('_'.join(fileinput.split('_')[1:4])==names2match)[0]
        times.append(praatTimes.iloc[rowidx])       
        
    times = pd.concat(times) # concatenating dfs from the list into one df
    reIdx = pd.Series(range(len(times)))
    times.set_index(reIdx, inplace = True) # re-indexing
    
    # merge data frames with trial info and times
    tab = pd.DataFrame.from_dict(fileDict)
    if len(files) == len(times):
        tab = tab.join(times)
    else:
        print('~~~~~~~~~~~~ d[O_o]b. Could not find times for all files. Revise your praat summary!')
    
    # % Merge to main dataframe 
    # fullTab = fullTab.append(tab)     # Again. Better to append to list and then concatenate
    fullTab = tab      # But since for experiment 2, I only have 1 noiseType and therefore the outermost loop is irrelevant, I can just do this.
    
    # %%    
    # Add index by noise , voice and Level (to use for block assignment)
    fullTab2save = fullTab.groupby(['noise','voice','levels']).sample(frac=1) 
    #fullTab2save = fullTab.groupby(['noise','voice','levels'])
    #fullTab2save['newidx'] = fullTab2save.groupby(['noise','voice','levels']).cumcount(ascending=True)
    fullTab2save['newidx'] = fullTab2save.groupby(['noise','voice','levels']).cumcount(ascending=True)
    
    # # assign blocks: only 16 trials per Level are taken 
    # fullTab2save['block'] = 0
    # fullTab2save.block[(fullTab2save['noise']=='SiSSN') & (fullTab2save['newidx'].between(0, 15, inclusive='both'))] = 'SSN1' 
    # fullTab2save.block[(fullTab2save['noise']=='SiSSN') & (fullTab2save['newidx'].between(16, 31, inclusive='both'))] = 'SSN2'
    # fullTab2save.block[(fullTab2save['noise']=='NV') & (fullTab2save['newidx'].between(0, 15, inclusive='both'))] = 'NV1'
    # fullTab2save.block[(fullTab2save['noise']=='NV') & (fullTab2save['newidx'].between(16, 31, inclusive='both'))] = 'NV2'
    # fullTab2save = fullTab2save.groupby('block').sample(frac=1)
    
    # # Discard excess trials
    # fullTab2save = fullTab2save[fullTab2save['block']!= 0];
    
    # #overview 
    # print(fullTab2save.groupby(['noise','block','voice','levels'])['block'].count())
    # overview = fullTab2save.groupby(['noise','block','voice','levels'])['words'].count().reset_index()
    
    # stimOverview = pd.concat([fullTab2save.groupby(['noise','block','voice','levels'])['words'].count().reset_index(),\
    #                           fullTab2save.groupby(['noise','block','voice','levels'])['callSign'].count().reset_index(),\
    #                               fullTab2save.groupby(['noise','block','voice','levels'])['colour'].count().reset_index(),\
    #                                   fullTab2save.groupby(['noise','block','voice','levels'])['number'].count().reset_index()])

# %% save to file
# with open(os.path.join(diroutput,'tts-golang-selected_PsyPySEQ.csv'),'w', newline='') as csvfile:
#     fullTab2save.to_csv(csvfile,index=False)
    
# # %% save per block    
# for block_value in fullTab2save['block'].unique():    
#     block_df = fullTab2save[fullTab2save['block'] == block_value]    
#     block_df.to_csv(os.path.join(diroutput, 'tts-golang-selected_PsyPySEQ_' + block_value + '.csv'), index=False)

# #%%
# with open(os.path.join(diroutput, 'tts-golang-selected_seqOverview.csv'),'w', newline='') as csvfile:
#         overview.to_csv(csvfile,index=False)

# #%%

# with open(os.path.join(diroutput , 'tts-golang-selected_stimOverview.csv'),'w', newline='') as csvfile:
#         stimOverview.to_csv(csvfile,index=False)
                
  
