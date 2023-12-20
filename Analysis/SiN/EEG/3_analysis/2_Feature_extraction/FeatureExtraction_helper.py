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
from glob import glob
thisDir = os.getcwd()

import mne
from mne.time_frequency import tfr_morlet
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd

import FeatureExtraction_constants as const

class TFRManager:
    """
    """
    # def __init__(self,epo):
    #     self.tmin = epo.times[0]
    #     self.tmax = epo.times[len(epo.times)-1]
    #     self.epo = epo
    
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
                print('---> No frequencies and n_cycles specified for the TFR analysis...\n Using default 3 cycles and 56 log-spaced freqs from 1 to 48 hz')
                
                  
            # Time freq
            tfr = tfr_morlet(epochs, 
                             freqs=freqs, 
                             decim= 2, # Decimates sampling rate by this factor (to avoid freezing the kernel)
                             n_cycles=n_cycles, 
                             average=False, 
                             use_fft=True, 
                             return_itc=False,
                             n_jobs=-1)
            
            if n_cycles != const.n_cycles:  # if not using default n_cycles, save n_cycles as comment
                tfr.comment = {'n_cycles':n_cycles}
            else:
                tfr.comment = {'n_cycles' : 'default: const.n_cycles'}
            
            
            self.ch_names=tfr.info.ch_names
            features_dict['TFR'] = tfr
            print('Done.')             
                    
           
        # % TODO % Phase connectivity (draft)
        #if spectral_connectivity: 
           # print(' ¸.·´¯`·.¸><(((º>  Running spectral connectivity per band')
           # method = 'pli2_unbiased' #['coh', 'cohy', 'imcoh', 'plv', 'ciplv', 'ppc', 'pli', 'dpli', 'wpli', 'wpli2_debiased'].        
            #fmin = [vals[0] for vals in freqbands.values()] # get lower bounds of freq bands
           # fmax = [vals[1] for vals in freqbands.values()] 
           # conn= spectral_connectivity_epochs(epochs,method=method,fmin=fmin, fmax=fmax, faverage=True)
            
           # print('Done.')        
           # features_dict['conn'] = conn
            
        return features_dict if features_dict else None
    

    def extractCOI(self,tfr):
        """Extract Cone of Influence (COI) from TFR
        =================================================================
        Created on Tue Jan 10 11:43:56 2023
        @author: gfraga & samuemu
     
        Parameters
        ----------
        tfr: Instance of 'tfr' 
            TFR Object from mne. Time frequency power per epoch. 
            
            
        Returns
        -------
        tfr_df : large data frame with tfr values per channel,epoch, tp, freqbin (columns: freq, time, epoch). Rows with values outside COI were dropped
                     
        """            
        if not tfr.comment['n_cycles']:
            print("Found no n_cycles in tfr.comment. Add this info to tfr object as tfr.comment = {'n_cycles':XXX}")
            sys.exit()
            
        else: # if n_cycles used in EEG_extract_feat is not the default, calculate coi
            if tfr.comment['n_cycles'] == 'default: const.n_cycles':
                coi = const.fwhm
                freqs=tfr.freqs
            else:
                n_cycles = tfr.comment['n_cycles'] 
                freqs = tfr.freqs
                sigma = n_cycles/(2 * np.pi * freqs)
                fwhm = sigma * 2 * np.sqrt(2 * np.log(2))
                coi = fwhm/2
        #% wavelet width and coi are determined by full width half maximum (fwhm): 
        #% the distance between 50% gain before peak to 50% gain after peak.
        #% So the edge of the COI is the point of 50% gain before/after peak (=fwhm/2)
        #% see Cohen (2019) https://doi.org/10.1016/j.neuroimage.2019.05.048
            
        # % get coi values  (times per freq bin)
        print('>> Cone of influence')

      
        print('Creating dataframe with tfr power and filtering out values outside COI ...')

        #Create a data frame with TFR power indicating frequency band
        tfr_df = tfr.to_data_frame(time_format=None)         
        for c,cval in enumerate(coi):    
            #define time boundaries for each freq bin
            timeCOI_starts = 0 - coi[c] # COI starts at the point of 50% gain before peak
            timeCOI_ends =   0 + coi[c] # COI ends at the point of 50% gain after peak
            
            #mark rows out of the COI as nan
            tfr_df[((tfr_df['time'] < timeCOI_starts) | (tfr_df['time'] > timeCOI_ends)) & (tfr_df['freq']==freqs[c])] = np.nan
        
        tfr_df.dropna(axis=0,inplace=True)                  
        print('Done.')             
        
        return tfr_df
    
    def extractFreqBands(self,tfr_df,freqbands = None):
     
        """TFR power mean per frequency band 
        =================================================================
        Created on Tue Jan 10 14:42:36 2023
        @author: gfraga & samuemu
        
        Parameters
        ----------
        tfr: df derived from an Instance of 'tfr' or the tfr object
            If TFR Object from mne it will be transformed to data frame. Expected a data frame after dropping data points out of the COI

            
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
        
        lowestFreq=tfr_df.freq.min()
        freq_bounds =  [0] +  [item[1][1] for item in freqbands.items()]
        if freq_bounds[1] < lowestFreq:
            raise ValueError(
                f"At least one frequency band lies below lowest covered Frequency of {lowestFreq} Hz. \n"
                 "            Change freqbands or perform the TFR for lower frequencies to proceed.")
        
        #% Instead of doing this below, we can also just take out delta-band
        #% We do this because we do the TFR from frequencies 6-48; so having a
        #% delta frequency band leads to errors due to it being below the frequencies
        #% covered in the TFR
        
        # if freq_bounds[0] < lowestFreq:
        #     freq_bounds = [i for i in freq_bounds if i>=lowestFreq]
        #     if freq_bounds[0] != lowestFreq:
        #         freq_bounds.insert(0,lowestFreq)


        tfr_df['band'] = pd.cut(tfr_df['freq'], list(freq_bounds),labels=list(freqbands))
        tfr_df.drop(columns='condition',inplace=True) 
        # We exclude the column "condition" for now because it contains the condition as str (e.g.  NV/Call/Stim1/Lv1/Inc/M)
        # and not as int (event-codes such as 111102). That will cause the an error in the groupby-function later
        # If needed, I can probably change the contents of the "condition" column to be event-codes instead of labels
        # TODO
    
        
        #save averaged power per band in a dictionary
        tfr_bands= {}
        print('>> O_o Adding power averages per band to a dictionary')
        tfr_bands['freqbands']=freqbands
        for thisband in list(freqbands):
            print('>>> computing '+thisband)                          
            # Mean 
            currentBandDF = tfr_df[tfr_df.band.isin([thisband])].copy() # reducing the df to only the selected freqbands
            currentBandDF.drop(columns='band',inplace=True) # dropping "band" column because it constains str (which would raise error)
            
            dfmean = currentBandDF.groupby(['epoch','time']).mean() # add mean per time point of all freqs selected across a selected set of channels
            dfmean.drop(columns='freq',inplace=True) # dropping the "freqs" column because it is now meaningless
            
            # get all unique time-values, so we have some information about the COI of a band
            ts = dfmean.index.get_level_values('time').unique()
            
            # Save data in arrays formatted for mvpa
            # !!! The following loop is MASSIVELY ressource-intense and WILL kill the kernel
            # DO NOT use append in a loop!!!!!!!
            x = 
            epIds = dfmean.index.get_level_values('epoch').unique() # get unique epochs
            for ep in epIds: # For each unique epoch...
                print('>>> computing epoch '+str(ep))
                thisEpoch = dfmean.filter(self.ch_names,axis = 1 ).loc[ep].to_numpy().transpose() # find columns with channel values for each epoch and transpose 
                x.append(thisEpoch)
                del thisEpoch  
            X = np.dstack(x)                                                                        
            
            # Add to dictionary in shape:  epochs x Channels x TimePoints # TODO this doesn't work
            tfr_bands[thisband] = X.transpose(2,0,1)       
            tfr_bands['times_' + thisband] = ts
            print('>>>> ' + thisband + ' avg per epoch added')
            
        return tfr_bands
