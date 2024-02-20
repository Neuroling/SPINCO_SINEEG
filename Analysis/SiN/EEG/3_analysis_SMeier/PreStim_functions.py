#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 09:01:21 2024

@author: samuemu
"""

import os
from glob import glob
import mne
import PreStim_constants as const
import statsmodels.formula.api as smf
import statsmodels.stats.multitest as ssm
import statsmodels.base.optimizer as smo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

class ERPManager:
    
    def __init__(self):
        self.dirinput = const.dirinput
    
    def get_data(self, output = False):
        """
        OPEN EPOCHED DATA AND RESHAPE IT FOR LMM
        =======================================================================
        
        Opens epoched data of every subject and stores it in a dict (data_dict) 
        along with trial information (metadata_dict)
        
        Automatically calls check_chans_and_times to check for equal n_channels and n_times across subj
        

        Parameters
        ----------
        output : bool, default = False
            Whether data_dict and metadata_dict should be returned. The default is False.
            In both cases, data_dict and metadata_dict will be stored in the ERPManager object.
            The function run_LMM() will default to using the dicts from the ERPManager object.
            Therefore, setting output to False will avoid storing two versions of the dicts in the memory

        Returns
        -------
        None if output == False (default)
        
        Otherwise:
            data_dict : dict
                contains [n_subj] arrays of shape [n_epochs, n_channels, n_times]
                
            metadata_dict : dict
                contains [n_subj] dataframes, each containing accuracy, levels, noiseType and subjID for every trial

        """
        
        #%% First, create a dict of all subj data to store in the memory
        data_dict = {}
        metadata_dict = {}
    
        for subjID in const.subjIDs:
            
            # get filepath
            epo_path = glob(os.path.join(self.dirinput, subjID, str(subjID + '_' + const.taskID + "*" + const.fifFileEnd)), recursive=True)[0]
            epo = mne.read_epochs(epo_path)
    
            
            data_dict[subjID] = epo.get_data(tmax = 0) # get data as array of shape [n_epochs, n_channels, n_times]
            metadata_dict[subjID] = epo.metadata # get trial information
            
            # re-code and delete unneeded data
            metadata_dict[subjID]['noiseType'] = metadata_dict[subjID]['block'] 
            metadata_dict[subjID]['subjID'] = [subjID for i in range(len(metadata_dict[subjID]))]
            metadata_dict[subjID]['levels'].replace('Lv1', 1, inplace=True)
            metadata_dict[subjID]['levels'].replace('Lv2', 2, inplace=True)
            metadata_dict[subjID]['levels'].replace('Lv3', 3, inplace=True)
            metadata_dict[subjID]['accuracy'].replace('inc', 0, inplace=True)
            metadata_dict[subjID]['accuracy'].replace('cor', 1, inplace=True)
            metadata_dict[subjID]['noiseType'].replace('NV', 0, inplace=True)
            metadata_dict[subjID]['noiseType'].replace('SSN', 1, inplace=True)
            metadata_dict[subjID].drop(labels=['tf','stim_code','stimtype','stimulus','voice','block'], axis = 1, inplace = True)
            
            
            #del epo
        self.LastSubjID = subjID
        self.data_dict = data_dict
        self.metadata_dict = metadata_dict
        
        self.check_chans_and_times() # do a quick check if n_channels and n_times are equal across subj
        
        if output : return data_dict, metadata_dict
    
    
    
    def check_chans_and_times(self):
        """
        CHECK FOR EQUAL CHANNEL AND TIMESAMPLE COUNT
        =======================================================================
        
        Quick check for equal numbers in channel and timeframes. 
        First checks channels, then timeframes.
        
        Will raise a value error if n_channels or n_times of the last subject processed is
        unequal to any of the other subj.
        
        This function is called by get_data()

        Raises
        ------
        ValueError

        """
        chan_N = self.data_dict[self.LastSubjID].shape[1]
        tf_N = self.data_dict[self.LastSubjID].shape[2]
        for subjID in const.subjIDs:
            if self.data_dict[subjID].shape[1] != chan_N:
                raise ValueError('not all subj have the same number of channels')
            if self.data_dict[subjID].shape[2] != tf_N:
                raise ValueError('not all subj have the same number of timepoints')

#%%
    def run_LMM(self, 
                data_dict= None, 
                metadata_dict = None,
                function = "accuracy ~ levels * eeg_data * noiseType", 
                groups = "subjID"):
        """
        # TODO

        Parameters
        ----------
        data_dict : TYPE, optional
            DESCRIPTION. The default is None.
        metadata_dict : TYPE, optional
            DESCRIPTION. The default is None.
        function : TYPE, optional
            DESCRIPTION. The default is "accuracy ~ levels * eeg_data * noiseType".
        groups : TYPE, optional
            DESCRIPTION. The default is "subjID".

        Returns
        -------
        p_values_FDR : TYPE
            DESCRIPTION.

        """
        
        if data_dict == None:
            data_dict = self.data_dict
            
        if metadata_dict == None:
            metadata_dict = self.metadata_dict
            
        #%% Create arrays and lists
        channels = [i for i in range(data_dict[self.LastSubjID].shape[1])] # list of channels
        times = [i for i in range(data_dict[self.LastSubjID].shape[2])] #list of timepoints

        p_values = np.zeros(shape=(len(channels),len(times),9)) # empty array for the p_values

        #%% And now the big loop - do the LMM for every channel and every timepoint

        for thisChannel in channels:
            print('>>>> running channel',thisChannel,'of', len(channels))
            
            for tf in times:
                   
                # the data & trial information of each subject at a given timepoint and channel
                tmp_dict = {}
                for subjID in const.subjIDs:    
                    tmp_dict[subjID] = metadata_dict[subjID]
                    tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,thisChannel,tf]

                
                # Combine all subject's data into one dataframe so we can run the LMM on that
                df = pd.concat(tmp_dict.values(), axis=0)
                del tmp_dict
                
                # calculate LMM
                md = smf.mixedlm(function, df, groups = groups)        
                mdf = md.fit(full_output = True) # This gives the convergence warning # TODO
                ## https://www.statsmodels.org/devel/_modules/statsmodels/regression/mixed_linear_model.html#MixedLM.fit
                ## Fitting is first tried with bfgs, then lbfgs, then cg - see https://www.statsmodels.org/stable/generated/statsmodels.base.optimizer._fit_lbfgs.html
                
                # record p-Values
                p_values[thisChannel,tf,:] = mdf.pvalues
                
        self.index_p_values = mdf.pvalues.index
        self.formula_LMM = md.formula


        #%% Now for the FDR correction...
        print('Time for the FDR.................................................................')
        p_values_1dim = p_values.flatten() #transforms the array into a one-dimensional array (needed for the FDR)
        rej, p_values_FDR = ssm.fdrcorrection(p_values_1dim) # get FDR corrected p-Values

        p_values_FDR = p_values_FDR.reshape(p_values.shape) # transform 1D array back to 3D array of shape [channel, timeframe, p-Value]

        print('done! ...........................................................................')
        return p_values_FDR, self.index_p_values

    def save_pValues(self, p_values):
        with open(const.diroutput + const.pValsPickleFileEnd, 'wb') as f:
            pickle.dump(p_values, f)
        print("saving to ",const.diroutput + const.pValsPickleFileEnd)
        
    def get_evokeds(self, save = True):
        accuracy = ['Cor','Inc']
        degradation = ['Lv1','Lv2','Lv3']
        noise = ['NV','SSN']

        # creating a list of every possible combination of accuracy, noise & degradation, separated by /
        conditions = [x + '/' + y + '/' + z for x in noise for y in degradation for z in accuracy]

        # This gives us a dict containing a lists for every condition, which contain evoked arrays for every subject
        evokeds = {condition : [] for condition in conditions}
        for subjID in const.subjIDs:
            epo_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.fifFileEnd)), recursive=True)[0]
            epo = mne.read_epochs(epo_path)
            for event_type in conditions:
                    evokeds[event_type].append(epo[event_type]._compute_aggregate(picks=None))

        if save:
            with open(const.diroutput + const.evokedsPickleFileEnd, 'wb') as f:
                pickle.dump(evokeds, f)
            print("saving...........................................................................")
        return evokeds
        
                
            