import pandas as pd
import numpy as np
####################################################################################    
# % ----------------------------------------------------------
def EEG_tfr_extract_freqBands(tfr_df,freqbands = None):
 
    """TFR power mean per frequency band 
    =================================================================
    Created on Tue Jan 10 14:42:36 2023
    @author: gfraga\n
    
    Parameters
    ----------
    tfr: df derived from an Instance of 'tfr' or the tfr object
        If TFR Object from mne it will be transformed to data frame. Expected a data frame after droping data points out of the COI

        
    freq_bands: dict (optional)
        A dictionary with frequency bands and their ranges. Default: 
         freqbands = dict(Delta = [1,4], Theta = [4,8], Alpha=[8,13], Beta= [13,25],Gamma =[25,48])
        
    Returns
    -------
    tfr_bands : dictionary
        Average power per band
         
         
    """      
    if freqbands is None: 
        freqbands = dict(Delta = [1,4],
                         Theta = [4,8],
                         Alpha=[8,13], 
                         Beta= [13,25],
                         Gamma =[25,48])
        print('no freqbands specified. Using function defaults')
    # %%
    if type(tfr_df) is not pd.core.frame.DataFrame:
        tfr_df = tfr_df.to_data_frame(time_format=None)   
        print('Input converted to DF')
                
    #%%         
    freq_bounds =  [0] +  [item[1][1] for item in freqbands.items()] 
    tfr_df['band'] = pd.cut(tfr_df['freq'], list(freq_bounds),labels=list(freqbands))    
    
    #save averaged power per band in a dictionary
    tfr_bands= {}
    print('>> O_o Adding power averages per band to a dictionary')
    tfr_bands['freqbands']=freqbands
    for thisband in list(freqbands):                     
        # Mean 
        curBandDF = tfr_df[tfr_df.band.isin([thisband])].copy()
        dfmean = curBandDF.groupby(['epoch','time']).mean() # add mean per time point of all freqs selected across a selected set of channels
        ts = dfmean.index.get_level_values('time').unique()
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
        tfr_bands['times_' + thisband] = ts
        print('>>> ' + thisband + ' avg per epoch added')
        
    return tfr_bands

#%% 
#import matplotlib.pyplot as plt
#plt.plot(tfr_bands['times_Beta'],tfr_bands['Beta'].mean(0).mean(0))
         
