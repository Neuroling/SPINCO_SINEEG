#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 07:53:56 2024

@author: testuser
"""

import LogReg_constants as const
import mne
import os
from glob import glob
import numpy as np
import pandas as pd
import random
from pymer4.models import Lmer
from warnings import warn


class LogRegManager:
    def __init__(self):
        self.metadata = {}
        self.dirinput = const.dirinput
    
    def get_data(self, output = False, condition = None, tmin = None, tmax = 0):
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
            The function run_LogitRegression() will default to using the dicts from the PreStimManager object.
            Therefore, setting output to False will optimise memory usage.
            
            (If you later decide you do want them in the variable explorer, 
             call `data_dict = PreStimManager.data_dict` )
            
        tmin : float or None, Default is None
            The start of the timewindow of which to get the data from the epoch.
            If None, will take the data from the start of the epoch to tmax.
            If float, must be in seconds.
            
        tmax : float or None, Default is 0
            The end of the timewindow of which to get the data from the epoch.
            If None, will take the data from tmin to the end of the epoch.
            If float, must be in seconds.
            The Default `0` will get only pre-stimulus data.


        Returns
        -------
        None if output = False (default)
        
        Otherwise:
            data_dict : dict
                contains [n_subj] arrays of shape [n_epochs, n_channels, n_times]
                
            condition_dict : dict
                contains [n_subj] dataframes, each containing accuracy, levels, noiseType and subjID for every trial

        """
        # make sure tmin is smaller than tmax
        if tmin is not None and tmax is not None:
            if tmin >= tmax:
                raise ValueError("tmin needs to be smaller than tmax")
        
        #% First, create a dict of all subj data to store in the memory
        data_dict = {}
        condition_dict = {}
        self.metadata['epo_paths'] = []
    
        for subjID in const.subjIDs:
            
            # get filepath
            epo_path = glob(os.path.join(self.dirinput, subjID, str(subjID + '_' + const.taskID + "*" + const.fifFileEnd)), recursive=True)[0]
            epo = mne.read_epochs(epo_path)
            self.metadata['epo_paths'].append(epo_path)
            
            if condition: # subset by condition
                epo = epo[condition]
            
            data_dict[subjID] = epo.get_data(tmax = tmax, tmin = tmin, copy = True) # get data as array of shape [n_epochs, n_channels, n_times]
            condition_dict[subjID] = epo.metadata # get trial information
            
            # rename some columns
            condition_dict[subjID]['noiseType'] = condition_dict[subjID]['block'] 
            condition_dict[subjID]['wordPosition'] = condition_dict[subjID]['stimtype'] 
            
            # add a column saying the subjID
            condition_dict[subjID]['subjID'] = [subjID for i in range(len(condition_dict[subjID]))]
            
            # Re-coding is only necessary for the DV
            condition_dict[subjID]['accuracy'] = condition_dict[subjID]['accuracy'].replace({'inc': 0, 'cor': 1})
            
            # drop unneeded columns
            condition_dict[subjID].drop(labels=['tf','stim_code','stimtype','stimulus','voice','block'], axis = 1, inplace = True)

            
        if condition:
            self.metadata['condition'] = condition
            
        self.LastSubjID = subjID
        self.data_dict = data_dict
        self.condition_dict = condition_dict
        
        self.check_chans_and_times() # do a quick check if n_channels and n_times are equal across subj
        
        # add channel names to metadata and sampling frequency to metadata
        self.metadata['ch_names'] = epo.ch_names
        self.metadata['original_sampling_frequency'] = epo._raw_sfreq[0]
        
        # add times in seconds and tmin/tmax to metadata
        times = epo._raw_times
        
        if tmin is not None:
            idx_tmin = next(i for i,v in enumerate(times) if v >= tmin)
            times = times[idx_tmin : len(times)]
            self.metadata['tmin'] = tmin
        else:
            self.metadata['tmin'] = "None"
     
        if tmax is not None:
            idx_tmax = next(i for i,v in enumerate(times) if v >= tmax)
            times = times[0: idx_tmax]
            self.metadata['tmax'] = tmax
        else:
            self.metadata['tmax'] = "None"     
        self.metadata['times'] = times
        
        
        if output : return data_dict, condition_dict



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

    
    def get_condition_df(self):
        """
        Just a quick function to call to create condition_df from condition_dict.
        condition_df is the aggregate of all dfs in condition_dict.
        
        This also re-indexes condition_df, because the indices are messed up after
        concatenating.
        """
        self.condition_df = pd.concat(self.condition_dict.values(), axis=0, ignore_index=True)
        reIdx = pd.Series(range(len(self.condition_df)))
        self.condition_df.set_index(reIdx, inplace = True)
 
        
    def CheckCompleteSeparation(self, trial_info = None):
        """
        CHECK CASES OF COMPLETE SEPARATION
        =======================================================================
        Complete or perfect separation in a logit regression refers to a situation 
        where one or more combinations of the categorical predictors completely 
        separates the outcome variable (i.e. for a combination of predictors, 
        all trials are correct). This causes an issue for the regression. 
        
        This function will check if any combination of 'levels', 'subjID', and
        'wordPosition' has a 100% accuracy.
        If this is the case, will return check_df.

        Returns
        -------
        check_df : dataframe
            All combinations of 'levels', 'subjID', & 'wordPosition' that are 100% accurate.

        """
        if trial_info is None:
            try:
                trial_info = self.condition_df 
            except AttributeError:
                self.get_condition_df()
                trial_info = self.condition_df 
            
        check_df = trial_info.groupby(['levels', 'subjID', 'wordPosition'])['accuracy'].mean().reset_index()
        idx = check_df.index[check_df['accuracy'] == 1.0].tolist()
        check_df = check_df.iloc[idx] # Now we know which combinations of levels, subjID and wordPosition are 100% correct
        if len(idx) != 0:
            warn('Complete Separation in at least one combination of predictors. Adding additional info to metadata.')
            self.metadata['completeSeparation'] = check_df
            return check_df
      
        
    def FixCompleteSeparation(self, trial_info = None):
        """
        FIX CASES OF COMPLETE SEPARATION IN PLACE
        =======================================================================
        Complete or perfect separation in a logit regression refers to a situation 
        where one or more combinations of the categorical predictors completely 
        separates the outcome variable (i.e. for a combination of predictors, 
        all trials are correct). This causes an issue for the regression. 
        
        This function calls CheckCompleteSeparation to check if any combination of 
        'levels', 'subjID', & 'wordPosition' has a 100% accuracy.
        If this is the case, will change the accuracy label to incorrect in 
        a single random trial for each condition in which it was previously 
        100% correct.
        
        This procedure was suggested by the statistics consultant I talked to.
        I could also find it listed as an option for dealing with this issue 
        here:     
        https://stats.stackexchange.com/a/68917
        
        # TODO I also need to check if I cannot do this another way
        (see link above for options)   
                
        """
        if trial_info is None:
            try:
                trial_info = self.condition_df 
            except AttributeError:
                self.get_condition_df()
                trial_info = self.condition_df 
                
        check_df = self.CheckCompleteSeparation()
        
        
        if check_df is not None:
            idx_changed_accuracy = []
            for index, row in check_df.iterrows():
                # Filter the original DataFrame to get rows with the same levels, subjID, wordPosition values
                filtered_rows = trial_info[(trial_info['levels'] == row['levels']) & (trial_info['subjID'] == row['subjID']) & (trial_info['wordPosition'] == row['wordPosition'])]
                # Randomly choose one row from the filtered rows and update the accuracy value to 0
                idx_changed_accuracy.append(filtered_rows.sample(n=1).index[0])
                
            trial_info.loc[idx_changed_accuracy, 'accuracy'] = 0
            self.metadata['changed_accuracy'] = idx_changed_accuracy

