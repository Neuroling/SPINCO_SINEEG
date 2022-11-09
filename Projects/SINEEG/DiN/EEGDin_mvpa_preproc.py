#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 10:26:03 2022

@author: gfraga
"""
import sys as sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import scipy.io as sio
import mne 

home = os.path.expanduser("~")

# %% Gather Target File info
# %------------------------
basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_alpha/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/mvpa/25subj_alpha/' 

if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
# find target files
files = glob(basedirinput + "*.set", recursive=True)
# Retrieve list of subjects name from folder structure
subjects = [fullpath.split('/')[-1].split('_')[0] for fullpath in files]
# Commented: Previous folder structure search: 
#subjects =  [[item for item in currpart if 'SUBJECT' in item] 
#             for currpart in [fullpath.split('/')
#                              for fullpath in files]] 
 
# Read/ import data 
# -----------------------------------------------
xlist = []
slist = []
ylist= []

for fileinput in files: 
    #fileinput = 's9_DiN_epoched_ICrem.set'
    print (fileinput)
    # Read Epochs in MNE 
    epochs = mne.io.read_epochs_eeglab(fileinput)
    
       
    # Retrieve trial accuracy
    mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)
    epochAccu = [epoch['accuracy'] for epoch in mdat['epoch']]

    
    # recode events in MNE-read data
    for epIdx in range(len(epochs.events)):
        epochs.events[epIdx][2]=epochAccu[epIdx]
    # add event information 
    epochs.event_id = {'correct': 1, 'incorrect':0}

    # prepared matrix for MNE
    #------------------------------------
    # We need an .m file with: 
    # Input data should be in the form of a .mat file containing four structs
        # S : array of size 1 x total number of trials; containing participant numbers corresponding to all trials
        # X : array of size number of channels x number of time points x number of trials; contains preprocessed channel voltage data at each time point for each trial
        # Y : array of size 1 x total number of trials; containing condition labels corresponding to all trials
        # times : array of size 1 x number of time points; contains all time points in the epoch of interest
    
    
   
    # Get index of the time window of interest to trim the data
    idx1 =  int(np.where(mdat['times'] == -2000)[0])
    idx2 =  int(np.where(mdat['times'] == 0)[0])

    # Data array  transposed to CH x pts x Trials
    dat = np.transpose(epochs._data,[1,2,0])
    dat =  dat[:,idx1:idx2,:] # trim to the specified time window
    
    xlist.append(dat)
    # Subject info: subject number repeated n trial times 
    subjectNum = int(fileinput.split('/')[-1].split('_')[0].replace('s',''))
    slist.append ([subjectNum]*dat.shape[2])
    #Condition
    ylist.append ([int(n) for n in epochAccu])
    
    #Save channel data for later concatenation
    sio.savemat((diroutput + '/s'+ str(subjectNum)+'_prep4mvpa.mat'),{'x':dat})
    
   
# MNE Gather info across subjects     
X = np.concatenate((xlist),axis=2) # arrays of all subjects concatenated along third dim (trials)
S = np.concatenate((slist),axis=0)
Y = np.concatenate((ylist),axis=0)
times =  mdat['times'][idx1:idx2] # contain info about time points (the same in all files)

# %% save
# number formatting (required? ) 
S = S.astype('int16')
Y = np.array(Y).astype('int16')
times = np.array(times).astype('int16')
 # Group arrays  
# Arrays X will be too large to export in a single file  
preproc_mvpa = {'S':S, 'Y':Y,'times':times}
sio.savemat(diroutput + '/info_trials_mvpa.mat',preproc_mvpa)
 

# %% Save script 
import datetime as dt

filename = diroutput +'/script'
timestamp = str(dt.datetime.now())[:19]
timestamp = re.sub(r'[\:-]','', timestamp) # replace unwanted chars 
timestamp = re.sub(r'[\s]','_', timestamp) # with regex and re.sub
print('{}_{}'.format(filename,timestamp))
# not included in output file
out_filename = ('{}_{}'.format(filename,timestamp))
with open(__file__, 'r') as f:
    with open(out_filename, 'w') as out:
        for line in (f.readlines()): #remove last 7 lines
            print(line, end='', file=out)

# %% SAVE THIS SECTION COMMENTED FOR FURTHER DEVELOPMENTS .... 
# #%%  Visualize data 
# #epochSel = 'correct'
# #stat = 'mean'
# #epochs[epochSel].plot_image(combine=stat,title= epochSel + ' trials (' + stat + ')')

# #epochs['incorrect'].plot_image(combine='mean')

# # %%

# # some tips for online displaying info
# dir(EEG) # this displays all attributes of this object
# EEG.info #summary of sampling rate, filters, nchans etc


# # Get most important data
# dat = np.transpose(EEG._data,[1,2,0]) # transpose to CH x pts x Trials
# chans = EEG.ch_names

# # %% visualization
# # -----------------------------------------------
# EEG.plot(event_color=dict(button='red', face='blue'),group_by='selection', butterfly=True)

# # %%

# os.chdir(basedirinput)
# import glob
# path = "/mnt/nfs/din_v1/experimentData"

# #glob.glob(path, * ,recursive=True)


# # %%
# # folder path
# dir_path = r'/mnt/nfs/din_v1/experimentData'

# # list to store files name
# res = []
# for (dir_path, dir_names, file_names) in os.walk(dir_path):
#     res.extend(file_names)
# print(res)
    
# # %%    
    

# #for path, currentDirectory, files in os.walk(basedirinput):
#  #   for file in files:
#        # print(os.path.join(path, file))
       
# for r, d, f in os.walk(path):
#     for file in f:
#         if '..m' in file:
#             files.append(os.path.join(r, file))

# for f in files:
#     print(f)

# # %%



# cd (dirinput);
# % read data 
# load('Results_Infants_included_decode_within_SVM_22-Sep-2022_44205.mat')
# DA = results.DA;

# %% Get mean classification accuracy
# means_1lv = mean(DA,[3 4],'omitnan');
# means_2lv = mean(DA,[1 3 4],'omitnan');

# %% PLOT 

# plot(results.times,means_1lv); hold on; 
# plot(results.times,
#      means_2lv','color', 'black','lineWidth',2)
 


# % %% list files 
# %# Fix for issue with spyder not showing plotly 

# path = basedirinput

# for root,d_names,f_names in os.walk(path):
# 	print root, d_names, f_names