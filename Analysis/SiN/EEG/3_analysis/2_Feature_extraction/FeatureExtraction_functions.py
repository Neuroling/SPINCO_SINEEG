#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper script for FeatureExtraction_runner
===============================================================================
@author: gfraga & samuemu
Created on Wed Dec 13 07:57:06 2023

This script contains all the functions needed to deal with Feature Extraction.

These functions are called by FeatureExtraction_runner, and require 
FeatureExtraction_constants for variables that do not change across files.


"""
import os
# from glob import glob
thisDir = os.getcwd()

# import mne
from mne.time_frequency import tfr_morlet
# import matplotlib.pyplot as plt
import numpy as np
# import sys
import pandas as pd
# import pickle


import FeatureExtraction_constants as const

class FeatureExtractionManager:
    """
    FeatureExtractionManager is an object used to handle feature extraction.
    It contains functions for computing power spectrum densities (PSD) and
    time frequency representations (TFR), for extracting the cone of Influence (COI)
    from the TFR, for computing an average of the TFR per frequency band, and for
    extracting the amplitude of a given frequency band.
    
    Unlike the EpochManager object, FeatureExtractionManager can be initiated
    on its own and does not require SubjIDs as parameters. Therefore, filepaths 
    will have to be handled outside of FeatureExtractionManager
    """
    def __init__(self):
        self.metadata={'codebook':const.codebook}

    
    def EEG_extract_feat(self, 
                         epochs,
                         freqs = None, 
                         n_cycles = None, 
                         PSD = True, 
                         TFR = True, 
                         spectral_connectivity = False):
     
        """Extract features from EEG epochs
        =================================================================
        Created on Tue Dec 13 16:39:45 2022
        @author: gfraga & samuemu
        Refs:  
        https://mne.tools/stable/index.html ;  
        https://mne.tools/mne-connectivity/
        
        Function to compute power spectrum densities (PSD) and time frequency 
        representations (TFR)
        
        === TFR notes ===
        We use Morlet wavelets for the TFR. Morlet wavelets is the product of a sine-wave in a given frequency,  
        multiplied by a gaussian envelope. 
        
        The width of the wavelet is determined by Sigma, which is the standard deviation of the Gaussian envelope.
        The wavelet extends to +/-5 standard deviations, so the values at tail ends are close to 0.
        Sigma is determined by freqs and n_cycles:
            >>> sigma = n_cycles/(2 * np.pi * freqs)

        In other words:
            (2 * np.pi * freqs) = one completed sine-wave of freqs (= one cycle)
            Therefore: n_cycles determines how many cycles are in a standard deviation of the gaussian envelope
            Higher n_cycles will give a higher sigma and therefore a broader wavelet, but a lower temporal resolution
        
        
        Parameters
        ----------
        epochs: Instance of 'Epochs'
            Epoched Object from mne. Features are extracted per epoch
        
        freqs: array (optional)
            Frequencies for the time frequency analysis. If none, the default is np.logspace(*np.log10([1, 48]), num=56)
        
        n_cycles: int (optional)
            number of cycles for the wavelet analysis. If none, the default is 3
            
        TFR: bool | (default True)
            True = run time frequency analysis (broadband and per band). False = do not run
            
        PSD: bool | (default True)
            True = run power analysis (spectrum of the entire epoch). False = do not run 
         
        spectral_connectivity: bool | (default False)   
            True = run connectivity analysis in the entire epoch (broadband and per band). False = do not run
             
            
        Returns
        -------
        features_dict : dictionary
            A dictionary containing mne objects with the selected features
         
            
        >> to dos...
        -----------------------
        spectroTemporalConnectivity: bool | (default True)   
             True = run connectivity analysis in the entire epoch (broadband and per band). False = do not run
             
        """      
      
        
        features_dict = {}    
        # Power spectrum (Whole epoch)
        if PSD: 
            print(' ¸.·´¯`·.¸><(((º>  Running spectra per epoch')        
            self.psd = epochs.compute_psd() # Power Spectrum object has power per epoch, preserves event info from Epochs object
            
            print('Done.')        
            features_dict['PSD'] = self.psd
            
        
        #  Time frequency analysis
        if TFR:                
            print(' ¸.·´¯`·.¸><(((º>  Running time frequency analysis')        
            if freqs is None or n_cycles is None:            
                freqs = const.freqs
                n_cycles=const.n_cycles
                print('---> No frequencies and n_cycles specified for the TFR analysis...\n ',
                      'Using those defined in constants:', const.n_cycles, 'cycles and', 
                      len(const.freqs), 'log-spaced freqs from',const.freqs[0],'to',const.freqs[len(const.freqs)-1],'hz')
                
                self.metadata['freqs_code'] = str("np.logspace(*np.log10(["+str(const.freqs[0])+", "+str(const.freqs[len(const.freqs)-1])+"]), num="+str(len(const.freqs))+")")
                self.metadata['freqs'] = freqs
            else:
                self.metadata['freqs'] = freqs
                  
            # Time freq
            tfr = tfr_morlet(epochs, 
                             freqs=freqs, 
                             decim= const.decim, # Decimates sampling rate by this factor (to avoid freezing the kernel)
                             n_cycles=n_cycles, 
                              average=False, 
                             use_fft=True, 
                             return_itc=False,
                             n_jobs=const.n_jobs)
            
            if n_cycles != const.n_cycles:  # if not using default n_cycles, save n_cycles as comment
                tfr.comment = {'n_cycles':n_cycles}
            else:
                tfr.comment = {'n_cycles' : 'default: const.n_cycles'}
            
            
            # self.ch_names=tfr.info.ch_names
            features_dict['TFR'] = tfr
            print('Done.')             
        
        self.metadata['n_cycles'] = n_cycles  
           
        # TODO % Phase connectivity (draft)
        #if spectral_connectivity: 
           # print(' ¸.·´¯`·.¸><(((º>  Running spectral connectivity per band')
           # method = 'pli2_unbiased' #['coh', 'cohy', 'imcoh', 'plv', 'ciplv', 'ppc', 'pli', 'dpli', 'wpli', 'wpli2_debiased'].        
            #fmin = [vals[0] for vals in freqbands.values()] # get lower bounds of freq bands
           # fmax = [vals[1] for vals in freqbands.values()] 
           # conn= spectral_connectivity_epochs(epochs,method=method,fmin=fmin, fmax=fmax, faverage=True)
            
           # print('Done.')        
           # features_dict['conn'] = conn
            
        return features_dict if features_dict else None
    

    def extractCOI(self, tfr, tmin = None, tmax = None):
        """Extract Cone of Influence (COI) from TFR
        =================================================================
        Created on Tue Jan 10 11:43:56 2023
        @author: gfraga & samuemu
        
        Calculates the cone of influence (COI) and drops values outside of it
        
        Wavelet width and COI are determined by half width half maximum (hwhm) of the gaussian envelope: 
        The distance between 50% gain to/after the peak of the gaussian envelope
        So the edge of the COI is the point of 50% gain before/after peak (=fwhm/2)
        see Cohen (2019) https://doi.org/10.1016/j.neuroimage.2019.05.048
        
        See also: Notes in the constants file
     
        Parameters
        ----------
        tfr: mne EpochsTFR object
            Time-frequency power per epoch.
            
        tmin : float or None, Default is None
            The start of the timewindow of which to get the COI in seconds.
            Timepoints before tmin will be dropped.
            If None, will take the data from the start of the epoch to tmax.
            If float, must be in seconds.
         
        tmax : float or None, Default is None
            The end of the timewindow of which to get the COI in seconds.
            Timepoints after tmax will be dropped.
            If None, will take the data from tmin to the end of the epoch.
            If float, must be in seconds.

            
        Returns
        -------
        tfr_df : pandas dataframe
            Very large dataframe with tfr values per channel, epoch, timepoint, frequency 
            (columns: time, freq, epoch, condition, channel). 
            Rows with values outside COI were dropped
                     
        """    
        
        print('>> Cone of influence')
        
        if not tfr.comment['n_cycles']:
            raise ValueError("Found no n_cycles in tfr.comment. Add this info to tfr object as tfr.comment = {'n_cycles': XXX}")
                   
        else: # if n_cycles used in EEG_extract_feat is not the default, calculate coi
            if tfr.comment['n_cycles'] == 'default: const.n_cycles':
                sigma = const.sigma
                freqs=tfr.freqs
            else:
                n_cycles = tfr.comment['n_cycles'] 
                freqs = tfr.freqs
                sigma = n_cycles/(2 * np.pi * freqs)

        # crop data (for separate pre-/post-stim COI)
        tfr = tfr.copy().crop(tmin = tmin, tmax = tmax)
        
        #% get timewindow of the data
        start = tfr.times[0]    
        end = tfr.times[len(tfr.times)-1]
        print(start, end)
        
        #% Create a dataframe with TFR power
        tfr_df = tfr.to_data_frame()   
        print('Creating dataframe with tfr power and filtering out values outside COI ...')
   
        for c,cval in enumerate(sigma):    
            #define time boundaries for each freq bin
            timeCOI_starts = start + (sigma[c]*const.hwhm_const) # COI starts at the point of 50% gain before peak
            timeCOI_ends =  end - (sigma[c]*const.hwhm_const) # COI ends at the point of 50% gain after peak
            
            #mark rows out of the COI as nan
            tfr_df[(tfr_df['freq']==freqs[c]) & ((tfr_df['time'] < timeCOI_starts) | (tfr_df['time'] > timeCOI_ends))] = np.nan
            
        self.metadata['COI_extraction']= const.comment_COI_extraction
        
        tfr_df.dropna(axis=0,inplace=True)                  
        print('Done.')             
        
        return tfr_df
    
    def extractFreqBands(self,tfr_df,freqbands = None):
     
        """TFR power mean per frequency band 
        =================================================================
        Created on Tue Jan 10 14:42:36 2023
        @author: gfraga & samuemu
        
        Function to split the TFR into frequency bands
        
        Parameters
        ----------
        tfr: df derived from an Instance of 'tfr' or the tfr object
            If TFR Object from mne it will be transformed to data frame. 
            Expected a data frame after dropping data points out of the COI

            
        freqbands: dict (optional)
            A dictionary with frequency bands and their ranges. Default: 
             freqbands = dict(Delta = [1,4], Theta = [4,8], Alpha=[8,13], Beta= [13,25],Gamma =[25,48])
             Note: Please make sure the TFR actually covers frequencies in those ranges.
            
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
        self.metadata['freqbands'] = freqbands
        
        # %%
        if type(tfr_df) is not pd.core.frame.DataFrame:
            tfr_df = tfr_df.to_data_frame(time_format=None)   
            print('Input converted to DF')
                    
        #%%  Setting the boundaries for the frequency bands        
        freq_bounds =  [0] +  [item[1][1] for item in freqbands.items()]
        
        #% Checking if the tfr_df covers all frequency bands
        lowestFreq = tfr_df.freq.min()
        highestFreq = tfr_df.freq.max()
        
        if freq_bounds[1] < lowestFreq or freq_bounds[-2] > highestFreq:
            raise ValueError(
                f"At least one frequency band lies outside covered frequency range of {lowestFreq} to {highestFreq} Hz. \n"
                 "            Change freqbands or perform the TFR for lower/higher frequencies to proceed.")


        tfr_df['band'] = pd.cut(tfr_df['freq'], list(freq_bounds),labels=list(freqbands))
        tfr_df.drop(columns='condition',inplace=True) 
        # We exclude the column "condition" for now because it contains the condition as str (e.g.  NV/Call/Stim1/Lv1/Inc/M)
        # and not as int (event-codes such as 111102). This will cause the an error in the groupby-function later.
        # If needed, I can probably change the contents of the "condition" column to be event-codes instead of labels
        # But we will have to remove them anyways for the .mean() later
    
        
        #%% save averaged power per band in a dictionary
        tfr_bands= {}
        tfr_bands['metadata']=self.metadata
        print('>> O_o Adding power averages per band to a dictionary')

        
        for thisband in list(freqbands):  
                      
            # Mean 
            currentBandDF = tfr_df[tfr_df.band.isin([thisband])].copy() # reducing the df to only the selected freqbands
            currentBandDF.drop(columns='band',inplace=True) # dropping "band" column because it constains str (which would raise error)
            
            dfmean = currentBandDF.groupby(['epoch','time']).mean() # add mean per time point of all freqs selected across a selected set of channels
            dfmean.drop(columns='freq',inplace=True) # dropping the "freqs" column because it is now meaningless
            
            # get all unique time-values, so we have some information about the COI of a band
            ts = dfmean.index.get_level_values('time').unique()
            
            #%% Save data in arrays formatted for mvpa
            epIds = dfmean.index.get_level_values('epoch').unique() # get unique epochs
            
            # creating a list of 0-arrays of appropriate size (DO NOT append inside a loop!)
            tempArray = np.zeros(shape=(dfmean.shape[1],len(ts)))
            tempList = [tempArray.copy() for _ in range(len(epIds))]
            del tempArray # we only used this to create tempList
            
            for ep in epIds: # For each unique epoch...
                thisEpoch = dfmean.loc[ep].to_numpy().transpose() # find columns with channel values for each epoch and transpose 
                tempList[int(ep)]=thisEpoch
                del thisEpoch  
            tempArray = np.dstack(tempList) # now we stack the lists to create a new tempArray                                                                       
            
            # Add to dictionary in shape:  epochs x Channels x TimePoints
            tfr_bands[thisband + '_data'] = tempArray.transpose(2,0,1)       
            tfr_bands[thisband + '_COI_times'] = ts
            print('>>>> ' + thisband + ' avg per epoch added')
            
        return tfr_bands
   
        
    #%% Amplitude extraction
    def extractFreqbandAmplitude(self, epo, diroutput, subjID):
        """
        D E P R E C A T E D
        
        EXTRACTING AMPLITUDE PER FREQUENCY BAND
        =======================================================================
        author: samuemu
        
        This function extracts the amplitude of a frequency band of a given epoched dataset.
        
        To do this,it will perform a bandpass filter on the data for every frequency band
        set in the constants (const.freqbands). The resulting epoched datasets will be saved
        as MNE -epo.fif files.
        
        CAUTION!!!! DEPRECATED!!!!
        Due to issues with performing a bandpass filter on epoched data, the amplitude extraction
        per frequency band will have to be done differently. This function is still here for
        documentation and later recycling purposes but it is not called by the runner-script.
        
        More detail on the issue:
            Got the following warning:
                "Runtime Warning: filter_length (423) is longer than the signal (256), 
                distortion is likely. Reduce filter length or filter a longer signal."
            Explanation: 
                The lower the frequency, the higher the filter_length (in samples).
                If you want to filter a signal into a low frequency band, you need 
                a longer signal in order to avoid aliasing/distorting the signal.

        Parameters
        ----------
        epo : MNE Epochs instance
            The epoched dataset
            
        diroutput : str
            directory where the new -epo.fif should be saved. Will be appended with
            subjID + const.taskID + [freqBand]+ const.AmplitudeExtractionFileEnd
            
        subjID : str
            the subject ID. Will only be used to construct the filename of the output

        Returns
        -------
        None.
        To view the new files, use mne.read_epochs()

        """
        
        for thisband in const.freqbands.keys():
            freq_epo = epo.filter(const.freqbands[thisband][0],const.freqbands[thisband][1],n_jobs=const.n_jobs)
           
            fname = os.path.join(diroutput, subjID +'_'+  const.taskID +'_'+ thisband + const.AmplitudeExtractionFileEnd)
            freq_epo.save(fname, overwrite = True)
            
   
