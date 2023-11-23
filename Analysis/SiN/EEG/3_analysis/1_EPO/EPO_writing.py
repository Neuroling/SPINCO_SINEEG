
""" READ EEGLAB EPOCHS in MNE 
=================================================================
@author: samuemu & gfraga

This script is an undocumented mess, because it is for trying out code and debugging before putting it into EPO_helper

NOTE: 
    Some MNE plotting functions start bugging with matplotlib version 3.7.2 or earlier.
    To ensure smooth operation, update to at least matplotlib version 3.7.3

 
""" 

import os
from glob import glob
import scipy.io as sio
thisDir = os.getcwd()
# import numpy as np
import mne 
# import pandas as pd
import EPO_helper as helper
import EPO_constants as const

#%% below is for debugging purposes
# subjID= 's001'
# dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', const.pipeID, const.taskID + '_preproc_epoched',subjID)
# set_fp = glob(os.path.join(dirinput, str("*"+ const.setFileEnd)), recursive=True)[0]
# epo_fp = set_fp[:set_fp.find(const.setFileEnd)]+'-epo.fif'
# events_fp = glob(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', const.pipeID, const.taskID, subjID,"*accu.tsv"), recursive=True)[0]
# beh_fp = glob(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subjID, const.taskID, 'beh',"*.csv"), recursive=True)[0]

   
#%% 

subjID= 's001'
EpoManager = helper.EpochManager(subjID)
# # epo = EpoManager.set2fif(metadata=True,relabelEvents=True)
epo = EpoManager.readEpo()

#%%

epo.info
epo.plot()
# plots from here on need matplotlib v3.7.3 or newer
epo.plot_image(picks=[41,42,43])
#%%
evo_NV=epo.__getitem__('NV').average()
evo_SSN=epo.__getitem__('SSN').average()

mne.viz.plot_compare_evokeds(dict(Nv=evo_NV, SSN=evo_SSN))



evo = epo.__getitem__('Lv3/Col/Cor').average()
evo.plot()
epo.compute_psd().plot(exclude=['Cz'])

#%% Old code to reuse


# # # CHECK EVENT CODES 
# # #  


# # # Some plots
# # 'V:\Projects\Spinco\SINEEG\Scripts\Analysis\SiN\EEG\3_analysis\old_functions\funs_eeg'   - recycle some stuff 

# # ############# THIS IS STILL WORK IN PROGRESSS
# # # %% 
# # #% Gather Target File info
# # # %------------------------
# # basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/_urepochs_eeglab/' 
# # diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 

# # if not os.path.exists(diroutput): 
# #     os.mkdir(diroutput)
# # # find target files
# # files = glob(basedirinput + "*.set", recursive=True)
# # subjects = [fullpath.split('/')[-1].split('_')[0] for fullpath in files]


# # # %% 
# # for fileinput in files:
# #    # %%
# #     epochs = mne.io.read_epochs_eeglab(fileinput)
    
# #     # Relevant event fields
# #     #mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)
# #     mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)['EEG']
# #     # accuracy
# #     epochAccu = [epoch['accuracy'] for epoch in mdat['epoch']]
     
    
# #     # degradation levels    
# #     epochDeg = [epoch['degBin'] for epoch in mdat['epoch']]
# #     epochDeg = [0 if x!=x else x for x in epochDeg] # replace nan by 0 
        
# #     # recode events in MNE-read data
# #     for epIdx in range(len(epochs.events)):
# #         epochs.events[epIdx][2]=epochAccu[epIdx]*10 + epochDeg[epIdx]
# #     # add event information 
# #     epochs.event_id = {'corr/clear': 10,'corr/easy': 11,'corr/mid': 12,'corr/hard': 13,'incorr/clear': 0,'incorr/easy': 1,'incorr/mid': 2,'incorr/hard': 3}
      
    
# #     # Subject info: subject number repeated n trial times 
# #     subjectID = fileinput.split('/')[-1].split('_')[0]
# #     types = [['corr/easy','corr/mid','corr/hard'],['incorr/easy','incorr/mid','incorr/hard']] # Clear conditions are excluded from this average to avoid bias
# #     difficulty = [['corr/clear','incorr/clear'],['corr/easy','incorr/easy'],['corr/mid','incorr/mid'],['corr/hard','incorr/hard']]
    
# #     # saving epochs -------------------------
# #     epochs.save(diroutput + fileinput.split('/')[-1].replace('.set','-epo.fif'),overwrite=True)
    
  