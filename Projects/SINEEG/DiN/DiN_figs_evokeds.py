#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: gfraga
"""

import os
from glob import glob
import scipy.io as sio
import mne 

home = os.path.expanduser("~")

#% Gather Target File info
# %------------------------
basedirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/evoked' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/evokeds' 

if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
# find target files

os.chdir(basedirinput)
# %% 
files = glob('*ave*.fif')  
#print(files)
subjects = set([fullpath.split('/')[-1].split('_')[0] for fullpath in files])
# %% 
#conditions = ['clear','easy','mid','hard','corr','incorr']
conditions = ['clear','easy','mid','hard','corr','incorr']
evokeds = {} # evokeds will be a dictionary with each condition as a key,each key having all files for a given condition
for c in conditions:
    files = glob('*_' + c+'-ave*.fif')  
    evokeds[c] = [mne.Evoked(d) for d in files]
    chanLabels = mne.Evoked(files[0]).ch_names
    #del files
 
# save dictionary with evoked objects     
mne.write_evokeds(diroutput + '/group_evokeds.fif', evokeds)


# %%  PLOTS
import matplotlib.pyplot as plt
plt.close('all')

# % ERP WAVE 

#roi = ['E45', 'E40', 'E46','E39', 'E38']
roi =  ['E55','E54','E61','E62','E79','E78']
mne.viz.plot_compare_evokeds(dict((k, evokeds[k]) for k in ('clear', 'easy','mid','hard')),
                             combine = 'mean', 
                             vlines = [0, 1],
                             legend='lower right',
                             picks = roi, 
                             show_sensors = False,
                             #colors = color_dict,
                             #linestyles=linestyle_dict,
                             title = 'Group ERPs. Chans ' + str(roi),
                             truncate_xaxis=False
                             )
plt.savefig('ERP_group.jpg',dpi=350)                          
plt.close()
 


# %% TOPOGRAPHIES 
os.chdir(diroutput)

import matplotlib.pyplot as plt
plt.close('all')
import numpy as np

times = np.arange(0.10, 0.350, 0.01)
for con in conditions:
    grandAvg = mne.grand_average(evokeds[con])                  
    # animated 
    fig, anim = grandAvg.animate_topomap(vmin=-1.5, vmax=1.5,
        times=times, ch_type='eeg', frame_rate=3, blit=False,butterfly=True,image_interp='cubic',show=False,sphere=[0,0,0,15])
        
    anim.save('TopoAnim_' + con + '.gif')
    plt.close()
    
    # static
    staticTimes = np.arange(0.10, 0.350, 0.05)
    
    mne.viz.plot_evoked_topomap(grandAvg,vmin=-1.5, vmax=1.5, 
                                times=staticTimes, average=0.025, 
                                title= 'Group Average ' + con ,
                                size=2, 
                                sphere= [0,0,0,15]
                               )
    plt.savefig('Topo_' + con + '.jpg',dpi=150)
    plt.close()
    
    
# %%

#plt.y('μV^2/Hz (dB)')
#plt.set_xlabel('Hz')    
 

# Adjust size and save   


    # Adjust size and save  
   # Figure = plt.gcf()
   # Figure.set_size_inches(10,10)
   # fname = 'Time_ERP_img_'+ epochSel[0].split('/')[1] + '_' +  subjectID +  '.jpg'
   # plt.savefig(fname,dpi=150)
   # plt.close()
              

    
 # %% 

# # Report generation -----
# sfreq = epochs.info['sfreq']
# events = epochs.events
# event_id = epochs.event_id
 
# report = mne.Report(title='my report')
# report.add_epochs(epochs=epochs, title='epochs', psd=True)  
# report.add_events(events=epochs.events, title='Events from "events"', sfreq=sfreq, event_id=epochs.event_id) 
# report.add_evokeds(evokeds=evoked_corr, titles=['EVOKED- Correct'], n_time_points=5)
# report.add_evokeds(evokeds=evoked_incorr, titles=['EVOKED- Incorrec1t'], n_time_points=5)
# report.add_epochs(epochs=epochs[types[0]], title='epochs corr', psd=True)  
# report.save('report_raw.html', overwrite=True)
 