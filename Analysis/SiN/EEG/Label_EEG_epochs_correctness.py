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
copyraw = 0;
subID = 'p002'

# PATHS
thisDir = os.path.dirname(os.path.abspath(__file__))
rawdir = os.path.join(thisDir[:thisDir.find('scripts')] + 'Data','SiN','raw', subID,'beh')
diroutput = os.path.join(thisDir[:thisDir.find('scripts')] + 'Data','SiN','preproc',subID,'beh')
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
        filepath = os.path.join(diroutput, file)
 
        # %% read data frame 
                 
        
        # %% Check accuracy 
        df = pd.read_csv(filepath)       
            

        df['callSignCorrect_raw'] = df['callSignCorrect_raw'].map({True: 1, False: 0, "NO_ANSW": ''})
        df['colourCorrect_raw'] = df['colourCorrect_raw'].map({'TRUE': 1, 'FALSE': 0, "NO_ANSW": ''})
        df['numberCorrect_raw'] = df['numberCorrect_raw'].map({'TRUE': 1, 'FALSE': 0, "NO_ANSW": ''})
        
        df['callSignCorrect_raw']
        df['colourCorrect_raw'] 
        df['numberCorrect_raw']




        
     #    #-Checking accuracy will change as future log files will have 3 boolean columns for each target item -------------------------------------------------   
     #    # % Assess accuracy     
     #    map_call = {'Ad':'call1','Dr':'call2','Kr':'call3','Ti':'call4'}
     #    map_col = {'ge':'colour1','gr':'colour2','ro':'colour3','we':'colour4'}
     #    map_num = {'Ei':'number1','Zw':'number2','Dr':'number3','Vi':'number4'}
        
     #    # Fix formatting issues, subject response values are coded as "['call1']"
     #  #  df['mouseClickOnCall.clicked_name_raw'] = df['mouseClickOnCall.clicked_name_raw'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))
     #   # df['mouseClickOnColour.clicked_name_raw'] = df['mouseClickOnColour.clicked_name_raw'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))
     #   # df['mouseClickOnNumber.clicked_name_raw'] = df['mouseClickOnNumber.clicked_name_raw'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))       
        
     #    # compare response with presented stimuli
     #    df.insert(0, 'accu_call', (df['mouseClickOnCall.clicked_name_raw'] == df.callSign.replace(map_call)).astype(int))
     #    df.insert(0, 'accu_col', (df['mouseClickOnColour.clicked_name_raw'] == df.colour.replace(map_col)).astype(int))
     #    df.insert(0, 'accu_num', (df['mouseClickOnNumber.clicked_name_raw'] == df.number.replace(map_num)).astype(int))
     #    # ----------------------------------------------------------------------------------------   

     # %% Summarize accuracy
    # call or callSign  = is the animal ; col = color and num = number 
    # 32 = is the number of target items per level, noise type and block (replace by infering this from data) 
    
    uniqueTrials = 32 
    
    (df.groupby(['noise', 'block', 'levels'])[['callSignCorrect_raw', 'colourCorrect_raw','numberCorrect_raw']].sum())*100/uniqueTrials
     
       
    
    # Save excel 
        
    # Performance plot




    



# %% 
