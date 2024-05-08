#!/usr/bin/env python3

""" Gather Behavioral Performance 
===============================================
Created on Tue Apr 25 10:56:48 2023
- Sentence-in-noise task in EEG experiment
- Read behavioural summary (which contains trial performance) of each subject
- Creates long & wide format .csv files containing all subjects' performance
- Creates some plots

!!! Important note!!!
Package ptitprince (which is used to create the raincloud plots) requires seaborn v0.11.0


@author: gfraga & samuemu
"""
import os 
#import shutil
import pandas as pd 

import matplotlib.pyplot as plt 
# import matplotlib.collections as clt
import ptitprince as pt
# import numpy as np
import seaborn as sns

# User inputs
copyraw = 0
taskID = 'task-sin'
save = 0 # if = 1 it will save excel files and plots

#%% PATHS
thisDir = os.getcwd()
subIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]
diroutput= os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis','beh')

#%% Reading Files
filepaths=list()
subIDlist = list()
for subID in subIDs:
    if subID=='pilots' or subID.endswith("discard"):
        pass
    else:
        #rawdir = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subID,taskID, 'beh')
        dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata',subID,taskID, 'beh','summary')
        beh_csv = os.listdir(dirinput)
        subIDlist.append(subID)
        for file in beh_csv:
            if file.endswith(".csv"):
                # The file is a CSV file, copy it to the output directory
                filepaths.append(os.path.join(dirinput, file))

#%% read data and include column for subjID         
df = pd.concat([pd.read_csv(i) for i in filepaths], ignore_index=True)

# uniqueTrials should be 12
uniqueTrials = df.nunique()['levels'] * df.nunique()['noise']
if len(df)/len(filepaths) != uniqueTrials:
    print('!!! ERROR: not all subjects have correct number of unique Trials')

# Creating a list of the subjIDs to insert into the df
subIDcol=list()
for subID in subIDlist:
    for i in range(uniqueTrials):
        subIDcol.append(subID)
df.insert(0,'subjID',subIDcol)  

#%% Create long and wide format tables
dfLF= pd.melt(df, id_vars=['subjID','noise','block','levels'], value_vars=['callSignCorrect', 'colourCorrect','numberCorrect'])

#dfMeanStim = (dfLF.groupby(['subjID','noise', 'block', 'levels'])[['value']].mean())
#dfTotalMeanStim = (dfLF.groupby(['noise', 'block','levels'])[['value']].mean())
dfTotal = (df.groupby(['noise', 'block','levels'])[['callSignCorrect', 'colourCorrect','numberCorrect']].mean())

dfSNL=df
dfSNL=dfSNL.replace(['-11db','0.2p'], 'Lv3')
dfSNL=dfSNL.replace(['-9db','0.4p'], 'Lv2')
dfSNL=dfSNL.replace(['-7db','0.6p'], 'Lv1')

dfWFtotal = pd.pivot_table(dfSNL,index='block',columns='levels',values=['callSignCorrect', 'colourCorrect','numberCorrect'])

dfSNL_long= pd.melt(dfSNL, id_vars=['subjID','noise','block','levels'], value_vars=['callSignCorrect', 'colourCorrect','numberCorrect'])

#%% Adds a column to the df which contains noise_block_stimulusType, then creates wide format df
# this could probably be done much easier, but I don't know how

label = list()
for i in dfSNL_long.index:
    tmp = dfSNL_long['noise'][i],dfSNL_long['levels'][i],dfSNL_long['variable'][i]
    label.append( '_'.join(tmp))
dfSNL_long.insert(5,'trial',label)    

dfWF = pd.pivot_table(dfSNL_long,index='subjID',columns='trial',values='value')

#%% Save excel
if save == 1:
    df.to_csv(diroutput+ '\\'+taskID+'_beh_summary_long.csv')    
    dfTotal.to_csv(diroutput+ '\\'+taskID+'_AvgAcrossSubj_beh_summary_long.csv')
    dfWF.to_csv(diroutput+ '\\'+taskID+'_beh_summary_wide.csv')
    dfWFtotal.to_csv(diroutput+ '\\'+taskID+'_AvgAcrossSubj_beh_summary_wide.csv')

