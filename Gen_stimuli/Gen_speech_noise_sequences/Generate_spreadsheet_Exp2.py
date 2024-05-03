# -*- coding: utf-8 -*-
""" GENERATE SPREADSHEETS FOR PSYCHOPY WITH LISTS OF TRIALS
---------------------------------------------------------------------

- Extract info from wav filename (tokens in sentence, voice, type of noise)
- Read wav durations
- Gather onset and offset of targets (inspected with Praat & Webmaus)
- Assign blocks splitting noise type: NV1, NV2:
- Select 1 voice and 3 degradation levels
- Equal number of trials for each level
- 32 trials x 2 voices x 3 levels = 192 trials per block (~20 min)
- Save the full table and a table per block   

Created on Thu Feb  9 10:37:20 2023
@author: gfraga & samuemu
"""
import os
import sys
from glob import glob
import pandas as pd
import numpy as np
import wave

#%% User Inputs
# Dictionaries with trigger codes: 1st digit = noise, 2nd digit=position (1-call,2-col,3-num), 3rd digit = item (see below)
triggerDict_noise = {'NV':1}

triggerDict_call = {'Adl':1, 'Eul':2, 'Rat':3, 'Tig':4, 
                    'Flu':5, 'Aut':6, 'Ham':7, 'Sch':8}
triggerDict_col  = {'gel':1, 'gru':2, 'rot':3, 'wei':4,
                    'bla':5, 'bra':6, 'pin':7, 'sch':8}
triggerDict_num  = {'Ein':1, 'Zwe':2, 'Dre':3, 'Vie':4,
                    'Fue':5, 'Sec':6, 'Ach':8, 'Neu':9}

# which degradation levels should be included? If empty, will include all.
degradation_levels = []

# %% paths 
thisDir = os.getcwd()

baseDir = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Stimuli', 'AudioGens', 'Experiment2')

diroutput = os.path.join(baseDir, 'flow')

audioDir = os.path.join(baseDir, 'tts-golang-44100hz','tts-golang-NV-click')
praatSummaryFile = os.path.join(baseDir, 'tts-golang-44100hz','word-times','automatic_tts-golang_wordTimes.csv')

# get files
audiofiles = glob(os.path.join(audioDir,'*.wav'))
praatTimes = pd.read_csv(praatSummaryFile) 


#%%
# Create dict summarizing audiofiles, add times from praat 
fileDict = {'audiofile':[],'duration':[],'noise':[],'voice':[],'words':[],'callSign':[],'colour':[],'number':[],'levels':[],\
            'NV_nChannels':[],'trigger_start':[],'trigger_end':[],'trigger_call':[],'trigger_col':[],'trigger_num':[],\
                'trigger_call_end': [],'trigger_col_end':[],'trigger_num_end':[]}
    
times=[] # appending to list and then concatenating to a df is always cheaper

tab = pd.DataFrame() # gather info in file 

#Loop thru .wav audiofiles 
for i, fileinput in enumerate(audiofiles): 
    
    
    # for readability and convenience, we do this here instead of repeating the fileinput.split('_')[n] over and over
    filename = fileinput[fileinput.rfind(os.sep)+1:]
    _noise_ = filename.split('_')[0]
    _voice_ = filename.split('_')[2]
    _words_ = filename.split('_')[3]
    
    _callSign_ = _words_.split('-')[0]
    _colour_ = _words_.split('-')[1]
    _number_ = _words_.split('-')[2]
    
    _level_ = filename.split('_')[4] 
    _nCh_ = filename.split('_')[5].split('.wav')[0]
    
    #if degradation_levels is not empty, only include audiofiles in with specified levels
    if degradation_levels: # lists are implicitly boolean: they are False if empty and True if not empty           
        if not any(_level_ in x  for x in degradation_levels):
            continue # Will skip this iteration and continue with next file

        
    # Extract file info
    fileDict['audiofile'].append('audio/'+filename)
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
if len(audiofiles) == len(times):
    tab = tab.join(times)
else:
    print('~~~~~~~~~~~~ d[O_o]b. Could not find times for all audiofiles. Revise your praat summary!')


# %%    
# Add index by noise , voice and Level (to use for block assignment)
tab2save = tab.groupby(['noise','voice','levels']).sample(frac=1) 
#tab2save = tab.groupby(['noise','voice','levels'])
#tab2save['newidx'] = tab2save.groupby(['noise','voice','levels']).cumcount(ascending=True)
tab2save['newidx'] = tab2save.groupby(['noise','voice','levels']).cumcount(ascending=True)

# # assign blocks: only 16 trials per Level are taken 
# tab2save['block'] = 0
# tab2save.block[(tab2save['noise']=='SiSSN') & (tab2save['newidx'].between(0, 15, inclusive='both'))] = 'SSN1' 
# tab2save.block[(tab2save['noise']=='SiSSN') & (tab2save['newidx'].between(16, 31, inclusive='both'))] = 'SSN2'
# tab2save.block[(tab2save['noise']=='NV') & (tab2save['newidx'].between(0, 15, inclusive='both'))] = 'NV1'
# tab2save.block[(tab2save['noise']=='NV') & (tab2save['newidx'].between(16, 31, inclusive='both'))] = 'NV2'
# tab2save = tab2save.groupby('block').sample(frac=1)

# # Discard excess trials
# tab2save = tab2save[tab2save['block']!= 0];

# #overview 
# print(tab2save.groupby(['noise','block','voice','levels'])['block'].count())
# overview = tab2save.groupby(['noise','block','voice','levels'])['words'].count().reset_index()

# stimOverview = pd.concat([tab2save.groupby(['noise','block','voice','levels'])['words'].count().reset_index(),\
#                           tab2save.groupby(['noise','block','voice','levels'])['callSign'].count().reset_index(),\
#                               tab2save.groupby(['noise','block','voice','levels'])['colour'].count().reset_index(),\
#                                   tab2save.groupby(['noise','block','voice','levels'])['number'].count().reset_index()])

# %% save to file
# with open(os.path.join(diroutput,'tts-golang-selected_PsyPySEQ.csv'),'w', newline='') as csvfile:
#     tab2save.to_csv(csvfile,index=False)
    
# # %% save per block    
# for block_value in tab2save['block'].unique():    
#     block_df = tab2save[tab2save['block'] == block_value]    
#     block_df.to_csv(os.path.join(diroutput, 'tts-golang-selected_PsyPySEQ_' + block_value + '.csv'), index=False)

# #%%
# with open(os.path.join(diroutput, 'tts-golang-selected_seqOverview.csv'),'w', newline='') as csvfile:
#         overview.to_csv(csvfile,index=False)

# #%%

# with open(os.path.join(diroutput , 'tts-golang-selected_stimOverview.csv'),'w', newline='') as csvfile:
#         stimOverview.to_csv(csvfile,index=False)
                
  
