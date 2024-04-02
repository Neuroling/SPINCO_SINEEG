#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:23:38 2024
@author: SibMei & samuemu

Liebe Sibylle,

mein Code findest du in PreStim_functions.py (wenn ich von "Funktion" rede, ist es da).
Ändere den Code in dem Skript nicht, weil es noch am laufen ist und ich es noch debugge,
aber kopiere den Code den du brauchst ruhig hier hin und passe ihn dann an.

Passe das Skript nur für s001 an, wir loopen es dann über alle TeilnehmerInnen.
"""

import pickle
import pandas as pd
import numpy as np
import PreStim_constants as const
import statsmodels.formula.api as smf
from PreStim_functions import PreStimManager
PreStimManager = PreStimManager() #initiate PreStimManager (collection of functions)


#%% 1. Datensatz öffnen =========================================================================
filepath = "/mnt/smbdir/Projects/Spinco/SINEEG/Data/SiN/derivatives_SM/task-sin/s001/s001_prestim_tfr_freqbands.pkl"
with open(filepath, 'rb') as f:
    tfr_band = pickle.load(f)

# Passe das Skript nur für das alpha-band an, wir loopen es dann später über alle anderen
data_array = tfr_band['Alpha_data']
condition_df = tfr_band['epoch_metadata']

# del tfr_band # wir löschen den dictionary mit den anderen Frequenzbändern

#%% 2. Datensatz vorbereiten ===================================================================
# Du musst zuerst data_array und condition_df in NV und SiSSN aufteilen
# Tipp: finde die index-Nummern für die NV oder SiSSN mit dem condition_df
# Und damit kannst du dann data_array filtern




# Dann, lass diesen Teil laufen. Ich hab das aus der Function get_epoData_singleSubj() kopiert.        
# re-name some columns
condition_df['noiseType'] = condition_df['block'] 
condition_df['wordPosition'] = condition_df['stimtype'] 

# Re-coding is necessary for the DV (needs to be numeric, not string)
condition_df['accuracy'].replace({'inc': 0, 'cor': 1}, inplace=True)

# drop unneeded columns
condition_df.drop(labels=['tf','stim_code','stimtype','stimulus','voice','block'], axis = 1, inplace = True)

# and, lastly, re-index (because the separation of conditions leads to non-sequential indices, which might lead to errors later)
reIdx = pd.Series(range(len(condition_df)))
condition_df.set_index(reIdx, inplace = True)

#%% 3. Logistische Regression ==================================================================
# Den Code hier habe ich aus den Funktionen kopiert. Er muss eventuell noch angepasst werden.
# Im Moment loopt es nur über channels[0:3] und timepoints[0:3] - das ist nur zum Testen.
# Ich passe es dann an, wenn wir es komplett laufen lassen.

formula = "accuracy ~ levels * eeg_data + wordPosition" # Das ist die Formel für die Regression
n_iter = 3 # Wir setzten das auf 3 zum Testen - Ich setze es dann auf 100 zum laufen lassen

#% Create arrays and lists
channelsIdx = [i for i in range(data_array.shape[1])] # list of channels
timesIdx = [i for i in range(data_array.shape[2])] #list of timepoints
channelsIdx = channelsIdx[0:3]
timesIdx = timesIdx[0:3]

# This will run a preliminary model, which is only used to extract the number of p-Values
# Which is needed to create an empty array for the p-Values
tmp_df = pd.DataFrame()
tmp_df = condition_df
tmp_df['eeg_data'] = data_array[:, 0, 0]
pVals_n = len(smf.logit(formula,
                        tmp_df
                        ).fit().pvalues.index)
del tmp_df

# now we know the dimensions of the empty array we need to create to collect p_Values
p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n,n_iter))
coefficients = np.zeros(shape=p_values.shape)
z_values = np.zeros(shape=p_values.shape)
coef_SD = np.zeros(shape=p_values.shape)


for iteration in range(n_iter):

    idx = PreStimManager.random_subsample_accuracy()

    # And now we run the model for every channel and every timepoint
    for thisChannel in channelsIdx:

        for tf in timesIdx:

            # extract the data & trial information at a given timepoint and channel              
            df = condition_df
            df['eeg_data'] = data_array[:,thisChannel,tf]
            df = df.iloc[idx] # subset the df by idx
                    
            # calculate Logit regression
            md = smf.logit(formula, 
                            df, 
                            )  
            
            mdf = md.fit(method = "lbgfs") 
            
            # record p-Values, z-Values and coefficients
            p_values[thisChannel,tf,:, iteration] = mdf.pvalues
            coefficients[thisChannel,tf,:, iteration] = mdf.params
            coef_SD[thisChannel,tf,:, iteration] = mdf.conf_int()[1] - mdf.params
            z_values[thisChannel,tf,:, iteration] = mdf.tvalues
 

p_values_mean = p_values.mean(axis = 3)
p_values_SD = p_values.std(axis = 3)
