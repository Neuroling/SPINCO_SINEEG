"""
Created on Thu Nov 17 14:34:15 2022

@author: gfraga
"""
import os
from glob import glob
import scipy.io as sio
import mne 

home = os.path.expanduser("~")

#% Gather Target File info
# %------------------------
basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/urepochs/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 

if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
# find target files
files = glob(basedirinput + "*.set", recursive=True)
subjects = [fullpath.split('/')[-1].split('_')[0] for fullpath in files]


# %% 
for fileinput in files:
   # %%
    epochs = mne.io.read_epochs_eeglab(fileinput)
    
    # Relevant event fields
    #mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)
    mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)['EEG']
    # accuracy
    epochAccu = [epoch['accuracy'] for epoch in mdat['epoch']]
    
    # Time adjustment
    epochs.shift_time(mdat['actualTimes']/1000-epochs.times)[0]
    
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
    types = [['corr/easy','corr/mid','corr/hard'],['incorr/easy','incorr/mid','incorr/hard']] # Clear conditions are excluded from this average to avoid bias
    difficulty = [['corr/clear','incorr/clear'],['corr/easy','incorr/easy'],['corr/mid','incorr/mid'],['corr/hard','incorr/hard']]
    
    # saving epochs -------------------------
    epochs.save(diroutput + fileinput.split('/')[-1].replace('.set','.fif'),overwrite=True)
    
    