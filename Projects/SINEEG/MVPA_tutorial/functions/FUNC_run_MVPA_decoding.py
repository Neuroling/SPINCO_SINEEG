#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 10:57:17 2022

@author: gfraga

"""
# %%
import sys
functionsPath = "/home/d.uzh.ch/gfraga/smbmount/gfraga/scripts_neulin/Projects/SINEEG/functions/mvpa" 
sys.path.insert(0,functionsPath)

from scipy.io import loadmat
import scipy.io
from datetime import date
import datetime
import numpy as np
from os import path
import os
import numpy.matlib
from SVM_decode import decode_within_SVM
from Euclidean_decode import decode_euclidean_dist

# %%
def FUNC_run_MVPA_decoding(DataPath,
                           time_start = None, 
                           time_end = None, 
                           parallel = True, 
                           SaveAll = True, 
                           decode_method = "decode_within_SVM",
                           nperms = 200,
                           nfolds = 4,
                           time_time  = False):

##
 #   DataPath      =  "/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/mvpa/25subj_TFR/" 
   

    """Run MVPA decoding.
    Parameters
    ----------
    DataPath : str
        Folder where your .mat files are located.
    
    time_start: float | 'none'
            if not specified the first time point of your data will define the starting time 
    
    time_end: float | 'none'
        if not specified the last time point of your data will define the end time 
    
    parallel: bool | (default True)
        False = not parallel; True = parallel
    
    SaveAll: bool | (default True)
        Save output? 
    
    decode_method: str | (default 'decode_within_SVM')
        Name of decoding function name (default) 'decode_within_SVM' or 'decode_euclidean_dist'
    
    nperms: int | (default 200) 
        number of permutations
    
    nfolds: int | (default 4)
        Number of cross validation folds
     
    time_time: bool | (default False)   
     compute time-time generalization (false: only compute the diagonal such that time_test=time_train) 
       
        
    Returns
    -------
    result : results | ''
        If save=True, will save a 'results...' .mat file (with time stamp) in a folder ./Results. 
        The file contains an 'out' array with the filename and struct array 'results' with x, labels, s, params_decoding, parforArg,times.
         
    """
    
    #--------------------------------------------------------
    params_decoding = {}

    # Classification
    params_decoding['function']         = decode_method #'decode_within_SVM' or 'decode_euclidean_dist'
   
    
    params_decoding['timetime']         = time_time  # compute time-time generalization (false: only compute the diagonal such that time_test=time_train)
    params_decoding['num_permutations'] = nperms
    params_decoding['L']                = nfolds    # Number of folds for pseudo-averaging/k-fold
    # Data selection
    
    #Extract data name from folder defined above
    params_decoding['DataName'] = DataPath.split('/')[-1] if DataPath.split('/')[-1] != "" else DataPath.split('/')[-2]      
    #time stamp 
    params_decoding['Date'] = date.today().strftime('%m.%d.%Y')
    now = datetime.datetime.now().strftime("%H.%M.%S")    
    
     #--------------------------------------------------------
    # Read individual x files  and trial info file with Y, S and times [gfraga]
    from glob import glob
    ParData = loadmat(DataPath +'/info_trials_mvpa.mat')
    files = glob(DataPath+'/s*_prep4mvpa.mat', recursive=True)
    xlist = []
    for inputfile in files:
        dat = loadmat(inputfile)            
        currX = dat['x'] 
        xlist.append(currX)
        print(inputfile)
    ParData['X'] = np.concatenate((xlist),axis=2)  # X is now the data arrays of all subjects concatenated along third dim (trials)
    # Commented lines below attempt to save the large array in file: 
    #    import zarr
    #    with open('ParData.zarr', 'wb') as f:                
    #        zarr.save('ParData_X.zarr', ParData['X']) 
    
    
    #--------------------------------------------------------
    Labels = ParData['Y']      
       
    # Filter by times/epochs we want to look at
    
    if time_start==None:
        st = ParData['times'][0][0]
    else:
        st = time_start
    if time_end==None: 
        en = ParData['times'][0][-1]+1
    else:
        en = time_end       
    params_decoding['Epoch_analysis'] = [ st, en ]    
    t = ParData['times'] # time range in ms     
    
    frames = (t>=params_decoding['Epoch_analysis'][0]) & (t<=params_decoding['Epoch_analysis'][1]) # filter for epoch specified in params   
    selected_epochs = ~np.isnan(Labels) # only applicable if you're filtering labels by setting them to nan, otherwise Labels 
    times = t[frames] 
        
    # Filter for participant data within the selected epoch
    x=ParData['X'][:,frames[0],:]
    x=x[:,:,selected_epochs[0]]
    labels=Labels[selected_epochs]
    s=ParData['S'][selected_epochs]
    
    # Do classification
    
    if decode_method == 'decode_within_SVM': # return pairwise classification accuracy 
        results= decode_within_SVM(x, labels, s, params_decoding,parallel, times)     
        
    elif decode_method == 'decode_euclidean_dist': # return euclidean distance between condition response patterns
        results= decode_euclidean_dist(x, labels, s, params_decoding,parallel,times)   
        
    else:
        print('Please select a valid decoding method')        
       
    
    # Save results
    
    if SaveAll:
        if params_decoding['timetime']:
            timetime_case='_timetime'
        else:
            timetime_case =''
    
        out = 'Results_'+ params_decoding['DataName']+'_'+ params_decoding['function']+ timetime_case
        out = out+'_'+params_decoding['Date']+'_'+now+'.mat'
    
        results['out'] = out
        results['results']['out'] = out
    
    
        outputdir = DataPath + '/Results/'
        os.makedirs(outputdir) 
        scipy.io.savemat(outputdir+out, results, do_compression=True)
        np.save(outputdir+out.replace('.mat','.npy'), results)
