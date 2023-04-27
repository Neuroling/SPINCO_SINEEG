# -*- coding: utf-8 -*-
""" Average WOrd times manually adjusted by several raters 
Created on Wed Mar 22 10:01:08 2023

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
files = [glob.glob(dirtimes + '/Rahel*Times.csv',recursive = True), glob.glob(dirtimes + '/Sibylle*Times.csv',recursive = True)]
 

# Concatenate frames 
df=[]
df = pd.concat([pd.read_csv(fileinput[0]) for fileinput in files])
# some correction in the 'file' columns for consistency
df.file = df.file.str.replace('-manual','')
df.file = df.file.str.replace('-man','')
df.file = df.file.str.replace('.manual','')


# %% average across raters 

dfmean = df.groupby('file').mean().reset_index()
dfmean['rater']= 'mean'
# merge
df2save = pd.concat([df,dfmean],keys='rater')
    
# %% Plot soundwave 

df2plot = df2save[df2save['rater']=='mean']
ynames = df2plot.filter(regex='^token|.*Sound.*').columns
colormap= ['red','blue','green'] # color map for each rater 

for file in df2plot.file.unique():
    rate, data = wavfile.read(diraudio + '/' + file.replace('TextGrid', 'wav'))
    time = np.arange(len(data)) / rate
    
    fig, axes = plt.subplots(nrows=len(df2plot.rater.unique()), ncols=1)
    
    ax = axes
    ax.plot(time, data, color='lightgray') # waveform
    
    for yvar in ynames:
        val = df2plot.loc[df2plot['file'] == file][yvar].to_numpy()[0]
        #ax.set_title(f'{file}_rater_{rater}')
        
    plt.subplots_adjust(hspace=0.3)
    plt.xlabel('Time (s)')
    # save 
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
   # plt.savefig(file + '.jpg')
   # plt.close()