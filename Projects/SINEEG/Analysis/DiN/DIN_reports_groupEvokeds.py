#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 10:17:00 2022

@author: gfraga
"""
import mne
import os
import numpy as np
import pandas as pd
from glob import glob
import scipy.io as sio
import pickle
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt 
from mne.stats import permutation_cluster_1samp_test as pcluster_test
from pathlib import Path
# dirs 
dirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/group/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/group/' 
os.chdir(dirinput)
# Read dictionaries with evokeds per subject
evokeds = pickle.load(open(dirinput + '/groupEvoked','rb' ))
powers = pickle.load(open(dirinput + '/groupPower','rb' ))
tfrs = pickle.load(open(dirinput + '/groupTFR','rb' ))  

# %% TIME AMPLITUDE AVERAGE 
###################################################################################
report = mne.Report(title='Group ERPs')
roi =  ['E55','E54','E61','E62','E79','E78'] # select  some  electrodes for figs

# Add GROUP ERP all conditions
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
# Add plots per condition 
for cond in evokeds.keys():    
    GA = mne.grand_average(evokeds[cond])
    
    figname =  cond + '_' + GA.comment.replace('Grand average ' ,'').replace('(n = ', '').replace(')','ss')
    report.add_evokeds(GA,titles = figname,tags = figname)
    #fig = GA.plot(gfp = True, spatial_colors=True, titles = figname, show=False,picks = roi, sphere= [0,0,0,14])
    #report.add_figure(fig = fig, title = figname , tags = figname)    

# Add code and save     
report.add_code(code=Path(os.path.abspath(__file__)),title="Code from Path",tags = "code") 
report.save(diroutput + '/report_group_timeAmp.html', overwrite=True, open_browser = False )        

# %% 
#for cond in powers.keys():
  #  GA = 
 #   figname =  cond + '_' + GA.comment.replace('Grand average ' ,'').replace('(n = ', '').replace(')','ss')
  #  report.add_evokeds(GA,titles= figname,tags = figname)  
#report.save(diroutput + '/report_group_timeFreqs.html', overwrite=True, open_browser = False )        

# %% TIME FREQUENCY  
###################################################################
plt.ioff()
report = mne.Report(title='Group TFRs')
for cond in tfrs.keys():        
    GA = mne.grand_average(tfrs[cond])
    # Time-Frequency power changes  ------------------------------------------------
    # add to report  
    # [plot avg of selected channels ]
    stat = 'mean'
    figname =  cond + '_' + GA.comment.replace('Grand average ' ,'').replace('(n = ', '').replace(')','ss')    
    fig = GA.plot(picks=roi,
                  combine=stat, 
                  mode='logratio', 
                  title=figname + ' (' + ', '.join(roi) + ')',
                  show = False)
    tagname =  cond + '_TimeFreq'
    report.add_figure(fig = fig, title = tagname , tags = tagname)    
    
    
    # % Topo plots per freq band ----------------------        
    fig, axes = plt.subplots(1, 4, figsize=(13,3))
    topomap_kw = dict( tmin=0.5, tmax=1.5, 
                      #baseline=(None, 0),
                      mode='logratio',
                      show=False)
    
    
    freqBand_dict = dict(Delta = dict(fmin = 0.5, fmax = 4),
                    Theta = dict(fmin = 4, fmax = 8),
                     Alpha=dict(fmin=8, fmax=13), 
                     Beta=dict(fmin=13, fmax=25))
    
    for ax, (title, fmin_fmax) in zip(axes, freqBand_dict.items()):
        GA.plot_topomap(**fmin_fmax, axes=ax, **topomap_kw,sphere=[0,0,0,14])
        ax.set_title(title) 

   
    figname =  cond + '_freqTopo'
    report.add_figure(fig = fig, title = figname , tags = figname)    
    
# %

# % LINE plots showing power changes over time per band  ---------------------        
df_tfrs = []
for cond in tfrs.keys():        
    GA = mne.grand_average(tfrs[cond])
    df = GA.to_data_frame(time_format=None, long_format=True)
    # Map to frequency bands:
    freq_bounds = {'_': 0,
                   'delta': list(freqBand_dict['Delta'].values())[1],
                   'theta': list(freqBand_dict['Theta'].values())[1],
                   'alpha': list(freqBand_dict['Alpha'].values())[1],
                   'beta': list(freqBand_dict['Beta'].values())[1],
                   'gamma': 48}
    df['band'] = pd.cut(df['freq'], list(freq_bounds.values()),
                        labels=list(freq_bounds)[1:])
    
    # Filter to retain only relevant frequency bands:
    freq_bands_of_interest = ['delta', 'theta', 'alpha', 'beta']
    df = df[df.band.isin(freq_bands_of_interest)]
    df['band'] = df['band'].cat.remove_unused_categories()
    
   
    
    # Add condition label and append to the main df
    df['condition'] = cond
    df_tfrs.append(df)
    
df_tfrs = pd.concat(df_tfrs) # bind list into single data frame 

# % 
# Select channels in data set 
df2plot =  df_tfrs.loc[df_tfrs.channel.isin(roi)]    
ylabel = str(GA.__class__).split('.')[-1].replace('\'>','')

# % 
plt.close('all')
g = sns.FacetGrid(df2plot, row='band', margin_titles=True)
g.map(sns.lineplot, 'time', 'value', 'condition', n_boot=10)  
axline_kw = dict(color='black', linestyle='dashed', linewidth=0.5, alpha=0.5)
g.map(plt.axhline, y=0, **axline_kw)
g.map(plt.axvline, x=0, **axline_kw)
g.set(ylim=(None, None))
g.set_axis_labels("Time (s)", ylabel)
g.set_titles(col_template="{col_name}", row_template="{row_name}")
g.add_legend(ncol=1, loc='upper right')
g.fig.subplots_adjust(left=0.1, right=0.7, top=0.9, bottom=0.08)
g.fig.suptitle(ylabel  +' (' + ', '.join(roi) + ')')
# We can only add matplot fig object to report ...
plt.show()
fig = matplotlib.pyplot.gcf()
plt.close('all')

# save  
figname = 'Mean_TFR'
report.add_figure(fig = fig, title = figname , tags = figname)      

#  add code and save 
report.add_code(code=Path(os.path.abspath(__file__)),title="Code from Path",tags = "code") 

# %
report.save(diroutput + '/report_group_timeFreq.html', overwrite=True, open_browser = False )            
     
    
    
    
    





     