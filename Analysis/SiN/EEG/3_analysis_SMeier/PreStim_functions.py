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
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import pickle
from datetime import datetime
import random


#%%
class PreStimManager: 
    
    def __init__(self, raiseWarnings = False):
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
        
        Parameters
        ----------
        raiseWarnings : bool, Default False
            If False, will not raise warnings

        """
        
        self.dirinput = const.dirinput
        self.metadata = {} # initialise empty metadata dict
        self.metadata['datetime_run_start'] = str(datetime.now())
        
        if not raiseWarnings:
            import warnings
            warnings.filterwarnings('ignore') 
 
#%% 
    def get_epoData_singleSubj(self, subjID, output = False, condition = None, tmin = None, tmax = 0):
        """
        OPEN EPOCHED DATA AND RESHAPE FOR THE REGRESSION (SINGLE SUBJECT)
        =======================================================================
        
        
        Parameters
        ----------
        subjID : str
            The subject ID. This will be used to get the directory of the epoched data,
            and will be stored in the PreStimManager object for later use.
        
        condition : str, default None
            Only get the data from trials of this condition. 
            Must be in the form of the event_id used to filter epochs with mne, like
            with the use of epoch['SomeCondition'].
            It is possible to set multiple conditions by separating the labels with /
            Example: `condition = 'NV/Lv1'` <-- will only get data from trials with NV and Lv1 degradation
                   
        output : bool, default = False
            Whether data_array and condition_df should be returned. The default is False.
            In both cases, data_array and condition_df will be stored in the PreStimManager object.
            The function run_LogitRegression_WithinSubj() will default to using the array/df saved
            internally in the PreStimManager-class.
            Therefore, setting output to False might optimise memory usage.
            
            (If you later decide you do want them in the variable explorer, 
             call `data_array = PreStimManager.data_array` )
            
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
        If output == False (default):
            None
        
        If output == True:
            data_array : numpy array
                numpy array of shape [n_epochs, n_channels, n_times]
                
            condition_df : pandas dataframe
                pandas dataframe, containing accuracy, levels, noiseType for every trial

        """
        # 
        self.subjID = subjID
        self.metadata['subjectID'] = subjID
        
        # get filepath, read epoch
        epo_path = glob(os.path.join(self.dirinput, subjID, str(subjID + '_' + const.taskID + "*" + const.fifFileEnd)), recursive=True)[0]
        epo = mne.read_epochs(epo_path)
        self.metadata['epo_path'] = epo_path
        
        # subset epoch to the desired condition
        if condition:
            epo = epo[condition]
            self.metadata['condition'] = condition
        
        # add channel names and time in seconds to metadata
        self.metadata['ch_names'] = epo.ch_names
        
        times = epo._raw_times
        if tmin is not None:
            if tmax is not None:
                if tmin >= tmax:
                    raise ValueError("tmin needs to be smaller than tmax")
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
        
        # extract data, then delete the epoch-object
        data_array = epo.get_data(tmax = tmax, tmin = tmin) # get data as array of shape [n_epochs, n_channels, n_times]
        condition_df = epo.metadata # get trial information
        del epo
        
        # re-name some columns
        condition_df['noiseType'] = condition_df['block'] 
        condition_df['wordPosition'] = condition_df['stimtype'] 

        # Re-coding is necessary for the DV (needs to be numeric, not string)
        condition_df['accuracy'].replace({'inc': 0, 'cor': 1}, inplace=True)
        # condition_df['wordPosition'].replace({'CallSign':'1','Colour':'2','Number':'3'},inplace=True)
        
        # drop unneeded columns
        condition_df.drop(labels=['tf','stim_code','stimtype','stimulus','voice','block'], axis = 1, inplace = True)
        
        # and, lastly, re-index (because the separation of conditions leads to non-sequential indices, which might lead to errors later)
        reIdx = pd.Series(range(len(condition_df)))
        condition_df.set_index(reIdx, inplace = True)
        
        # Store data in the PreStimManager class
        self.data_array = data_array
        self.condition_df = condition_df
        
        return data_array, condition_df if output else None

#%% # TODO not yet working (wait for Sibylle)
    def get_freqData_singleSubj(self, subjID, output = False, condition = None):
        """
        OPEN FREQUENCY DATA AND RESHAPE FOR THE REGRESSION (SINGLE SUBJECT)
        =======================================================================
        # TODO document
        
        Parameters
        ----------
        subjID : str
            The subject ID. This will be used to get the directory of the epoched data,
            and will be stored in the PreStimManager object for later use.
        
        condition : str, default None
            Only get the data from trials of this condition. 
            Must be in the form of the event_id used to filter epochs with mne, like
            with the use of epoch['SomeCondition'].
            It is possible to set multiple conditions by separating the labels with /
            Example: `condition = 'NV/Lv1'` <-- will only get data from trials with NV and Lv1 degradation
                   
        output : bool, default = False
            Whether data_array and condition_df should be returned. The default is False.
            In both cases, data_array and condition_df will be stored in the PreStimManager object.
            The function run_LogitRegression_WithinSubj() will default to using the array/df saved
            internally in the PreStimManager-class.
            Therefore, setting output to False might optimise memory usage.
            
            (If you later decide you do want them in the variable explorer, 
             call `data_array = PreStimManager.data_array` )


        Returns
        -------
        If output == False (default):
            None
        
        If output == True:
            data_array : numpy array
                numpy array of shape [n_epochs, n_channels, n_times]
                
            condition_df : pandas dataframe
                pandas dataframe, containing accuracy, levels, noiseType for every trial

        """
        raise NotImplementedError()
        
        
        self.subjID = subjID
        self.metadata['subjectID'] = subjID
        
        # get filepath, read pickle
        freq_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.freqPickleFileEnd)), recursive=True)[0]
        with open(freq_path, 'rb') as f:
            tfr_band = pickle.load(f)
        self.metadata['frequency_dict_path'] = freq_path

        # TODO get a way to loop over freqband without having to unpickle the dict every time
        data_array = tfr_band['Alpha_data'] # data is an array of shape [n_epochs, n_channels, n_times]
        condition_df = tfr_band['epoch_metadata'] # trial information

        # TODO
        # subset epochs to the desired condition
        if condition:
            epo = epo[condition]
            self.metadata['condition'] = condition
        
        # add channel names and time in seconds to metadata
        self.metadata['ch_names'] = tfr_band['metadata']['ch_names']
        self.metadata['times'] = epo._raw_times[0:-1] #TODO
        
        
        # re-name some columns
        condition_df['noiseType'] = condition_df['block'] 
        condition_df['wordPosition'] = condition_df['stimtype'] 

        # Re-coding is necessary for the DV (needs to be numeric, not string)
        condition_df['accuracy'].replace({'inc': 0, 'cor': 1}, inplace=True)
        # condition_df['wordPosition'].replace({'CallSign':'1','Colour':'2','Number':'3'},inplace=True)
        
        # drop unneeded columns
        condition_df.drop(labels=['tf','stim_code','stimtype','stimulus','voice','block'], axis = 1, inplace = True)
        
        # and, lastly, re-index (because the separation of conditions leads to non-sequential indices, which might lead to errors later)
        reIdx = pd.Series(range(len(condition_df)))
        condition_df.set_index(reIdx, inplace = True)
        
        # Store data in the PreStimManager class
        self.data_array = data_array
        self.condition_df = condition_df
        
        return data_array, condition_df if output else None
    
#%% 
    def run_LogitRegression_withinSubj(self, 
                data_array = None, 
                condition_df = None,
                formula = "accuracy ~ levels * eeg_data + wordPosition", 
                n_iter = 100, 
                sub_sample = True,
                solver = "lbfgs"
                ):
        """
        LOGIT REGRESSION WITHIN SUBJECT
        =======================================================================
             
        Regression for binary DV. 
     
        In case of sub_sample = True, will equalise trial numbers of correct and
        incorrect trials by calling the function PreStimManager.random_subsample_accuracy().
        For more information, see docstring of that function.
        
        If sub_sample = False, n_iter will be overwritten as 1.
        
        Results will not be returned but stored in the PreStimManager class object.
        If needed, they can be called by `SomeVariable = PreStimManager.DesiredResult`
        (substituting DesiredResult by one of the results below)
        
        These results are collected:
            p_values : array of shape [n_channels, n_times, n_coefficient, n_iter]
                The p-Values of all regression coefficients for each channel, timepoint, and iteration.
                
            coefficients : array of shape [n_channels, n_times, n_coefficient, n_iter]
                Each regression coefficient for each channel, timepoint, and iteration.
                
            coef_SD : array of shape [n_channels, n_times, n_coefficient, n_iter]
                The standard deviation of each regression coefficient for each channel, timepoint, and iteration.

                
            z_values : array of shape [n_channels, n_times, n_coefficient, n_iter]
                The z-Values of all regression coefficients for each channel, timepoint, and iteration.

            p_values_mean : array of shape [n_channels, n_times, n_coefficient]
                The p-Values of all regression coefficients for each channel, timepoint, but
                averaged over the iterations.
                Will only be calculated if sub_sample = True
                
            p_values_SD : array of shape [n_channels, n_times, n_coefficient]
                The standard deviation of the p-Values across iterations
                Will only be calculated if sub_sample = True
            
                 

        Parameters
        ----------
        data_array : array of shape [n_epochs, n_channels, n_times] or None; optional
            # !!! Notice !!! Currently not working if data_array is not None
            The array containing the data. 
            The default is None, in which case the data_array stored in the 
            PreStimManager class is used (meaning, the data_array from the previous call of 
            `PreStimManager.get_epoData_singleSubj()` or `PreStimManager.get_freqData_singleSubj()` )
            
        condition_df : dataFrame or None; optional
            # !!! Notice !!! Currently not working if condition_df is not None
            The dataframe containing the trial information such as accuracy, condition, etc.
            The default is None, in which case the condition_df stored in the 
            PreStimManager class is used (meaning, the condition_df from the previous call of 
            `PreStimManager.get_epoData_singleSubj()` or `PreStimManager.get_freqData_singleSubj()` )

        formula : str, optional
            The formula to be passed to smf.logit(). 
            The default is "accuracy ~ levels * eeg_data + wordPosition".
        
        sub_sample : bool, optional
            Whether to equalise trial-number of correct and incorrect trials
            by randomly subsampling the data. 
            The default is True.

        n_iter : int, optional
            How many iterations of subsampling and regression should be done. 
            This option is only available if sub_sample is set to True, otherwise,
            n_iter will be overwritten as 1.
            The default is 100.
            
        solver : str, optional
            The solver to be used when calling `mdf = md.fit(method = solver)`.
            For information on the solvers, see documentation on statsmodels:
                https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.Logit.fit.html
                https://www.statsmodels.org/stable/dev/generated/statsmodels.base.model.LikelihoodModelResults.html
            The default is "lbfgs", which appears to be the fastest. The default of the function
            would be "newton", which causes LinAlgError in some subjects (see comment in the README)

        Returns
        -------
        None.

        """

        self.metadata['fitting_solver'] = solver
        
        #  TODO does not actually work if input is not none
        # If no data given, use the data stored in the class object
        if data_array == None:
            data_array = self.data_array
        else:
            pass
        
        if condition_df == None:
            condition_df = self.condition_df
        else:
            pass
            
        if not sub_sample: # do not iterate if no sub-sampling is performed
            n_iter = 1
        self.withinSubj = True # we use this later for the filenames
        
        #% Create arrays and lists
        channelsIdx = [i for i in range(data_array.shape[1])] # list of channels
        timesIdx = [i for i in range(data_array.shape[2])] #list of timepoints
        
        
        # This will run a preliminary model, which is only used to extract the number of p-Values
        # Which is needed to create an empty array for the p-Values
        tmp_df = pd.DataFrame()
  
        tmp_df = condition_df
        tmp_df['eeg_data'] = data_array[:,0,0]
        pVals_n = len(smf.logit(formula, 
                                tmp_df
                                ).fit().pvalues.index)
        del tmp_df

        # now we know the dimensions of the empty array we need to create to collect p_Values
        p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n,n_iter))
        coefficients = np.zeros(shape=p_values.shape)
        z_values = np.zeros(shape=p_values.shape)
        coef_SD = np.zeros(shape=p_values.shape)
        
        
        # But gfraga also asked to save the whole model output, soooo... # TODO
        # Actually, I opted not to do that because n_iter*n_times*n_channels mdf objects would be... a lot


        for iteration in range(n_iter):

            if sub_sample:
                # we sub-sample running the function below. which will give us a set of indices (idx)
                # and later we subset the data by idx
                idx = self.random_subsample_accuracy()

            else: # if no sub-sampling is asked for, just get every idx
                idx = [ids for ids in range(len(condition_df))]


            # And now we run the model for every channel and every timepoint
            for thisChannel in channelsIdx:



                for tf in timesIdx:

                    # extract the data & trial information at a given timepoint and channel              
                    df = condition_df
                    df['eeg_data'] = data_array[:,thisChannel,tf]
                    df = df.iloc[idx] # subset the df by idx
                    
                    
                    # calculate Logit regression
                    md = smf.logit(formula, 
                                   df, 
                                   )  

                    
                    mdf = md.fit(method = solver) # ??? don't know what the correct solver is
                    
                    # record p-Values, z-Values and coefficients
                    p_values[thisChannel,tf,:, iteration] = mdf.pvalues
                    coefficients[thisChannel,tf,:, iteration] = mdf.params
                    coef_SD[thisChannel,tf,:, iteration] = mdf.conf_int()[1] - mdf.params
                    z_values[thisChannel,tf,:, iteration] = mdf.tvalues
 
        
        if sub_sample: # get mean and sd of the p-Values across iterations
            self.p_values_mean = p_values.mean(axis = 3)
            self.p_values_SD = p_values.std(axis = 3)
        else:
            pass
        
        self.p_values = p_values
        self.coefficients = coefficients
        self.z_values = z_values
        self.coef_SD = coef_SD
        

        self.metadata['p_Values_index'] = mdf.pvalues.index
        self.metadata['regression_formula'] = md.formula
        self.metadata['regression_groups'] = "NONE"
        self.metadata['regression_type'] = str(mdf.model)
        self.metadata['FDR_correction'] = False # This will change to True once the FDR is run
        self.metadata['axes'] = ['channel, timeframe, p-Value']
        self.metadata['iterations'] = n_iter
        self.metadata['equalized_accuracy_sample'] = sub_sample
        
        if sub_sample:
            self.metadata['sub_sample_dataframe_length'] = len(df)

#%% # TODO organise documentation
    def random_subsample_accuracy(self, trial_info = None):
        """
        RANDOMLY SUBSAMPLES TRIAL TO EQUALISE ACCURACY COUNTS
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

        # TODO this does not currently account for uneven numbers of wordPosition, or levels that could result from this
        # (see comment below, which is copy-pasted from sketch_PreStim_writing)
           
