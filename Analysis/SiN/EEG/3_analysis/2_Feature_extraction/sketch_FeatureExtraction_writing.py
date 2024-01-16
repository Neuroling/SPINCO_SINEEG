#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feature extraction - writing and trial script
===============================================================================
author: samuemu
Created on Fri Dec  8 12:18:39 2023

Yet another largely undocumented script meant to try code in, which will then be 
put into a "*_functions.py" and "*_runner.py" script

list of abbreviations:
    epo = epoch
    const = constants
    freqs = frequencies
    psd = power spectrum density
    itc = inter-trial coherence
    tfr = time frequency representation
    
sources: 
    https://mne.tools/stable/auto_tutorials/time-freq/20_sensors_time_frequency.html
    https://mne.tools/stable/auto_tutorials/epochs/20_visualize_epochs.html#plotting-epochs-as-an-image-map
    https://mne.tools/stable/generated/mne.time_frequency.EpochsSpectrum.html#mne.time_frequency.EpochsSpectrum
    https://mne.tools/stable/generated/mne.time_frequency.tfr_morlet.html
    
"""

import os
from glob import glob
thisDir = os.path.dirname(__file__)

import mne
from mne.time_frequency import tfr_morlet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold,cross_validate  
from sklearn import metrics
from sklearn import svm

import FeatureExtraction_constants as const
import FeatureExtraction_helper as helper

#%% User inputs ###########################################################################################################
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', 
                        const.pipeID, const.taskID + '_preproc_epoched',subjID)
epo_path = glob(os.path.join(dirinput, str("*"+ const.fifFileEnd)), recursive=True)[0]




#%% Read epoched data #####################################################################################################
epo = mne.read_epochs(epo_path)
tmin = epo.times[0]
tmax = epo.times[len(epo.times)-1]

# #% Conventient way to visualise epochs: The x-axis is time, and on the y-axis, each row of pixels represents a single epoch, 
# #% with the colour of each pixel representing signal value (if combine="mean" it's the average of all electrodes)
# #% https://mne.tools/stable/auto_tutorials/epochs/20_visualize_epochs.html#plotting-epochs-as-an-image-map
epo['NV/Call/Cor'].plot_image(picks="eeg",combine="mean")

#%% Copied from runner
TFRManager = helper.TFRManager()
features_dict=TFRManager.EEG_extract_feat(epo)
tfr=features_dict['TFR']

tfr_df = TFRManager.extractCOI(tfr)
tfr_bands = TFRManager.extractFreqBands(tfr_df,freqbands=const.freqbands)

#%% Plot Power Spectrum densities #########################################################################################
#% https://mne.tools/stable/generated/mne.time_frequency.EpochsSpectrum.html#mne.time_frequency.EpochsSpectrum

epo.compute_psd().plot() 
epo.compute_psd().plot(average=True)
epo.compute_psd().plot_topomap(ch_type="eeg", normalize=False, contours=0)


#%% Now let's do the morlet time frequency representation (TFR) ###########################################################
#% https://mne.tools/stable/generated/mne.time_frequency.tfr_morlet.html



"""
https://mne.tools/stable/generated/mne.time_frequency.morlet.html#mne.time_frequency.morlet

Paraphrased:
The width of a wavelet is determined by Sigma, which is the standard deviation of the Gaussian envelope.
The wavelet extends to +/-5 standard deviations, so the values at tail ends are close to 0.
Sigma is determined by freqs and n_cycles:
    >>> sigma = n_cycles/(2 * np.pi * freqs)

The full-width half-maximum (FWHM) can be determined by:
    >>> fwhm = sigma * 2 * np.sqrt(2 * np.log(2))
    or 
    >>> fwhm = n_cycles * np.sqrt(2 * np.log(2))/(np.pi * freqs)
    
if << n_cycles = freqs / 2 >> then sigma will always be = 1 / (4 * np.pi) = 0.079577
"""
# This creates TFR that are AVERAGED over epochs
tfr, itc = tfr_morlet(
    epo,
    freqs=const.freqs,
    n_cycles=const.n_cycles,
    use_fft=True,
    decim=3, # reduces data by this factor after convolution to reduce memory usage. May create aliasing artefacts
    n_jobs=None # sequential execution (less memory usage)
)



#%% power plots ###########################################################################################################

"""
[abcde]
https://mne.tools/stable/generated/mne.time_frequency.AverageTFR.html#mne.time_frequency.AverageTFR.plot
to read so I understand the parameters "baseline" and "mode" and know which are appropriate

baseline is the time interval to apply baseline correction (quote from link above)
mode is how the baseline correction is done, e.g. by subtracting the mean of baseline values ('mean')
    or by dividing by the mean of baseline values and taking the log (‘logratio’)
    
