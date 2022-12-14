"""
RUN function to Extract features 
#--------------------------------------
- Read epochs per subject 
- Save features per subject  (each obj contains event/epoch info )

Created on Wed Dec 14 14:09:29 2022
@author: gfraga
"""
import sys
sys.path.insert(0,"/home/d.uzh.ch/gfraga/smbmount/gfraga/scripts_neulin/Projects/SINEEG/functions/" )
from fun_eeg_feat import *
import mne
import os
from glob import glob
#  paths
dirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/'
os.chdir(dirinput)


 
# list files
files = glob(dirinput + "s*.fif", recursive=True)

# File loop: 

for thisFile in files:
    epochs = mne.read_epochs(thisFile)
    epochs.info['description'] = thisFile # store source filename 
    
    # %% run function 
    out = fun_eeg_feat(epochs, spectral_connectivity=False)
 
    # %% 
    # Save each output, use dict key to define server and filenames
    for i in out.keys():
        #%% 
        i = 'tfr'
        newdirout = diroutput + 'epochs_' + i + '/'
        if not os.path.exists(newdirout): os.mkdir(newdirout)
        fileout = thisFile.split('/')[-1].split('_')[0] + '_epochs_' + i +'.h5'
        #
        out[i].save(newdirout + fileout,overwrite=True)
        
    