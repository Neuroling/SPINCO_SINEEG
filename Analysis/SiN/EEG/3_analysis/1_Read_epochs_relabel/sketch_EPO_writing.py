
""" 
READ EEGLAB EPOCHS IN MNE - WRITING AND TRIAL SCRIPT
===============================================================================
@author: samuelmull & gfraga
Created November 2023

This script is an undocumented mess, because it is for trying out code and 
debugging before putting it into EPO_functions


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
import EPO_functions as helper
import EPO_constants as const
import pandas as pd

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
# epo = EpoManager.set2fif(metadata=True,relabelEvents=True)
epo = EpoManager.readEpo() # reading the epoched data 
freqTable = EpoManager.countEventFrequency(epo) # creating a frequency of ocurrence table
metadata=EpoManager.constructMetadata() # constructing metadata

epo = EpoManager.relabelEvents(epo) # relabelling events


#%%

epo.info
epo.plot()
epo["NV/Lv1"].plot()
epo.plot_sensors(kind="3d", ch_type="all")

epo["NV/Lv1"].compute_psd(exclude=['Cz']).plot(picks="eeg",average=False)

# # plots from here on need matplotlib v3.7.3 or newer
epo.plot_image(picks=[41,42,43])

# #%%
# evo_NV=epo.__getitem__('NV').average()
# evo_SSN=epo.__getitem__('SSN').average()

# mne.viz.plot_compare_evokeds(dict(Nv=evo_NV, SSN=evo_SSN))



# evo = epo.__getitem__('Lv3/Col/Cor').average()
# evo.plot()
# epo.compute_psd().plot(exclude=['Cz'])

#%%




    
  
