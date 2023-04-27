#!/usr/bin/env python3

""" Gather Behavioral Performance 
===============================================
Created on Tue Apr 25 10:56:48 2023
- Sentence-in-noise task in EEG experiment
- Read trial info with performance 
- Summarize 

@author: gfraga
"""
import os 
import shutil
import pandas as pd 

rawdir = 'V:/Projects/Spinco/SINEEG/Data/SiN/raw/p001'
diroutput = 'V:/Projects/Spinco/SINEEG/Outputs/SiN/p001'
os.makedirs(diroutput, exist_ok=True);

# %% Copy raw data into the analysis folder 
rawfiles = os.listdir(rawdir)
# Loop through the files to find the CSV file
for file in rawfiles:
    if file.endswith(".csv") and file[-5].isdigit():
        # If the file is a CSV file, copy it to the output directory
        filepath = os.path.join(rawdir, file)
        outputpath = os.path.join(diroutput, file)
        shutil.copyfile(filepath, outputpath)

# %% Read and summary from Analysis folder 
files = os.listdir(rawdir)

# Loop through the files to find the CSV file
for file in files:
    if file.endswith(".csv") and file[-5].isdigit():
        filepath = os.path.join(diroutput, file)
 
        # %% read data frame 
        df = pd.read_csv(filepath)
        df = df.iloc[:, :-1] # SEEMS to read an additional blank column [!!!revise if in all files]
        
        # % Assess accuracy         
        map_call = {'Ad':'call1','Dr':'call2','Kr':'call3','Ti':'call4'}
        map_col = {'ge':'colour1','gr':'colour2','ro':'colour3','we':'colour4'}
        map_num = {'Ei':'number1','Zw':'number2','Dr':'number3','Vi':'number4'}
        
        # Fix formatting issues, subject response values are coded as "['call1']"
        df['mouseClickOnCall.clicked_name'] = df['mouseClickOnCall.clicked_name'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))
        df['mouseClickOnColour.clicked_name'] = df['mouseClickOnColour.clicked_name'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))
        df['mouseClickOnNumber.clicked_name'] = df['mouseClickOnNumber.clicked_name'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))       
        
        # compare response with presented stimuli
        sum(df['mouseClickOnCall.clicked_name'] == df.callSign.replace(map_call))
        sum(df['mouseClickOnColour.clicked_name'] == df.colour.replace(map_col))
        sum(df['mouseClickOnNumber.clicked_name'] == df.number.replace(map_num))

# %% 


    



# %% 
