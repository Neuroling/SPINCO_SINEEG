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
        df = pd.read_csv(filepath, usecols= )
        
        #df.iloc[:, -1]


# %% 


  
    nblocks = 2 
    nreps = len(df.trial.unique()) / (nblocks*len(df.LV.unique()) * len(df.TYPE.unique()))   #  number of trials per degradation level in a block (changes across tasks)
    
    # %% 
    counts = df['TYPE'].value_counts()
    for level, count in counts.iteritems():
        
        print(df[df['TYPE']=='NV'].LV.value_counts())
        print(df[df['TYPE']=='SiSSN'].LV.value_counts())

    # %% # Stats per block, type and level (averaging trials)          
    names = ['SubjectID','task', 'block', 'TYPE', 'LV','Accuracy']
    
    # accuracy summary 
    
    accu = df.groupby(names)['trial'].agg(['count']).reset_index()
    accu['propTrials'] = round(accu['count']/nreps,ndigits=2)
    
    #Fix header (join by '-')
    rts = df.groupby(names)[['RT']].agg(['mean', 'std']).reset_index()
    rts.columns  =  ['_'.join(i) if len(i[1]) else ''.join(i) for i in rts.columns.tolist() ]
    
    grouped = pd.merge(accu, rts, on=names)

    # % Expand with all combinations of the variables 
    unique_categories = [grouped[col].unique() for col in names]    
    multiindex = pd.MultiIndex.from_product(unique_categories, names=names)
    
    # reindexing
    grouped = (grouped
                 .set_index(names) 
                 .reindex(multiindex,fill_value= '')
                 .reset_index())
    

    grouped['SubjectID'] = grouped['SubjectID'].astype('object')
    grouped['block'] = grouped['block'].astype('object')

    return grouped