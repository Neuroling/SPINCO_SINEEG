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


 # TODO describe input and output files  

"""
#%% USER INPUT 
Runner = True 
doPlots = False

"""
Runner : bool
    if True, will re-run the LMM and re-compute the evokeds, and save them,
    overwriting previously saved pickles. This will take a lot of time.
    If False, will open previously saved pickles instead
    
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

import PreStim_constants as const
from PreStim_functions import PreStimManager
PreStimManager = PreStimManager() #initiate PreStimManager (collection of functions)


#%%
if Runner:
    #%% Run LMM and save p-Values #############################################################################################
    
    for noise in const.noise:
        PreStimManager.get_data(condition = noise)
        p2, md2 = PreStimManager.run_LogitRegression()
        # PreStimManager.FDR_correction()
        # p_values_FDR = PreStimManager.save_pValues()
    
    #%% get evoked objects # TODO document more
    # TODO separate noiseType
    # evokeds = PreStimManager.get_evokeds()
    
else:
    #%% Open p-Values & evokeds ###############################################################################################
    # TODO I need to change this now that we separated NoiseType and have different filenames
    with open(const.diroutput + const.pValsPickleFileEnd, 'rb') as f:
        p_values_FDR = pickle.load(f)
    
    with open(const.diroutput + const.evokedsPickleFileEnd, 'rb') as f:
        evokeds = pickle.load(f)


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
            axs[i, j].set_title(const.idx[i * 3 + j])  # Set the title
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
    
    