# Figures --------------------------------------------------------------------------------------------------
doplots = 0
if doplots == 1:
    #  Checking version of seaborn
    vers_sns = int(sns.__version__[2:4])
    
    # %% Performance plots
    ## palettes with accessible colours
    pal2 = ('#648fff','#ffb000')
    pal3 = ('#648fff', '#dc267f', '#ffb000')
    pal4 = ('#648fff', '#8068f1','#fe6100', '#ffb000')
     



    ## Plots comparing noise conditions (NV vs SiSSN)
    plt.figure()
    f, ax = plt.subplots(figsize=(7, 5))
    dy="noise"; dx="value"; ort="h";
    ax=pt.half_violinplot( x = dx, y = dy, data = dfLF, palette = pal2, bw = .2, cut = 0.,
                          scale = "area", width = .6, inner = None, orient = ort)
    ax=sns.stripplot( x = dx, y = dy, data = dfLF, palette = pal2, edgecolor = "white", size = 3, jitter = 0.1, zorder = 0, orient = ort)
    plt.xlabel('percent correct')
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_noise_raincloudPlot.png'),bbox_inches = "tight")
    
    plt.figure()
    sns.boxplot(data=dfLF, x='value',y='noise', linewidth=(0.5),palette=pal2)
    plt.xlabel('percent correct')
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_noise_boxplot.png'),bbox_inches = "tight")
    
    
    ## Plots comparing blocks (NV1, NV2, SiSSN1, SiSSN2)
    
    plt.figure()
    ax=sns.boxplot(data=dfLF, x='value',y='noise', hue='block', linewidth=(0.5),palette=pal4)
    plt.xlabel('percent correct')
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_block_boxplot.png'),bbox_inches = "tight")
    
    plt.figure()
    ax=sns.violinplot(data=dfLF, x='value',y='noise', hue='block', linewidth=(0.5),split=True, inner="quart", palette=pal4)
    plt.xlabel('percent correct')
    if vers_sns >= 12: sns.move_legend(ax, "center left")
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_block_violinplot.png'),bbox_inches = "tight")
    
    
    ## Plots comparing levels and noise condition (-11db, -9db, -7db, 0.2p, 0.4p, 0.6p)
    plt.figure()
    ax=sns.boxplot(data=dfLF, x='value',y='block', hue='levels', linewidth=(0.5),
                    palette=sns.color_palette("husl", 6), 
                    hue_order=['0.2p','0.4p','0.6p','-11db','-9db','-7db'])
    if vers_sns >= 12: sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.xlabel('percent correct')
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_levels_block_boxplot_v2.png'),bbox_inches = "tight")
    
    plt.figure()
    ax=sns.boxplot(data=dfSNL_long, x='value',y='block', hue='levels', linewidth=(0.5), palette=pal3)
    plt.xlabel('percent correct')
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_levels_block_boxplot.png'),bbox_inches = "tight")
    
    plt.figure()
    ax=sns.boxplot(data=dfSNL_long, x='value',y='noise', hue='levels', linewidth=(0.5), palette=pal3)
    plt.xlabel('percent correct')
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_levels_noise_boxplot.png'),bbox_inches = "tight")
    
    plt.figure()
    ax=sns.violinplot(data=dfSNL_long, x='value',y='levels', hue='noise', linewidth=(0.5),split=True, inner="quart", palette=pal2)
    plt.xlabel('percent correct')
    if vers_sns >= 12: sns.move_legend(ax, "lower left")
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_levels_noise_violinplot.png'),bbox_inches = "tight")
    
    
    ## Plots comparing the different stimuli (CallSign, Colour, Number)
    plt.figure()
    ax=sns.boxplot(dfTotal,linewidth=(0.5), orient=('h'), palette=pal3)
    ax.set_xlim(30,100)
    plt.xlabel('percent correct')
    plt.ylabel('stimulus')
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_stim_boxplot.png'),bbox_inches = "tight")
    
    #plt.figure()
    #f, ax = plt.subplots(figsize=(7, 5))
    #dy="variable"; dx="value"; ort="h"
    #ax=pt.half_violinplot( x = dx, y = dy, data = dfLF, palette = pal3, bw = .2, cut = 0.,
     #                     scale = "area", width = .6, inner = None, orient = ort)
    ax=sns.stripplot( x = dx, y = dy, data = dfLF, palette = pal3, edgecolor = "white", size = 3, jitter = 0.1, zorder = 0, orient = ort)
    plt.ylabel('stimulus')
    plt.xlabel('percent correct')
    if save ==1: plt.savefig((diroutput+ '\\'+taskID+ '_stim_raincloudPlot.png'),bbox_inches = "tight")
