#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:34:15 2022

@author: gfraga
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:35:32 2022

@author: gfraga
"""

import os
from glob import glob
import scipy.io as sio
import mne 

home = os.path.expanduser("~")

#% Gather Target File info
# %------------------------
basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/evoked/' 

if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
# find target files
files = glob(basedirinput + "*.set", recursive=True)
subjects = [fullpath.split('/')[-1].split('_')[0] for fullpath in files]


# %% 
for fileinput in files:
   # %%
    epochs = mne.io.read_epochs_eeglab(fileinput)
    
    # Relevant event fields
    #mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)
    mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)['EEG']
    # accuracy
    epochAccu = [epoch['accuracy'] for epoch in mdat['epoch']]
    
    # Time adjustment
    epochs.shift_time(mdat['actualTimes']/1000-epochs.times)[0]
    
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
    types = [['corr/clear','corr/easy','corr/mid','corr/hard'],['incorr/clear','incorr/easy','incorr/mid','incorr/hard']]
    difficulty = [['corr/clear','incorr/clear'],['corr/easy','incorr/easy'],['corr/mid','incorr/mid'],['corr/hard','incorr/hard']]
    
    # %%  Creating and saving evoked objects
    
    os.chdir(diroutput)
        
    for events in types:
            eventname = events[0].split('/')[0]
            evoked = epochs[events].average()
            evoked.comment = events[0].split('/')[0]
            outputfilename = fileinput.split('/')[-1].split('_')[0] + '_' + eventname + '-ave.fif'
            mne.write_evokeds(outputfilename, evoked, overwrite=(True))
       
            # %% 
    
    for events in difficulty:
            eventname = events[0].split('/')[1]
            evoked = epochs[events].average()
            evoked.comment = events[0].split('/')[1]
            outputfilename = fileinput.split('/')[-1].split('_')[0] + '_' + eventname + '-ave.fif'
            mne.write_evokeds(outputfilename, evoked, overwrite=(True))
            
    
    allCombos = types[0] + types[1]
    for events in allCombos:
            eventname = events.replace('/','-')
            evoked = epochs[events].average()
            evoked.comment = events
            print(events)
            outputfilename = fileinput.split('/')[-1].split('_')[0] + '_' + eventname + '-ave.fif'
            mne.write_evokeds(outputfilename, evoked,overwrite=(True))
    
    
# % -------------------------------------------------------------------

# %% 

# # Report generation -----
# sfreq = epochs.info['sfreq']
# events = epochs.events
# event_id = epochs.event_id
 
# report = mne.Report(title='my report')
# report.add_epochs(epochs=epochs, title='epochs', psd=True)  
# report.add_events(events=epochs.events, title='Events from "events"', sfreq=sfreq, event_id=epochs.event_id) 
# report.add_evokeds(evokeds=evoked_corr, titles=['EVOKED- Correct'], n_time_points=5)
# report.add_evokeds(evokeds=evoked_incorr, titles=['EVOKED- Incorrect'], n_time_points=5)
# report.add_epochs(epochs=epochs[types[0]], title='epochs corr', psd=True)  
# report.save('report_raw.html', overwrite=True)

 
# # %% 
# # Read/ import data 
# # -----------------------------------------------
# xlist = []
# slist = []
# ylist= []

# for fileinput in files: 
#     #fileinput = 's9_DiN_epoched_ICrem.set'
#     print (fileinput)
#     # Read Epochs in MNE 
#     epochs = mne.io.read_epochs_eeglab(fileinput)
    
       
#     # Relevant event fields
#     #mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)
#     mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)['EEG']
#     # accuracy
#     epochAccu = [epoch['accuracy'] for epoch in mdat['epoch']]
    
#     # degradation levels    
#     epochDeg = [epoch['degBin'] for epoch in mdat['epoch']]
#     epochDeg = [0 if x!=x else x for x in epochDeg] # replace nan by 0 
        
#     # recode events in MNE-read data
#     for epIdx in range(len(epochs.events)):
#         epochs.events[epIdx][2]=epochAccu[epIdx]*10 + epochDeg[epIdx]
#     # add event information 
#     epochs.event_id = {'corr/clear': 10,'corr/easy': 11,'corr/mid': 12,'corr/hard': 13,'incorr/clear': 0,'incorr/easy': 1,'incorr/mid': 2,'incorr/hard': 3}
  
    
#     # Subject info: subject number repeated n trial times 
#     subjectID = fileinput.split('/')[-1].split('_')[0]
 

#     # %% 
#     # VISUALIZATIONS 
#     # ---------------------------------------------------------------------------------------------------
#     #%matplotlib qt5
#     types = [['corr/clear','corr/easy','corr/mid','corr/hard'],['incorr/clear','incorr/easy','incorr/mid','incorr/hard']]
#     difficulty = [['corr/clear','incorr/clear'],['corr/easy','incorr/easy'],['corr/mid','incorr/mid'],['corr/hard','incorr/hard']]
#     preffix = subjectID
    
#     currdiroutput =  diroutput + '/' + subjectID
#     if not os.path.exists(currdiroutput): 
#         os.mkdir(currdiroutput)
    
    
#     # %%
#     # All chans ERP 
#     # =================
#     #epochs[epochSel].average().plot()
#     fig,axs = plt.subplots(2,1)
#     axs = axs.flatten()
#     for e, epochSel in enumerate(types):
#         ep2plot = epochs[epochSel]
#         ep2plot.average().plot(gfp = True, spatial_colors=True, titles = preffix + ' ERP ' + epochSel[0].split('/')[0] ,axes = axs[e])
    
#     # Display full screen 
#     #mng = plt.get_current_fig_manager()
#     #mng.full_screen_toggle()
#     #plt.show()
    
#     # Adjust size and save  
#     Figure = plt.gcf()
#     Figure.set_size_inches(15,15)
#     fname = 'Time_ERP_GFP' + '_' +  subjectID + '.jpg'
#     plt.savefig(fname,dpi=150)
#     plt.close()
    
#     # %% 
#     # All chans ERP  by difficulty
#     # =================
#     #epochs[epochSel].average().plot()
#     fig,axs = plt.subplots(4,1)
#     axs = axs.flatten()
#     for e, epochSel in enumerate(difficulty):
#         ep2plot = epochs[epochSel]
#         ep2plot.average().plot(gfp = True, spatial_colors=True, titles = preffix + ' ERP ' + epochSel[1].split('/')[1] ,axes = axs[e])
    
#     # Display full screen 
#     #mng = plt.get_current_fig_manager()
#     #mng.full_screen_toggle()
#     #plt.show()
    
#     # Adjust size and save  
#     Figure = plt.gcf()
#     Figure.set_size_inches(20,25)
#     fname = 'Time_ERP_GFP_bySNR' + '_' +  subjectID + '.jpg'
#     plt.savefig(fname,dpi=100)
#     plt.close()
    
#     # %% 
#     # GFP only
#     # =================    
#     #fig,axs = plt.subplots(2,1)
#     #axs = axs.flatten()
#     #stat = 'mean'
#     #for e, epochSel in enumerate(types):
#     #     ep2plot = epochs[epochSel]
#     #     ep2plot.average().plot(gfp = 'only', spatial_colors=True, titles = 'GFP ' + epochSel[0].split('/')[0],axes = axs[e])
    
    
#     # %% ERP images 
#     #======================================
#     stat = 'mean'
#     for epochSel in types:
#         ep2plot = epochs[epochSel]
#         ep2plot.plot_image(combine=stat,title= preffix + ' ' + epochSel[0].split('/')[0] + ' trials (' + stat + ')')
        
#         # Adjust size and save  
#         Figure = plt.gcf()
#         Figure.set_size_inches(10,10)
#         fname = 'Time_ERP_img_'+ epochSel[0].split('/')[0] + '_' +  subjectID + '.jpg'
#         plt.savefig(fname,dpi=150)
#         plt.close()   
        
        
#     # %% ERP images by difficulty 
#     #======================================
     
#     stat = 'mean'
    
#     for epochSel in difficulty:
#         ep2plot = epochs[epochSel]
#         ep2plot.plot_image(combine=stat,title= preffix + ' ' + epochSel[0].split('/')[1] + ' trials (' + stat + ')')
        
#         # Adjust size and save  
#         Figure = plt.gcf()
#         Figure.set_size_inches(10,10)
#         fname = 'Time_ERP_img_'+ epochSel[0].split('/')[1] + '_' +  subjectID +  '.jpg'
#         plt.savefig(fname,dpi=150)
#         plt.close()
                
#     # %% Topographies  
#     # =================
#     for timeInterval in ['prestim','postim']:
#         if timeInterval=='prestim':
#             times = np.arange(-0.5, 0, 0.05)
#         elif timeInterval == 'postim':
#             times = np.arange(0, 0.5, 0.05)
#         # %
#         plt.close()
#         fig,axs = plt.subplots(2,11,gridspec_kw={"width_ratios":[3]*len(times)+[1]}, figsize=[25,7])
#         for e,epochSel in enumerate(types):    
#             ep2plot = epochs[epochSel]
#             fig = ep2plot.average().plot_topomap(times, ch_type='eeg',axes=axs[e,:])
#             axs[e,0].set_title(preffix + ' ' + '['+ epochSel[0].split('/')[0]+']' + '\n' + str(times[0]))
#             fig.suptitle('Topographies ' + timeInterval)
                         
#         plt.subplots_adjust(left=0.08, right=0.85, bottom=0.14, top=0.85,hspace=0.5, wspace=0.3)
        
#         # Adjust size and save     
#         fname = 'Time_ERP_topo' + timeInterval + '_' +  subjectID +  '.jpg'
#         plt.savefig(fname,dpi=150)
#         plt.close()   
    
#     # %%  Frequency spec
#     #======================================
#     fig,axs = plt.subplots(2,1)
#     #axs = axs.flatten()
#     for e,epochSel in enumerate(types):
#         evoked = epochs[epochSel].average()
#         evk_spectrum = evoked.compute_psd()
#         evk_spectrum.plot(average=True, axes=axs[e])
#         axs[e].set_title(preffix + ' ' + '['+epochSel[0].split('/')[0]+']' )
#         axs[e].set_ylabel('μV^2/Hz (dB)')
#         axs[e].set_xlabel('Hz')    
#         #evk_spectrum.plot(average=True,axes=axs[e])
#         #evk_spectrum.plot_topomap(ch_type='eeg', agg_fun=np.median,axes=axs[e,e])
    
#     # Adjust size and save  
#     Figure = plt.gcf()
#     Figure.set_size_inches(10,10)
#     fname = 'Freq_PSD_spec' + '_' +  subjectID + '.jpg'
#     plt.savefig(fname,dpi=150)
#     plt.close()
    
#      # %%  Frequency topopgraphies
#     #======================================
#     fig,axs = plt.subplots(2,5,gridspec_kw={"width_ratios":[3]*5}, figsize=[25,7])
#     #axs = axs.flatten()
#     for e,epochSel in enumerate(types):
#         evoked = epochs[epochSel].average()
#         evk_spectrum = evoked.compute_psd()
#         evk_spectrum.plot_topomap(ch_type='eeg', agg_fun=np.median,axes=axs[e,:])
#         axs[e,0].set_title(preffix + ' ' +'['+epochSel[0].split('/')[0]+']' + '\n' + 'delta (0-4 Hz)')
#         #axs[e].set_title('['+epochSel+']' )
#         #axs[e].set_ylabel('μV^2/Hz (dB)')
#         #axs[e].set_xlabel('Hz')    
#         #evk_spectrum.plot(average=True,axes=axs[e])
#         #evk_spectrum.plot_topomap(ch_type='eeg', agg_fun=np.median,axes=axs[e,e])
#         plt.subplots_adjust(left=0.08, right=0.85, bottom=0.14, top=0.85,hspace=0.5, wspace=0.3)
    
#     # Adjust size and save  
#     Figure = plt.gcf()
#     Figure.set_size_inches(10,10)
#     fname = 'Freq_PSD_topo' + '_' +  subjectID + '.jpg'
#     plt.savefig(fname,dpi=150)
#     plt.close()
    
#     # %%
#     plt.close('all')
    


# # # %%
# # # #%matplotlib 
# # # evokeds = dict(corr=list(epochs['correct'].iter_evoked()),
# # #                incorr=list(epochs['incorrect'].iter_evoked()))

# # # meanCorr = epochs['correct'].average()
# # # meanIncorr = epochs['incorrect'].average()

# # # #for evk in (meanCorr, meanIncorr):
# # #  #   evk.plot(gfp=True, spatial_colors=True)

# # # diffs = mne.combine_evoked([meanCorr,meanIncorr], weights=[1, -1])
# # # diffs.plot_joint()
# # # #mne.viz.plot_compare_evokeds(evokeds, combine='mean')



# # # %% 
# # #       ep2plot.average().plot_topomap(times, ch_type='eeg',axes=axs[e*i])

# # # %% 
# # # Epochs mean all chans 
# # #[epochs[epochSel].plot_image(combine=stat,title= epochSel + ' trials (' + stat + ')') for epochSel in ['correct','incorrect']]

# # #% SAVE THIS SECTION COMMENTED FOR FURTHER DEVELOPMENTS .... 
# # # Visualize data 
# # stat = 'mean'
# # fig,axs = plt.subplots(3,2)
# # for e,epochSel in enumerate(['correct','incorrect']):    
# #     ep2plot = epochs[epochSel]
# #     ep2plot.plot_image(combine=stat,title= epochSel + ' trials (' + stat + ')',axes=axs[e,:]) 
            
# # #plt.subplots_adjust(left=0.01, right=0.975, bottom=0.14, top=0.85,hspace=0.5, wspace=0.3)

# # # %%
# # # epochs[epochSel].average().plot()


# # # %%













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


 