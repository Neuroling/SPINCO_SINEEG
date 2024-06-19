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
output_fp = beh_fp[:beh_fp.find('SentenceInNoise')] + 'ADJUSTED_' + beh_fp[beh_fp.find('SentenceInNoise'):beh_fp.rfind('.xlsx')] + '.csv'

print('Reading subject', subjID)

df_dict = pd.read_excel(beh_fp, sheet_name=None)
df_list = []
#%%
for key in df_dict.keys():
    df = df_dict[key]
    
    # get the index of the NaN-row (after the trial data, before the additional info)
    idx = df.index[df['audiofile'].isnull()][0]
    
    # save the additional info
    extraInfo = df.copy()
    toDrop = list(range(0,idx+2, 1))
    extraInfo = extraInfo.drop(index = toDrop)
    extraInfo = pd.Series(extraInfo['duration'].tolist(), index= extraInfo['audiofile'])
    
    # drop additional information
    toDrop = list(range(idx,len(df), 1))
    df = df.drop(index = toDrop)
    
    #%% delete additional mouse clicks. Iterate over call, colour and number
    stim_word = ['Call', 'Colour', 'Number']
    # col_names = ['mouseClickOnCall.clicked_name_raw','mouseClickOnColour.clicked_name_raw','mouseClickOnNumber.clicked_name_raw']
    
    for stimName in stim_word:
        clicked_name = 'mouseClickOn' + stimName +'.clicked_name_raw'
        clicked_name_idx = df.columns.get_loc(clicked_name)
        
        # iterate over rows (trials)
        for index, row in df.iterrows():
            
            mouse_clicks = row.iloc[clicked_name_idx +4 : clicked_name_idx +7]
            if all(cell in [0, 1] for cell in mouse_clicks):
                
                # Get the values of the row as a list
                row_values = row.tolist()
                
                # get idx of first non 0 or 1
                nextIdx = [row_values.index(i) for i in row_values[clicked_name_idx+1:] if (i not in [0,1, '0', '1'])][0]
                
                # So now we know that the rows are shifted by TWICE this amount (once for mouse clicks, once for their timings)
                shiftedBy = (nextIdx - clicked_name_idx -1)-3
                if shiftedBy % 3 != 0:
                    raise ValueError
                
                # Delete the contents of the cells we don't need
                del row_values[clicked_name_idx +4 : clicked_name_idx +4 + shiftedBy]
                del row_values[clicked_name_idx +7 : clicked_name_idx +7 + shiftedBy]
                
                # Append None values to the end of the row to maintain the length
                row_values.extend([None] * (shiftedBy * 2))
               
                # Update the row in the DataFrame
                df.loc[index] = row_values
                
    df['trials.thisIndex'] = df.index
    
    # sort by order of presentation
    df = df.sort_values(by='order')
    df = df.reset_index(drop=True)
    df.rename(columns = {'order' : 'trials.thisN', 'callSignCorrect_raw': 'callSignCorrect',
                         'colourCorrect_raw': 'colourCorrect', 'numberCorrect_raw' : 'numberCorrect',
                         'mouseClickOnCall.clicked_name_raw':'mouseClickOnCall.clicked_name',
                         'mouseClickOnColour.clicked_name_raw':'mouseClickOnColour.clicked_name',
                         'mouseClickOnNumber.clicked_name_raw' : 'mouseClickOnNumber.clicked_name' }, inplace = True)

    # drop empty columns
    toDrop = [colName for colName in df.columns if ('Unnamed' in colName) ]
    df = df.drop(columns = toDrop)
    
    # append to list of dfs
    df_list.append(df)

df = pd.concat(df_list)
df = df.reset_index(drop=True)



# add extra info as column
for i, variable in enumerate(extraInfo):
    idx = extraInfo.index[i]
    df[idx] = variable

df.to_csv(output_fp,index=False)
