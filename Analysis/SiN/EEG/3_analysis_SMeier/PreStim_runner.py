#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RUNNER SCRIPT FOR PreStim
===============================================================================
Created on Fri Feb  2 09:01:21 2024
@author: samuemu

This is the runner script for the Pre-Stimulus analyses.

It calls the functions from PreStim_functions. To do this, it is necessary to
first initialize the class by calling `PreStimManager = PreStimManager()`

This script and the functions script requires the PreStim_constants script,
which contains variables used across scripts and functions, such as filepath chunks
or condition labels.

Input files:
    - epoched data from MNE *epo.fif
        - Handled entirely by PreStimManager
        - The filepaths are in PreStim_constants and adpted to each subject by PreStimManager.
        
Output files:
    - p-Values array as .pkl
        - A dict containing the array of p-Values as well as the metadata. 
        - The metadata contains information on how the p-Values were computed, including the
          type of regression (logit or LMM), regression formula, FDR-correction, etc.
        - p-Values are saved by calling PreStimManager.save_pValues()
        - This can be done regardless of regression type (logit or LMM) or FDR-correction.
        - The output filepath is in PreStim_constants and adapted to each case by PreStimManager.
        
    - evokeds dict as .pkl
        - A dict which has all possible combinations of accuracy, noiseType & degradation
          as keys, which each have the corresponding value of a list containing the evoked arrays
          of every subject. 
        - In other words: A dict of evoked arrays for every combination of subjID, accuracy, noiseType & degradation
        - They are created and saved by calling PreStimManager.get_evokeds().
        - The output filepath is in PreStim_constants.
        

