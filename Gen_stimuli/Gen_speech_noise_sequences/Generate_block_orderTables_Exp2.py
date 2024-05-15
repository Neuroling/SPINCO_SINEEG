# -*- coding: utf-8 -*-
""" Generate tables defining block order 
----------------------------------------------
- Tables for PsychoPy block organization 

Created on Tue Mar 21 08:32:28 2023

@author: gfraga
"""

import pandas as pd
import numpy as np 
import os 
import itertools
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

for i in range(8):
    order1_tmp = blocks[0:6]
    order2_tmp = swap_pairs(order1_tmp)
    blocks = np.roll(blocks,-9)
    all_orders.append(order1_tmp)
    all_orders.append(order2_tmp)
    


for i, thisOrder in enumerate(all_orders):
    for ii, item in enumerate(thisOrder):
        thisOrder[ii] = os.path.join('flow','tts-golang-selected_PsyPySEQ_' + item + '.csv')
    tab = pd.DataFrame({'condsFile':thisOrder})
    tab.to_csv(os.path.join(diroutput,'order' + str(i) + '.csv'),index=False)

#%%
# NV1 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV1.csv')
# NV2 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV2.csv')
# NV3 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV3.csv')
# NV4 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV4.csv')
# NV5 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV5.csv')
# NV6 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV6.csv')
# NV7 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV7.csv')
# NV8 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV8.csv')

# list1 = [NV1, NV2, NV3, NV4, NV5, NV6, NV7, NV8]
# #%% Orders 

# order1 = list1
# # allOrders = list(itertools.permutations(list1))
# # order1 = [NV1,NV2,NV3,NV4]
# order2 = np.roll(order1, 1)
# # order3 = [NV2,SS1,NV1,SS2]
# # order4 = np.roll(order3, 1)
# # order5 = [NV1,SS2,NV2,SS1]
# # order6 = np.roll(order5, 1)
# # order7 = [NV2,SS2,NV1,SS1]
# # order8 = np.roll(order7, 1)

# # tables 
# os.chdir(diroutput)
# for i in range(1,9):
#     print(i)
#     tab = pd.DataFrame({'condsFile':globals()['order'+str(i)]})
#     tab.to_csv('order' + str(i) + '.csv',index=False)
    
