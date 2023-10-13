#!/usr/bin/env python3

""" Gather Behavioral Performance 
===============================================
Created on Tue Apr 25 10:56:48 2023
- Sentence-in-noise task in EEG experiment
- Read trial info with performance 
- Summarize 

@author: gfraga & samuemu
"""

import os 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# User inputs
copyraw = 0;
taskID = 'task-sin'

# PATHS
thisDir = os.path.dirname(os.path.abspath(__file__))
subIDs= os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata'))


for subID in subIDs:
    if subID=='pilots' or subID.endswith("discard"):
        pass
    else:
        
        rawdir = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subID,taskID, 'beh')
        diroutput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata',subID,taskID, 'beh','summary')
        os.makedirs(diroutput, exist_ok=True)
        
        # %% Get raw data 
        rawcsv = os.listdir(rawdir)
        for file in rawcsv:
            if file.endswith(".csv") and file[-5].isdigit():
                # The file is a CSV file, get its filepath
                filepath = os.path.join(rawdir, file)
                        
         
        # %% read data frame 
        df = pd.read_csv(filepath)     
           
        df.replace('NO_ANSW', eval('False'), inplace=True)
        df.replace('False', eval('False'), inplace=True)
        df.replace('True', eval('True'), inplace=True)

        # %% Summarize accuracy
        # call or callSign  = is the animal ; col = color and num = number 
        # 'uniqueTrials' is the number of target items per level, noise type and block (should be 32)
        if np.average(df.value_counts('block'))/3 != np.average(df.value_counts('levels'))/2 or np.average(df.value_counts('noise'))/6 != np.average(df.value_counts('block'))/3:
            print('!!! not equal number of target items per noise, level and block!!!')
        
        uniqueTrials = np.average(df.value_counts('block'))/3  
        beh_stats=(df.groupby(['noise', 'block', 'levels'])[['callSignCorrect', 'colourCorrect','numberCorrect']].sum())*100/uniqueTrials
        
        # Save excel
        beh_stats.to_csv(diroutput+ '\\'+subID+'_'+taskID+ '_beh_summary.csv')
            
        # %% Performance plot
        plt.figure()
        bp1= sns.boxplot(beh_stats,linewidth=(0.5), orient=('h'))
        bp1.set_title(subID)
        bp1.set_xlim(30,100)
        plt.xlabel('percent correct')
        plt.savefig((diroutput+ '\\'+subID+'_'+taskID+ '_stim_plot.png'),bbox_inches = "tight")
        plt.close()
        
        beh_stat2=pd.read_csv(diroutput+ '\\'+subID+'_'+taskID+ '_beh_summary.csv')
        beh_statLF= pd.melt(beh_stat2, id_vars=['noise','block','levels'], value_vars=['callSignCorrect', 'colourCorrect','numberCorrect'])
        
        plt.figure()
        bp2=sns.boxplot(data=beh_statLF, x='value',y='noise', hue='block', linewidth=(0.5), palette=sns.color_palette("husl", 6))
        bp2.set_title(subID)
        bp2.set_xlim(30,100)
        plt.xlabel('percent correct')
        plt.savefig((diroutput+ '\\'+subID+'_'+taskID+ '_block_plot.png'),bbox_inches = "tight")
        plt.close()
        
        plt.figure()
        bp3=sns.boxplot(data=beh_statLF, x='value',y='block', hue='levels', linewidth=(0.5), palette=sns.color_palette("husl", 9))
        bp3.set_title(subID)
        bp3.set_xlim(30,100)
        plt.xlabel('percent correct')
        plt.savefig((diroutput+ '\\'+subID+'_'+taskID+ '_levels_plot.png'),bbox_inches = "tight")
        plt.close()
        
        plt.figure()
        bp4=sns.boxplot(data=beh_statLF, x='value',y='noise', linewidth=(0.5), palette=sns.color_palette("husl", 2))
        bp4.set_title(subID)
        bp4.set_xlim(30,100)
        plt.xlabel('percent correct')
        plt.savefig((diroutput+ '\\'+subID+'_'+taskID+ '_noise_plot.png'),bbox_inches = "tight")
        plt.close()