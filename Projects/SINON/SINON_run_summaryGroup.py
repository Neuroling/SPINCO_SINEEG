# -*- coding: utf-8 -*-
#%reset -f #clear all ? 
"""
Created on Mon Oct 10 10:04:55 2022
@author: gfraga

"""
import os  # Commands to remember: os.getcwd(), os.listdir() 
import pandas as pd
import glob
import sys as sys
import seaborn as sns
import matplotlib.pyplot as plt        

# %% 
# paths
if sys.platform=='linux':  basedir  = '/home/d.uzh.ch/gfraga/smbmount/'
else:  basedir ='V:/'

# Add custom functions 
sys.path.append(basedir + 'gfraga/scripts_neulin/Projects/SINON/')
from functions import multiplot_lines,multiplot_lines_scatter,multiplot_rainclouds,gorilla_out_preproc,gorilla_out_summary

dirinput =  basedir + 'spinco_data/SINON/outputs/data_exp_116083-v1/preprocessed'

# %% Find files with stats 

files = glob.glob(dirinput + '/**/*_stats.csv' ,recursive=True)

#Read files of this taks and concatenate
dfs = [pd.read_csv(fileinput) for fileinput in files]
concat_df = pd.concat(dfs, axis=0)    
#concat_df['SubjectID'] = concat_df['SubjectID'].astype('object')
#concat_df['block'] = concat_df['block'].astype('object')    
#concat_df['LV'] = concat_df['LV'].astype('object')    
concat_df.Accuracy = concat_df.Accuracy.replace('1.0','1').replace('0.0','0').replace(0.0,'0').replace(1.0,'1')

# %%
os.chdir(dirinput)
for currTask in concat_df.task.unique():
    concat_df = concat_df[concat_df['Accuracy']=='1']
    
    plt.close('all')
    d2plot = concat_df[concat_df['task']== currTask]
    
    g = sns.FacetGrid(d2plot, col="TYPE",  row="SubjectID")
    g.map(sns.lineplot, 'LV','propTrials','block',palette='Set2')
    g.map_dataframe(sns.lineplot, x ='LV',y=0.5, color='gray',linestyle='dotted')
    g.map_dataframe(sns.scatterplot, x='LV', y='propTrials', marker='o', hue='block',palette='Set2')
    #g.map_dataframe(sns.lineplot, x='LV', y='propTrials', marker='o')
    g.add_legend()
    g.fig.suptitle(currTask)


    # ssave     
    g.savefig('FIG_' + currTask + '_stats.jpg')

 
