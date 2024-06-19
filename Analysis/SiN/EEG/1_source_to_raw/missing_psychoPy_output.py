#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CREATE .CSV FILE FROM INCOMPLETE PSYCHOPY OUTPUTS
=================================================
Created on Tue Jun 18 08:36:29 2024
@author: samuemu

In s203, PsychoPy froze while saving the data and had to be killed. As a result, 
the s203_SentenceInNoise_[date]_[time].csv file we usually use is empty. 
However, the s203_SentenceInNoise_[date]_[time].xlsx file is there.
Unfortunately, that file has some issues, such as:
    - every block is in different excel sheet
    - the rows (trials) are not in the (randomised) order in which they were 
        presented, but there is a column indicating trial number
    - Precise timing for presentations of stimuli (relative to the start of 
        the experiment) is missing. This includes the recorded audio onset. 
        However, we never used that in our previous analyses.
    - Sometimes, multiple mouse clicks are recorded for the same stimulus,
        which leads to weird formatting:
            In the usual .csv file, clicks are listed with square brackets. So
            multiple clicks would be listed as (for example) `[1,1]`. But in
            this file, they are listed without the square brackets (e.g. `1,1). 
            Therefore, multiple mouse clicks are treated as separate cells, 
            shifting all other cells to the right by 6 (mouse click left, middle 
            and right, plus timing or each)
        In these instances, all mouse clicks beyond the first ones are deleted
        in this script, then the cells are shifted back to where they should be.
        It's not ideal, but since we never used this data anyways... well.
"""
from glob import glob
import os 
import pandas as pd 
import numpy as np

# User inputs
taskID = 'task-sin'
subjID = 's203'

# PATHS
_thisDir = os.getcwd()
dirinput = os.path.join(_thisDir[:_thisDir.find('Scripts')] + 'Data','SiN','sourcedata', subjID)
beh_fp = glob(os.path.join(dirinput, '*.xlsx'))[0]

print('Reading subject', subjID)

df_dict = pd.read_excel(beh_fp, sheet_name=None)

#%%
for key in df_dict.keys():
    df = df_dict[key]
    
    # get the index of the NaN-row (after the trial data, before the additional info)
    idx = df.index[df['audiofile'].isnull()][0]
    
    # drop additional information
    toDrop = list(range(idx,len(df), 1))
    df = df.drop(index = toDrop)
    
    #%% delete additional mouse clicks
    col_idx = df.columns.get_loc('mouseClickOnColour.clicked_name_raw')
    
    # iterate over rows
    for index, row in df.iterrows():
        # check if the row is recorded accurately (i.e. if the cell contains a string)
        if not isinstance(row.iloc[col_idx], str):
            
            # Get the values of the row as a list
            row_values = row.tolist()
            
            # get the index of where 'mouseClickOnColour.clicked_name_raw' actually is
            actualStr = [row_values.index(i) for i in row_values[col_idx:] if(type(i) is str)][0]
            shiftedBy = actualStr - col_idx
            
            idxToDelete
            
            # # # Delete the contents of the cells we don't need
            # del row_values[col_idx -3 : col_idx]
            # del row_values[col_idx : col_idx +3]
           
            # # Append None values to the end of the row to maintain the length
            # row_values.extend([None] * 6)
           
            # # Update the row in the DataFrame
            # df.loc[index] = row_values
            break
    break
