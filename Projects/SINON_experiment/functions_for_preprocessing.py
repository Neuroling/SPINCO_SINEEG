#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 10:25:33 2022

@author: gfraga
"""
def preprocess_gorilla_output(dat):
    import pandas as pd
    import numpy as np 
    
    dat = dat.iloc[:,(dat.columns.get_loc('Checkpoint')  + 1): len(dat.columns)] #discard some initial cols
    
    # find rows with response(rows following 'audio play requested')
    idx_resp = dat.index[(dat.Response == 'AUDIO PLAY REQUESTED') & (dat.display!= 'example')] + 1
    
    df = dat.iloc[idx_resp]
    
    # Replace Correct responses of 'miss' trials by NAs
    df.loc[df['Timed Out']==1,'Correct'] = np.nan
    df.loc[df['Timed Out']==1,'Reaction Time'] = np.nan
    
    #  Additional info (type, LV) from parts of Audiofile name
    df.insert(2,"STIM",df[np.unique(df.list)]) # audio presented for this subject
    df.insert(2,"TYPE",df['STIM'].str.split('norm').str[0].str.split('_').str[0])
    df.insert(2,"LV",df['STIM'].str.split('norm').str[1].str.replace('_','').str.replace('.wav','')) # use string split from filenames
    df['LV'].replace({'-10db': '1','-5db': '2', '0db': '3', '5db': '4','10db': '5',\
                       '4chans': '1','5chans': '2', '6chans': '3', '7chans': '4','8chans': '5' }, inplace=True)
        
    df['block'] = pd.Categorical(df.block)    
    df['LV'] = pd.Categorical(df.LV)    
    df.dtypes
    
 
    # recode blocks for clarity in plots (1 and 2 value only)
    df.loc[:,'block'] = df['block'].replace({1:1,2.0:1,3.0:2,4.0:2}) 
    
    return (df)


def describe_gorilla_output(df):
    import pandas as pd     
    
    # DESCRIPTIVE STATS 
    #----------------------------------------------------------------
    nreps = len(df.loc[(df['block']==1) & (df['LV']=='1') & (df['TYPE']=='NV')])   # Check number of trials per degradation level in a block 

    ## Summarize accuracy 
    dv= 'Correct'
    #one block    
    means = df.groupby(['block','TYPE','LV'])[dv].describe().reset_index()           
    proportions = df.groupby(['block','TYPE','LV'])[dv].sum().reset_index()
    proportions['Correct'] = proportions[dv]/nreps     
    
    #both blocks
    meansAllBlocks = df.groupby(['TYPE','LV'])[dv].describe().reset_index()
    meansAllBlocks.insert(0,'block','all')
    proportionAllBlocks = df.groupby(['TYPE','LV'])[dv].sum().reset_index()
    proportionAllBlocks['Correct'] = proportionAllBlocks[dv]/(nreps*2) # assumes 2 blocks per type of noise      
    proportionAllBlocks.insert(0,'block','all')
      
    # merge descriptives
    accu = pd.merge(pd.concat([means,meansAllBlocks]),pd.concat([proportions,proportionAllBlocks]))
    accu.rename({dv:'prop_hits'},axis='columns',inplace=True)
    accu.insert(4,'count_miss', nreps-accu['count'])
    accu.loc[accu['count']>nreps,'count_miss']  =  (nreps*2) - accu[accu['count']>nreps]['count']
    #accu.loc[:,'block'] = accu['block'].replace({1:1,2.0:1,3.0:2,4.0:2}) # recode blocks for clarity in plots (1 and 2 value only)
    accu['block'] = pd.Categorical(accu.block)    
     
    del dv,means,meansAllBlocks
    # Summarize Reaction Time 
    dv= 'Reaction Time'
    means = df.groupby(['block','TYPE','LV'])[dv].describe().reset_index()           
    meansAllBlocks = df.groupby(['TYPE','LV'])[dv].describe().reset_index()
    meansAllBlocks.insert(0,'block','all')
    
      
    # merge descriptives
    rt = pd.concat([means,meansAllBlocks])
    rt.insert(4,'count_miss', nreps-rt['count'])
    rt.loc[rt['count']>nreps,'count_miss']  =  (nreps*2) - rt[rt['count']>nreps]['count']
 
    return (accu,rt)