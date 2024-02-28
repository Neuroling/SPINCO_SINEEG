#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PreStim FUNCTION SCRIPT
===============================================================================
Created on Fri Feb  2 09:01:21 2024
@author: samuemu

- All functions in this is script belong to the class "PreStimManager". 
- In the runner script you first need to initialize this class to be able to use the functions. 
    Do  `PreStimManager = PreStimManager()` . This is similar to importing a module with functions. 
- This also initializes metadata and set input directory (see `def __init__(self)` code below)
    The metadata is used to collect information across functions
- "self" just means the current class. Variables with the prefix `self.` (i.e. `self.SomeVariable`) 
    can be called outside of the class by calling `PreStimManager.SomeVariable`

"""

import os
from glob import glob
import mne
import PreStim_constants as const
import statsmodels.formula.api as smf
import statsmodels.stats.multitest as ssm
# import statsmodels.base.optimizer as smo
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import pickle
from datetime import datetime



class PreStimManager: 
    
    def __init__(self):
        """
        INITIALIZING FUNCTION
        =======================================================================
        
        This function is called automatically when initializing PreStimManager,
        by PreStimManager = PreStimManager()
        
        It will set the input directory (taken from the constants) and initialize
        the metadata dict. The metadata dict will collect information across as
        different functions in the PreStimManager class are called. It is saved
        with the p_Value array.
        
        The date when the script was run is also saved in the metadata. Together
        with the date of when changes were pushed to github, this gives us
        version control for outputs.

        """
        
        self.dirinput = const.dirinput
        self.metadata = {}
        self.metadata['date_run'] = str(datetime.now())
 
#%%    
    def get_data(self, output = False, condition = None):
        """
        OPEN EPOCHED DATA AND RESHAPE IT FOR LMM
        =======================================================================
        
        Opens epoched data of every subject and stores it in a dict (data_dict) 
        along with trial information (condition_dict)
        
        Automatically calls check_chans_and_times() to check for equal n_channels and n_times across subj
        

        Parameters
        ----------
        condition : str, default None
            Only get the data from trials of this condition. 
            Must be in the form of the event_id used to filter epochs with mne
            with the use of epoch['SomeCondition'].
            It is possible to set multiple conditions by separating the labels with /
            example: `condition = 'NV/Lv1'` <-- will only get data from trials with NV and Lv1 degradation
            
            
        output : bool, default = False
            Whether data_dict and condition_dict should be returned. The default is False.
            In both cases, data_dict and condition_dict will be stored in the PreStimManager object.
            The function run_LMM() will default to using the dicts from the PreStimManager object.
            Therefore, setting output to False will optimise memory usage.
            
            (If you later decide you do want them in the variable explorer, 
             call `data_dict = PreStimManager.data_dict` )


        Returns
        -------
        None if output == False (default)
        
        Otherwise:
            data_dict : dict
                contains [n_subj] arrays of shape [n_epochs, n_channels, n_times]
                
            condition_dict : dict
                contains [n_subj] dataframes, each containing accuracy, levels, noiseType and subjID for every trial

        """
        
        #% First, create a dict of all subj data to store in the memory
        data_dict = {}
        condition_dict = {}
        self.metadata['epo_paths'] = []
    
        for subjID in const.subjIDs:
            
            # get filepath
            epo_path = glob(os.path.join(self.dirinput, subjID, str(subjID + '_' + const.taskID + "*" + const.fifFileEnd)), recursive=True)[0]
            epo = mne.read_epochs(epo_path)
            self.metadata['epo_paths'].append(epo_path)
            
            if condition:
                epo = epo[condition]
            
            # TODO give option to adapt timewindow in function parameters
            data_dict[subjID] = epo.get_data(tmax = 0) # get data as array of shape [n_epochs, n_channels, n_times]
            condition_dict[subjID] = epo.metadata # get trial information
            
            # re-code and delete unneeded data
            condition_dict[subjID]['noiseType'] = condition_dict[subjID]['block'] 
            condition_dict[subjID]['wordPosition'] = condition_dict[subjID]['stimtype'] 
            condition_dict[subjID]['subjID'] = [subjID for i in range(len(condition_dict[subjID]))]
            
            # Re-coding is only necessary for the DV
            condition_dict[subjID]['accuracy'].replace('inc', 0, inplace=True)
            condition_dict[subjID]['accuracy'].replace('cor', 1, inplace=True)
            condition_dict[subjID]['wordPosition'].replace({'CallSign':'1','Colour':'2','Number':'3'},inplace=True)
            # condition_dict[subjID]['levels'].replace('Lv1', 1, inplace=True)
            # condition_dict[subjID]['levels'].replace('Lv2', 2, inplace=True)
            # condition_dict[subjID]['levels'].replace('Lv3', 3, inplace=True)
            # condition_dict[subjID]['noiseType'].replace('NV', 0, inplace=True)
            # condition_dict[subjID]['noiseType'].replace('SSN', 1, inplace=True)
            # condition_dict[subjID].drop(labels=['tf','stim_code','stimtype','stimulus','voice','block'], axis = 1, inplace = True)
            
            if condition:
                condition_dict[subjID].drop(labels=['noiseType'], axis = 1, inplace = True)
            
            #del epo
        if condition:
            self.metadata['condition'] = condition

        self.LastSubjID = subjID
        self.data_dict = data_dict
        self.condition_dict = condition_dict
        
        self.check_chans_and_times() # do a quick check if n_channels and n_times are equal across subj
        
        # add channel names and time in seconds to metadata
        self.metadata['ch_names'] = epo.ch_names
        self.metadata['times'] = epo._raw_times[0:-1]
        
        if output : return data_dict, condition_dict
    
    
#%%    
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
                condition_dict = None,
                formula = "accuracy ~ levels * eeg_data + wordPosition", 
                groups = "subjID"):
        """
        # TODO BINARY dependent variable adjustments (logistic regression)
        # TODO save entire model output obj (mdf)

        Parameters
        ----------
        data_dict : TYPE, optional
            DESCRIPTION. The default is None.
        condition_dict : TYPE, optional
            DESCRIPTION. The default is None.
        formula : TYPE, optional
            DESCRIPTION. The default is "accuracy ~ levels * eeg_data".
        groups : TYPE, optional
            DESCRIPTION. The default is "subjID".

        Returns
        ------- for the p_values

        #% And now the big loop - do the LMM for every channel and every timepoint
        p_values_FDR : TYPE
            DESCRIPTION.

        """
        
        if data_dict == None:
            data_dict = self.data_dict
            
        if condition_dict == None:
            condition_dict = self.condition_dict
            
        #% Create arrays and lists
        channelsIdx = [i for i in range(data_dict[self.LastSubjID].shape[1])] # list of channels
        timesIdx = [i for i in range(data_dict[self.LastSubjID].shape[2])] #list of timepoints
        
        
        # This will run a first LMM, which is only used to extract the number of p-Values
        # Which is needed to create an empty array for the p-Values
        tmp_dict = {}
        for subjID in const.subjIDs:    
            tmp_dict[subjID] = condition_dict[subjID]
            tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,0,0]
        df = pd.concat(tmp_dict.values(), axis=0)
        pVals_n = len(smf.mixedlm(formula, df, groups = groups).fit().pvalues.index)
        del tmp_dict, df
        
        # now we know the dimensions of the empty array we need to create to collect p_Values
        p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n))

        # And here we run the LMM for every channel and every timepoint
        for thisChannel in channelsIdx:
            print('>>>> running channel',thisChannel,'of', len(channelsIdx))
            
            for tf in timesIdx:
                   
                # extract the data & trial information of each subject at a given timepoint and channel
                tmp_dict = {}
                for subjID in const.subjIDs:    
                    tmp_dict[subjID] = condition_dict[subjID]
                    tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,thisChannel,tf]

                
                # Combine all subject's data into one dataframe so we can run the LMM on that
                df = pd.concat(tmp_dict.values(), axis=0)
                del tmp_dict
                
                # calculate LMM
                md = smf.mixedlm(formula, df, groups = groups)        
                mdf = md.fit(full_output = True) # This gives the convergence warning # TODO
                ## https://www.statsmodels.org/devel/_modules/statsmodels/regression/mixed_linear_model.html#MixedLM.fit
                ## Fitting is first tried with bfgs, then lbfgs, then cg - see https://www.statsmodels.org/stable/generated/statsmodels.base.optimizer._fit_lbfgs.html
                
                # record p-Values
                p_values[thisChannel,tf,:] = mdf.pvalues
        
        self.metadata['p_Values_index'] = mdf.pvalues.index
        self.metadata['regression_formula'] = md.formula
        self.metadata['regression_groups'] = groups
        self.metadata['regression_type'] = str(mdf.model)
        self.metadata['FDR_correction'] = False # This will change to True once the FDR is run
        self.metadata['axes'] = ['channel, timeframe, p-Value']
        
        self.p_values = p_values
        return p_values
    
    #%%
    def run_LogitRegression(self, 
                data_dict= None, 
                condition_dict = None,
                formula = "accuracy ~ levels * eeg_data + wordPosition", 
                groups = "subjID"
                ):
        
        # If no data given, use the data stored in the class object
        if data_dict == None:
            data_dict = self.data_dict    
        if condition_dict == None:
            condition_dict = self.condition_dict
            
        #% Create arrays and lists
        channelsIdx = [i for i in range(data_dict[self.LastSubjID].shape[1])] # list of channels
        timesIdx = [i for i in range(data_dict[self.LastSubjID].shape[2])] #list of timepoints
        
        
        # This will run a first LMM, which is only used to extract the number of p-Values
        # Which is needed to create an empty array for the p-Values
        tmp_dict = {}
        for subjID in const.subjIDs:    
            tmp_dict[subjID] = condition_dict[subjID]
            tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,0,0]
        df = pd.concat(tmp_dict.values(), axis=0)
        pVals_n = len(smf.logit(formula, df, groups = groups).fit().pvalues.index)
        del tmp_dict, df

        # now we know the dimensions of the empty array we need to create to collect p_Values
        p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n))
        
        # But gfraga also asked to save the whole model output, soooo...
        #mdf_dict = {key1: {key2: None for key2 in self.metadata['ch_names']} for key1 in self.metadata['times']}


        # And here we run the LMM for every channel and every timepoint
        for thisChannel in channelsIdx:
            print('>>>> running channel',thisChannel,'of', len(channelsIdx))
            
            for tf in timesIdx:
                   
                # extract the data & trial information of each subject at a given timepoint and channel
                tmp_dict = {}
                for subjID in const.subjIDs:    
                    tmp_dict[subjID] = condition_dict[subjID]
                    tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,thisChannel,tf]

                
                # Combine all subject's data into one dataframe so we can run the LMM on that
                df = pd.concat(tmp_dict.values(), axis=0)
                del tmp_dict
                
                # calculate LMM
                md = smf.logit(formula, df, groups = groups)  # TODO groups doesn't work >:(
                mdf = md.fit() # ??? Convergence warning
                ## https://www.statsmodels.org/stable/generated/statsmodels.formula.api.logit.html
                
                # record p-Values
                p_values[thisChannel,tf,:] = mdf.pvalues
        
        self.metadata['p_Values_index'] = mdf.pvalues.index
        self.metadata['regression_formula'] = md.formula
        self.metadata['regression_groups'] = "NONE"
        self.metadata['regression_type'] = str(mdf.model)
        self.metadata['FDR_correction'] = False # This will change to True once the FDR is run
        self.metadata['axes'] = ['channel, timeframe, p-Value']
        
        self.p_values = p_values
        return p_values
    
    #%%
    def run_logisticRegression_sklearn(self,
                          data_dict= None, 
                          condition_dict = None
                          ):
        # for a version with sklearn, see https://www.statology.org/logistic-regression-python/
        raise NotImplementedError
    
#%%
    def FDR_correction(self, p_values = None, alpha = 0.05):
        """
        # TODO

        """
    
            
        if not p_values:
            p_values = self.p_values
            if self.metadata['FDR_correction']:
                raise ValueError('data is already FDR corrected')
        else: 
            if p_values['metadata']['FDR_correction']:
                raise ValueError('data is already FDR corrected')
            p_values = p_values.p_values
            
        print('Time for the FDR.................................................................')
        p_values_1dim = p_values.flatten() #transforms the array into a one-dimensional array (needed for the FDR)
        rej, p_values_FDR = ssm.fdrcorrection(p_values_1dim, alpha = alpha) # get FDR corrected p-Values
        
        
        # TODO do not correct for the number of interactions     
        # TODO run FDR corr separately for each channel  (so only correct across timepoints)
        p_values_FDR = p_values_FDR.reshape(p_values.shape) # transform 1D array back to 3D array of shape [channel, timeframe, p-Value]

        print('done! ...........................................................................')
        
        self.p_values_FDR = p_values_FDR
        self.metadata['FDR_correction'] = True
        self.metadata['FDR_alpha'] = alpha
        
        return p_values_FDR

#%%
    def save_pValues(self, addMetadata = True):
        """
        # TODO

        Parameters
        ----------
        p_values : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        p_values = {'metadata':self.metadata} # create a dict and add the metadata we collected
        
        # Now add the p-Values to the dict. First try to add the FDR-corrected p-Values 
        # and if there are none, add non-FDR-corrected p-Values
        try:
            p_values['p_values'] = self.p_values_FDR
            FDR_name = 'FDR_'
        except AttributeError:
            p_values['p_values'] = self.p_values
            FDR_name = 'uncorrected_'
        
        # See if there is a condition for the model, so that can be added to the filename
        try:
            condition_name = str(self.metadata['condition'] + '_')
        except AttributeError:
            condition_name = ''
        
        # This will take the regression model method that we got from mdf.model()
        # Because mdf.model() gives an output like '<statsmodels.discrete.discrete_model.MNLogit object at 0x7fbf691a7b50>'
        # We take the position of the final '.' and the first ' ' (blank space) and use the str between those two
        regression_name = str(
            self.metadata['regression_type'][self.metadata['regression_type'].rfind('.')+1:
                                             self.metadata['regression_type'].find(' ')] + '_')
            
        filepath = const.diroutput +  regression_name + condition_name + FDR_name + const.pValsPickleFileEnd
        
        # TODO save under different name if not FDR correcetd (as **_uncor)
        with open(filepath, 'wb') as f:
            pickle.dump(p_values, f)
        print("saving to ",filepath)
        return p_values
 