"""

#%% USER INPUT 
Runner = True 
doPlots = False

"""
Runner : bool
    if True, will re-run the regression and re-compute the evokeds, and save them,
    overwriting previously saved pickles. This will take a lot of time.
    If False, will open previously saved pickles instead (Not working right now, # TODO )
    
doPlots : bool
    if True, will run plots

"""
#%% Imports ###################################################################################################################
import os
from glob import glob
import mne

import statsmodels.formula.api as smf
import statsmodels.stats.multitest as ssm
import statsmodels.base.optimizer as smo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from datetime import datetime
from multiprocessing import Pool, Process
import time
import warnings

import PreStim_constants as const
from PreStim_functions import PreStimManager
PreStimManager = PreStimManager() #initiate PreStimManager (collection of functions)

start_time = datetime.now() # recording the time when the script starts running (helpful for debugging, optimisation and control)

# warnings.filterwarnings('ignore') 
#%%
if Runner:
    
    # def within_subj_analysis(subjID):
    #     for noise in const.noise:
    #     # for noise in ['NV']:
    #         PreStimManager.get_data_singleSubj(subjID, condition = noise)
    #         PreStimManager.run_LogitRegression_withinSubj(sub_sample= True, n_iter = 1000)
    #         # PreStimManager.FDR_correction()
    #         # PreStimManager.save_pValues()
            
   
            
    # if __name__ == "__main__":
    #     with Pool() as pool:
    #       pool.map(within_subj_analysis, const.subjIDs)
    #     print("Program finished!")
    
    # #%% 
    # def noise_separated_regression(noise):
    #     PreStimManager.get_data_singleSubj('s006', condition = noise)
    #     PreStimManager.run_LogitRegression_withinSubj(sub_sample= True, n_iter = 1000)
    #     # PreStimManager.FDR_correction()
    #     PreStimManager.save_pValues()
    
    
    # for noise in const.noise:
    #     noise_separated_regression(noise)
        
    # # if __name__ == '__main__':
    # #     with Pool() as pool:
    # #         pool.map(noise_separated_regression, const.noise)
    
    #%% Run regression and save p-Values #############################################################################################
    time_control = []
    for noise in const.noise: # separately for each noiseType
    # for noise in ['NV']: # for debugging, only run one condition
        
        for subjID in const.subjIDs[4:5]:
            time_control.append("start " + subjID + ": " + str(datetime.now()))
            
            PreStimManager.get_data_singleSubj(subjID, condition = noise) # Get epoched data in a format usable for regression
            PreStimManager.run_LogitRegression_withinSubj() # run the regression separately for each timepoint & channel  
            # PreStimManager.FDR_correction() # FDR correct the p-Values (separately for each channel & parameter)
            PreStimManager.save_pValues() # save the p-Value array and return it
    
    #%% get evoked objects for every subj of every possible combination of accuracy, noiseType & degradation
    # evokeds = PreStimManager.get_evokeds()
    
# else:
#     #%% Open p-Values & evokeds ###############################################################################################
#     # TODO I need to change this now that we separated NoiseType and have different filenames
#     with open(const.diroutput + const.pValsPickleFileEnd, 'rb') as f:
#         p_values_FDR = pickle.load(f)
    
#     with open(const.diroutput + const.evokedsPickleFileEnd, 'rb') as f:
#         evokeds = pickle.load(f)


#%% do some plots =============================================================================================================
if doPlots:

    pVals = p_values_FDR['p_values']     
    
# Heatmaps for the parameters
    plt.figure()
    f, axs = plt.subplots(3, 3, figsize=(10, 8))   
    # Iterate over the subplots, plot the heatmaps, and set the titles
    for i in range(3):
        for j in range(3):
            sns.heatmap(pVals[:, :, i * 3 + j], vmin=0, vmax=0.15, ax=axs[i, j])
            axs[i, j].set_title(p_values_FDR['metadata']['p_Values_index'][i * 3 + j])  # Set the title
            axs[i,j].set(xlabel="times", ylabel="electrodes")
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.show()
    # TODO change electrode numbers in y-axis to labels like Fpz, Oz, etc
    # TODO change times to seconds instead of tf

    
    # sns.lineplot(data=p_values_FDR[1:10,1:10,3])

#%% Amplitude Comparison of Accuracy ===========================================================================
## see https://neuraldatascience.io/7-eeg/erp_group_viz.html
    
    roi = ['C3', 'Cz', 'C4', 
           'P3', 'Pz', 'P4']
    
    # Create a 3x2 grid of subplots
    plt.figure()
    fig, axs = plt.subplots(2,3, figsize=(20, 12))
    
    # Loop through each combination of degradation and noise
    for i, n in enumerate(const.noise):
        for j, d in enumerate(const.degradation):
            conditions = [n + '/' + d + '/' + a for a in const.accuracy]
            evokeds_to_plot = [evokeds[condition] for condition in conditions]
    
            # Plot the evokeds in the corresponding subplot
            mne.viz.plot_compare_evokeds(
                evokeds_to_plot,
                combine='mean',
                legend='lower right',
                picks=roi,
                show_sensors='upper right',
                title=f'ERP ({n}/{d})',
                show = False, #If plotting multiple figures in one plot with MNE, set show = False and call plt.show() at the end
                axes=axs[i, j]  # Specify the subplot to use
            )
    
    # Adjust layout
    # plt.tight_layout()
    plt.show()



#%% This section would run the above plots for every single electrode ============================================

# for thisChannel in p_values_FDR['metadata']['ch_names']:
    
#     # Create a 3x2 grid of subplots
#     plt.figure()
#     fig, axs = plt.subplots(2,3, figsize=(20, 12))
    
#     # Loop through each combination of degradation and noise
#     for i, n in enumerate(const.noise):
#         for j, d in enumerate(const.degradation):
#             conditions = [n + '/' + d + '/' + a for a in const.accuracy]
#             evokeds_to_plot = [evokeds[condition] for condition in conditions]
    
#             # Plot the evokeds in the corresponding subplot
#             mne.viz.plot_compare_evokeds(
#                 evokeds_to_plot,
#                 combine='mean',
#                 legend='lower right',
#                 picks=thisChannel,
#                 show_sensors='upper right',
#                 title=f'{thisChannel} ({n}/{d})',
#                 show = False, 
#                 axes=axs[i, j]  # Specify the subplot to use
#             )
    
#     # Adjust layout
#     # plt.tight_layout()
#     plt.show()
    
#%% topomap
    evokeds_gAvg = PreStimManager.grandaverage_evokeds(evokeds)
    
    # times_array = [-0.5, -0.4,-0.3,-0.2,-0.1,0]
    
    for condition in const.conditions:
        #f, axs = plt.subplots(1,10, figsize=(10, 8
        # plt.figure()
        fig = mne.viz.plot_evoked_topomap(
            evokeds_gAvg[condition],
            # times = times_array
            )
        # fig.suptitle(f'Topomaps for {condition}')
        # plt.show()
     
    for condition in const.conditions:
        #f, axs = plt.subplots(1,10, figsize=(10, 8
        # plt.figure()
        fig = mne.viz.plot_evoked_topo(
            evokeds_gAvg[condition],
            title=f'{condition}'
            )
        # fig.suptitle(f'Topomaps for {condition}')
        # plt.shSow()

end_time = datetime.now()    # To record the time of when the script finishes running
    

