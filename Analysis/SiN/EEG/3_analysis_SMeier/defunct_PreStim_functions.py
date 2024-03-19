#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OBSOLETE & DEFUNCT PreStim FUNCTIONS
===============================================================================
Created on Tue Mar 19 09:43:16 2024
@author: samuemu

The functions here have been part of the PreStimManager-class, which can be found in the script
PreStim_functions.py

Most are quite well documented, but no longer needed, so I copy-pasted them out of their original
script to keep them on hand in case we can recycle some things.


Some things might need to be changed to be reusable, because they are taken out of their class

"""
import mne
import pandas as pd
import numpy as np
from multiprocessing import Pool
import PreStim_constants as const
import statsmodels.formula.api as smf
import os
from glob import glob

#%% defunct because we now use the single subj data
def get_data(self, output = False, condition = None, tmin = None, tmax = 0):
     """
     OPEN EPOCHED DATA AND RESHAPE IT FOR REGRESSION (between subject)
     =======================================================================
     
     NOTICE: The latest version of the code uses the within-subject data that is
     aquired by get_data_singleSubj()
     This function is not used at the moment (12.03.24) but may be useful again
     in the future.
     
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
         
         data_dict[subjID] = epo.get_data(tmax = tmax, tmin = tmin) # get data as array of shape [n_epochs, n_channels, n_times]
         condition_dict[subjID] = epo.metadata # get trial information
         
         # re-code and delete unneeded data
         condition_dict[subjID]['noiseType'] = condition_dict[subjID]['block'] 
         condition_dict[subjID]['wordPosition'] = condition_dict[subjID]['stimtype'] 
         condition_dict[subjID]['subjID'] = [subjID for i in range(len(condition_dict[subjID]))]
         
         # Re-coding is only necessary for the DV
         condition_dict[subjID]['accuracy'].replace({'inc': 0, 'cor': 1}, inplace=True)
         condition_dict[subjID]['wordPosition'].replace({'CallSign':'1','Colour':'2','Number':'3'},inplace=True)
         # condition_dict[subjID]['levels'].replace({'Lv1': 1, 'Lv2':2,'Lv3':3}, inplace=True)
         # condition_dict[subjID]['noiseType'].replace({'NV': 0, 'SSN':1}, inplace=True)
         condition_dict[subjID].drop(labels=['tf','stim_code','stimtype','stimulus','voice','block'], axis = 1, inplace = True)
         
         
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
     
     return data_dict, condition_dict if output else None
 
#%% obsolete because we no longer do between-subj analyses 
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

#%% defunct because we run logit regressions instead             
def run_LMM(self, 
             data_dict= None, 
             condition_dict = None,
             formula = "accuracy ~ levels * eeg_data + wordPosition", 
             groups = "subjID"):

     
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
             mdf = md.fit(full_output = True) # This gives the convergence warning # ???
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

