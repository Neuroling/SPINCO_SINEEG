#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 08:07:16 2024

@author: testuser
"""


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
evokeds_gAvg_list = list(evokeds_gAvg.values())
#%%
# condition = const.conditions[3]
# fig = mne.viz.plot_evoked_topomap(
#     evokeds_gAvg[condition],
#     vlim = (-1.5,1.5)
#     # times = times_array
#     )

# # times_array = [-0.5, -0.4, -0.3, -0.2, -0.1, 0]

# for condition in const.conditions:
#     #f, axs = plt.subplots(1,10, figsize=(10, 8
#     # plt.figure()
#     fig = mne.viz.plot_evoked_topomap(
#         evokeds_gAvg[condition],
#         # times = times_array
#         )
#     fig.suptitle(f'Topomaps for {condition}')
#     # plt.show()

# for i in range(1, len(const.conditions), 2):
#     const.conditions[i-1]
#     const.conditions[i]

# for condition in const.conditions:
#     fig = evokeds_gAvg[condition].plot()

#%% initiate report
filename = "evoked_grandAverage_topomaps_report.html"
report = mne.Report(title='Grand-Averaged Evoked Topographies')

times_list = np.linspace(-0.5, 0.492, 64)

for condition in const.conditions:
    tags_ = condition.split("/")
    # tags_cond = tags_.copy()
    
    report._add_evoked_topomap_slider(
        evoked = evokeds_gAvg[condition],
        n_time_points=64,
        n_jobs = -1,
        tags = tags_ + ['topomap'], 
        replace=False, 
        topomap_kwargs=None, 
        section = condition,
        image_format = report.image_format,
        ch_types = ['eeg']
        )
    
    report.add_figure(fig = evokeds_gAvg[condition].plot(gfp=True), 
                      section = condition, 
                      title = "electrodes butterfly plot", 
                      tags = tags_ + ['butterfly'])
    
    report.add_figure(fig = evokeds_gAvg[condition].plot_image(), 
                      section = condition, 
                      title = "electrodes image plot", 
                      tags = tags_ + ['image'])
    
report.save(os.path.join(const.diroutput,filename), overwrite=True)

# TODO find a way to do the image plot of correct - incorrect

#%%
"""
Okay so, this code is a mess:
   
    ```
    for condition in const.conditions:
        report._add_evoked_topomap_slider(
            evoked = evokeds_gAvg[condition],
            n_time_points=64,
            n_jobs = -1,
            tags = (condition.split("/"),"topomaps"), 
            replace=False, 
            topomap_kwargs=None, 
            section = condition,
            image_format = report.image_format,
            ch_types = ['eeg']
            )
    ```

because report._add_evoked_topomap_slider() is actually not a function that should be called 
by an end-user. It is a function that is called by report._add_evoked(), which is called by
report.add_evokeds() - so the end-user should be calling report.add_evokeds(), like this:

```
report.add_evokeds(
    evokeds=evokeds_gAvg_list,
    n_time_points=64,
    n_jobs = -1
)
```

and that will add the topomaps with sliders by calling report._add_evoked_topomap_slider().
However: This will also add the evokeds.plot_joint() and a plot of the gfp. There is no option
to opt out of that or remove them from the report (at least not that I could find).
So, if you only want the topomaps with slider, you need to go with either this:
    
```
times_list = np.linspace(-0.5, 0.492, 64)

for condition in const.conditions:
    figures = []
    for timepoint in times_list:
        fig = mne.viz.plot_evoked_topomap(
            evokeds_gAvg[condition],
            times = timepoint,
            vlim = (-1.5,1.5)
            )
        figures.append(fig)
    report.add_figure(fig = figures, 
                      section = condition, 
                      title = condition + " topographies over time", 
                      tags = (condition.split("/"),"topomaps"))
```

which will give you topomaps with sliders without having to go through mne's source code.
But the topomaps look much less nice than they do with report.add_evokeds().

So, if you want the good looking topomaps with slider, you have to go through the source code
and use report._add_evoked_topomap_slider() - this is inconvenient because none of the 
parameters are optional (since they should be given by report.add_evokeds() )
but it works. 

https://github.com/mne-tools/mne-python/blob/maint/1.6/mne/report/report.py#L3495
source code for report._add_evoked_topomap_slider()

"""
#%% Copied from DiN
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
