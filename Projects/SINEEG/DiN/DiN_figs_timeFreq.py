#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:35:32 2022

@author: gfraga
""" 
import os
import numpy as np
from glob import glob
import scipy.io as sio
import mne 
from mne.time_frequency import tfr_morlet

home = os.path.expanduser("~")

#% Gather Target File info
# %------------------------
basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/evokeds_timeFreq' 
 
if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
# find target files
files = glob(basedirinput + '*.set', recursive=True)
print(files)
subjects = [fullpath.split('/')[-1].split('_')[0] for fullpath in files]

# Info about conditions
conditions = ['corr/clear','incorr/clear','corr/easy','incorr/easy','corr/mid','incorr/mid','corr/hard','incorr/hard']

# %% 
# Read/ import data 
# -----------------------------------------------

evokedsTFR = {}
for c, con in enumerate(conditions):
    conditionTFR= []
    for f,fileinput in enumerate(files): 
        #fileinput = 's9_DiN_epoched_ICrem.set'
        print (fileinput)
        # Read Epochs in MNE 
        epochs = mne.io.read_epochs_eeglab(fileinput)
            
        # ADD CRUCIAL INFO FROM READING THE MAT FILE (missed by mne read)
        mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)['EEG']
        # Correct times using the actualTimes variable (were 0 = digit onset) 
        epochs.shift_time(mdat['actualTimes']/1000-epochs.times)[0]

        #trial accuracy
        epochAccu = [epoch['accuracy'] for epoch in mdat['epoch']]       
        
        # degradation levels    
        epochDeg = [epoch['degBin'] for epoch in mdat['epoch']]
        epochDeg = [0 if x!=x else x for x in epochDeg] # replace nan by 0 
            
        # recode events in MNE-read data
        for epIdx in range(len(epochs.events)):
            epochs.events[epIdx][2]=epochAccu[epIdx]*10 + epochDeg[epIdx]
        # add event information 
        epochs.event_id = {'corr/clear': 10,'corr/easy': 11,'corr/mid': 12,'corr/hard': 13,'incorr/clear': 0,'incorr/easy': 1,'incorr/mid': 2,'incorr/hard': 3}
            
        # Subject info: subject number repeated n trial times 
        subjectID = fileinput.split('/')[-1].split('_')[0]
 
        # % TIME FREQ  ------------------- -
        curEpochs= epochs[con]
        freqs = np.logspace(*np.log10([1, 48]), num=56)
        n_cycles = freqs / 2.  # different number of cycle per frequency
        power, itc = tfr_morlet(curEpochs, freqs=freqs, n_cycles=n_cycles, use_fft=True, return_itc=True, decim=3, n_jobs=None,average=True)
        
        #Store in large array             
        power.comment = fileinput.split('/')[-1]
        conditionTFR.append(power)
        
evokedsTFR[con] = conditionTFR

# %%
# Write to file
# save dictionary with evoked objects     
mne.write_evokeds(diroutput + '/group_TFRs.fif', evokedsTFR, overwrite=True)

# %%
 

    
 