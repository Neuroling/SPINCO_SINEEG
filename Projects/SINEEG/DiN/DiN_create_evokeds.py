#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:35:32 2022

@author: gfraga
"""
import os
from glob import glob
import mne 

home = os.path.expanduser("~")

#% Gather Target File info
# %------------------------
basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/evoked/' 

if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
# find target files
files = glob(basedirinput + "*.fif", recursive=True)
subjects = [fullpath.split('/')[-1].split('_')[0] for fullpath in files]


# %% 
for fileinput in files:
   # % Read epochs
    epochs = mne.read_epochs(fileinput)
         
    # Subject info: subject number repeated n trial times 
    subjectID = fileinput.split('/')[-1].split('_')[0]
    types = [['corr/easy','corr/mid','corr/hard'],['incorr/easy','incorr/mid','incorr/hard']] # Clear conditions are excluded from this average to avoid bias
    difficulty = [['corr/clear','incorr/clear'],['corr/easy','incorr/easy'],['corr/mid','incorr/mid'],['corr/hard','incorr/hard']]
    allCombos = types[0] + types[1]
    # %%  Creating and saving evoked objects
    
    os.chdir(diroutput)
        
    for events in types:
            eventname = events[0].split('/')[0]
            evoked = epochs[events].average()
            # shorten the comment so it only displays the conditions names (and not proportion of epochs)
            evoked.comment = events[0].split('/')[0]
            outputfilename = fileinput.split('/')[-1].split('_')[0] + '_' + eventname + '-ave.fif'
            mne.write_evokeds(outputfilename, evoked, overwrite=True)
       
            # %% 
    
    for events in difficulty:
            eventname = events[0].split('/')[1]
            evoked = epochs[events].average()
            # shorten the comment so it only displays the conditions names (and not proportion of epochs)
            evoked.comment = events[0].split('/')[1]
            outputfilename = fileinput.split('/')[-1].split('_')[0] + '_' + eventname + '-ave.fif'
            mne.write_evokeds(outputfilename, evoked, overwrite=True)
            
    
    allCombos = types[0] + types[1]
    for events in allCombos:
            eventname = events.replace('/','-')
            evoked = epochs[events].average() 
            # shorten the comment so it only displays the conditions names (and not proportion of epochs)
            evoked.comment = events
            print(events)
            outputfilename = fileinput.split('/')[-1].split('_')[0] + '_' + eventname + '-ave.fif'
            mne.write_evokeds(outputfilename, evoked,overwrite=True)
