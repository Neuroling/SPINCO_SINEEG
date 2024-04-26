#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Evaluation of the Level Test
===============================================================================
Created on Wed Apr 24 07:36:35 2024
@author: samuemu

This script needs to be saved in the same directory as the "data" folder.
Simply adjust the subjID below this docstring, and receive trial accuracy 
and a summary of the accuracy within degradation levels.

"""
subjID = 's003'

import os
import pandas as pd
import numpy as np
from glob import glob

thisDir = os.getcwd()


filepath = glob(os.path.join(thisDir, 'data', str(subjID + '_SentenceInNoise_' +"*" + "trials.csv")), recursive=True)[0]


data_raw = pd.read_csv(filepath)
columns = ['callSign', 'colour', 'number', 'levels', 'mouseClickOnCall.clicked_name_raw', 'mouseClickOnColour.clicked_name_raw','mouseClickOnNumber.clicked_name_raw']
data = pd.DataFrame()
for col in columns:
    data[col] = data_raw[col]
    
data.dropna(subset=['callSign', 'colour', 'number', 'levels'], inplace=True)
data.replace({'call1': 'Ad', 'call2':'Dr','call3':'Kr','call4':'Ti',
              'colour1':'ge','colour2':'gr','colour3':'ro','colour4':'we',
              'number1':'Ei','number2':'Zw','number3':'Dr','number4':'Vi'}, inplace= True)

data['callCor'] = np.where((data['callSign'] == data['mouseClickOnCall.clicked_name_raw']), 1, 0)
data['colCor'] = np.where((data['colour'] == data['mouseClickOnColour.clicked_name_raw']), 1, 0)
data['numCor'] = np.where((data['number'] == data['mouseClickOnNumber.clicked_name_raw']), 1, 0)
data['totalCor'] = data[['callCor', 'colCor','numCor']].mean(axis=1)

sum_data = data.groupby(['levels'])['totalCor'].mean()
