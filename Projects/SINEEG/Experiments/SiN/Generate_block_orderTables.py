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

diroutput = 'V:/spinco_data/AudioGens'
# File names to provide 
NV1 = 'flow\tts-golang-selected_PsyPySEQ_NV1.csv'
NV2 = 'flow\tts-golang-selected_PsyPySEQ_NV2.csv'
SS1 = 'flow\tts-golang-selected_PsyPySEQ_SSN1.csv'
SS2 = 'flow\tts-golang-selected_PsyPySEQ_SSN2.csv'

# Orders 

order1 = [NV1,SS1,NV2,SS2]
order2 = np.roll(order1, 1)
order3 = [NV2,SS1,NV1,SS2]
order4 = np.roll(order3, 1)
order5 = [NV1,SS2,NV2,SS1]
order6 = np.roll(order5, 1)
order7 = [NV2,SS2,NV1,SS1]
order8 = np.roll(order7, 1)

# tables 
os.chdir(diroutput)
for i in range(1,9):
    print(i)
    tab = pd.DataFrame({'condsFile':globals()['order'+str(i)]})
    tab.to_csv('order' + str(i) + '.csv',index=False)