#%% binTimes # TODO document    
    def binTimes(self, n_bins):
        """
        CREATE TIME BINS IN PLACE
        =======================================================================

        Parameters
        ----------
        n_bins : int
            How many bins the data should be split into. The data's n_times must be
            divisible by n_bins without remainder

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        times = self.metadata['times']
        if len(times) % n_bins != 0:
            raise ValueError('number of timepoints must be divisible by number of bins without remainder.')
        
        # Only do this if there are at least twice as many timepoints as n_bins
        if self.data_dict[self.LastSubjID].shape[2] > 2*n_bins:   
            for subjID in const.subjIDs:
                data_tmp = self.data_dict[subjID].copy()
                bin_size = data_tmp.shape[2] // n_bins
                
                # reshape data to [:,:, n_bins, bin_size]
                data_tmp = data_tmp.reshape(data_tmp.shape[0], data_tmp.shape[1], n_bins, bin_size)
                
                # Take the mean along the axis 3 to compute averages for each bin
                self.data_dict[subjID] = np.mean(data_tmp, axis=3)
                
            self.metadata['times_bins'] = np.array_split(times, n_bins)
            self.metadata['n_times_bins'] = n_bins
        else: 
            raise ValueError('not enough timepoints to bin') # TODO raise error instead
            
        return self.data_dict

 
        
                
#%% # TODO update documentation
# TODO do this within subj
    def random_subsample_accuracy_equalise(self, 
                                  trial_info = None):
        """
        RANDOMLY SUBSAMPLES TRIALS TO EQUALISE ACCURACY COUNTS
        =======================================================================
        
        This function counts how many trials were correct and how many incorrect.
        It will then get the lower of those two numbers (let's call it minumum)
        and then it will randomly select [minumum] correct and incorrect trials
        and return their indices ("subsample_idx").
        The length of subsample_idx is therefore = 2*minimum.
        Half the indices are from correct, and half from incorrect trials.
        
        
        Parameters
        ----------
        trial_info : dict or pandas DataFrame, optional
            The trial information - for instance condition_dict or condition_df. 
            The default is None, in which case the function will try to use the
            condition-dict stored in the PreStimManager object. If there is none, it
            will try to use the condition_df stored in the PreStimManager object.
            
        Raises
        ------
        AttributeError
            if no trial information was provided and none could be found.
            
        Returns
        -------
        subsample_idx : indexes
            the subsampled indices, which can be applied to the df by calling 
            `df = df.iloc[subsample_idx]`
            Note : if the df has non-sequential indices (which can happen when filtering or
                 concatentaing), this will not work.
            
        """
        
        if trial_info is None: 
            try:
                tmp_df = self.condition_df.copy()
            except AttributeError:
                try:
                    self.get_condition_df()
                    tmp_df = self.condition_df.copy()
                except AttributeError:
                    raise AttributeError("cannot subsample data - no trial information (condition_dict or condition_df) found")
        else:
            tmp_df = trial_info.copy()
            
        # combine all subj condition dataframes to get across-subj accuracy
        if type(tmp_df) is dict: 
            tmp_df = pd.concat(tmp_df.values(), axis=0, ignore_index=True)
            # re-Index because after combination the idx will be non-sequential
            reIdx = pd.Series(range(len(tmp_df)))
            tmp_df.set_index(reIdx, inplace = True)
         
        # counting total correct and incorrect
        count_cor = tmp_df['accuracy'].value_counts()[1]
        count_inc = tmp_df['accuracy'].value_counts()[0]
        
        idx_cor = tmp_df.index[tmp_df['accuracy'] == 1]
        idx_inc = tmp_df.index[tmp_df['accuracy'] == 0]
        
        minimum = min(count_cor, count_inc)
        subsample_idx = random.sample(list(idx_cor), minimum) + random.sample(list(idx_inc), minimum)
        
        return subsample_idx
    
    def random_subsample_accuracy_decimate(self, 
                                  trial_info = None,
                                  decimation_factor = 10):
        """
        RANDOMLY SUBSAMPLES TRIALS 
        =======================================================================
        # TODO document
        
        Parameters
        ----------
        trial_info : dict or pandas DataFrame, optional
            The trial information - for instance condition_dict or condition_df. 
            The default is None, in which case the function will try to use the
            condition-dict stored in the PreStimManager object. If there is none, it
            will try to use the condition_df stored in the PreStimManager object.
            
        Raises
        ------
        AttributeError
            if no trial information was provided and none could be found.
            
        Returns
        -------
        subsample_idx : indexes
            the subsampled indices, which can be applied to the df by calling 
            `df = df.iloc[subsample_idx]`
            Note : if the df has non-sequential indices (which can happen when filtering or
                 concatentaing), this will not work.
            
        """
        
        if trial_info is None: 
            try:
                tmp_df = self.condition_df.copy()
            except AttributeError:
                try:
                    self.get_condition_df
                    tmp_df = self.condition_df.copy()
                except AttributeError:
                    raise AttributeError("cannot subsample data - no trial information (condition_dict or condition_df) found")
        else:
            tmp_df = trial_info.copy()
            
        # combine all subj condition dataframes to get across-subj accuracy
        if type(tmp_df) is dict: 
            tmp_df = pd.concat(tmp_df.values(), axis=0, ignore_index=True)
            
            # re-Index because after combination the idx will be non-sequential
            reIdx = pd.Series(range(len(tmp_df)))
            tmp_df.set_index(reIdx, inplace = True)
        
        
        # get n_combinations, n_trials per combination, and the n_trials remaining after decimation
        n_trials_per_condition = tmp_df.groupby(['levels', 'subjID', 'wordPosition'])['accuracy'].size().reset_index()
        n_trials_per_condition = round(n_trials_per_condition['accuracy'].mean())
        n_decim_trials = n_trials_per_condition // decimation_factor
        
        conditions = tmp_df.groupby(['levels', 'subjID', 'wordPosition','accuracy']).indices
        
        subsample_idx = []
        for indices in conditions.values():
            if n_decim_trials >= len(indices):
                subsample_idx += list(indices)
            else:
                subsample_idx += list(random.sample(list(indices), n_decim_trials))
                        

        return subsample_idx

    def run_LogitRegression(self, 
            data_dict= None, 
            condition_dict = None,
            formula = "accuracy ~ levels * eeg_data + wordPosition + (1|subjID)", 
            family = 'binomial',
            n_iter = 500, 
            equalise_accuracy = True,
            time_bins = None
            ):
        """
        LOGIT REGRESSION
        =======================================================================
        
        Regression for binary DV. 
        
        In case of equalise_accuracy = True, will equalise trial numbers of correct and
        incorrect trials by calling the function LogRegManager.random_subsample_accuracy()
        
        If time_bins is not None, will group the data into bins along the time-axis
        and average measurement values within the bin. The number of bins is = time_bins
        
    
        Parameters
        ----------
        data_dict : dict of [n_subj] arrays of shape [n_epochs, n_channels, n_times]; optional
            The dict containing the data for each subject. The default is None, in which
            case the data_dict from the previous call of PreStimManager.get_data() is used.
            
        condition_dict : dict of [n_subj] dataframes with trial information; optional
            The dict containing trial information such as accuracy, condition, etc. for every subj.
            The default is none, in which case the condition_dict from the previous 
            call of PreStimManager.get_data() is used
    
        formula : str, optional
            The formula to be passed to smf.logit(). 
            The default is "accuracy ~ levels * eeg_data + wordPosition + (1|subjID)".
            
        family : str, optional
            The family for the regression. Used in the same way as with the R lmer package.
            The default is "binomial" for a logit regression
            
        equalise_accuracy : bool, optional
            Whether to equalise trial-number of correct and incorrect trials
            by randomly subsampling the data. The default is True.
            
        time_bins : int, optional
            How many bins there should be made (timewise). Will split the data into time_bins
            groups on the axis of time and average timepoints inside the bin.
            The default is None, in which case it will not bin the data.
    
        n_iter : int, optional
            How many iterations of subsampling and regression should be done. 
            This option is only available if equalise_accuracy is set to True, otherwise,
            n_iter will be overwritten with 1.
            The default is 500.
            

        """
    
        
        # If no data given, use the data stored in the class object
        if data_dict is None:
            data_dict = self.data_dict    
        if condition_dict is None:
            condition_dict = self.condition_dict
            
        if not equalise_accuracy: # do not iterate if no sub-sampling is performed
            n_iter = 1
            
        # create bins for the times (if desired)
        if time_bins is not None:
            self.binTimes(time_bins)
            
            
        #% Create arrays and lists
        channelsIdx = [i for i in range(data_dict[self.LastSubjID].shape[1])] # list of channels
        timesIdx = [i for i in range(data_dict[self.LastSubjID].shape[2])] #list of timepoints
        
        
        # This will run a first model which is only used to extract the number of p-Values
        # Which is needed to create an empty array for the p-Values
        tmp_dict = {}
        for subjID in const.subjIDs:    
            tmp_dict[subjID] = condition_dict[subjID]
            tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,0,0]
        df = pd.concat(tmp_dict.values(), axis=0)
        n_coef = Lmer(formula, data = df, family = family).fit().shape[0]

        
        # now we know the dimensions of the empty array we need to create to collect p_Values
        n_channels = len(channelsIdx)
        n_times = len(timesIdx)
        shape_1 = (n_channels, n_times, n_coef, n_iter)
        
        p_values = np.zeros(shape = shape_1)
        coefficients = np.zeros(shape = shape_1)
        z_values = np.zeros(shape = shape_1)
        coef_SD = np.zeros(shape = shape_1)
        OR = np.zeros(shape = shape_1)
        
        del tmp_dict, df
    

        for iteration in range(n_iter):
            
            if equalise_accuracy:
                # we sub-sample running the function below. which will give us a set of indices (idx)
                # and later we subset the data by idx
                idx = self.random_subsample_accuracy()
            else: # if no sub-sampling is asked for, just get every idx
                idx = [i for i in range(len(pd.concat(condition_dict.values(), axis=0, ignore_index=True)))]
            
            # And now we run the model for every channel and every timepoint
            for thisChannel in channelsIdx:
                print('>>>> running channel',thisChannel,'of', len(channelsIdx))
                
                for tf in timesIdx:
                       
                    # extract the data & trial information of each subject at a given timepoint and channel
                    tmp_dict = {}
                    for subjID in const.subjIDs:    
                        tmp_dict[subjID] = condition_dict[subjID]
                        tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,thisChannel,tf]
    
                    
                    # Combine all subject's data into one dataframe so we can run the model on that
                    df = pd.concat(tmp_dict.values(), axis=0,ignore_index=True)
                    del tmp_dict

                    # re-Index because after combination the idx will be non-sequential
                    reIdx = pd.Series(range(len(df)))
                    df.set_index(reIdx, inplace = True)
                    
                    # use the idx we got previously to subsample the data
                    df = df.iloc[idx]
                    

                    # calculate Logit regression
                    md = Lmer(formula, data = df, family = family)
                    md.fit()
                    
                    # TODO save AIC

                    
                    # record p-Values, z-Values and coefficients
                    p_values[thisChannel,tf,:, iteration] = md.coefs['P-val']
                    coefficients[thisChannel,tf,:, iteration] = md.coefs['Estimate']
                    coef_SD[thisChannel,tf,:, iteration] = md.coefs['SE']
                    z_values[thisChannel,tf,:, iteration] = md.coefs['Z-stat']
                    OR[thisChannel,tf,:,iteration] = md.coefs['OR']

                    
                    self.currentChannelTimeIter = [thisChannel, tf, iteration]
                    self.idx = idx
                    
        if n_iter == 1:  # reduce dimensions of output if no subsampling was performed
            p_values = p_values[:,:,:,0]
            coefficients = coefficients[:,:,:,0]
            z_values = z_values[:,:,:,0]
            coef_SD = coef_SD[:,:,:,0]
            OR = OR[:,:,0]
        
        self.p_values = p_values
        self.coefficients = coefficients
        self.z_values = z_values
        self.coef_SD = coef_SD
        self.OR = OR
        
        if equalise_accuracy: # get mean and sd of the p-Values across iterations
            self.p_values_mean = p_values.mean(axis = 3)
            self.p_values_SD = p_values.std(axis = 3)
        else:
            pass
        
        count_cor = df['accuracy'].value_counts()[1]
        count_inc = df['accuracy'].value_counts()[0]
        self.metadata['n_correct/n_incorrect'] = (count_cor, count_inc)

        self.metadata['p_Values_index'] = md.coefs.index
        self.metadata['regression_formula'] = formula
        self.metadata['regression_type'] = family
        self.metadata['FDR_correction'] = False # This will change to True once the FDR is run
        self.metadata['axes'] = ['channel, timeframe, (coefficients), iteration']
        self.metadata['subsampling_iterations'] = n_iter
        self.metadata['subsampling_performed'] = equalise_accuracy
        # self.metadata['degrees_of_freedom_Model'] = md.coefs.df_model # TODO
        # self.metadata['degrees_of_freedom_Residuals'] = md.coefs.df_resid # TODO
        self.metadata['n_observations_per_Regression'] = len(df)

        
        if equalise_accuracy:
            self.metadata['subsample_length'] = len(df)
    
    
