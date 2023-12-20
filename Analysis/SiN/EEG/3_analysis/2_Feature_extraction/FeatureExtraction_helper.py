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
import pickle

from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold,cross_validate  
from sklearn import metrics
from sklearn import svm

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
                             n_jobs=const.n_jobs)
            
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
        tfr_df = tfr.to_data_frame()         
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
        # But we will have to remove them anyways for the .mean() later
    
        
        #%% save averaged power per band in a dictionary
        tfr_bands= {}
        print('>> O_o Adding power averages per band to a dictionary')
        tfr_bands['freqbands']=freqbands
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
            del tempArray
            
            for ep in epIds: # For each unique epoch...
                thisEpoch = dfmean.loc[ep].to_numpy().transpose() # find columns with channel values for each epoch and transpose 
                tempList[int(ep)]=thisEpoch
                del thisEpoch  
            tempArray = np.dstack(tempList)                                                                        
            
            # Add to dictionary in shape:  epochs x Channels x TimePoints
            tfr_bands[thisband] = tempArray.transpose(2,0,1)       
            tfr_bands['times_' + thisband] = ts
            print('>>>> ' + thisband + ' avg per epoch added')
            
        return tfr_bands
      
    
    #%%
    def get_crossval_scores(self,X,y=None,clf=svm.SVC(C=1, kernel='linear'),cv=None,scoretype='accuracy'):    
        """ Get classification scores with a scikit classifier 
        =================================================================
        Created on Thu Dec 22 13:44:33 2022
        @author: gfraga & samuemu
        Ref: visit documentation in https://scikit-learn.org/stable/modules/classes.html
        https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
        https://scikit-learn.org/stable/modules/svm.html
        
        Parameters
        ----------
        X: array
         feature vector (e.g., [epochs x channels] x times) 
         # ??? but below we put it in ( epochs x [channels x times] )
        
        y: array-like of shape (n_samples,) or (n_samples, n_outputs)
            The target variable to try to predict in the case of supervised learning.
        
        clf: str 
           Define classifier, i.e. the object to use to fit the data. 
           e.g., clf = svm.SVC(C=1, kernel='linear')
        
        cv: int | str
            cross validation choice. If int is a k-fold CV (e.g, 5) or ShuffleSplit or Stratified 5 fold etc 
            or: StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            # ???
            
        scoretype: str
            the type of score (e.g., 'roc_auc','accuracy','f1')
            see https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
        
        Returns
        -------       
        scores_full: classification score for the whole epoch
        
        scores: classification scores for each time point (time-resolved mvpa)
        
        std_scores: std of scores
        
        """  
        
        
        # #[MVPA] Decoding based on entire epoch
        # ---------------------------------------------
        if len(X.shape) != 3:
            if len(X.shape) > 3:
                raise ValueError(f'Array X needs to be 2 or 3-dimensional, not {len(X.shape)}')
            X_2d = X.reshape(len(X), -1) # Now it is epochs x [channels x times]   
        
        #% see https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
        all_scores_full = cross_validate(estimator = clf,
                                         X = X_2d, # the data to fit the model
                                         y= y,  # target variable to predict
                                         cv=cv, # cross-validation splitting strategy
                                         n_jobs=const.n_jobs,
                                         scoring=scoretype)
        
        all_scores_full = {key: all_scores_full[key] for key in all_scores_full if key.startswith('test')} #get only the scores from output (also contains times)
        print('--> run classification on the full epoch')
        
        
        
        #[MVPA] Time-resolved decoding 
        # ---------------------------------------------
        n_times = X.shape[2]       
        
        #Use dictionaries to store values for each score type 
        scores = {name: [] for name in scoretype}
        std_scores = {name: [] for name in scoretype}
        
        print('[--> starting classification per time point....')
        for t in range(n_times):
            Xt = X[:, :, t]
            
            # Standardize features
            Xt -= Xt.mean(axis=0)
            Xt /= Xt.std(axis=0)
            
            #[O_O] Run cross-validation 
            scores_t = cross_validate(clf, 
                                      Xt, 
                                      y, 
                                      cv=cv, 
                                      n_jobs=const.n_jobs,
                                      scoring=scoretype)     
            
            #Add CV mean and std of this time point to my output dict 
            for name in scoretype:
                scores[name].append(scores_t['test_' + name].mean()) 
                std_scores[name].append(scores_t['test_' + name].std())
        
        #from lists to arrays 
        scores = {key: np.array(value) for key, value in scores.items()}
        std_scores = {key: np.array(value) for key, value in std_scores.items()}
          
        print('Done <--]')
        return all_scores_full, scores, std_scores 
    
