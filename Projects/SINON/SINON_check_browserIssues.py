# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:47:12 2023

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
import numpy as np
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
 

# %%
for i,fileinput  in enumerate(validfiles):
    
    
    dat = pd.read_csv(fileinput)
    
    
    times = dat['Reaction Time'].unique()
    
    if 'LOADING DELAY' in times:
                print('>>>>>>>>>>>>> DETECTED DELAY IN ' + fileinput)
                print(i)
                
                count = np.sum(times == 'LOADING DELAY')
               