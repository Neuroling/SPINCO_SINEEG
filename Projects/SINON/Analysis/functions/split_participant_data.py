#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def split_participant_data(fileinput):
    """Separate participants data  ---- -TESt
    =================================================================
    Created on Tue Jan 24 17:03:17 2023
    @author: gfraga\n
    
    Parameters
    ----------
    fileinput: string
    Name of a csv file with the data pulled from gorilla. Containing task data from one or multiple participants 
       
    Returns
    -------
    participants_data : dictionary
    A separate data frame per participant, after some triming of the original dataset        
           

    """
    import pandas as pd
    import numpy as np
      # %%   
    # read dat
    dat = pd.read_csv(fileinput)
    
    # split by participant       
    groups =  dat.groupby('Participant Private ID')
    #subjects = [key for key in ppdat.groups.keys()]    
    #subjects_lists = [ppdat.get_group(ss) for ss in subjects]
    
   #pd.DataFrame(subjects_lists[1])
    return ppdat 



