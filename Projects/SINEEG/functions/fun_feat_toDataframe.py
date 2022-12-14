

def fun_feat_toDataframe (epoched_object):   
    """Extract data from mne Epochs to data frames
    =========================================================================
    Created on Wed Dec 14 16:14:10 2022    @author: gfraga
    
    Some epoched objects turned out to be too large to be stored in file
    
    Parameters
    ----------
    MNE objects: EpochsSpectrum or EpochsTFR. 
         
    Returns
    ----------
    data frames with the data formatted for later ML decoding
     
    """
    
    
    
    if str(epoched_object.__class__).split('.')[-1] == "EpochsSpectrum'>" :
        
        
        
        
        
    
    
 
    #  LOOP thru frequency bands 
    for thisband in freq_bands_of_interest:                     
        # Mean 
        curBandDF = df[df.band.isin([thisband])]
        dfmean = curBandDF.groupby(['epoch','time']).mean() # add mean per time point of all freqs selected across a selected set of channels
    
        # Save data in arrays formated for mvpa                     
        x = []
        epIds = dfmean.index.get_level_values('epoch').unique()
        for ep in epIds:
            thisEpoch = dfmean.filter(regex='^E.*',axis = 1 ).loc[ep].to_numpy().transpose()
            x.append(thisEpoch)
            del thisEpoch  
        X = np.dstack(x)  
                                                                  
        # X shape must be :  Trials x Channels x TimePoints
        X = X.transpose(2,0,1)
        n_times= X.shape[2]
        
        # Condition labels (vector of length = X[0])
        y = np.array([e[2] for e in curEpochs.events])# epochs codes should have dimensions [ n_trials , ]
        times = power.times
                