# # next we would need to get the minimum number of cor & inc of each combination of subjID, levels, wordPosition
# # and then select that many trials from every combination of accuracy, subjID, levels and wordPosition
# # but that's not possible since some subj are 100% correct on some of those combinations.
# # even when not accounting for word position, and only for subjID and levels - roughly a fourth of combinations are >90% correct
# # meaning that accounting for accuracy, subjID and levels for the sub-sampling will give us only about 10% of the data for each sample

# newdf = stacked_cond_df.drop(labels=['wordPosition','noiseType', 'levels'], axis = 1, inplace = False)
# tmp = newdf.groupby(['subjID']).sum() # when only accounting for subjID
# max(tmp['accuracy']) 
# # 530 correct out of 576. Which would mean we would sub-sample 46 correct and incorrect trials of every subj
# # for a total of 1288 trials per sub-sample. We would reduce the dataset by a sixth of its size.
# # Only accounting for accuracy results in a sub-sample of 2924 trials - reducing the dataset by a third of its size

        if not trial_info: 
# TODO : account for if input is dict - 
# maybe take the concat out of the if loop and do another if-loop outside, i.e. `if trial_info.type=dict: concat`
            try:
                trial_info = self.condition_dict
                # combine all subj condition dataframes to get across-subj accuracy
                # TODO for within-subj (see comment in sketch_PreStim_writing)
                tmp_df = pd.concat(trial_info.values(), axis=0, ignore_index=True)
            except AttributeError:
                try:
                    tmp_df = self.condition_df
                except AttributeError:
                    raise AttributeError("cannot subsample data - no trial information (condition_dict or condition_df) found")
        
        
        # counting total correct and incorrect
        count_cor = tmp_df['accuracy'].value_counts()[1]
        count_inc = tmp_df['accuracy'].value_counts()[0]

        idx_cor = tmp_df.index[tmp_df['accuracy'] == 1]
        idx_inc = tmp_df.index[tmp_df['accuracy'] == 0]

        minimum = min(count_cor, count_inc)
        subsample_idx = random.sample(list(idx_cor), minimum) + random.sample(list(idx_inc), minimum)


        return subsample_idx

