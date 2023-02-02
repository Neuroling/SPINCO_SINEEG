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
import plotly.io as io
import matplotlib.pyplot as plt        
import re
# %% 
# Fix for issue with spyder not showing plotly 
io.renderers.default='browser'
# %% 
# paths
if sys.platform=='linux':  basedir  = '/home/d.uzh.ch/gfraga/smbmount/'
else:  basedir ='V:/'

# Add custom functions 
sys.path.append(basedir + 'gfraga/scripts_neulin/Projects/SINON/')
from functions import multiplot_lines,multiplot_lines_scatter,multiplot_rainclouds,gorilla_out_preproc,gorilla_out_summary

dirinput =  basedir + 'spinco_data/SINON/outputs/data_exp_116083-v1/gathered'

# %% find relevant files (Files have a number id before the extension. This is used in the reg exp matching)

validfiles= [files for files in glob.glob(dirinput + '/**/*.csv' ,recursive=True) if 'gathered/Concat' not in files and re.search(r'\d+\.csv', files)] # find files for each subject in subfolder


 
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
    (accu,rt) = gorilla_out_summary(df)
    
    # SAVE 
    #------
    # Tables 
    df.to_csv(df.task.unique()[0] + '-PREPROC.csv', index = False)
    accu.to_csv(df.task.unique()[0] + '-ACCU.csv', index = False)
    rt.to_csv(df.task.unique()[0] + '-RT.csv', index = False)    
    
    print('---<< done preprocessing ' +  fileinput +'. \n' )
    #del dat, df, accu, rt

    # % PLOTs
    #----------------------------------------------------------------
    # Accuracy plots 
    xvar = 'LV' ; yvar = 'prop_hits'; yvar2='count_miss' ; zvar= 'block' ; facet_var = 'TYPE' # here column that defines different plots /facets
    data = accu
    multi_title = df.task.unique()[0] + ' Accuracy (n ' + str(len(accu.SubjectID.unique())) +')'
    fi1= multiplot_lines_scatter(data,xvar,yvar,yvar2, zvar,facet_var,multi_title)
    
    # %
    # RT plots
    xvar = 'LV'; yvar = 'mean'; zvar= 'block'; facet_var = 'TYPE' # here column that defines different plots /facets
    data = rt
    multi_title= df.task.unique()[0] + ' RT (n ' + str(len(rt.SubjectID.unique()))+')'
    fi2 = multiplot_lines(data, xvar, yvar, zvar, facet_var,multi_title)
    
    # Save figures    
    outputsuffix = df.task.unique()[0] + '.jpg' 
    fi1.savefig('FIG_lin_accu_' + outputsuffix)
    fi2.savefig('FIG_lin_rt_' + outputsuffix)
    
    plt.close('all')
# %% 
# # % Rain cloud
# xvar = 'LV'; yvar = 'Reaction Time'; zvar= 'block'; 
# facet_var = 'TYPE' ; facet_var2 = 'block' 
# data = df.loc[(df['Correct']==1.0),]
# multi_title='RTs '
# ort="v";
# color_pals=['mako','rocket']
# fi3 = multiplot_rainclouds(data,xvar,yvar,zvar,facet_var,facet_var2,multi_title,color_pals,ort)
   

   
# # %% RTs per block and per correct/incorrect responses
# # blocks2plot = df.block.unique()
# fi4= sns.catplot(data=df, x="LV", y="Reaction Time", hue="Correct", 
#     kind="violin",split=True,title='RTs per Block and correctness',col='TYPE',row='block',
#     inner='stick',palette='pastel')


#     #%% 
   
    #fi3.savefig('FIG_rain_rt_' + fileinput.replace('.csv','.jpg'))
    #fi4.savefig('FIG_vio_rt_' + fileinput.replace('.csv','.jpg'))
    
    
    










