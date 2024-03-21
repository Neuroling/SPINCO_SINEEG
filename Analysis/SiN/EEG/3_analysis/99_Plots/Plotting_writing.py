#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 08:07:16 2024

@author: testuser
"""

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

import os
from glob import glob
import mne
import pickle

import Plotting_constants as const
from Plotting_functions import PlottingManager
PlottingManager = PlottingManager()

#%% get evokeds
evokeds = PlottingManager.get_evokeds()
evokeds_gAvg = PlottingManager.grandaverage_evokeds(evokeds)

# # times_array = [-0.5, -0.4,-0.3,-0.2,-0.1,0]

# for condition in const.conditions:
#     #f, axs = plt.subplots(1,10, figsize=(10, 8
#     # plt.figure()
#     fig = mne.viz.plot_evoked_topomap(
#         evokeds_gAvg[condition],
#         # times = times_array
#         )
#     fig.suptitle(f'Topomaps for {condition}')
#     # plt.show()

#%% initiate report
filename = "evoked_grandAverage_topomaps_report.html"
report = mne.Report(title='Grand-Averaged Evoked Topographies')
# roi =  ['E55','E54','E61','E62','E79','E78'] # select  some  electrodes for figs

times_list = np.linspace(-0.5, 0.492, 64)

for condition in const.conditions:
    #f, axs = plt.subplots(1,10, figsize=(10, 8
    # plt.figure()
    figures = []
    for timepoint in times_list:
        fig = mne.viz.plot_evoked_topomap(
            evokeds_gAvg[condition],
            times = timepoint
            )
        figures.append(fig)
    report.add_figure(fig = figures, title = condition)
    # plt.show()

# report.add_evokeds(
#     evokeds=evokeds_gAvg,
#     n_time_points=64,
#     n_jobs = -1
# )

report.save(os.path.join(const.diroutput,filename), overwrite=True)

#%%
# # Add GROUP ERP all conditions
# fig = mne.viz.plot_compare_evokeds(evokeds,
#                              combine='mean',
#                              legend='lower right',
#                              picks=roi, show_sensors='upper right',
#                              #colors=color_dict,
#                              #linestyles=linestyle_dict,
#                              title='comp',
#                              sphere = [0,0,0,12],
#                              truncate_xaxis=False,
#                              show = False
#                             )

# figname = 'Group_ERPs'
# report.add_figure(fig= fig, title = figname, tags = figname)
# # Add plots per condition 
# for cond in evokeds.keys():    
#     GA = mne.grand_average(evokeds[cond])
    
#     figname =  cond + '_' + GA.comment.replace('Grand average ' ,'').replace('(n = ', '').replace(')','ss')
#     report.add_evokeds(GA,titles = figname,tags = figname)
#     #fig = GA.plot(gfp = True, spatial_colors=True, titles = figname, show=False,picks = roi, sphere= [0,0,0,14])
#     #report.add_figure(fig = fig, title = figname , tags = figname)    

# # Add code and save     
# report.add_code(code=Path(os.path.abspath(__file__)),title="Code from Path",tags = "code") 
# report.save(diroutput + '/report_group_timeAmp.html', overwrite=True, open_browser = False )        
