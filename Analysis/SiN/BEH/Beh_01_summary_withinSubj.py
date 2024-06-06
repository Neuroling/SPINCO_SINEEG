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
#import seaborn as sns
#import matplotlib.pyplot as plt
import numpy as np

# User inputs
taskID = 'task-sin'

# PATHS
thisDir = os.getcwd()
subIDs= [item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]

# %% 
for subID in subIDs:
    if subID=='pilots' or subID.endswith("discard"):
        pass
    else:
        
        rawdir = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subID,taskID, 'beh')
        diroutput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis','beh',taskID)
        os.makedirs(diroutput, exist_ok=True)
        
        # %% Get raw data 
        rawcsv = os.listdir(rawdir)
        for file in rawcsv:
            if file.endswith(".csv") and file[-5].isdigit():
                # The file is a CSV file, get its filepath
                filepath = os.path.join(rawdir, file)
                        
                print(file)
                # %% read data frame 
                df = pd.read_csv(filepath)     
                   
                df.replace('NO_ANSW', eval('False'), inplace=True)
                df.replace('FALSE', eval('False'), inplace=True)
                df.replace('TRUE', eval('True'), inplace=True)               
                
                
                # % drop the example trials
                df = df.dropna(subset=['condsFile'])
                
                # % Add sentence information 
                df['sentence'] = (df.groupby('block').cumcount() + 1).astype('category')
                
                # recode block to remove info from noise level 
                df['block'] = df['block'].str.replace('NV','').str.replace('SSN','').astype('category')                
                
                #    
                df['n_cor_items'] = df[['callSignCorrect', 'colourCorrect', 'numberCorrect']].sum(axis=1)
                
                df[['callSign_resp','col_resp','numb_resp']]  = df[['mouseClickOnCall.clicked_name','mouseClickOnColour.clicked_name','mouseClickOnNumber.clicked_name']] 
                
                # %% Recode responses for clarity 
                
                df['callSign_resp'] = df['callSign_resp'].apply(lambda x: x.replace('call1', 'Adler').replace('call2', 'Drossel').replace('call3', 'Kroete').replace('call4', 'Tiger'))
                
                df['col_resp'] = df['col_resp'].apply(lambda x: x.replace('colour1', 'gelb').replace('colour2', 'gruen').replace('colour3', 'rot').replace('colour4', 'weiss'))
                
                df['numb_resp'] = df['numb_resp'].apply(lambda x: x.replace('number1', 'eins').replace('number2', 'zwei').replace('number3', 'drei').replace('number4', 'vier'))
                    
                # %% Summarize accuracy
                # # call or callSign  = is the animal ; col = color and num = number 
                # # 'uniqueTrials' is the number of target items per level, noise type and block (should be 32)
                # if np.average(df.value_counts('block'))/3 != np.average(df.value_counts('levels'))/2 or np.average(df.value_counts('noise'))/6 != np.average(df.value_counts('block'))/3:
                #     print('!!! not equal number of target items per noise, level and block!!!')
                
                # #  
                # uniqueTrialsPerItem = np.average(df.value_counts('block'))/3   # There are three item per trial 
                # beh_stats=((df.groupby(['noise', 'block', 'levels'])[['callSignCorrect', 'colourCorrect','numberCorrect']].sum())*100/uniqueTrialsPerItem).reset_index()
                
                # # add subject identifyer 
                # beh_stats.insert(0, 'subj',subID)

                # # Save excel
                # beh_stats.to_csv(os.path.join(diroutput, str(subID + '_' +  taskID + '_beh_summary.csv')),index=False)
                
               
                # %%  Gather relevant variables for further analysis
                
                gathered = df[['noise','block','voice','sentence','levels','callSign','colour','number','callSign_resp','col_resp','numb_resp','callSignCorrect', 'colourCorrect', 'numberCorrect','n_cor_items']]
                
                # add subject identifyer 
                gathered.insert(0, 'subj',subID)
                
                #  Save excel
                gathered.to_csv(os.path.join(diroutput, str(subID + '_' +  taskID + '_beh_gathered.csv')),index=False)
                                
# %%  Concatenate and Save in file 
files =  [os.path.join(diroutput, f) for f in os.listdir(diroutput) if f.startswith('s') and f.endswith('.csv')]

# Concatenate 
concat_df = pd.concat([pd.read_csv(f, index_col=None) for f in files], ignore_index=True)

# Save 
concat_df.to_csv(os.path.join(diroutput, str('Gathered_beh_all.csv')),index=False)
print('Saved concatenated tables')
      
# %% Figures from previous packages commented             
            # # Figures -----------------------------------------------------------
            # Transform to long                
            #beh_stat_long= pd.melt(beh_stats, id_vars=['subj','noise','block','levels'], value_vars=['callSignCorrect', 'colourCorrect','numberCorrect'])
                   
            # # %% Performance plot
            # doplots = 0
            # if doplots == 1:
            #     plt.figure()
            #     bp1= sns.boxplot(beh_stats,linewidth=(0.5), orient=('h'))
            #     bp1.set_title(subID)
            #     bp1.set_xlim(30,100)
            #     plt.xlabel('percent correct')
            #     plt.savefig((diroutput+ '\\'+subID+'_'+taskID+ '_stim_plot.png'),bbox_inches = "tight")
            #     plt.close()
                
                
                
            #     # Figures ----- 
            #     plt.figure()
            #     bp2=sns.boxplot(data=beh_stat_long, x='value',y='noise', hue='block', linewidth=(0.5), palette=sns.color_palette("husl", 6))
            #     bp2.set_title(subID)
            #     bp2.set_xlim(30,100)
            #     plt.xlabel('percent correct')
            #     plt.savefig((diroutput+ '\\'+subID+'_'+taskID+ '_block_plot.png'),bbox_inches = "tight")
            #     plt.close()
                
            #     plt.figure()
            #     bp3=sns.boxplot(data=beh_stat_long, x='value',y='block', hue='levels', linewidth=(0.5), palette=sns.color_palette("husl", 9))
            #     bp3.set_title(subID)
            #     bp3.set_xlim(30,100)
            #     plt.xlabel('percent correct')
            #     plt.savefig((diroutput+ '\\'+subID+'_'+taskID+ '_levels_plot.png'),bbox_inches = "tight")
            #     plt.close()
                
            #     plt.figure()
            #     bp4=sns.boxplot(data=beh_stat_long, x='value',y='noise', linewidth=(0.5), palette=sns.color_palette("husl", 2))
            #     bp4.set_title(subID)
            #     bp4.set_xlim(30,100)
            #     plt.xlabel('percent correct')
            #     plt.savefig((diroutput+ '\\'+subID+'_'+taskID+ '_noise_plot.png'),bbox_inches = "tight")
            #     plt.close()
