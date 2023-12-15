#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:18:39 2023

@author: samuemu
source: https://mne.tools/stable/auto_tutorials/time-freq/20_sensors_time_frequency.html

Yet another largely undocumented script meant to try code in, which will then be 
put into a "*_helper.py" and "*_runner.py" script

list of abbreviations:
    epo = epoch
    const = constants
    freqs = frequencies
    psd = power spectrum density
    itc = inter-trial coherence
    tfr = time frequency representation
    
"""

import os
from glob import glob
thisDir = os.getcwd()

import mne
from mne.time_frequency import tfr_morlet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import FeatureExtraction_constants as const
# import FeatureExtraction_helper as FeatureExtractor

#%% User inputs ###########################################################################################################
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives', 
                        const.pipeID, const.taskID + '_preproc_epoched',subjID)
epo_path = glob(os.path.join(dirinput, str("*"+ const.fifFileEnd)), recursive=True)[0]
# set_path = glob(os.path.join(dirinput, str("*"+ const.setFileEnd)), recursive=True)[0]


#%% Read epoched data #####################################################################################################
epo = mne.read_epochs(epo_path)
tmin = epo.times[0]
tmax = epo.times[len(epo.times)-1]

# # Conventient way to visualise epochs: The x-axis is time, and on the y-axis, each row of pixels represents a single epoch, 
# # with the colour of each pixel representing signal value (if combine="mean" it's the average of all electrodes)
# # https://mne.tools/stable/auto_tutorials/epochs/20_visualize_epochs.html#plotting-epochs-as-an-image-map
# epo['NV/Call/Cor'].plot_image(picks="eeg",combine="mean")


#%% Plot Power Spectrum densities #########################################################################################
# https://mne.tools/stable/generated/mne.time_frequency.EpochsSpectrum.html#mne.time_frequency.EpochsSpectrum

epo.compute_psd().plot() 
epo.compute_psd().plot(average=True)
epo.compute_psd().plot_topomap(ch_type="eeg", normalize=False, contours=0)


#%% Now let's do the morlet time frequency representation (TFR) ###########################################################
# https://mne.tools/stable/generated/mne.time_frequency.tfr_morlet.html



freqs = np.logspace(*np.log10([5, 48]), num=56) # define frequencies of interest
n_cycles = 3 #
sigma = n_cycles/(2 * np.pi * freqs)

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

tfr, itc = tfr_morlet(
    epo,
    freqs=const.freqs,
    n_cycles=const.n_cycles,
    use_fft=True,
    decim=3, # reduces data by this factor after convolution to reduce memory usage. May create aliasing artefacts
    n_jobs=None # sequential execution (less memory usage)
)

#%% COI
if not tfr.comment['n_cycles']:
    print("Found no n_cycles in tfr.comment. Add this info to tfr object as tfr.comment = {'n_cycles':XXX}")
    

    
else: 
    if tfr.comment['n_cycles'] == 'default: const.n_cycles':
        wavelet_width = const.fwhm
        print('using default fwhm')
    else:
        n_cycles = tfr.comment['n_cycles'] 
        freqs = tfr.freqs
        sigma = n_cycles/(2 * np.pi * freqs)
        fwhm = sigma * 2 * np.sqrt(2 * np.log(2))
        wavelet_width = fwhm
   
    
# % get coi values  (times per freq bin)
print('>> Cone of influence')
coi = wavelet_width/2
  
print('Creating dataframe with tfr power and filtering out values outside COI')
ts = tfr.times.copy()

#Create a data frame with TFR power indicating frequency band
tfr_df = tfr.to_data_frame(time_format=None)         
for c,cval in enumerate(coi):    
    #define time boundaries for each freq bin
    timeCOI_starts = ts[0] + coi[c]
    timeCOI_ends =   0 -coi[c]  
    
    #mark rows out of the COI as nan
    tfr_df[((tfr_df['time'] < timeCOI_starts) | (tfr_df['time'] > timeCOI_ends)) & (tfr_df['freq']==freqs[c])] = np.nan

tfr_df.dropna(axis=0,inplace=True)                  
print('Done.') 

#%% Freq Bands

freqbands = dict(Delta = [1,4],
                 Theta = [4,8],
                 Alpha=[8,13], 
                 Beta= [13,25],
                 Gamma =[25,48])

# %%
if type(tfr_df) is not pd.core.frame.DataFrame:
    tfr_df = tfr_df.to_data_frame(time_format=None)   
    print('Input converted to DF')
            
#%%         
freq_bounds =  [0] +  [item[1][1] for item in freqbands.items()] 
tfr_df['band'] = pd.cut(tfr_df['freq'], list(freq_bounds),labels=list(freqbands))    

#save averaged power per band in a dictionary
tfr_bands= {}
print('>> O_o Adding power averages per band to a dictionary')
tfr_bands['freqbands']=freqbands
for thisband in list(freqbands):                     
    # Mean 
    curBandDF = tfr_df[tfr_df.band.isin([thisband])].copy()
    dfmean = curBandDF.groupby(['epoch','time']).mean() # add mean per time point of all freqs selected across a selected set of channels
    ts = dfmean.index.get_level_values('time').unique()
    # Save data in arrays formated for mvpa                     
    x = []
    epIds = dfmean.index.get_level_values('epoch').unique()
    for ep in epIds:
        thisEpoch = dfmean.filter(regex='^E.*',axis = 1 ).loc[ep].to_numpy().transpose() # find columns with channel values (start with E*.) for each epoch and transpose 
        x.append(thisEpoch)
        del thisEpoch  
    X = np.dstack(x)                                                                        
    
    # Add to dictionary in shape:  epochs x Channels x TimePoints
    tfr_bands[thisband] = X.transpose(2,0,1)       
    tfr_bands['times_' + thisband] = ts
    print('>>> ' + thisband + ' avg per epoch added')

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
