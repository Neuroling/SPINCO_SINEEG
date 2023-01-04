#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 10:26:03 2022
   
# GATHER GROUP TRIAL INFORMATION FOR SVM
# ============================================
# Read .mat files with subject and trial info. Concatenate in group array and save 
    
@author: gfraga
"""
import os

import numpy as np
from glob import glob
import scipy.io as sio
import mne 
import pandas as pd

home = os.path.expanduser("~")

#% Gather Target File info
# %------------------------
basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/mvpa/25subj_TFR/'
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/mvpa/25subj_TFR' 

if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
        
# find target files
files = glob(basedirinput + "*info_trials_mvpa.mat", recursive=True)

print(files) 


# %% # Loop thru subjects 
slist= []
ylist = []
for fileinput in files: 
    print (fileinput)

    #Read matlab file for addtional time and trial info 
    mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)
    # append info
    
    slist.append(mdat['S'])
    ylist.append(mdat['Y'])

# compile 
S = np.concatenate((slist),axis=0)
Y = np.concatenate((ylist),axis=0)
times = mdat['times']

# save 
S = S.astype('int16')
Y = np.array(Y).astype('int16')
#times = np.array(times)
 # Group arrays  
# Arrays X will be too large to export in a single file  
preproc_mvpa = {'S':S, 'Y':Y,'times':times}
sio.savemat(diroutput + '/info_trials_mvpa.mat',preproc_mvpa)
 