#%% defunct because we now run the logit regression within subject instead of between subject
def run_LogitRegression(self, 
             data_dict= None, 
             condition_dict = None,
             formula = "accuracy ~ levels * eeg_data + C(wordPosition)", 
             # groups = "subjID",
             n_iter = 500, 
             sub_sample = True
             ):
     """
     LOGIT REGRESSION
     =======================================================================
     
     Regression for binary DV. 
     
     In case of sub_sample = True, will equalise trial numbers of correct and
     incorrect trials by calling the function PreStimManager.random_subsample_accuracy()
     

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
         The default is "accuracy ~ levels * eeg_data + wordPosition".
         
     groups : str, optional - NOT IMPLEMENTED
         ATTENTION!!!! Currently, the logit model DOES NOT account for multilevel data!!!
         Therefore, it is currently not possible to input "groups" as a parameter. 
         The default is "subjID".
         
     sub_sample : bool, optional
         Whether to equalise trial-number of correct and incorrect trials
         by randomly subsampling the data. The default is True.

     n_iter : int, optional
         How many iterations of subsampling and regression should be done. 
         This option is only available if sub_sample is set to True, otherwise,
         n_iter will be overwritten with 1.
         The default is 500.
         
     Returns
     -------
     p_values : array of shape [n_channels, n_times, n_p-Values]
         The p-Values from the regression. If there are multiple iterations, will return the mean.

     """

     # If no data given, use the data stored in the class object
     if not data_dict:
         data_dict = self.data_dict    
     if not condition_dict :
         condition_dict = self.condition_dict
         
     if not sub_sample: # do not iterate if no sub-sampling is performed
         n_iter = 1
     
     # Get a list of all subj in the data_dict
     SubjList = list(data_dict.keys())
     self.metadata['subjects'] = SubjList
     
     if len(SubjList) == 1:
         self.metadata['subject_design'] = "within_Subject"
         self.withinSubj = True # we use this later for the filenames
     else:
         self.metadata['within-subject'] = "between_Subject"
         self.withinSubj = False
     
     #% Create arrays and lists
     channelsIdx = [i for i in range(data_dict[SubjList[0]].shape[1])] # list of channels
     timesIdx = [i for i in range(data_dict[SubjList[0]].shape[2])] #list of timepoints
     # ""data_dict[SubjList[0]].shape"" means this: Get the shape of the dict-entry of the first subj in SubjList
     
     
     # This will run a preliminary model, which is only used to extract the number of p-Values
     # Which is needed to create an empty array for the p-Values
     tmp_dict = {}
     for subjID in SubjList:    
         tmp_dict[subjID] = condition_dict[subjID]
         tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,0,0]
     df = pd.concat(tmp_dict.values(), axis=0)
     pVals_n = len(smf.logit(formula, 
                             df,
                             ).fit().pvalues.index)
     del tmp_dict, df

     # now we know the dimensions of the empty array we need to create to collect p_Values
     p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n))
     
     
     # But gfraga also asked to save the whole model output, soooo... # TODO
     #mdf_dict = {key1: {key2: None for key2 in self.metadata['ch_names']} for key1 in self.metadata['times']}
     
     for i in range(n_iter):
         
         if sub_sample:
             # we sub-sample running the function below. which will give us a set of indices (idx)
             # and later we subset the data by idx
             idx = self.random_subsample_accuracy(condition_dict = condition_dict)
         else: # if no sub-sampling is asked for, just get every idx
             idx = [i for i in range(len(pd.concat(condition_dict.values(), axis=0, ignore_index=True)))]
         
         # And now we run the model for every channel and every timepoint
         for thisChannel in channelsIdx:
             print('>>>> running channel',thisChannel,'of', len(channelsIdx))
             
             for tf in timesIdx:
                    
                 # extract the data & trial information of each subject at a given timepoint and channel
                 tmp_dict = {}
                 for subjID in SubjList:    
                     tmp_dict[subjID] = condition_dict[subjID]
                     tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,thisChannel,tf]
 
                 
                 # Combine all subject's data into one dataframe, so we can run the model on that
                 df = pd.concat(tmp_dict.values(), axis=0,ignore_index=True)
                 df = df.iloc[idx] # subset the df by idx
                 del tmp_dict
                 
                 
                 # calculate Logit regression
                 md = smf.logit(formula, 
                                df, 
                                # groups = groups
                                )  # TODO groups doesn't work >:(
                 
                 mdf = md.fit() # ??? Convergence warning
                 ## https://www.statsmodels.org/stable/generated/statsmodels.formula.api.logit.html
                 
                 # record p-Values 
                 # This adds the p-values to the values already present in the array at the specified location
                 # for the first iteration, the array only contains 0s. Then, with every iteration, 
                 # the array contains the sum of p-values of each channel and tf
                 # and later we will get the mean by dividing by n_iter
                 p_values[thisChannel,tf,:] += mdf.pvalues
 
     
     if sub_sample: # get mean and sd of the p-Values across iterations
         p_values_mean = p_values / n_iter
         self.p_values_SD = np.sqrt(p_values_mean - np.square(p_values_mean))
         self.p_values = p_values_mean

     else:
         self.p_values = p_values

     
     
     self.metadata['p_Values_index'] = mdf.pvalues.index
     self.metadata['regression_formula'] = md.formula
     self.metadata['regression_groups'] = "NONE" # TODO
     self.metadata['regression_type'] = str(mdf.model)
     self.metadata['FDR_correction'] = False # This will change to True once the FDR is run
     self.metadata['axes'] = ['channel, timeframe, p-Value']
     self.metadata['iterations'] = n_iter
     self.metadata['equalized_accuracy_sample'] = sub_sample
     
     if sub_sample:
         self.metadata['sub_sample_dataframe_length'] = len(df)
     
     
     return p_values
 
