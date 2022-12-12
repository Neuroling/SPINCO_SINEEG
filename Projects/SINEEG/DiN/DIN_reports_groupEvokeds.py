#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 10:17:00 2022

@author: gfraga
"""
import mne
import os
from glob import glob
import scipy.io as sio
import pickle
import matplotlib.pyplot as plt 
# dirs 
dirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/reports_group/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/reports_group/' 
os.chdir(dirinput)
# Read dictionaries with evokeds per subject
evokeds = pickle.load(open(dirinput + '/groupEvoked','rb' ))

# %%  START report

report = mne.Report(title='Group ERPs')
roi =  ['E55','E54','E61','E62','E79','E78'] # select  some  electrodes for figs

# Add ERPs 
fig = mne.viz.plot_compare_evokeds(evokeds,
                             combine='mean',
                             legend='lower right',
                             picks=roi, show_sensors='upper right',
                             #colors=color_dict,
                             #linestyles=linestyle_dict,
                             title='comp',
                             sphere = [0,0,0,12],
                             truncate_xaxis=False,
                             show = False
                            )

figname = 'Group_ERPs'
report.add_figure(fig= fig, title = figname, tags = figname)

# 

for cond in evokeds.keys():
    GA = mne.grand_average(evokeds[cond])
    figname =  cond + '_' + GA.comment.replace('Grand average ' ,'').replace('(n = ', '').replace(')','ss')
    report.add_evokeds(GA,titles= figname,tags = figname) 
    
    
report.add_evokeds(GA, )     
report.save(diroutput + '/report_group_amplitudes.html', overwrite=True, open_browser = False )        







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
 



