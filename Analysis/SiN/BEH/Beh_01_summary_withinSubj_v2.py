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
taskID = 'task-sin'

# PATHS
thisDir = os.getcwd()
subjIDs= [item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','sourcedata')) if item[-3] == '2']

# %% 
for subjID in subjIDs:
    if subjID=='pilots' or subjID.endswith("discard"):
        pass
    else:
        
        rawdir = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','sourcedata', subjID)
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
                df.replace('False', eval('False'), inplace=True)
                df.replace('True', eval('True'), inplace=True)
                
                # % drop the example trials
                # df = df.dropna(subset=['condsFile'])
                
                # % Add sentence information 
                df['sentence'] = (df.groupby('block').cumcount() + 1).astype('category')
                
                # recode block to remove info from noise level 
                # df['block'] = df['block'].str.replace('NV','').str.replace('SSN','').astype('category')                
                
                #    
                df['n_cor_items'] = df[['callSignCorrect', 'colourCorrect', 'numberCorrect']].sum(axis=1)
                
                df[['callSign_resp','col_resp','numb_resp']]  = df[['mouseClickOnCall.clicked_name','mouseClickOnColour.clicked_name','mouseClickOnNumber.clicked_name']] 
                
                # %% Recode responses for clarity 
                
                # df['callSign_resp'] = df['callSign_resp'].apply(lambda x: x.replace('call1', 'Adler').replace('call2', 'Drossel').replace('call3', 'Kroete').replace('call4', 'Tiger'))
                
                # df['col_resp'] = df['col_resp'].apply(lambda x: x.replace('colour1', 'gelb').replace('colour2', 'gruen').replace('colour3', 'rot').replace('colour4', 'weiss'))
                
                # df['numb_resp'] = df['numb_resp'].apply(lambda x: x.replace('number1', 'eins').replace('number2', 'zwei').replace('number3', 'drei').replace('number4', 'vier'))
                    
                # %% Summarize accuracy
                # # call or callSign  = is the animal ; col = color and num = number 
                # # 'uniqueTrials' is the number of target items per level, noise type and block (should be 32)
                # if np.average(df.value_counts('block'))/3 != np.average(df.value_counts('levels'))/2 or np.average(df.value_counts('noise'))/6 != np.average(df.value_counts('block'))/3:
                #     print('!!! not equal number of target items per noise, level and block!!!')
                
                # #  
                # uniqueTrialsPerItem = np.average(df.value_counts('block'))/3   # There are three item per trial 
                # beh_stats=((df.groupby(['noise', 'block', 'levels'])[['callSignCorrect', 'colourCorrect','numberCorrect']].sum())*100/uniqueTrialsPerItem).reset_index()
                
                # # add subject identifyer 
                # beh_stats.insert(0, 'subj',subjID)

                # # Save excel
                # beh_stats.to_csv(os.path.join(diroutput, str(subjID + '_' +  taskID + '_beh_summary.csv')),index=False)
                
               
                # %%  Gather relevant variables for further analysis
                
                gathered = df[['noise','block','voice','sentence','levels','callSign','colour','number','callSign_resp','col_resp','numb_resp','callSignCorrect', 'colourCorrect', 'numberCorrect','n_cor_items']]
                
                # add subject identifyer 
                gathered.insert(0, 'subjID',subjID)
                
                #  Save excel
                output_filename = os.path.join(diroutput, str(subjID + '_' +  taskID + '_beh_gathered.csv'))
                gathered.to_csv(output_filename,index=False)
                print('save to', output_filename)
                                
# %%  Concatenate and Save in file 
files =  [os.path.join(diroutput, f) for f in os.listdir(diroutput) if f.startswith('s2') and f.endswith('.csv')]

# # Concatenate 
concat_df = pd.concat([pd.read_csv(f, index_col=None) for f in files], ignore_index=True)

# # Save 
concat_df.to_csv(os.path.join(diroutput, str('Gathered_beh_all_Exp2.csv')),index=False)
print('Saved concatenated tables to',os.path.join(diroutput, str('Gathered_beh_all_Exp2.csv')))
      
# %% Figures from previous packages commented             
# Figures -----------------------------------------------------------
# Transform to long                
beh_stat_long= pd.melt(concat_df, id_vars=['subjID', 'noise','block'], value_vars=['callSignCorrect', 'colourCorrect','numberCorrect'])

beh_stat_wide = beh_stat_long.groupby(['subjID', 'noise', 'block','variable'])['value'].mean()*100
beh_stat_wide = pd.DataFrame(beh_stat_wide)
beh_stat_wide.columns = ['Accuracy']

pal2 = ('#648fff','#ffb000')
pal3 = ('#648fff', '#dc267f', '#ffb000')
pal4 = ('#648fff', '#8068f1','#fe6100', '#ffb000')
# %% Performance plot

plt.figure()
fig = sns.violinplot(beh_stat_wide, x= 'Accuracy', y = 'noise',hue = 'subjID', linewidth=(0.5), orient=('h'),palette=pal4)
fig.set_xlim(0,100)
plt.show()
plt.xlabel('percent correct')
# plt.savefig((diroutput+ '\\'+subjID+'_'+taskID+ '_stim_plot.png'),bbox_inches = "tight")
plt.close()


plt.figure()
fig = sns.boxplot(beh_stat_wide, x= 'Accuracy', y = 'noise',hue = 'subjID', linewidth=(0.5), orient=('h'),palette=pal4)
fig.set_xlim(0,100)
plt.show()
plt.xlabel('percent correct')
# plt.savefig((diroutput+ '\\'+subjID+'_'+taskID+ '_stim_plot.png'),bbox_inches = "tight")
plt.close()

plt.figure()
fig = sns.swarmplot(beh_stat_wide, x= 'Accuracy', y = 'noise',hue = 'subjID', linewidth=(0.5), orient=('h'),palette=pal4)
fig.set_xlim(0,100)
plt.show()
plt.xlabel('percent correct')
# plt.savefig((diroutput+ '\\'+subjID+'_'+taskID+ '_stim_plot.png'),bbox_inches = "tight")
plt.close()

#%%
plt.figure()
fig = sns.violinplot(beh_stat_wide, x= 'Accuracy', y = 'subjID', hue = 'noise', linewidth=(0.5), orient=('h'), palette=pal3)
fig.set_xlim(0,100)
plt.show()
plt.xlabel('percent correct')
# plt.savefig((diroutput+ '\\'+subjID+'_'+taskID+ '_stim_plot.png'),bbox_inches = "tight")
plt.close()

#%%
plt.figure()
fig = sns.swarmplot(data=beh_stat_wide, x='Accuracy', y='noise', hue='block', linewidth=(0.5), palette=pal3)
fig.set_xlim(0,100)
plt.xlabel('percent correct')
# plt.savefig((diroutput+ '\\'+subjID+'_'+taskID+ '_block_plot.png'),bbox_inches = "tight")
plt.show()
plt.close()

#%%
plt.figure()
fig = sns.boxplot(data=beh_stat_wide, x='Accuracy',y='noise', hue='variable', linewidth=(0.5), palette=pal3)
fig.set_xlim(0,100)
plt.xlabel('percent correct')
# plt.savefig((diroutput+ '\\'+subjID+'_'+taskID+ '_levels_plot.png'),bbox_inches = "tight")
plt.show()
plt.close()

#%%
plt.figure()
fig = sns.swarmplot(data=beh_stat_wide, x='Accuracy',y='noise', linewidth=(0.5), palette=pal3)
fig.set_xlim(0,100)
plt.xlabel('percent correct')
# plt.savefig((diroutput+ '\\'+subjID+'_'+taskID+ '_noise_plot.png'),bbox_inches = "tight")
plt.show()
plt.close()