"""

tfr.plot_topo(baseline=(-0.5, 0), mode="logratio", title="Average power")
tfr.plot([28], baseline=(-0.5, 0), mode="logratio", title=tfr.ch_names[28])

fig, axes = plt.subplots(1, 2, figsize=(7, 4), layout="constrained")
topomap_kw = dict(
    ch_type="eeg", tmin=tmin, tmax=tmax, baseline=(-0.5, 0), mode="logratio", show=False
)

plot_dict = dict(Alpha=dict(fmin=8, fmax=12), Beta=dict(fmin=13, fmax=25))
for ax, (title, fmin_fmax) in zip(axes, plot_dict.items()):
    tfr.plot_topomap(**fmin_fmax, axes=ax, **topomap_kw)
    ax.set_title(title)

tfr.plot_joint(
    baseline=(-0.5, 0), mode="mean", tmin=tmin, tmax=tmax, 
    # timefreqs=[(-0.3, 10), (0.2, 8)] #this will plot the topomap at X seconds in Y frequency for each tuple (X,Y)
    # if timefreqs == None it will choose the absolute peak of time-frequency and plot the topomap there
    )

# #%% ITC plots  ############################################################################################################
# itc.plot_topo(baseline=(-0.5, 0), mode="logratio", title="Average ITC")


# fig, axes = plt.subplots(1, 2, figsize=(7, 4), layout="constrained")
# topomap_kw = dict(
#     ch_type="eeg", tmin=tmin, tmax=tmax, baseline=(-0.5, 0), mode="logratio", show=False
# )

# plot_dict = dict(Alpha=dict(fmin=8, fmax=12), Beta=dict(fmin=13, fmax=25))
# for ax, (title, fmin_fmax) in zip(axes, plot_dict.items()):
#     itc.plot_topomap(**fmin_fmax, axes=ax, **topomap_kw)
#     ax.set_title(title)

# itc.plot_joint(
#     baseline=(-0.5, 0), mode="mean", tmin=tmin, tmax=tmax, 
#     # timefreqs=[(-0.3, 10), (0.2, 8)] #this will plot the topomap at X seconds in Y frequency for each tuple (X,Y)
#     # if timefreqs == None it will choose the absolute peak of time-frequency and plot the topomap there
#     )

#%% MVPA
X= tfr_bands['Gamma']
y=epo.metadata['accuracy']
clf=svm.SVC(C=1, kernel='linear')
cv=None
scoretype='accuracy'

# #[MVPA] Decoding based on entire epoch
# ---------------------------------------------
if len(X.shape) != 3:
    if len(X.shape) > 3:
        raise ValueError(f'Array X needs to be 2 or 3-dimensional, not {len(X.shape)}')
    X_2d = X.reshape(len(X), -1) # Now it is epochs x [channels x times]   

#% see https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
all_scores_full = cross_validate(estimator = clf,
                                 X = X_2d, # the data to fit the model
                                 y= y,  # target variable to predict
                                 #cv=cv, # cross-validation splitting strategy
                                 n_jobs=const.n_jobs,
                                 scoring=scoretype,
                                 error_score='raise')
"""
Documentation for the function cross_validate:
 Returns
    -------
    scores : dict of float arrays of shape (n_splits,)
        Array of scores of the estimator for each run of the cross validation.

        A dict of arrays containing the score/time arrays for each scorer is
        returned. The possible keys for this ``dict`` are:

            ``test_score``
                The score array for test scores on each cv split.
                Suffix ``_score`` in ``test_score`` changes to a specific
                metric like ``test_r2`` or ``test_auc`` if there are
                multiple scoring metrics in the scoring parameter.
            ``train_score``
                The score array for train scores on each cv split.
                Suffix ``_score`` in ``train_score`` changes to a specific
                metric like ``train_r2`` or ``train_auc`` if there are
                multiple scoring metrics in the scoring parameter.
                This is available only if ``return_train_score`` parameter
                is ``True``.
            ``fit_time``
                The time for fitting the estimator on the train
                set for each cv split.
            ``score_time``
                The time for scoring the estimator on the test set for each
                cv split. (Note time for scoring on the train set is not
                included even if ``return_train_score`` is set to ``True``
            ``estimator``
                The estimator objects for each cv split.
                This is available only if ``return_estimator`` parameter
                is set to ``True``.
            ``indices``
                The train/test positional indices for each cv split. A dictionary
                is returned where the keys are either `"train"` or `"test"`
                and the associated values are a list of integer-dtyped NumPy
                arrays with the indices. Available only if `return_indices=True`.
"""

all_scores_full = {key: all_scores_full[key] for key in all_scores_full if key.startswith('test')} #get only the scores from output (also contains times)
print('--> run classification on the full epoch')

#%%

#[MVPA] Time-resolved decoding 
# ---------------------------------------------
n_times = X.shape[2]       

#Use dictionaries to store values for each score type 
scores = {name: [] for name in scoretype}
std_scores = {name: [] for name in scoretype}

print('[--> starting classification per time point....')
for t in range(n_times):
    Xt = X[:, :, t]
    
    # Standardize features
    Xt -= Xt.mean(axis=0)
    Xt /= Xt.std(axis=0)
    
    #[O_O] Run cross-validation 
    scores_t = cross_validate(clf, 
                              Xt, 
                              y, 
                              cv=cv, 
                              n_jobs=const.n_jobs,
                              scoring=scoretype)     
    
    #Add CV mean and std of this time point to my output dict 
    for name in scoretype:
        scores[name].append(scores_t['test_' + name].mean()) 
        std_scores[name].append(scores_t['test_' + name].std())

#from lists to arrays 
scores = {key: np.array(value) for key, value in scores.items()}
std_scores = {key: np.array(value) for key, value in std_scores.items()}
  
print('Done <--]')
# return all_scores_full, scores, std_scores 


