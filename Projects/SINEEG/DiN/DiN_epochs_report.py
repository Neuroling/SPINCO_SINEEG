#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------------------------
 CREATE A SUMMARY REPORT 
---------------------------------------------------------------------------------------------------------------------  
* Reads MNE epoched objects. 
* Makes a report for quality assessment and results inspection 
* 
@author: gfraga
Created on Tue Dec  6 15:03:56 2022
"""
import mne
from mne.time_frequency import tfr_morlet
import os
from glob import glob
import numpy as np
# %%  Access epoched data
dir_epoched = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/'
dir_evoked  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/evoked/'
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/reports_singles' 
if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
    
files = glob(dir_epoched + "s*.fif", recursive=True)
subjects = [f.split('/')[-1].split('_')[0] for f in files ]


for thisSubject in subjects:
    # %% read epochs
    #-----------------------------------------------------------------------------------------            
    # for thisSubject in subjects:
    fileinput = thisSubject +'_DiN_epoched_ICrem.fif'
    
    # read epochs
    epochs = mne.read_epochs(glob(dir_epoched + fileinput)[0])
    
    #Specify conditions and group of conditions to average to: 
    condition_sets = {'corr': ['corr/easy','corr/mid','corr/hard'],
                      'incorr':['incorr/easy','incorr/mid','incorr/hard'],
                       'easy':['corr/easy','incorr/easy'],
                       'mid':['corr/mid','incorr/mid'],
                       'hard':['corr/hard','incorr/hard'],
                       'clear':['corr/clear','incorr/clear']}  
    
    # %% Start report                       
    #-----------------------------------------------------------------------
    
    roi =  ['E55','E54','E61','E62','E79','E78'] # select  some  electrodes for figs
    report = mne.Report(title= 'TIME-AMP summary of ' + thisSubject )
    #report.add_epochs(epochs=epochs, title= fileinput, psd=False, tags = 'allEpochs')  # omit PSD plot. Use this just for the summary table of number of epochs/condition
    eventInfo = str(list(epochs.event_id.items())).replace('(','').replace(')','').replace('\', ' ,'\'=').replace('[','').replace(']','')
    report.add_events(epochs.events,title='EVENTS ' + eventInfo,sfreq=epochs.info['sfreq'], tags='Events')
        
    for set in condition_sets:
        conditions = condition_sets[set]    
        evoked = epochs[conditions].average()
        figname = set + '_evoked'
        report.add_evokeds(evoked,titles = figname , tags= figname) 
        # ERPs 
        #----------------------
        figname = set + '_ERP'
        fig = epochs[conditions].average().plot(gfp = True, spatial_colors=True, titles = figname, show=False,picks = roi, sphere= [0,0,0,14])
        report.add_figure(fig= fig, title = figname, tags = figname)
        del fig
        
        # ERP image
        stat = 'mean'
        figname = set + '_ERP_image_' + stat 
        fig = epochs[conditions].plot_image(combine=stat,title= figname,show=False,picks=roi)
        report.add_figure(fig= fig, title = figname, tags = figname)
    
    report.save(diroutput + '/report_' + thisSubject +'_amplitudes.html', overwrite=True, open_browser = False )        
    
    # %%
    report = mne.Report(title= 'FREQUENCY summary of ' + thisSubject )
    #report.add_epochs(epochs=epochs, title= fileinput, psd=False, tags = 'allEpochs')  # omit PSD plot. Use this just for the summary table of number of epochs/condition
    eventInfo = str(list(epochs.event_id.items())).replace('(','').replace(')','').replace('\', ' ,'\'=').replace('[','').replace(']','')
    report.add_events(epochs.events,title='EVENTS ' + eventInfo,sfreq=epochs.info['sfreq'], tags='Events')
     
    for set in condition_sets:
        conditions = condition_sets[set]    
        # Spectrum per epoch
        #----------------------
        epo_spectrum = epochs[conditions].compute_psd()    
        # add to report 
        fig= epo_spectrum.plot(average=False,picks=roi,show=False,sphere= [0,0,0,14]) 
        figname = set + '_power'
        report.add_figure(fig = fig, title = figname , tags = figname)
        del fig
        
        # topo 
        fig = epo_spectrum.plot_topomap(ch_type='eeg', agg_fun=np.median, show = False)
        figname = set + '_powerTopo'
        report.add_figure(fig = fig, title = figname, tags=figname)
        del fig
    
        # % Time-Frequency 
        # ----------------------------------------
        freqs = np.logspace(*np.log10([1, 48]), num=56)
        n_cycles = freqs / 2.  # different number of cycle per frequency
        power = tfr_morlet(epochs, freqs=freqs, decim= 3, n_cycles=3, average=True, use_fft=True, return_itc=False,n_jobs=4)
        
        # [plot avg of selected channels ]
        stat = 'mean'
        figname = set  + ' \n ' + stat + ' (' + ','.join(roi) + ')'
        fig = power.plot(picks=roi,combine=stat, mode='logratio', title=figname,show = False)
        tagname =  set + '_TimeFreq'
        report.add_figure(fig = fig, title = tagname , tags = tagname)
        del fig
        
    report.save(diroutput + '/report_' + thisSubject +'_frequencies.html', overwrite=True, open_browser = False)                             
     




