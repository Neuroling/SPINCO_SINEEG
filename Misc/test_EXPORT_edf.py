# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:10:24 2023

@author: gfraga
"""
import os
import mne 
os.chdir('v:\\projects\\spinco\\sineeg\\Data\\SiN\\raw\\p004\\')
#fileinput= 'MNE_exported.edf'
fileinput= 'p004_task.bdf'
#raw = mne.io.read_raw_bdf(fileinput, preload=True,  infer_types=True)
#raw = mne.io.read_raw_edf(fileinput, preload=True, infer_types=True )
raw = mne.io.read_raw_bdf(fileinput, preload=True, infer_types=True)
raw.drop_channels(['EXG7','EXG8','Erg1'])
 
# %% 

FOLDER_OUT = 'v:\\projects\\spinco\\sineeg\\Data\\SiN\\raw\\p004\\'
raw.load_data()
fileout = 'MNE_exported.edf'
mne.export.export_raw(os.path.join(FOLDER_OUT, 'MNE_exported.edf'),raw,fmt='edf', overwrite= True) # note: 2GB is the default and the maximum

# %% 
import mne
raw = mne.io.read_raw_edf('MNE_exported.edf', preload=True, infer_types=False)   

#%% 
raw.plot()