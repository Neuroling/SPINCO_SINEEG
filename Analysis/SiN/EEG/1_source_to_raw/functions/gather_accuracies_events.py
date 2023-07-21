# -*- coding: utf-8 -*-
def gather_accuracies_events(tsv_file_path):
    """ Gather accuracy
    =================================================================
    Created on Tue Apr 25 10:56:48 2023
    @author: gfraga\n

    - Label epochs as correct vs incorrect for two class classification
    - Read trial info from raw Psychopy .csv file logging experiment performance
    - Use start of the block as anchor event
    
    Parameters
    ----------
    tsv_file_path: string 
        Path where event .tsv file was saved
        
        
    Returns
    -------
    Saves event file with additional columns (accuracy and item)
                 
    """  
    
    import os 
    import pandas as pd 
    import json 
    
    # %% Find psychopy log file with task performance
    behave_path = os.path.join(os.path.split(os.path.dirname(tsv_file_path))[0],'beh')
    behave_files = os.listdir(behave_path)
    # 
    for file in behave_files:
        if file.endswith(".csv") and file[-5].isdigit():
            filepath = os.path.join(behave_path, file)             
            subID = file.split('_')[0]
    
   
    #% read data frame 
    df = pd.read_csv(filepath, header = 0)                   
    
    # Exclude last row if the number of rows is more than 388
    if len(df) > 388:
        df = df.iloc[:-1]
    if len(df) > 388:
        raise ValueError("The number of rows exceeds 388. Script terminated.")

    #% ensure 'correct' columns are read as text (it will read boolean if they are only True or False and have no NO_ANSW)
    df[['callSignCorrect','colourCorrect','numberCorrect']] = df[['callSignCorrect','colourCorrect','numberCorrect']].astype(str)
            
    # %% Recode to numerico to compute summary descriptives 
    df['callSignCorrect'] = pd.to_numeric(df['callSignCorrect'].map({'True': 1, 'False': 0, "NO_ANSW":''}))
    df['colourCorrect'] =  pd.to_numeric(df['colourCorrect'].map({'True': 1, 'False': 0, "NO_ANSW": ''}))
    df['numberCorrect'] =  pd.to_numeric(df['numberCorrect'].map({'True': 1, 'False': 0, "NO_ANSW": ''}))
    
    # Reshape set 
    cols2melt = ['noise','block','levels','callSignCorrect','colourCorrect','numberCorrect','mouseClickOnCall.clicked_name','mouseClickOnNumber.clicked_name','mouseClickOnColour.clicked_name']
    idvars = ['noise','block','levels', 'mouseClickOnCall.clicked_name','mouseClickOnNumber.clicked_name','mouseClickOnColour.clicked_name'] 
   
    correctness =  pd.melt(df[cols2melt],id_vars=idvars)                
    correctness = correctness[~correctness.noise.isna()] # remove files for the example trials         
        
    
    # %% Summarize accuracy
    # ----------------------------------------------------------------------------------------   
    # call or callSign  = is the animal ; col = color and num = number 
    # 32 = is the number of target items per level, noise type and block (replace by infering this from data) 
      
    uniqueTrials = 32     
    result = (df.groupby(['noise', 'block', 'levels'])[['callSignCorrect', 'colourCorrect', 'numberCorrect']].sum()) * 100 / uniqueTrials
    result = result.reset_index()
    
    # %%  Read events from eeg file and add accuracy and response to each target 
    # ----------------------------------------------------------------------------------------------
    events = pd.read_csv(tsv_file_path,delimiter='\t') 
    events['ACCURACY'] = ''
    events['RESPONSE_ITEM'] = ''
    
    # % Fill in responses 
    # for first target (call sign)
    value_list = ['111','112','113','114','211','212','213','214']
    for i,idx in enumerate(events.loc[events['VALUE'].isin(value_list)].index):
        events.loc[idx, 'ACCURACY'] = correctness.value[correctness['variable'] == 'callSignCorrect'].iloc[i]
        events.loc[idx, 'RESPONSE_ITEM'] = correctness['mouseClickOnCall.clicked_name'].iloc[i].replace('[\'','').replace('\']','')
        
    # for second target (color)
    value_list = ['121','122','123','124','221','222','223','224']
    for i,idx in enumerate(events.loc[events['VALUE'].isin(value_list)].index):
        events.loc[idx, 'ACCURACY'] = correctness.value[correctness['variable'] == 'colourCorrect'].iloc[i]
        events.loc[idx, 'RESPONSE_ITEM'] = correctness['mouseClickOnColour.clicked_name'].iloc[i].replace('[\'','').replace('\']','')
        
    # for third target (number)
    value_list = ['131','132','133','134','231','232','233','234']
    for i,idx in enumerate(events.loc[events['VALUE'].isin(value_list)].index):
        events.loc[idx, 'ACCURACY'] = correctness.value[correctness['variable'] == 'numberCorrect'].iloc[i]
        events.loc[idx, 'RESPONSE_ITEM'] = correctness['mouseClickOnNumber.clicked_name'].iloc[i].replace('[\'','').replace('\']','')
     
    
    # %% SAVING OUTPUTS    
    # Save table 
    outputname_accu =  subID + '_accu.csv'
    result.to_csv(os.path.join(behave_path,outputname_accu))
    
    outputname_trials =   subID + '_accu_trialsLong.csv'
    correctness.to_csv(os.path.join(behave_path,outputname_trials), index= False)
            
    # Save events with additional coding of accuracy
    outputname_events =  os.path.basename(tsv_file_path).replace('events','events_accu')
    events.to_csv(os.path.join(os.path.dirname(tsv_file_path), outputname_events),sep='\t' , index= False)
     
    
    # %% Metadata 
    metaData = {       
          file: "raw task log (generated by PsychoPy)",
          outputname_accu: "summary of accuracy as % correct over all trials ", 
          outputname_trials: "long-formated accuracy as % correct for each trial type (empty  = missing response) ",
        }
    with open(os.path.join(behave_path, 'info.json'), 'w') as ff:
        json.dump(metaData, ff, indent=2)
        print('---> saved metadata file')

