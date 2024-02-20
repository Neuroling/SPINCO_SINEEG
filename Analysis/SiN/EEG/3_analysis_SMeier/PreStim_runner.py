#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 09:01:21 2024

@author: samuemu
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
from PreStim_functions import ERPManager
ERPManager = ERPManager() #initiate ERPManager

#%% 
Runner = False 
"""
If Runner == True, will re-run the LMM and re-compute the evokeds, and save them,
overwriting previously saved pickles. This will take a lot of time.

If Runner == False, will open previously saved pickles.

"""

if Runner:
    #%% Run LMM and save p-Values #############################################################################################
    ERPManager.get_data()
    p_values_FDR, index_p_values = ERPManager.run_LMM(function = "accuracy ~ levels * eeg_data * noiseType")
    ERPManager.save_pValues(p_values_FDR)
    
    #%% get evoked objects # TODO document more
    evokeds = ERPManager.get_evokeds()
    
else:
    #%% Open p-Values & evokeds ###############################################################################################
    with open(const.diroutput + const.pValsPickleFileEnd, 'rb') as f:
        p_values_FDR = pickle.load(f)
    
    with open(const.diroutput + const.evokedsPickleFileEnd, 'rb') as f:
        evokeds = pickle.load(f)

#%% do some plots
run = True
if run == True:
     
    
# Heatmaps for the parameters
    plt.figure()
    f, axs = plt.subplots(3, 3, figsize=(10, 8))   
    # Iterate over the subplots, plot the heatmaps, and set the titles
    for i in range(3):
        for j in range(3):
            sns.heatmap(p_values_FDR[:, :, i * 3 + j], vmin=0, vmax=0.20, ax=axs[i, j])
            axs[i, j].set_title(const.idx[i * 3 + j])  # Set the title
            axs[i,j].set(xlabel="times", ylabel="electrodes")
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.show()

    
    # sns.lineplot(data=p_values_FDR[1:10,1:10,3])

#%%
# Create a 3x2 grid of subplots
fig, axs = plt.subplots(3,2, figsize=(12, 18))
roi = ['C3', 'Cz', 'C4', 
       'P3', 'Pz', 'P4']

accuracy = ['Cor','Inc']
degradation = ['Lv1','Lv2','Lv3']
noise = ['NV','SSN']

# color_dict = {'Correct':'blue', 'Incorrect':'red'}
# linestyle_dict = {'Correct':'-', 'Incorrect':'--'}

# Loop through each combination of degradation and noise
for i, d in enumerate(degradation):
    for j, n in enumerate(noise):
        conditions = [n + '/' + d + '/' + a for a in accuracy]
        evokeds_to_plot = [evokeds[condition] for condition in conditions]
        print(evokeds_to_plot)

        # Plot the evokeds in the corresponding subplot
        mne.viz.plot_compare_evokeds(
            evokeds_to_plot,
            combine='mean',
            legend='lower right',
            picks=roi,
            show_sensors='upper right',
            # colors = color_dict,
            # linestyles = linestyle_dict,
            title=f'Waveforms ({n}/{d})',
            axes=axs[i, j]  # Specify the subplot to use
        )

# Adjust layout
plt.tight_layout()
plt.show()

