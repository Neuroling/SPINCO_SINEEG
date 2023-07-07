import numpy as np 
from mne.time_frequency import tfr_morlet
from mne_connectivity import spectral_connectivity_epochs

def fun_eeg_feat(epochs, power = True, TFR = True, spectral_connectivity = True):
 
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
    
    TFR: bool | (default True)
        True = run time frequency analysis (broadband and per band). False = do not run
        
    power: bool | (default True)
         True = run power analysis (spectrum of the entire epoch). False = do not run 
     
    spectral_connectivity: bool | (default True)   
         True = run connectivity analysis in the entire epoch (broadband and per band). False = do not run
               
        
    Returns
    -------
    features_dict : dictionary
        A dictionary containing mne objects with the selected features
         

    >>>>> Work in progress
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
    
    out = {}
    
    #%  Analysis
    # Power spectrum per epoch
    if power: 
        print(' ¸.·´¯`·.¸><(((º>  Running spectra per epoch')        
        spec = epochs.compute_psd() # Power Spectrum object has power per epoch, preserves event info from Epochs object
        
        print('Done.')        
        out['spec'] = spec
        
    
    #  Time frequency analysis     
    if TFR:                
        print(' ¸.·´¯`·.¸><(((º>  Running time frequency analysis')        
        # Time freq
        freqs = np.logspace(*np.log10([1, 48]), num=56)
        tfr = tfr_morlet(epochs, freqs=freqs, decim= 3, n_cycles=3, average=False, use_fft=True, return_itc=False,n_jobs=8)
        
        
        print('Done.')        
        out['tfr'] = tfr
        
    # % Phase connectivity     
    if spectral_connectivity: 
        print(' ¸.·´¯`·.¸><(((º>  Running spectral connectivity per band')
        method = 'pli2_unbiased' #['coh', 'cohy', 'imcoh', 'plv', 'ciplv', 'ppc', 'pli', 'dpli', 'wpli', 'wpli2_debiased'].        
        fmin = [vals[0] for vals in freqbands.values()] # get lower bounds of freq bands
        fmax = [vals[1] for vals in freqbands.values()] 
        conn= spectral_connectivity_epochs(epochs,method=method,fmin=fmin, fmax=fmax, faverage=True)
        
        print('Done.')        
        out['conn'] = conn
        
    return out if out else None
    
    
    