#%% # TODO - not working anymore because of the higher dimension of the p-Values array

    def FDR_correction(self, p_values = None, alpha = 0.05, output = False):
        """
        FDR CORRECTION
        =======================================================================
        
        This function will FDR-correct p_values. The correction is separately run
        for each channel and parameter - therefore, we only correct for repeated measures in time
        but not for the multiple channels.


        Parameters
        ----------
        p_values : array of shape [n_channels, n_timepoints, n_pValues], optional
            The p-Values that should be FDR corrected. The default is None, in which case
            the p-Values stored in the PreStimManager class are used (meaning `PreStimManager.p_values`).
            Therefore, with `p_values = None`, the p-Values of the last performed regression are FDR-corrected.
            
        alpha : float, Default = 0.05
            The alpha value for the FDR. The default is 0.05.
            
        output : bool, Default = False
            Whether or not the FDR-corrected p-Values should be returned. The default is False.
            In both cases, p_values_FDR will be stored in the PreStimManager object.
            The function save_pValues() will default to using the p_values from the PreStimManager object.
            Therefore, setting output to False will optimise memory usage.
            
            (If you later decide you do want them in the variable explorer, 
             call `p_values_FDR = PreStimManager.p_values_FDR` )

        Raises
        ------
        ValueError
            If the p_values are already FDR-corrected, raises an error. 
            The function uses the metadata to check if the p_values are already FDR-corrected.

        Returns
        -------
        If output = False : Nothing
        
        If output = True :      
            p_values_FDR : array of shape [n_channels, n_timepoints, n_pValues]
                the FDR-corrected p-Values

        """
    
        print('Time for the FDR.................................................................')
    
        if not p_values:
            p_values = self.p_values
            if self.metadata['FDR_correction']:
                raise ValueError('data is already FDR corrected')
        else: 
            if p_values['metadata']['FDR_correction']:
                raise ValueError('data is already FDR corrected')
            p_values = p_values.p_values
        
        # make empty array
        p_values_FDR = np.zeros(shape=p_values.shape) # They are of shape `p_values[thisChannel,tf,:] = mdf.pvalues`
        
        #
        for channelsIdx in range(p_values.shape[0]):
            for pValsIdx in range(p_values.shape[2]):
                rej, temp_pValsFDR = ssm.fdrcorrection(p_values[channelsIdx, :, pValsIdx], alpha = alpha) # get FDR corrected p-Values
                p_values_FDR[channelsIdx, :, pValsIdx] = temp_pValsFDR

        print('done! ...........................................................................')
        
        self.p_values_FDR = p_values_FDR
        self.metadata['FDR_correction'] = True
        self.metadata['FDR_alpha'] = alpha
        
        return p_values_FDR if output else None

