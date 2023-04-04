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
#import plotly.io as io
import matplotlib.pyplot as plt        
import seaborn as sns
import re
# %% 
# Fix for issue with spyder not showing plotly 
#io.renderers.default='browser'
# %% 
# paths
if sys.platform=='linux':  basedir  = '/home/d.uzh.ch/gfraga/smbmount/'
else:  basedir ='V:/'
# Add custom functions 
sys.path.append(basedir + 'gfraga/scripts_neulin/Projects/SINON/')
from functions import multiplot_lines,multiplot_lines_scatter,multiplot_rainclouds,gorilla_out_preproc,gorilla_out_summary
dirinput =  basedir + 'spinco_data/SINON/outputs/data_exp_116083-v1/preprocessed'

# %% find relevant files (Files have a number id before the extension. This is used in the reg exp matching)
validfiles= [files for files in glob.glob(dirinput + '/**/*.csv' ,recursive=True) if 
             'gathered/Concat' not in files and re.search(r'\d+\.csv', files)] # subject files here have a digit before extension 
 

# %%  Summary per subject
for fileinput in validfiles: 
    #fileinput = validfiles[0]
    
    os.chdir(os.path.dirname(fileinput))
    print('[-_-] >>>> Start ' +  fileinput )
    
    # %  DATA PREP
    #----------------------------------------------------------------
    # read data, select columns
    dat = pd.read_csv(fileinput)         
    
    # Preprocessing 
    df = gorilla_out_preproc(dat)        
    
    #descriptive statistics
    df_summary = gorilla_out_summary(df)
    
    # SAVE 
    #------------------------------------------------------------------
    # Tables 
    df_summary.to_csv(fileinput.replace('.csv','_stats.csv'), index = False)    
    
    print('---<< done preprocessing and summary ' +  fileinput +'. \n' )
    #del dat, df, accu, rt

    # %%  PLOTs
    #----------------------------------------------------------------
    plt.close('all')
    d2plot = df_summary[df_summary['Accuracy'] == 1].copy()
    g = sns.FacetGrid(d2plot, col="TYPE")
    g.map(sns.pointplot, "LV", "propTrials", "block",palette="Set2")
    g.map(sns.lineplot)
    g.refline(y = 0.5,color = "gray",lw = 1, linestyle='--')
    g.add_legend()
    g.fig.suptitle(os.path.basename(fileinput).replace('.csv',''))
    
    # Save figure    
    g.savefig(fileinput.replace('.csv','_stats.jpg'))


    










