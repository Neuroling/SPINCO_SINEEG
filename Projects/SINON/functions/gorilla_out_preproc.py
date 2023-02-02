#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def gorilla_out_preproc(dat):
    """ Separate participants data 
        =================================================================
        Created on Wed Jan 25 11:25:37 2023
        @author: gfraga
        
        Parameters
        ----------
        dat: data frame
            data frame after reading csv or xlsx file with task performance data. Expects multiple subjects in the file
           
        Returns
        -------
        df : data frame 
            Preprocessed data frame with column selection and should have only the rows corresponding to the trials (no examples, etc)
        
    """
    import pandas as pd
    import numpy as np 
    
    #Rename variable to use as subject id
    dat.rename(columns={'Participant Private ID':'SubjectID'}, inplace=True)
    dat.SubjectID = pd.Series(dat.SubjectID,dtype="object")

    # %
    # Leave rows with trial response(always the one after 'audio play requested')
    idx_resp = dat.index[(dat.Response == 'AUDIO PLAY REQUESTED')] + 1    
    df = dat.iloc[idx_resp]
    df = df[df.display.str.contains('trial_')]
    # Replace Correct responses of 'miss' trials by NAs
    df.loc[df['Timed Out']==1,'Correct'] = np.nan
    df.loc[df['Timed Out']==1,'Incorrect'] = np.nan
    df.loc[df['Timed Out']==1,'Reaction Time'] = np.nan
      
    
    #% PER SUBJECT: code the presented audio based on list info 
    # First rename column with the list name (exact column varies with task, i.e., across csv file )
    cols2search = [i for i,val in enumerate(df.columns.str.contains('counterbalance*')) if val] 
    colWithList = [cols2search[i] for i, val in enumerate(df.iloc[1,cols2search].str.contains('list*')) if val==True] #The actual column with the list
    df.insert(2,"STIMLIST",df.iloc[:,colWithList]) #Add conveniently named column with list info    
    
    # % create a variable 'audio' with the sound that was presented 
    audio=[]
    for row in range(len(df)):
        audio.append(df[df.iloc[row]['STIMLIST']].iloc[row])
    
    df.insert(len(df.columns),'AUDIO',audio)           
    
   # %% Extract trial INFO from the audiofilenames   
    
   # Whether SiSSN or NV
    df.insert(2,"TYPE",df['AUDIO'].str.split('norm').str[0].str.split('_').str[0])
    
    # Levels of degradation
    df.insert(2,"LV",df['AUDIO'].str.split('norm').str[1].str.replace('_','').str.replace('.wav','')) # use string split from filenames
    #replace_map = {'-10db': '1','-7.5db': '2', '-5db': '3', '-2.5db': '4','0db': '5','15db':'6',\
     #                  '0.7p': '1','0.75p': '2', '0.8p': '3', '0.85p': '4','0.9p': '5' ,'32ch1p':'6'}
    replace_map = {'-10db': '1','-7.5db': '2', '-5db': '3', '-2.5db': '4','0db': '5',\
                           '0.7p': '1','0.75p': '2', '0.8p': '3', '0.85p': '4','0.9p': '5'}
        
    df['LV'] = df['LV'].map(replace_map)
             
    # some  formatting    
    df['block'] = df['block'].astype('object')
    df['LV'] = df['LV'].astype('object')
    df['Reaction Time'] = df['Reaction Time'].astype('float64')

    df.rename(columns={'Trial Number': 'trial'}, inplace=True)    
    df.rename(columns={'Task Name': 'task'}, inplace=True)    
    df.rename(columns={'Reaction Time': 'RT'}, inplace=True)    
    df.rename(columns={'Timed Out': 'Miss'}, inplace=True)    
     
    # recode blocks for clarity in plots (1 and 2 value only)
    df.loc[:,'block'] = df['block'].replace({1:1,2.0:1,3.0:2,4.0:2})     
    df = df.loc[:,['SubjectID','task','STIMLIST', 'set','block','trial', 'AUDIO', 'LV','TYPE','Correct','Incorrect','Miss','RT']]
    return (df)