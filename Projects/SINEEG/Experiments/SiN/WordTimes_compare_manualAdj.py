# -*- coding: utf-8 -*-
""" Gather files with manually adjusted word times and compare
--------------------------------------------------------------

Created on Tue Mar  7 08:59:01 2023
@author: gfraga
"""
import pandas as pd
import glob as glob
import matplotlib.pyplot as plt
import os 
from scipy.io import wavfile
import numpy as np    

# directories
diraudio = 'V:/spinco_data/AudioGens/tts-golang-selected'
dirtimes = 'V:/spinco_data/AudioGens/word_times'
diroutput = 'V:/spinco_data/AudioGens/word_times'
os.chdir(diroutput)

# gather files with times 
files = glob.glob(dirtimes + '/*Times.csv',recursive = True)

#%% Concatenate frames 
df=[]
df = pd.concat([pd.read_csv(fileinput) for fileinput in files],ignore_index= True)
# some correction in the 'file' columns for consistency
df.file = df.file.str.replace('-manual','')
df.file = df.file.str.replace('-man','')
df.file = df.file.str.replace('.manual','')

# %% average across raters 

dfmean = df.groupby('file').mean().reset_index()
dfmean['rater']= 'mean'

#save average 
dfmean.to_csv(diroutput + '/MEAN_tts-golang-selected_wordTimes.csv',index=False)
# merge
df = pd.concat([df,dfmean],keys='rater',ignore_index=True)
    
# %% plots 
# LINEPLOTS. FILES IN X AXIS.
ynames = df.filter(regex='^token|.*Sound.*').columns

for yvar in ynames:    
    fig, ax = plt.subplots()
    for rater, group in df.groupby('rater'):        
        ax= group.plot(ax= ax , x='file', y=yvar,label=rater)    
        plt.xlabel('File')
        plt.ylabel(yvar)
        plt.title( yvar + ' by Rater')
        plt.legend()
        plt.show()
        plt.xticks(rotation=20)
    plt.savefig('COMPARE_' + yvar + '.jpg')
    plt.close()
    
    
# %% Plot soundwave 

ynames = df.filter(regex='^token|.*Sound.*').columns
colormap= ['red','blue','green','black'] # color map for each rater 

for n,file in enumerate(df.file.unique()):
    rate, data = wavfile.read(diraudio + '/' + file.replace('TextGrid', 'wav'))
    time = np.arange(len(data)) / rate
    print(n)
    fig, axes = plt.subplots(nrows=len(df.rater.unique()), ncols=1, figsize=(8, 4*len(df.rater.unique())), sharex=True)
    
    for i, (rater, group) in enumerate(df.groupby('rater')):
        ax = axes[i]
        ax.plot(time, data, color='lightgray') # waveform
        for yvar in ynames:
            val = group.loc[group['file'] == file][yvar].to_numpy()[0]
            ax.axvline(x=val, color=colormap[i])
        ax.set_title(f'{file}_rater_{rater}')
        
    plt.subplots_adjust(hspace=0.3)
    plt.xlabel('Time (s)')
    # save 
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.savefig(file + '.jpg')
    plt.close()