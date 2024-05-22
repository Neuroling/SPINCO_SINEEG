#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 06:47:27 2024

@author: samuemu

This is copied and adapted from Generate_spreadsheet_Exp2.py
"""
import os
from glob import glob
import pandas as pd
import numpy as np
import wave
import random
import itertools

#%% User Inputs
# Dictionaries with trigger codes: 1st digit = noise, 2nd digit=position (1-call,2-col,3-num), 3rd digit = item (see below)
triggerDict_noise = {'NV':1, 'SiSSN':2, 'clear':3}

triggerDict_call = {'Adl':1, 'Eul':2, 'Rat':3, 'Tig':4, 
                    'Vel':5, 'Aut':6, 'Mes':7, 'Gab':8}
triggerDict_col  = {'gel':1, 'gru':2, 'rot':3, 'wei':4,
                    'bla':5, 'bra':6, 'pin':7, 'sch':8}
triggerDict_num  = {'Ein':1, 'Zwe':2, 'Dre':3, 'Vie':4,
                    'Fue':5, 'Sec':6, 'Neu':7, 'Nul':8}

# which degradation levels should be included? If empty, will include all.
degradation_levels = []

# %% paths 
thisDir = os.getcwd()

baseDir = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Stimuli', 'AudioGens', 'Experiment2')

diroutput = os.path.join(thisDir[:thisDir.find('Scripts')], 'Scripts', 'Experiments','SiN','Experiment2','SiN_practice')

audioDir = os.path.join(baseDir ,'selected_audio_psychoPy_click')
praatSummaryFile = os.path.join(baseDir,'tts-golang-44100hz', 'word-times','equalised_tts-golang_wordTimes.csv')

# get files
audiofiles = glob(os.path.join(audioDir,'*clear.wav'))
praatTimes = pd.read_csv(praatSummaryFile) 


#%%
# Create dict summarizing audiofiles, add times from praat 
fileDict = {'audiofile':[],'duration':[],'noise':[],'voice':[],'words':[],'callSign':[],'colour':[],'number':[],'levels':[],
            'trigger_start':[],'trigger_end':[],'trigger_call':[],'trigger_col':[],'trigger_num':[],
                'trigger_call_end': [],'trigger_col_end':[],'trigger_num_end':[]}
    
times=[] # appending to list and then concatenating to a df is always cheaper

tab = pd.DataFrame() # gather info in file 

#Loop thru .wav audiofiles 
for i, fileinput in enumerate(audiofiles): 
    
    
    # for readability and convenience, we do this here instead of repeating the fileinput.split('_')[n] over and over
    filename = fileinput[fileinput.rfind(os.sep)+1:]
    noise_ = filename.split('_')[0]
    voice_ = '_'.join(filename.split('_')[2:4])
    words_ = filename.split('_')[4]
    
    callSign_ = words_.split('-')[0]
    colour_ = words_.split('-')[1]
    number_ = words_.split('-')[2]
    
    level_ = '.'.join(filename.split('_')[5:])
    level_ = level_[:level_.rfind('.')]
    if len(level_) > 5:
        level_ = level_[:level_.rfind('.')]


    #if degradation_levels is not empty, only include audiofiles in with specified levels
    if degradation_levels: # lists are implicitly boolean: they are False if empty and True if not empty           
        if not any(level_ in x  for x in degradation_levels):
            continue # Will skip this iteration and continue with next file

        
    # Extract file info
    fileDict['audiofile'].append('audio/'+filename)
    fileDict['noise'].append(noise_)
    fileDict['voice'].append(voice_)
    
    # info about sentence content
    fileDict['words'].append(words_)
    fileDict['callSign'].append(callSign_)
    fileDict['colour'].append(colour_)
    fileDict['number'].append(number_)
    
    # degradation/noise levels
    fileDict['levels'].append(level_)
    

         
    #add file duration         
    with wave.open(fileinput, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        length = np.round(frames / float(rate), 4)
        
    fileDict['duration'].append(length)
    
    # Add trigger codes, defined by parts in the filename 
    tmpcode  = [triggerDict_noise[noise_], 0, 0]
    fileDict['trigger_start'].append(''.join(map(str,tmpcode)))
    
    tmpcode  = [triggerDict_noise[noise_], 0, 1]
    fileDict['trigger_end'].append(''.join(map(str,tmpcode)))
    
    tmpcode  = [triggerDict_noise[noise_], 1, triggerDict_call[callSign_]]
    fileDict['trigger_call'].append(''.join(map(str,tmpcode)))
    fileDict['trigger_call_end'].append(''.join(map(str,tmpcode[0:2])) + '0')
    
    tmpcode  = [triggerDict_noise[noise_], 2,triggerDict_col[colour_]]
    fileDict['trigger_col'].append(''.join(map(str,tmpcode)))
    fileDict['trigger_col_end'].append(''.join(map(str,tmpcode[0:2])) + '0')
    
    tmpcode  = [triggerDict_noise[noise_], 3, triggerDict_num[number_]]
    fileDict['trigger_num'].append(''.join(map(str,tmpcode)))
    fileDict['trigger_num_end'].append(''.join(map(str,tmpcode[0:2])) + '0')
    
    
    
    #Get praat info of onsets/offsets
    praatTimes.file = praatTimes.file.str.replace('-man.','.')
    names2match = praatTimes['file'].str.split('.TextGrid').str[0]
    rowidx = np.where('_'.join(filename.split('_')[2:5])==names2match)[0]
    times.append(praatTimes.iloc[rowidx])       
    
times = pd.concat(times) # concatenating dfs from the list into one df
reIdx = pd.Series(range(len(times)))
times.set_index(reIdx, inplace = True) # re-indexing

# merge data frames with trial info and times
tab = pd.DataFrame.from_dict(fileDict)
if len(audiofiles) == len(times):
    tab = tab.join(times)
else:
    print('~~~~~~~~~~~~ d[O_o]b. Could not find times for all audiofiles. Revise your praat summary!')


# %%  ----- GENERATING ALL UNIQUE LISTS OF 32 TRIALS -----  
call = list(triggerDict_call.keys())
col = list(triggerDict_col.keys())
num = list(triggerDict_num.keys())
random.shuffle(call)
random.shuffle(col)
random.shuffle(num)


#%% create the unique lists
ColNum = list(itertools.product(*[col,num]))
ColNum = ['-'.join(i) for i in ColNum]

n_targets = len(col)
n_allocations = 16
allocation_list = np.arange(n_allocations//2)
random.shuffle(allocation_list)
designation_lists = {key: [] for key in range(n_allocations//1)}

for y in allocation_list:
    tmp_list = []
    for i, call_ in enumerate(call):
        
        for x in range(n_targets):
            CallColNum = '-'.join([call_, ColNum[x*n_targets+x]])
            tmp_list.append(CallColNum)   
        ColNum = np.roll(ColNum, -n_targets)
        
    designation_lists[y] = tmp_list[::2]
    designation_lists[y+8] = tmp_list[1::2]
    
    call = np.roll(call, -1)


     
#%%
# check if the lists are actually unique
check_unique = []
check_duplicates = []
for i in range(len(designation_lists)):
    if len(set(designation_lists[i])) != len(designation_lists[i]):
        check_duplicates.append[i]
    for j in range(i+1, len(designation_lists)):
        if any(item in designation_lists[i] for item in designation_lists[j]):   
            ch_count = [item in designation_lists[i] for item in designation_lists[j]].count(True)
            print('True', i, j, 'overlap:', ch_count)
            check_unique.append([i,j,ch_count])
if check_unique: raise ValueError('lists are not unique')
if check_duplicates: raise ValueError('at least one list contains duplicates')




#%%

# Function to find the key for a given value in the dictionary of lists
def find_key(value):
    for key, value_list in designation_lists.items():
        if value in value_list:
            return key
    return None

# Adding a new column to the DataFrame with the key from the dictionary of lists
tab['allocation_list'] = tab['words'].apply(find_key)

# Add a new column with the block designation for NV
tab['block'] = tab['allocation_list'].apply(lambda x: str(x)) # cast to str
tab.loc[tab['noise'] == 'clear', 'block'] = tab.loc[tab['noise'] == 'clear', 'block'].apply(lambda x: 'block'+x)

tab2save = tab.loc[tab['block'] == 'block1']

# %% save to file
outputname = 'flow' + os.sep + 'tts-golang-selected_PsyPySEQ.csv'
with open(os.path.join(diroutput,outputname),'w', newline='') as csvfile:
    tab2save.to_csv(csvfile,index=False)

    
orderTab = pd.DataFrame({'condsFile':outputname}, index = [0])
orderTab.to_csv(os.path.join(diroutput,'order1.csv'),index=False)
