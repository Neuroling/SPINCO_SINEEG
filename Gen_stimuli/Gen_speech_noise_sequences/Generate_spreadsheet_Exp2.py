# -*- coding: utf-8 -*-
""" GENERATE SPREADSHEETS FOR PSYCHOPY WITH LISTS OF TRIALS
---------------------------------------------------------------------

- Extract info from wav filename (tokens in sentence, voice, type of noise)
- Read wav durations
- Gather onset and offset of targets (inspected with Webmaus)
- Assign blocks splitting noise type: NV1, NV2,... and same for SSN
    - In each block, every unique callSign, colour and number will occur 4 times exactly
      as degraded stimuli (32 trials of degraded stimuli) and 2 times as clear/non-degraded
      stimuli (16 trials of non-degraded stimuli).
    - No combination of callSign, colour or number is repeated
    
- Save the full table and a table per block   

Created on Thu Feb  9 10:37:20 2023
@author: gfraga & samuemu
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

diroutput = os.path.join(baseDir, 'flow')

audioDir = os.path.join(baseDir ,'selected_audio_psychoPy_click')
praatSummaryFile = os.path.join(baseDir,'tts-golang-44100hz', 'word-times','equalised_tts-golang_wordTimes.csv')

# get files
audiofiles = glob(os.path.join(audioDir,'*.wav'))
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
ls1 = list(triggerDict_call.keys())
ls2 = list(triggerDict_col.keys())
ls3 = list(triggerDict_num.keys())
random.shuffle(ls1)
random.shuffle(ls2)
random.shuffle(ls3)

listOfLs = [ls1, ls2, ls3]


n_allocations = 16 # How many unique & non-overlapping blocks we want
n_targets = len(ls1) # how many items are in each list (assuming they are equal)
n_possiblecombinations = n_targets**3 # possible combinations (n_targets to the power of 3)
n_trialsPerBlock = n_possiblecombinations // n_allocations

n_appearcancesPerBlock = n_trialsPerBlock // n_targets # how many times each item should appear in each block

#%% create some variables
allocation_list = np.arange(n_allocations//2)
random.shuffle(allocation_list) # shuffle so they are randomly assigned to block
allocation_list = list(allocation_list)
# designation_lists = {key: [] for key in range(n_allocations//1)}
designation_lists = {key: [] for key in range(n_allocations)}

#%%
item_allocation_list = np.arange(n_targets)
indexes = []
for i in range(n_targets):
    indexes += [i * 8 + item for item in item_allocation_list[:4]]
    item_allocation_list = np.roll(item_allocation_list, -1)


#%% create the unique lists
# list of every combination of ls2 and ls3
ls2ls3 = list(itertools.product(*[ls2,ls3]))
ls2ls3 = ['-'.join(i) for i in ls2ls3]


for y in allocation_list: # for every list we want...
    tmp_list = []
    
    for i, ls1_ in enumerate(ls1): # for every possible item on lst1
        
        for x in range(n_targets):
            ls1ls2ls3 = '-'.join([ls1_, ls2ls3[x*n_targets+x]])
            tmp_list.append(ls1ls2ls3)   
        ls2ls3 = np.roll(ls2ls3, -n_targets)
        
    designation_lists[y*2] = [tmp_list[idx] for idx in indexes]
        
    # designation_lists[y] = tmp_list[::2]
    designation_lists[y*2+1] = [item for item in tmp_list if item not in designation_lists[y*2]]
    
    ls1 = np.roll(ls1, -1)


     
#%% check if the lists are actually unique, check if they contain duplicates
check_unique = []
check_duplicates = []
check_n_appearances = []

# Loop over every list in the dict
for i in range(len(designation_lists)):
    
    # transforming a list to set will erase duplicates. 
    # So if len(set(someList)) != len(someList) then there are duplicates
    if len(set(designation_lists[i])) != len(designation_lists[i]):
        check_duplicates.append[i]
        print('list', i, 'contains duplicates')
    
    # check every list in the dict against every other list in the dict    
    for j in range(i+1, len(designation_lists)):
        
        # check if any items in any two lists overlap, if yes, count how many common elements
        if any(item in designation_lists[i] for item in designation_lists[j]):   
            ch_count = [item in designation_lists[i] for item in designation_lists[j]].count(True)
            print('lists', i,'and', j, 'overlap in', ch_count, 'items')
            check_unique.append([i,j,ch_count])

# check if every item occurs as many times as it should            
for key, desig_lst in enumerate(designation_lists.values()):
    for lst in listOfLs:
        for substr in lst:
            occ_count = len([i for i in desig_lst if substr in i])
            if occ_count != n_appearcancesPerBlock: 
                print('in List', key, "item", substr, "occurs", occ_count, 'times') 
                check_n_appearances.append([key,substr,occ_count])
                
if check_unique: 
    raise ValueError('lists are not unique')
if check_duplicates: 
    raise ValueError('at least one list contains duplicates')
if check_n_appearances: 
    raise ValueError('not all items appear %s times', n_appearcancesPerBlock)



#%%

"""
Now, I need to create the blocks...

