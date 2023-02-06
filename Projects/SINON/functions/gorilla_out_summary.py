#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def gorilla_out_summary(df):
    """ Summarize Gorilla's output 
    =================================================================
    Created on Fri Oct 14 10:25:33 2022
    @author: gfraga
    
    Parameters
    ----------
    df: data frame
        preprocessed data frame with task performance. Expects multiple subjects        
        
    Returns
    -------
    accu: data frame
        data frame with a summary of accuracy per subject, block, etc
    rt:
        data frame wtih a summary of reaction times per subject,block, etc
    
    """ 
    import pandas as pd     
    
    # DESCRIPTIVE STATS 
    #----------------------------------------------------------------
    nblocks = 2 
    nreps = len(df.trial.unique()) / (nblocks*len(df.LV.unique()) * len(df.TYPE.unique()))   #  number of trials per degradation level in a block (changes across tasks)
    
    # %% 
    counts = df['TYPE'].value_counts()
    for level, count in counts.iteritems():
        
        print(df[df['TYPE']=='NV'].LV.value_counts())
        print(df[df['TYPE']=='SiSSN'].LV.value_counts())

    
    # %% Summarize accuracy 
    grouped = df.groupby(['SubjectID', 'block', 'TYPE', 'LV'])[['Correct', 'Incorrect','Miss', 'RT']].agg(['count', 'mean', 'std','sum'])
    grouped = grouped.reset_index()
    print(grouped)
    #make a single header (join by '-')
    grouped.columns  =  ['_'.join(i) if len(i[1]) else ''.join(i) for i in grouped.columns.tolist() ]
    print(grouped)
    
    
    # %% group2
    g2 = df.groupby(['SubjectID', 'block', 'TYPE', 'LV','Correct'])[['RT']].agg(['count', 'mean', 'std','sum'])
    g2 = g2.reset_index()
    g2.columns  =  ['_'.join(i) if len(i[1]) else ''.join(i) for i in g2.columns.tolist() ]

    g3 = df.groupby(['SubjectID', 'block', 'TYPE', 'LV'])[['RT']].agg(['count', 'mean', 'std','sum']).reset_index()
    
    # %%
    
    
    # dv= 'Correct'
    # #one block    
    # means = df.groupby(['SubjectID','block','TYPE','LV'])[dv].describe().reset_index()           
    # proportions = df.groupby(['SubjectID','block','TYPE','LV'])[dv].sum().reset_index()
    # proportions['Correct'] = proportions[dv]/nreps     
    
    # #both blocks
    # meansAllBlocks = df.groupby(['SubjectID','TYPE','LV'])[dv].describe().reset_index()
    # meansAllBlocks.insert(0,'block','all')
    # proportionAllBlocks = df.groupby(['SubjectID','TYPE','LV'])[dv].sum().reset_index()
    # proportionAllBlocks['Correct'] = proportionAllBlocks[dv]/(nreps*nblocks) # assumes 2 blocks per type of noise      
    # proportionAllBlocks.insert(0,'block','all')
      
    # # merge descriptives
    # accu = pd.merge(pd.concat([means,meansAllBlocks]),pd.concat([proportions,proportionAllBlocks]))
    # accu.rename({dv:'prop_hits'},axis='columns',inplace=True)
    # accu.insert(4,'count_miss', nreps-accu['count'])
    # accu.loc[accu['count']>nreps,'count_miss']  =  (nreps*nblocks) - accu[accu['count']>nreps]['count']
    # #accu.loc[:,'block'] = accu['block'].replace({1:1,2.0:1,3.0:2,4.0:2}) # recode blocks for clarity in plots (1 and 2 value only)
    # accu['block'] = pd.Categorical(accu.block)    
     
    # del dv,means,meansAllBlocks
    
    #-------------------------------------------------------------------
    # %% Summarize Reaction Times
    dv= 'RT'
    means = df.groupby(['SubjectID','block','TYPE','LV'])[dv].describe().reset_index()           
    meansAllBlocks = df.groupby(['SubjectID','TYPE','LV'])[dv].describe().reset_index()
    meansAllBlocks.insert(1,'block','all')
    
      
    # merge descriptives
    rt = pd.concat([means,meansAllBlocks])
    rt.insert(4,'count_miss', nreps-rt['count'])
    rt.loc[rt['count']>nreps,'count_miss']  =  (nreps*nblocks) - rt[rt['count']>nreps]['count']
    rt.rename(columns={'top':'mean'},inplace=True)
    rt['mean'] = pd.to_numeric(rt['mean'], errors='coerce')
    return (accu,rt)
