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


#%%
thisScriptDir = os.getcwd()
scripts_index = thisScriptDir.find('Scripts')
diroutput = os.path.join(thisScriptDir[:scripts_index] + 'Stimuli', 'AudioGens','flow_Experiment2')

#%% File names to provide 

NV1 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV1.csv')
NV2 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV2.csv')
NV3 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV3.csv')
NV4 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV4.csv')
NV5 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV5.csv')
NV6 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV6.csv')
NV7 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV7.csv')
NV8 = os.path.join(diroutput,'tts-golang-selected_PsyPySEQ_NV8.csv')

list1 = [NV1, NV2, NV3, NV4, NV5, NV6, NV7, NV8]
#%% Orders 

order1 = list1
# allOrders = list(itertools.permutations(list1))
# order1 = [NV1,NV2,NV3,NV4]
order2 = np.roll(order1, 1)
# order3 = [NV2,SS1,NV1,SS2]
# order4 = np.roll(order3, 1)
# order5 = [NV1,SS2,NV2,SS1]
# order6 = np.roll(order5, 1)
# order7 = [NV2,SS2,NV1,SS1]
# order8 = np.roll(order7, 1)

# tables 
os.chdir(diroutput)
for i in range(1,9):
    print(i)
    tab = pd.DataFrame({'condsFile':globals()['order'+str(i)]})
    tab.to_csv('order' + str(i) + '.csv',index=False)
    
#%% for level test:
# os.chdir(diroutput)
# for i in range(1,9):
#     print(i)
#     tab = pd.DataFrame({'condsFile':list1[i:i+1]})
#     tab.to_csv('order' + str(i) + '.csv',index=False)
