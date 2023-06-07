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
    grouped: data frame
        A long formatted dataframe 
    
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

    # %% # Stats per block, type and level (averaging trials)          
    names = ['SubjectID','task', 'block', 'TYPE', 'LV','Accuracy']
    
    # accuracy summary 
    
    accu = df.groupby(names)['trial'].agg(['count']).reset_index()
    accu['propTrials'] = round(accu['count']/nreps,ndigits=2)
    
    #Fix header (join by '-')
    rts = df.groupby(names)[['RT']].agg(['mean', 'std']).reset_index()
    rts.columns  =  ['_'.join(i) if len(i[1]) else ''.join(i) for i in rts.columns.tolist() ]
    
    grouped = pd.merge(accu, rts, on=names)

    # % Expand with all combinations of the variables 
    unique_categories = [grouped[col].unique() for col in names]    
    multiindex = pd.MultiIndex.from_product(unique_categories, names=names)
    
    # reindexing
    grouped = (grouped
                 .set_index(names) 
                 .reindex(multiindex,fill_value= '')
                 .reset_index())
    

    grouped['SubjectID'] = grouped['SubjectID'].astype('object')
    grouped['block'] = grouped['block'].astype('object')

    return grouped