#%% not working. This was one way to try parallel processing
def run_LogitRegression_withinSubj_parallel(self, 
            data_array = None, 
            condition_df = None,
            formula = "accuracy ~ levels * eeg_data + C(wordPosition)", 
            n_iter = 1000, 
            sub_sample = True
            ):

    raise NotImplementedError("This code is not yet working")
    

    # If no data given, use the data stored in the class object
    if data_array is None:
        data_array = self.data_array
    else:
        pass
    
    if condition_df is None:
        condition_df = self.condition_df
    else:
        pass
        
    if not sub_sample: # do not iterate if no sub-sampling is performed
        n_iter = 1

    self.withinSubj = True # we use this later for the filenames
    self.formula = formula

    
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
    p_values = np.zeros(shape=(len(channelsIdx),len(timesIdx),pVals_n))
    

    for iteration in range(n_iter):
        # print(str(iteration) + "---------------------------------------------")
        
        if sub_sample:
            # we sub-sample running the function below. which will give us a set of indices (idx)
            # and later we subset the data by idx
            self.idx = self.random_subsample_accuracy()
        else: # if no sub-sampling is asked for, just get every idx
            self.idx = [ids for ids in range(len(condition_df))]
        
        # And now we run the model for every channel and every timepoint
        for self.thisChannel in channelsIdx:
            
            if __name__ == "__main__":
                with Pool() as pool:
                    result = pool.map(self.do_regression_timewise, timesIdx)  

###### !!! I've stopped working on this from here on
                # record p-Values 
                # This adds the p-values to the values already present in the array at the specified location
                # for the first iteration, the array only contains 0s. Then, with every iteration, 
                # the array contains the sum of p-values of each channel and tf
                # and later we will get the mean by dividing by n_iter
                p_values[self.thisChannel,tf,:] += mdf.pvalues
 
    
    if sub_sample: # get mean and sd of the p-Values across iterations
        p_values_mean = p_values / n_iter
        self.p_values_SD = np.sqrt(p_values_mean - np.square(p_values_mean))
        self.p_values = p_values_mean

    else:
        self.p_values = p_values

    
    
    self.metadata['p_Values_index'] = mdf.pvalues.index
    self.metadata['regression_formula'] = self.formula
    self.metadata['regression_groups'] = "NONE" 
    self.metadata['regression_type'] = str(mdf.model)
    self.metadata['FDR_correction'] = False # This will change to True once the FDR is run
    self.metadata['axes'] = ['channel, timeframe, p-Value']
    self.metadata['iterations'] = n_iter
    self.metadata['equalized_accuracy_sample'] = sub_sample
    
    if sub_sample:
        self.metadata['sub_sample_dataframe_length'] = len(df)
    
    
    return p_values

#%% Obsolete because this would only be used to implement the parallel processing 
def do_regression_timewise(self,tf):
    raise NotImplementedError()
    # extract the data & trial information at a given timepoint and channel              
    df = self.condition_df # TODO need to change this in case condition_df is provided
    df['eeg_data'] = self.data_array[:,self.thisChannel,tf]

    df = df.iloc[self.idx] # subset the df by idx

    
    
    # calculate Logit regression
    md = smf.logit(self.formula, 
                    df, 
                    )  
    
    mdf = md.fit() # ??? Convergence warning
    ## https://www.statsmodels.org/stable/generated/statsmodels.formula.api.logit.html
    return mdf.pvalued


