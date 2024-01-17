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
Then, crossvalidation scores are processed

So far, this script does not loop over subjects
"""

#%% Set working directory
#% This requires working with the spyder project on this directory: Y:\Projects\Spinco\SINEEG\Scripts\Analysis\SiN\EEG    # TODO
import os
from glob import glob

# thisDir = os.path.join(os.getcwd(),'3_analysis','2_Feature_extraction')
# os.chdir(thisDir)

thisDir = os.getcwd()

#%% Imports
import mne
# from mne.time_frequency import tfr_morlet
# import matplotlib.pyplot as plt
# import numpy as np
import pickle

import FeatureExtraction_constants as const
import FeatureExtraction_functions as functions

#%% Looping over subjects
for subjID in const.subjIDs:
    
    #%% File paths ###########################################################################################################

    dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', 
                            const.pipeID, const.taskID + '_preproc_epoched',subjID)
    epo_path = glob(os.path.join(dirinput, str("*"+ const.fifFileEnd)), recursive=True)[0]
    diroutput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                            const.taskID,'features',subjID)
    
    if not os. path.exists(diroutput):
        os.makedirs(diroutput)
        print("path created: "+diroutput)
    pickle_path = os.path.join(diroutput, subjID + const.pickleFileEnd)
    
    
    #%% Read epoched data #####################################################################################################
    epo = mne.read_epochs(epo_path)
    events = epo.events[:,2]
    event_id = epo.event_id
    
    
    
    #%% Extract features ######################################################################################################
    FeatureExtractionManager = functions.FeatureExtractionManager()
    features_dict = FeatureExtractionManager.EEG_extract_feat(epo)
    tfr = features_dict['TFR']
    
    #%% Get Cone of Influence #################################################################################################
    tfr_df = FeatureExtractionManager.extractCOI(tfr)
    
    #%% Split into frequency bands ############################################################################################
    tfr_bands = FeatureExtractionManager.extractFreqBands(tfr_df,freqbands=const.freqbands)
    
    #%% Adding condition & trial information
    tfr_bands['all_epoch_eventIDs'] = list(events)
    tfr_bands['metadata'] = epo.metadata
    tfr_bands['all_epoch_conditions'] = [key for item in events for key, value in event_id.items() if value == item]
    #% the code above is a complicated way of saying "use the dict event_id to find the key corresponding to the value in events"
    #% Which is a complicated way of saying "For each epoch, give me the event-labels instead of the numeric event-codes"
    
    #%% save dictionary (pickle it!) ##########################################################################################
    with open(pickle_path, 'wb') as f:
        pickle.dump(tfr_bands, f)
    print("pickling the dictionary")
    
    # #%% Get crossvalidation scores
    # y = epo.metadata['accuracy'] # What variable we want to predict
    
    # for thisBand in const.freqbands:
    #     all_scores_full, scores, std_scores = FeatureExtractionManager.get_crossval_scores(X=tfr_bands[thisBand], y = y)
    #     tfr_bands[thisBand+'_crossval_FullEpoch'] = all_scores_full
    #     tfr_bands[thisBand+'_crossval_timewise_mean'] = scores
    #     tfr_bands[thisBand+'_crossval_timewise_std'] = std_scores
    # # TODO - Hm. all [band]_timewise_mean and all [band]_timewise_std are the same value. Check if there's an error somewhere
    
    #%% Extracting and saving amplitude per frequency band
    # CAUTION: running the next line might be too much for your RAM to handle.
    # If your kernel keeps restarting, change const.n_jobs to None and
    # try again. (this will take a while to run)
    # If that still does not help, comment the next line so it doesn't execute
    # and then run the amplitude extraction alone without the TFR stuff later
    FeatureExtractionManager.extractFreqbandAmplitude(epo, diroutput, subjID)
    
print("All done.")
