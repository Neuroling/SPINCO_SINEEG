import numpy as np
import sys
####################################################################################    
# % ----------------------------------------------------------
def EEG_tfr_cone_of_influence(tfr):
    """Extract Cone of Influence
    =================================================================
    Created on Tue Jan 10 11:43:56 2023
    @author: gfraga\n
 
    Parameters
    ----------
    tfr: Instance of 'tfr' 
        TFR Object from mne. Time frequency power per epoch. 
        
        
    Returns
    -------
    tfr_bands : data frame with tfr values per channel, and columns: freq, time, epoch. Rows with values outside COI were dropped
                 
    """            
    if not tfr.comment['n_cycles']:
        print("Found no n_cycles in tfr.comment. Add this info to tfr object as tfr.comment = {'n_cycles':XXX}")
        sys.exit()
        
    else: n_cycles = tfr.comment['n_cycles']        
        
    # % get coi values  (times per freq bin)
    print('>> Cone of influence  ')            
    freqs = tfr.freqs
    wavelet_width = n_cycles/freqs
    coi = wavelet_width/2      
  
    print('Creating dataframe with tfr power and filtering out values outside COI')
    ts =tfr.times.copy()
    
    #Create a data frame with TFR power indicating frequency band
    tfr_df = tfr.to_data_frame(time_format=None)         
    for c,cval in enumerate(coi):    
        #define time boundaries for each freq bin
        timeCOI_starts = ts[0] + coi[c]
        timeCOI_ends =   0 -coi[c]  
        
        #mark rows out of the COI as nan
        tfr_df[((tfr_df['time'] < timeCOI_starts) | (tfr_df['time'] > timeCOI_ends)) & (tfr_df['freq']==freqs[c])] = np.nan
    
    tfr_df.dropna(axis=0,inplace=True)                  
    print('Done.')             
    
    return tfr_df
    # %% Some Old-unverified coi plots left here for recycling... 
    # data = tfr.data[1,0].copy()           
    # ts =tfr.times.copy()
    # for c,cval in enumerate(coi):
    #     data[c][np.where((ts < (ts[0] + coi[c])) | (ts > -coi[c]))] = np.nan #for each freq bind find index in times array of times shorter than first time value + COI and 0 ms - COI value                
    
    # plt.close('all')
    # fig, ax = plt.subplots()
    # ax.imshow(data, origin='lower',cmap='viridis' )        
    # ax.set_xticks(np.linspace(range(data.shape[1])[0], range(data.shape[1])[-1], 10))
    # ax.set_xticklabels(np.linspace(ts[0], ts[-1], 10).round(2))
    # ax.set_yticks(np.linspace(freqs[0], freqs[-1],6))
    # #ax.set_xticklabels(np.linspace(ts[0], ts[-1], 10).round(2))
    # plt.axvline(x=np.argmin(np.abs(ts)),linestyle="dashed", color="black")
    # plt.show()        
          
    