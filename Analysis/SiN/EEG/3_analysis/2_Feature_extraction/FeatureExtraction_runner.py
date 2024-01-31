#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runner-script for the Feature extraction
===============================================================================
@author: samuemu
Created on Wed Dec 13 07:57:50 2023

This is the runner-script for the Feature extraction. 
All Functions are in the FeatureExtraction_functions.py script, and
all constants are in the FeatureExtraction_constants.py script.

First, TFR is extracted
Then, values outside the COI are excluded
Then, TFR means for every frequency band are computed.
Then, the TFR dict is saved using the pickle-module

FREEZING KERNEL
If your kernel keeps freezing when trying to run the code,
try one or more of these solutions
    - In the constants, set n_jobs = None
    - In the constants, set decim = 2 (or higher if necessary. This will decimate the sampling rate.)
    - Instead of looping over subjects, manually run the code for each subject. Open a new console for every subject.
"""

#%% Set working directory #####################################################################################################
#% This requires working with the spyder project on this directory: Y:\Projects\Spinco\SINEEG\Scripts\Analysis\SiN\EEG  # TODO
import os
from glob import glob

# thisDir = os.path.join(os.getcwd(),'3_analysis','2_Feature_extraction')
# os.chdir(thisDir)

thisDir = os.getcwd()

#%% Imports ###################################################################################################################
import mne
# from mne.time_frequency import tfr_morlet
# import matplotlib.pyplot as plt
# import numpy as np
import pickle
from datetime import datetime

import FeatureExtraction_constants as const
import FeatureExtraction_functions as functions


#%% Looping over subjects #####################################################################################################
for subjID in const.subjIDs:
    
    print('_.~"(_.~"(_.~"(_.~"(_.~"(  now processing',subjID,'   _.~"(_.~"(_.~"(_.~"(_.~"(')
    #%% File paths ############################################################################################################

    dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', 
                            const.pipeID, const.taskID + '_preproc_epoched',subjID)
    epo_path = glob(os.path.join(dirinput, str("*"+ const.taskID + const.fifFileEnd)), recursive=True)[0]
    diroutput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                            const.taskID,'features',subjID)
    
    if not os. path.exists(diroutput): # If the output directory doesn't exist, create it
        os.makedirs(diroutput)
        print("path created: "+diroutput)
    pickle_path = os.path.join(diroutput, subjID + const.pickleFileEnd)
    
    #%% Read epoched data #####################################################################################################
    epo = mne.read_epochs(epo_path)
    events = epo.events[:,2]
    event_id = epo.event_id
    
    #%% Extract features ######################################################################################################
    FeatureExtractionManager = functions.FeatureExtractionManager()
    features_dict = FeatureExtractionManager.EEG_extract_feat(epo, PSD=False)
    tfr = features_dict['TFR']
    del features_dict
    
    #%% Get Cone of Influence #################################################################################################
    tfr_df = FeatureExtractionManager.extractCOI(tfr)
    del tfr
    
    #%% Split into frequency bands ############################################################################################
    tfr_bands = FeatureExtractionManager.extractFreqBands(tfr_df,freqbands=const.freqbands)
    del tfr_df
    
    #%% Adding condition & trial information ##################################################################################
    tfr_bands['epoch_eventIDs'] = list(events)
    tfr_bands['epoch_metadata'] = epo.metadata
    tfr_bands['epoch_conditions'] = [key for item in events for key, value in event_id.items() if value == item]
    #% the line above is a complicated way to say "use the dict event_id to find the key corresponding to the value in events"
    #% Which is a complicated way of saying "For each epoch, give me the event-labels instead of the numeric event-codes"
    
    #%% Add additional information to the metadata of the dict ################################################################
    tfr_bands['metadata']['epoch_path']=epo_path
    tfr_bands['metadata']['date_created']=str(datetime.now())
    tfr_bands['metadata']['decimation_factor']=const.decim
    tfr_bands['metadata']['ch_names']=epo.ch_names
    
    #%% save dictionary (pickle it!) ##########################################################################################
    with open(pickle_path, 'wb') as f:
        pickle.dump(tfr_bands, f)
    print("pickling the dictionary")
    
    del tfr_bands
    del FeatureExtractionManager # to make sure there is no spill-over between subjects, we delete the Manager in each loop
    
    
print("All done.")
