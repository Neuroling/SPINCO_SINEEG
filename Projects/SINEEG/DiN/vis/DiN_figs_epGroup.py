#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 12:14:35 2022

@author: gfraga
"""
 
import os
from glob import glob
import scipy.io as sio
import mne 

home = os.path.expanduser("~")

#% Gather Target File info
# %------------------------
basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/' 

if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
# find target files
files = glob(basedirinput + "*.set", recursive=True)
subjects = [fullpath.split('/')[-1].split('_')[0] for fullpath in files]

conditions = ['corr/clear','corr/easy','corr/mid','corr/hard','incorr/clear','incorr/easy','incorr/mid','incorr/hard']
# %% 
# Read/ import data 
# -----------------------------------------------
 
for fileinput in files: 
    #fileinput = 's9_DiN_epoched_ICrem.set'
    print (fileinput)
    # Read Epochs in MNE 
    epochs = mne.io.read_epochs_eeglab(fileinput)
    
    
    # ADD CRUCIAL INFO FROM READING THE MAT FILE (missed by mne read)
    mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)['EEG']
    # Correct times using the actualTimes variable (were 0 = digit onset) 
    epochs.shift_time(mdat['actualTimes']/1000-epochs.times)[0]
    
    #trial accuracy
    epochAccu = [epoch['accuracy'] for epoch in mdat['epoch']]
    
    # degradation levels    
    epochDeg = [epoch['degBin'] for epoch in mdat['epoch']]
    epochDeg = [0 if x!=x else x for x in epochDeg] # replace nan by 0 
        
    # recode events in MNE-read data
    for epIdx in range(len(epochs.events)):
        epochs.events[epIdx][2]=epochAccu[epIdx]*10 + epochDeg[epIdx]
    # add event information 
    epochs.event_id = {'corr/clear': 10,'corr/easy': 11,'corr/mid': 12,'corr/hard': 13,'incorr/clear': 0,'incorr/easy': 1,'incorr/mid': 2,'incorr/hard': 3}
  
    
    # Subject info: subject number repeated n trial times 
    subjectID = fileinput.split('/')[-1].split('_')[0]
 

    # %% 
   
    


# # %%
# # #%matplotlib 
# # evokeds = dict(corr=list(epochs['correct'].iter_evoked()),
# #                incorr=list(epochs['incorrect'].iter_evoked()))

# # meanCorr = epochs['correct'].average()
# # meanIncorr = epochs['incorrect'].average()

# # #for evk in (meanCorr, meanIncorr):
# #  #   evk.plot(gfp=True, spatial_colors=True)

# # diffs = mne.combine_evoked([meanCorr,meanIncorr], weights=[1, -1])
# # diffs.plot_joint()
# # #mne.viz.plot_compare_evokeds(evokeds, combine='mean')



# # %% 
# #       ep2plot.average().plot_topomap(times, ch_type='eeg',axes=axs[e*i])

# # %% 
# # Epochs mean all chans 
# #[epochs[epochSel].plot_image(combine=stat,title= epochSel + ' trials (' + stat + ')') for epochSel in ['correct','incorrect']]

# #% SAVE THIS SECTION COMMENTED FOR FURTHER DEVELOPMENTS .... 
# # Visualize data 
# stat = 'mean'
# fig,axs = plt.subplots(3,2)
# for e,epochSel in enumerate(['correct','incorrect']):    
#     ep2plot = epochs[epochSel]
#     ep2plot.plot_image(combine=stat,title= epochSel + ' trials (' + stat + ')',axes=axs[e,:]) 
            
# #plt.subplots_adjust(left=0.01, right=0.975, bottom=0.14, top=0.85,hspace=0.5, wspace=0.3)

# # %%
# # epochs[epochSel].average().plot()


# # %%













#  # %%
#  # Helper function for plotting spread
# def stat_fun(x):
#     """Return sum of squares."""
#     return np.sum(x ** 2, axis=0)
# from mne.stats import bootstrap_confidence_interval
# from mne.baseline import rescale
 
# # let's explore some frequency bands
# iter_freqs = [
#     ('Theta', 4, 7),
#     ('Alpha', 8, 12),
#     ('Beta', 13, 25),
#     ('Gamma', 30, 45)
# ]

# # set epoching parameters
# event_id, tmin, tmax = 1, -1., 3.
# baseline = None


# frequency_map = list()
# for band, fmin, fmax in iter_freqs:
#     # (re)load the data to save memory

#    # bandpass filter
#     epochs.filter(fmin, fmax, n_jobs=None,  # use more jobs to speed up.
#                l_trans_bandwidth=1,  # make sure filter params are the same
#                h_trans_bandwidth=1)  # in each band and skip "auto" option.

#     # remove evoked response
#     epochs.subtract_evoked()

#     # get analytic signal (envelope)
#     epochs.apply_hilbert(envelope=True)
#     frequency_map.append(((band, fmin, fmax), epochs.average()))
 
 
# # Plot
# fig, axes = plt.subplots(4, 1, figsize=(10, 7), sharex=True, sharey=True)
# colors = plt.colormaps['winter_r'](np.linspace(0, 1, 4))
# for ((freq_name, fmin, fmax), average), color, ax in zip(
#         frequency_map, colors, axes.ravel()[::-1]):
#     times = average.times * 1e3
#     gfp = np.sum(average.data ** 2, axis=0)
#     gfp = mne.baseline.rescale(gfp, times, baseline=(None, 0))
#     ax.plot(times, gfp, label=freq_name, color=color, linewidth=2.5)
#     ax.axhline(0, linestyle='--', color='grey', linewidth=2)
#     ci_low, ci_up = bootstrap_confidence_interval(average.data, random_state=0,
#                                                   stat_fun=stat_fun)
#     ci_low = rescale(ci_low, average.times, baseline=(None, 0))
#     ci_up = rescale(ci_up, average.times, baseline=(None, 0))
#     ax.fill_between(times, gfp + ci_up, gfp - ci_low, color=color, alpha=0.3)
#     ax.grid(True)
#     ax.set_ylabel('GFP')
#     ax.annotate('%s (%d-%dHz)' % (freq_name, fmin, fmax),
#                 xy=(0.95, 0.8),
#                 horizontalalignment='right',
#                 xycoords='axes fraction')
#     #ax.set_xlim(-41000, 3000)

# axes.ravel()[-1].set_xlabel('Time [ms]')


 