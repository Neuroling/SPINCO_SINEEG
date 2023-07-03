# -*- coding: utf-8 -*-
""" Label EEG epochs
===============================================
Created on Tue Apr 25 10:56:48 2023
- Label epochs as correct vs incorrect for two class classification
- Read trial info from Psychopy .csv file logging experiment performance
- Use start of the block as anchor event

Created on Thu Jun 15 08:54:39 2023
@author: gfraga
"""
import os 
import shutil
import pandas as pd 

# User inputs
copyraw = 1;
subID = 'p004'
taskID = 'task-sin'

# PATHS
thisDir = os.path.dirname(os.path.abspath(__file__))
rawdir = os.path.join(thisDir[:thisDir.find('scripts')] + 'Data','SiN','rawdata', subID,taskID,'beh')
diroutput = os.path.join(thisDir[:thisDir.find('scripts')] + 'Data','SiN','derivatives',subID,taskID,'beh')
os.makedirs(diroutput, exist_ok=True);

# %% Copy raw data into the analysis folder 
if copyraw == 1:
    rawfiles = os.listdir(rawdir)
    # Loop through the files to find the CSV file
    for file in rawfiles:
        if file.endswith(".csv") and file[-5].isdigit():
            # If the file is a CSV file, copy it to the output directory
            filepath = os.path.join(rawdir, file)
            outputpath = os.path.join(diroutput, file)
            
            shutil.copyfile(filepath, outputpath)
            print(['saved ' + outputpath])

# %% Read and summary from Analysis folder 
files = os.listdir(diroutput)

# Loop through the files to find the CSV file
for file in files:
    if file.endswith(".csv") and file[-5].isdigit():  #do not the one ending in *trials.csv 
        
 
        # %% read data frame 
        filepath = os.path.join(diroutput, file)         
        df = pd.read_csv(filepath, header = 0)                   
        # % Check accuracy 

        # Exclude last row if the number of rows is more than 388
        if len(df) > 388:
            df = df.iloc[:-1]
        if len(df) > 388:
            raise ValueError("The number of rows exceeds 388. Script terminated.")

        #%

        df['callSignCorrect'] = pd.to_numeric(df['callSignCorrect'].map({'True': 1, 'False': 0, "NO_ANSW": ''}),errors='coerce')
        df['colourCorrect'] =  pd.to_numeric(df['colourCorrect'].map({'True': 1, 'False': 0, "NO_ANSW": ''}),errors='coerce')
        df['numberCorrect'] =  pd.to_numeric(df['numberCorrect'].map({'True': 1, 'False': 0, "NO_ANSW": ''}),errors='coerce')
        
        df['callSignCorrect']
        df['colourCorrect'] 
        df['numberCorrect']


# # %% cross check 

        
# #    #-Checking accuracy will change as future log files will have 3 boolean columns for each target item -------------------------------------------------   
# #    # % Assess accuracy     
#     map_call = {'Ad':'call1','Dr':'call2','Kr':'call3','Ti':'call4'}
#     map_col = {'ge':'colour1','gr':'colour2','ro':'colour3','we':'colour4'}
#     map_num = {'Ei':'number1','Zw':'number2','Dr':'number3','Vi':'number4'}
   

      
#  #    # compare response with presented stimuli
# tester = df.copy().iloc[4:]

# #    # Fix formatting issues, subject response values are coded as "['call1']"
# tester['mouseClickOnCall.clicked_name'] = tester['mouseClickOnCall.clicked_name'].apply(lambda x:       x.replace('[\'', '').replace('\']', ''))
# tester['mouseClickOnColour.clicked_name'] = tester['mouseClickOnColour.clicked_name'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))
# tester['mouseClickOnNumber.clicked_name'] = tester['mouseClickOnNumber.clicked_name'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))   
    
# tester.insert(0, 'accu_call', (tester['mouseClickOnCall.clicked_name'] == tester.callSign.replace(map_call)).astype(int))
# tester.insert(0, 'accu_col', (tester['mouseClickOnColour.clicked_name'] == tester.colour.replace(map_col)).astype(int))
# tester.insert(0, 'accu_num', (tester['mouseClickOnNumber.clicked_name'] == tester.number.replace(map_num)).astype(int))
# #    
# %% Summarize accuracy
# ----------------------------------------------------------------------------------------   

    # call or callSign  = is the animal ; col = color and num = number 
    # 32 = is the number of target items per level, noise type and block (replace by infering this from data) 
    
uniqueTrials = 32 
    
result = (df.groupby(['noise', 'block', 'levels'])[['callSignCorrect', 'colourCorrect', 'numberCorrect']].sum()) * 100 / uniqueTrials

# Print the result
print(result)
    
    # Save excel 
        
    # Performance plot


#%%    
df.groupby(['noise', 'block', 'levels'])[['callSignCorrect', 'colourCorrect', 'numberCorrect']].count()


# %% 
