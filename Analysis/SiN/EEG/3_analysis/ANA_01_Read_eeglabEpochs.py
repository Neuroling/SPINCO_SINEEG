
""" READ EEGLAB EPOCHS in MNE  
=================================================================
@author: gfraga\n

Parameters
----------

Returns
-------
ioepoch ... 
 
""" 

import os
from glob import glob
import scipy.io as sio
import numpy as np
import mne 
import pandas as pd
#import MVPA.ANA_01_helper as hp

#%% inputs and paths
taskID = 'task-sin'
pipeID = 'pipeline-01'
subjID='s015'
setFileEnd = '_epoched_2.set'


thisDir = os.path.dirname(os.path.abspath(__file__))
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]

#%% input directories
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', pipeID, taskID + '_preproc_epoched',subjID)
set_fp = glob(os.path.join(dirinput, str("*"+ setFileEnd)), recursive=True)[0]
epo_fp = set_fp[:set_fp.find(setFileEnd)]+'-epo.fif'

#%% Read accu.tsv files for the event ids
events_fp = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', pipeID, taskID, subjID)
events_fp = glob(os.path.join(events_fp, "*accu.tsv"), recursive=True)[0]
events_tsv = pd.read_csv(events_fp,sep='\t')

#%% making an array of event ids to add as metadata
event_ids = np.zeros(shape=(1152,3))
idx = 0
for i in range(1,len(events_tsv)):
    if np.isnan(events_tsv['ACCURACY'][i]):
        continue
    else:
        event_ids[idx] = [(events_tsv['SAMPLES'][i]),(events_tsv['VALUE'][i]),(events_tsv['ACCURACY'][i])]
        idx=idx+1
        
event_ids=pd.DataFrame(event_ids,columns=['tf','stim_code','accuracy'])
event_ids['accuracy'].replace(0,'inc', inplace=True)
event_ids['accuracy'].replace(1,'cor', inplace=True)
event_ids['block']=event_ids['stim_code']
event_ids['block'].replace([111,112,113,114,121,122,123,124,131,132,133,134],'NV',inplace=True)
event_ids['block'].replace([211,212,213,214,221,222,223,224,231,232,233,234],'NV',inplace=True)
event_ids['stim']=event_ids['stim_code']
event_ids['stim'].replace([111,112,113,114,211,212,213,214],'CallSign',inplace=True)
event_ids['stim'].replace([121,122,123,124,221,222,223,224],'Colour',inplace=True)
event_ids['stim'].replace([131,132,133,134,231,232,233,234],'Number',inplace=True)
#%% creating .fif files - takes a lot of ressources, only run if necessary
# for subjID in subjIDs:
#     dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', pipeID, taskID + '_preproc_epoched',subjID)
#     set_fp = glob(os.path.join(dirinput, "*_epoched.set"), recursive=True)[0]
#     print(set_fp)
#     hp.eeglabEpo2mneEpo(set_fp)


#%% read epochs from eeglab .set file & save as mne .fif file
epochs = mne.io.read_epochs_eeglab(set_fp)
epochs.metadata=event_ids # add metadata
epochs.save(epo_fp, overwrite=True, fmt='double')

#%% Read epochs from .fif file
epo = mne.read_epochs(epo_fp)
# epo.plot(events=True)
# epo_filt = epo.__getitem__('cor')

# %% Read epochs

# # CHECK EVENT CODES 
# #  


# # Some plots
# 'V:\Projects\Spinco\SINEEG\Scripts\Analysis\SiN\EEG\3_analysis\old_functions\funs_eeg'   - recycle some stuff 

# ############# THIS IS STILL WORK IN PROGRESSS
# # %% 
# #% Gather Target File info
# # %------------------------
# basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/_urepochs_eeglab/' 
# diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 

# if not os.path.exists(diroutput): 
#     os.mkdir(diroutput)
# # find target files
# files = glob(basedirinput + "*.set", recursive=True)
# subjects = [fullpath.split('/')[-1].split('_')[0] for fullpath in files]


# # %% 
# for fileinput in files:
#    # %%
#     epochs = mne.io.read_epochs_eeglab(fileinput)
    
#     # Relevant event fields
#     #mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)
#     mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)['EEG']
#     # accuracy
#     epochAccu = [epoch['accuracy'] for epoch in mdat['epoch']]
     
    
#     # degradation levels    
#     epochDeg = [epoch['degBin'] for epoch in mdat['epoch']]
#     epochDeg = [0 if x!=x else x for x in epochDeg] # replace nan by 0 
        
#     # recode events in MNE-read data
#     for epIdx in range(len(epochs.events)):
#         epochs.events[epIdx][2]=epochAccu[epIdx]*10 + epochDeg[epIdx]
#     # add event information 
#     epochs.event_id = {'corr/clear': 10,'corr/easy': 11,'corr/mid': 12,'corr/hard': 13,'incorr/clear': 0,'incorr/easy': 1,'incorr/mid': 2,'incorr/hard': 3}
      
    
#     # Subject info: subject number repeated n trial times 
#     subjectID = fileinput.split('/')[-1].split('_')[0]
#     types = [['corr/easy','corr/mid','corr/hard'],['incorr/easy','incorr/mid','incorr/hard']] # Clear conditions are excluded from this average to avoid bias
#     difficulty = [['corr/clear','incorr/clear'],['corr/easy','incorr/easy'],['corr/mid','incorr/mid'],['corr/hard','incorr/hard']]
    
#     # saving epochs -------------------------
#     epochs.save(diroutput + fileinput.split('/')[-1].replace('.set','-epo.fif'),overwrite=True)
    
  