#%%  #TODO document
    def save_pValues(self, addMetadata = True):
# TODO
        self.metadata["datetime_run_end"] = str(datetime.now())
        output_dict = {'metadata':self.metadata} # create a dict and add the metadata we collected
        
        # Now add the p-Values to the dict. First try to add the FDR-corrected p-Values 
        # and if there are none, add non-FDR-corrected p-Values
        try:
            output_dict['p_values'] = self.p_values_FDR
            FDR_name = 'FDR_'
        except AttributeError:
            output_dict['p_values'] = self.p_values
            FDR_name = 'uncorrected_'
    
        try:
            output_dict['z_values'] = self.z_values
            output_dict['coefficients'] = self.coefficients
            output_dict['coefficients_SD'] = self.coef_SD
            values_name = 'allValues'
        except AttributeError:
            values_name = 'pValues'
            pass
        
        
        # See if there is a condition for the data, so that can be added to the filename
        try:
            condition_name = (str(self.metadata['condition']) + '_')
        except AttributeError:
            condition_name = ''

        # check if the data is sub-sampled to add that to the filename
        if self.metadata['equalized_accuracy_sample']:
            subsample_name = 'sub-sampled_'
            n_iter = str(self.metadata['iterations']) + "iter_"
            try:
                output_dict['p_values_SD'] = self.p_values_SD
                output_dict['p_values_mean'] = self.p_values_mean
            except AttributeError:
                pass
        else:
            subsample_name = ''
            n_iter = ''
            
        # This will take the regression model method that we got from mdf.model()
        # Because mdf.model() gives an output like '<statsmodels.discrete.discrete_model.Logit object at 0x7fbf691a7b50>'
        # We take the position of the final '.' and the first ' ' (blank space) and use the str between those two
        regression_name = str(
            self.metadata['regression_type'][self.metadata['regression_type'].rfind('.')+1:
                                             self.metadata['regression_type'].find(' ')] + '_')
        
        # if there is a within subj design, get the subjID, add that to the output filepath
        if self.withinSubj:
            subjID = self.subjID
            diroutput = const.dirinput + "/" + subjID + "/" + subjID + "_"
        else: # if there is no within subj design, get output filepath from constants
            diroutput = const.diroutput
            
        
            
        filepath = diroutput + regression_name + condition_name + subsample_name + n_iter + FDR_name + values_name + const.pValsPickleFileEnd
        output_dict['metadata']['output_filepath'] = filepath
        with open(filepath, 'wb') as f:
            pickle.dump(output_dict, f)
        print("saving to ",filepath)
        # return output_dict
 
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
        
        print("creating evokeds...")
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
                
        filepath = os.path.join(const.dirinput,const.evokedsPickleFileEnd)
        if save:
            with open(filepath, 'wb') as f:
                pickle.dump(evokeds, f)
            print('evokeds saved to',filepath)
        return evokeds
    
#%% #TODO comment
    def grandaverage_evokeds(self, evokeds):
        evokeds_gAvg= {}
        for condition in const.conditions:
            evokeds_gAvg[condition] = mne.grand_average(evokeds[condition], drop_bads = False, interpolate_bads = False)
        return evokeds_gAvg
    
                
            