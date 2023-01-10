import pandas as pd
import numpy as np
from mne.time_frequency import tfr_morlet
from mne_connectivity import spectral_connectivity_epochs
import matplotlib.pyplot as plt

####################################################################################    
# % ----------------------------------------------------------
def EEG_extract_feat(epochs,freqs = None, n_cycles = None, power = True, TFR = True, spectral_connectivity = False):
 
    """Extract features from EEG epochs
    =================================================================
    Created on Tue Dec 13 16:39:45 2022
    @author: gfraga\n
    Refs:  
    https://mne.tools/stable/index.html ;  
    https://mne.tools/mne-connectivity/
    
    Parameters
    ----------
    epochs: Instance of 'Epochs'
        Epoched Object from mne. Features are extracted per epoch
    
    freqs: array (optional)
        Frequencies for the time frequency analysis. If none, the default is: np.logspace(*np.log10([1, 48]), num=56)
    
    n_cycles: int (optional)
        number of cycles for the wavelet analysis. If none, the default is: 3
        
    TFR: bool | (default True)
        True = run time frequency analysis (broadband and per band). False = do not run
        
    power: bool | (default True)
         True = run power analysis (spectrum of the entire epoch). False = do not run 
     
    spectral_connectivity: bool | (default False)   
         True = run connectivity analysis in the entire epoch (broadband and per band). False = do not run
         
        
    Returns
    -------
    features_dict : dictionary
        A dictionary containing mne objects with the selected features
         
    >> Work in progress
    -----------------------
    spectroTemporalConnectivity: bool | (default True)   
         True = run connectivity analysis in the entire epoch (broadband and per band). False = do not run
         
    """      
    #% Some definitions:    
    freqbands = dict(Delta = [1,4],
                     Theta = [4,8],
                     Alpha=[8,13], 
                     Beta= [13,25],
                     Gamma =[25,48])
    
    features_dict = {}
    
    #%  Analysis
    # Power spectrum per epoch
    if power: 
        print(' ¸.·´¯`·.¸><(((º>  Running spectra per epoch')        
        spec = epochs.compute_psd() # Power Spectrum object has power per epoch, preserves event info from Epochs object
        
        print('Done.')        
        features_dict['spec'] = spec
        
    
    #  Time frequency analysis
    if TFR:                
        print(' ¸.·´¯`·.¸><(((º>  Running time frequency analysis')        
        if freqs is None or n_cycles is None:            
            freqs = np.logspace(*np.log10([1, 48]), num=56)
            n_cycles=3
            print('---> No frequencies and n_cycles specified for the TFR analysis...Using default 3 cycles and 56 log-spaced freqs from 1 to 48 hz')
            
            
        
        # Time freq
        tfr = tfr_morlet(epochs, freqs=freqs, decim= 3, n_cycles=n_cycles, average=False, use_fft=True, return_itc=False,n_jobs=8)
        tfr.comment = {'n_cycles':n_cycles}
        features_dict['tfr'] = tfr        
        print('Done.')             
                
       
    # % Phase connectivity     
    if spectral_connectivity: 
        print(' ¸.·´¯`·.¸><(((º>  Running spectral connectivity per band')
        method = 'pli2_unbiased' #['coh', 'cohy', 'imcoh', 'plv', 'ciplv', 'ppc', 'pli', 'dpli', 'wpli', 'wpli2_debiased'].        
        fmin = [vals[0] for vals in freqbands.values()] # get lower bounds of freq bands
        fmax = [vals[1] for vals in freqbands.values()] 
        conn= spectral_connectivity_epochs(epochs,method=method,fmin=fmin, fmax=fmax, faverage=True)
        
        print('Done.')        
        features_dict['conn'] = conn
        
    return features_dict if features_dict else None