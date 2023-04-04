# -*- coding: utf-8 -*-
""" Catch trials
    =================================================================
 - Quickly preprocess Gorilla files and get info about accuracy in catch trials 
 

Created on Wed Feb  8 15:18:30 2023
@author: gfraga

"""
import os  # Commands to remember: os.getcwd(), os.listdir() 
import pandas as pd
import glob
import sys as sys 
import seaborn as sns
import re 
import numpy as np
import matplotlib.pyplot as plt        

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
    
    #Rename variable to use as subject id
    dat.rename(columns={'Participant Private ID':'SubjectID'}, inplace=True)
    dat.SubjectID = pd.Series(dat.SubjectID,dtype="object")

    # %
    # Leave rows with trial response(always the one after 'audio play requested')
    idx_resp = dat.index[(dat.Response == 'AUDIO PLAY REQUESTED')] + 1    
    df = dat.iloc[idx_resp]
    df = df[df.display.str.contains('catch')]
    
    
    # Replace Correct responses of 'miss' trials by NAs
    df.loc[df['Timed Out']==1,'Correct'] = 'miss'
    df.loc[df['Timed Out']==1,'Reaction Time'] = np.nan      
    df['Reaction Time'] = df['Reaction Time'].astype('float64')
    df.rename(columns={'Trial Number': 'trial'}, inplace=True)    

    df.rename(columns={'Task Name': 'task'}, inplace=True)    
    df.rename(columns={'Reaction Time': 'RT'}, inplace=True)    
    df.rename(columns={'Timed Out': 'Miss'}, inplace=True)    
    df.rename(columns={'Correct': 'Accuracy'}, inplace=True)    
     
    df['task'] = df['task'].str.replace('SINON_task_','')
    
    # recode blocks for clarity in plots (1 and 2 value only)
    df.loc[:,'block'] = df['block'].replace({1:1,2.0:1,3.0:2,4.0:2})     
    df = df.loc[:,['SubjectID','task','set','block','trial','Accuracy','RT']]
    
    #Reset index 
    df = df.reset_index(drop=True)
    
    # %%  STATS
    names = ['SubjectID','task', 'block','Accuracy']
    # accuracy summary    
    accu = df.groupby(names)['trial'].agg(['count']).reset_index()
    accu['propTrials'] = round(accu['count']/(len(df)/2),ndigits=2)
    
    #Fix header (join by '-')
    rts = df.groupby(names)[['RT']].agg(['mean', 'std']).reset_index()
    rts.columns  =  ['_'.join(i) if len(i[1]) else ''.join(i) for i in rts.columns.tolist() ]
    
    df_summary = pd.merge(accu, rts, on=names)

    # % Expand with all combinations of the variables 
    unique_categories = [df_summary[col].unique() for col in names]    
    multiindex = pd.MultiIndex.from_product(unique_categories, names=names)
    
    # reindexing
    df_summary = (df_summary
                 .set_index(names) 
                 .reindex(multiindex,fill_value= '')
                 .reset_index())
    

    df_summary['SubjectID'] = df_summary['SubjectID'].astype('object')
    df_summary['block'] = df_summary['block'].astype('object')
   
    # save 
    df_summary.to_csv(fileinput.replace('.csv','_CatchStats.csv'), index = False)         

    # %%  PLOTs
    #----------------------------------------------------------------
    plt.close('all')
    df = df.block.replace({1.0:'b1',2.0:'b2'})
    
    d2plot = df_summary[df_summary['Accuracy'] == 1].copy()
    g = sns.FacetGrid(d2plot)
    g.map(sns.pointplot, "block","propTrials",palette="Set2")
    #g.map(sns.barplot)
    g.refline(y = 0.5,color = "gray",lw = 1, linestyle='--')
    g.add_legend()
    g.fig.suptitle(os.path.basename(fileinput).replace('.csv',''))
    
    # Save figure    
    g.savefig(fileinput.replace('.csv','_CatchStats.jpg'))


    # %%
    plt.close('all')
       
    d2plot = df_summary[df_summary['Accuracy'] == 1].copy()
    g = sns.FacetGrid(d2plot)
    g.map(sns.pointplot, "block","RT_mean",palette="Set2")
    #g.map(sns.barplot)
    g.add_legend()
    g.fig.suptitle(os.path.basename(fileinput).replace('.csv',''))
    
    # Save figure    
    g.savefig(fileinput.replace('.csv','_CatchStats_RT.jpg'))


    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
