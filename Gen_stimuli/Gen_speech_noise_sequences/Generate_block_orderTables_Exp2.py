# -*- coding: utf-8 -*-
""" 
Generate tables defining block order 
----------------------------------------------
- Tables for PsychoPy block organization 

Created on Tue Mar 21 08:32:28 2023

@author: gfraga & samuemu
"""

import pandas as pd
import numpy as np 
import os 
from glob import glob


#%%
thisDir = os.getcwd()
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Stimuli', 'AudioGens','Experiment2', 'flow')
diroutput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Stimuli', 'AudioGens','Experiment2', 'block_order') 

#%% File names to provide 
files = glob(os.path.join(dirinput,'tts-golang-selected_PsyPySEQ_*'))

#%% create a list of all blocks (alternating SSN and NV)
n_blocks = list(range(len(files)//2))
blocks_NV = ['NV' + str(i) for i in n_blocks]
blocks_SSN = ['SSN' + str(i) for i in n_blocks]
blocks = [item for pair in zip(blocks_SSN, blocks_NV) for item in pair]

#%%
# Function to swap the order of NV and SSN but keeping the sequence of the block numbers
# i.e. ['SSN0', 'NV0', 'SSN1', 'NV1', 'SSN2', 'NV2'] becomes ['NV0', 'SSN0', 'NV1', 'SSN1', 'NV2', 'SSN2']
def swap_pairs(order):
    return [order[i + 1] if i % 2 == 0 else order[i - 1] for i in range(len(order))]

all_orders = []

# create lists of block orders
# range(N) will create N*2 block orders. 
# The biggest value for N before the orders start repeating is N=len(files)/2
for i in range(8): 
    order1_tmp = blocks[0:6]
    order2_tmp = swap_pairs(order1_tmp)
    blocks = np.roll(blocks,-9)
    all_orders.append(order1_tmp)
    all_orders.append(order2_tmp)
    
for i, thisOrder in enumerate(all_orders):
    for ii, item in enumerate(thisOrder): # replace block designations (e.g. NV1) by filepath to csv file of the block
        thisOrder[ii] = os.path.join('flow','tts-golang-selected_PsyPySEQ_' + item + '.csv')
    tab = pd.DataFrame({'condsFile':thisOrder})
    tab.to_csv(os.path.join(diroutput,'order' + str(i+1) + '.csv'),index=False)
