
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
import MVPA.ANA_01_helper as hp

# inputs and paths Paths
taskID = 'task-sin'
pipeID = 'pipeline-01'
subjID='s015'


thisDir = os.path.dirname(os.path.abspath(__file__))
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', pipeID, taskID + '_preproc_epoched',subjID)


#%% creating .fif files - takes a lot of ressources, only run if necessary
# for subjID in subjIDs:
#     dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', pipeID, taskID + '_preproc_epoched',subjID)
#     fileinput = glob(os.path.join(dirinput, "*_epoched.set"), recursive=True)[0]
#     print(fileinput)
#     hp.eeglabEpo2mneEpo(fileinput)


#%% Read accu.tsv files for the event ids
events_fp = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', pipeID, taskID, subjID)
events_fp = glob(os.path.join(events_fp, "*accu.tsv"), recursive=True)[0]
events_tsv = pd.read_csv(events_fp,sep='\t')

#%% making an array of event ids to add to the epochs file
event_ids = np.zeros(shape=(1152,3))
idx = 0
for i in range(1,len(events_tsv)):
    if np.isnan(events_tsv['ACCURACY'][i]):
        continue
    else:
        event_ids[idx] = [(events_tsv['SAMPLES'][i]),(events_tsv['VALUE'][i]),(events_tsv['ACCURACY'][i])]
        idx=idx+1
        
del events_fp, events_tsv
event_idds = [1,0]

#%% from set file
fileinput = glob(os.path.join(dirinput, "*_epoched.set"), recursive=True)[0]
epochs = mne.io.read_epochs_eeglab(fileinput, events= event_ids, event_id=event_idds)

# %% Read epochs
#epochs.events= event_ids.astype(int)

epo_fn = fileinput[:fileinput.find('_epoched.set')]+'-epo.fif'
epochs.save(epo_fn, overwrite=True, fmt='double')
epo = mne.read_epochs(epo_fn)
# epo.plot()

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
    
  