# %%-------------------------------------------------     
# Some old code that got accuracy from other columns        
# #    #-Checking accuracy will change as future log files will have 3 boolean columns for each target item 
# #    # % Assess accuracy     
#     map_call = {'Ad':'call1','Dr':'call2','Kr':'call3','Ti':'call4'}
#     map_col = {'ge':'colour1','gr':'colour2','ro':'colour3','we':'colour4'}
#     map_num = {'Ei':'number1','Zw':'number2','Dr':'number3','Vi':'number4'}
   

      
#  #    # compare response with presented stimuli
# tester = df.copy().iloc[4:]

# #    # Fix formatting issues, subject response values are coded as "['call1']"
# tester['mouseClickOnCall.clicked_name'] = tester['mouseClickOnCall.clicked_name'].apply(lambda x:       x.replace('[\'', '').replace('\']', ''))
# tester['mouseClickOnColour.clicked_name'] = tester['mouseClickOnColour.clicked_name'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))
# tester['mouseClickOnNumber.clicked_name'] = tester['mouseClickOnNumber.clicked_name'].apply(lambda x: x.replace('[\'', '').replace('\']', ''))   
    
# tester.insert(0, 'accu_call', (tester['mouseClickOnCall.clicked_name'] == tester.callSign.replace(map_call)).astype(int))
# tester.insert(0, 'accu_col', (tester['mouseClickOnColour.clicked_name'] == tester.colour.replace(map_col)).astype(int))
# tester.insert(0, 'accu_num', (tester['mouseClickOnNumber.clicked_name'] == tester.number.replace(map_num)).astype(int))
# #  