#%%       
    def get_evokeds(self, save = True):
        """
        This function returns a dict containing a lists for every condition, 
        which contain evoked arrays for every subject.
        
        In other words: Every subjects *_epo.fif is opened, then the evoked is
        created for every possible combination of degradation_level, noise_Type and
        accuracy. The evoked object is then appended to a list - there is a list
        for every combination of conditions, and each list stores the evoked-object
        of that condition of every subject. All lists are stored in a dict.

        Parameters
        ----------
        save : bool, default = True
            Whether the evoked dict should be saved as .pkl or only returned
            The default is True.

        Returns
        -------
        evokeds : dict of lists containing MNE evoked objects
            

        """


        # list of every possible combination of accuracy, noise & degradation, separated by /
        conditions = const.conditions
        
        
        # This will give us a dict containing a lists for every condition, which contain evoked arrays for every subject
        evokeds = {condition : [] for condition in conditions} # Create dict with empty lists for every condition
        
        for subjID in const.subjIDs: # for every subj, open *_epo.fif 
            epo_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.fifFileEnd)), recursive=True)[0]
            epo = mne.read_epochs(epo_path)
            
            for event_type in conditions: # create the evoked-object for every condition and append to list inside the dict
                evo = epo[event_type]._compute_aggregate(picks=None)
                evo.comment = event_type
                evokeds[event_type].append(evo)

        if save:
            with open(const.diroutput + const.evokedsPickleFileEnd, 'wb') as f:
                pickle.dump(evokeds, f)
            print("saving...........................................................................")
            print('saved to', const.diroutput + const.evokedsPickleFileEnd)
        return evokeds
        
    def grandaverage_evokeds(self, evokeds):
        evokeds_gAvg= {}
        for condition in const.conditions:
            evokeds_gAvg[condition] = mne.grand_average(evokeds[condition], drop_bads = False, interpolate_bads = False)
        return evokeds_gAvg
    
                
            