We do 3 blocks per noise type, so 6 blocks in total.
Each block has 32 degraded trials, and 16 clear trials (total 48).
Therefore, I will use 9 unique lists for each participant:
    - each block has a unique list for the degraded stimuli
    - for clear stimuli, additional 3 lists which are divided in two

So, for participant 1, it needs to be 
NV:    allocation list 0, 1, 2
SiSSN: allocation list 3, 4, 5
clear: allocation list 6, 7, 8

Block designations: 
    NVx means the NV stimuli of allocation list x
    SSNx means the SSN stimuli of allocation list x+3

For the clear stimuli:
    the clear stimuli of allocation list x+6 are assigned to NVx and SSNx in alternating order
    
Note: We have 16 allocation lists. If x+3 or x+6 is over 15, it will wrap around to 0
"""

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
tab.loc[tab['noise'] == 'NV', 'block'] = tab.loc[tab['noise'] == 'NV', 'block'].apply(lambda x: 'NV'+x)

# create the block designations for SiSSN - first we need a list that is shifted by 3 (3,4,5,...,15,0,1,2)
numbers_list = np.arange(16)
numbers_list = np.roll(numbers_list, -3)

for i in range(16): # iterate over the 16 blocks

    # Create designation for current block
    block_designation = 'SSN' + str(i) 
    
    #subset df by SiSSN and allocation_list i+3
    tmp_df = tab[tab['noise'] == 'SiSSN']
    tmp_df = tmp_df[tmp_df['allocation_list'] == numbers_list[i]]
    
    # Replace the values in 'block' for SiSSN and allocation_list i+3 by 'SSN(i)'
    tab.loc[tmp_df.index, 'block'] = block_designation
    
    # subset df by clear stimuli and allocation list i+6
    tmp_df = tab[tab['noise'] == 'clear']
    tmp_df = tmp_df[tmp_df['allocation_list'] == np.roll(numbers_list,-3)[i]]
    
    # Replace the values in 'block' for clear stimuli and allocation_list i+6 by 'NV(i)'
    tab.loc[tmp_df.index, 'block'] = 'NV' + str(i)
    # Same as the last line, but only replace every second value (so half are SSNi and half are NVi)
    tab.loc[tmp_df.index[1::2], 'block'] = 'SSN' + str(i)


# %% save to file
with open(os.path.join(diroutput,'tts-golang-selected_PsyPySEQ.csv'),'w', newline='') as csvfile:
    tab.to_csv(csvfile,index=False)
    
# %% save per block    
for block_value in tab['block'].unique():    
    block_df = tab[tab['block'] == block_value]    
    block_df.to_csv(os.path.join(diroutput, 'tts-golang-selected_PsyPySEQ_' + block_value + '.csv'), index=False)
