import pandas as pd
import numpy as np
from mne.time_frequency import tfr_morlet
from mne_connectivity import spectral_connectivity_epochs

####################################################################################    
# % ----------------------------------------------------------
def EEG_extract_feat(epochs, power = True, TFR = True, spectral_connectivity = False):
 
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
        # Time freq
        freqs = np.logspace(*np.log10([1, 48]), num=56)
        n_cycles = 3
        tfr = tfr_morlet(epochs, freqs=freqs, decim= 3, n_cycles=n_cycles, average=False, use_fft=True, return_itc=False,n_jobs=8)
        features_dict['tfr'] = tfr        
        # %% get coi
        wavelet_width = n_cycles/freqs
        coi = wavelet_width/2      
        
        
        # Create a mask using broadcasting
        mask = np.abs(tfr.times) < coi[:, np.newaxis]
        
        # %%
        data = tfr.data[0]
        fig, ax = plt.subplots()

        im = ax.imshow(data[0])
        masked_data = np.ma.masked_array(data[0], mask=mask)
        ax.imshow(masked_data, cmap='Reds_r', alpha=0.5)

        plt.show()
        
        # %% plot mask
        mask = np.tile(mask[np.newaxis, :, :], (128, 1, 1))
        data = np.random.randn(128, 56, 354)
        
        # Create a figure and axes
       import matplotlib.pyplot as plt
       import numpy as np
       fig, ax = plt.subplots(nrows=1, ncols=2)
       ax[0].imshow(data[0])
       ax[1].imshow(mask, cmap='gray')

       plt.show()
        #%%
        
                
        # Generate a random data array
        data = np.random.rand(128, 56, 354)
        
        # Generate a random boolean mask
        mask = np.random.randint(0, 2, (56, 354), dtype=bool)
        
        # Plot the data and the mask
        fig, ax = plt.subplots(nrows=1, ncols=2)
        ax[0].imshow(data[0])
        ax[1].imshow(mask, cmap='gray')
        
        plt.show()

        
        
        
        

        
        #%%
        
        print('Done.')             

        

        print('>> Creating data set with tfr power per frequency band')
        #Create a data frame with TFR power indicating frequency band
        df = tfr.to_data_frame(time_format=None)  
        freq_bounds =  [0] +  [item[1][1] for item in freqbands.items()] 
        df['band'] = pd.cut(df['freq'], list(freq_bounds),labels=list(freqbands))    
        
        #save averaged power per band in a dictionary
        tfr_bands= {}
        print('>> O_o Adding power averages per band to a dictionary')
        for thisband in list(freqbands):                     
            # Mean 
            curBandDF = df[df.band.isin([thisband])]
            dfmean = curBandDF.groupby(['epoch','time']).mean() # add mean per time point of all freqs selected across a selected set of channels
            
            # Save data in arrays formated for mvpa                     
            x = []
            epIds = dfmean.index.get_level_values('epoch').unique()
            for ep in epIds:
                thisEpoch = dfmean.filter(regex='^E.*',axis = 1 ).loc[ep].to_numpy().transpose() # find columns with channel values (start with E*.) for each epoch and transpose 
                x.append(thisEpoch)
                del thisEpoch  
            X = np.dstack(x)                                                                        
            
            # Add to dictionary in shape:  epochs x Channels x TimePoints
            tfr_bands[thisband] = X.transpose(2,0,1)       
            print('>>> ' + thisband + ' avg per epoch added')
            
    # Add to function output dict
    features_dict['tfr_bands'] = tfr_bands
        
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