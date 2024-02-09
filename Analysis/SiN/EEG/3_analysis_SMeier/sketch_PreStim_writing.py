#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 09:01:21 2024

@author: samuemu
"""
#%% Imports
import os
from glob import glob
import mne
import PreStim_constants as const
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np
import pickle

#%% filepaths
subjID = 's001'

dirinput = os.path.join(const.thisDir[:const.thisDir.find(
    'Scripts')] + 'Data', 'SiN', 'derivatives', const.pipeID, const.taskID + '_preproc_epoched')
epo_path = glob(os.path.join(dirinput, subjID, str("*" + const.fifFileEnd)), recursive=True)[0]

pickle_path_in = os.path.join(dirinput[:dirinput.find(
    'derivatives/')] + 'analysis', 'eeg', const.taskID,'features',subjID,subjID + const.inputPickleFileEnd)

#%%
print('opening dict:',pickle_path_in)
with open(pickle_path_in, 'rb') as f:
    tfr_bands = pickle.load(f)
    



#%% create frequency dataset to run the LMM on
df = tfr_bands['epoch_metadata'] # get trial information 
df['data'] = tfr_bands['Alpha_data'][:,0,0] # get data of all trials, at electrode 0, and at timepoint 0
df['subjID'] = [subjID for i in range(len(df))] # Put in a column with the subject ID


#%%
"""
Okay so this is a first draft. A bad one.

It takes a long time to open the pickled dict. Every single analysis takes a full minute to run
because it takes so long to open the dict.

We need to run this analysis for every electrode and every timepoint.
The Theta band has the lowest number of timepoints, 136.
For only the theta band, this script would be complete in 145 hours (6 days).
And we would need to run this for every single freq band.

Which means that this script is so ridiculously badly optimised, that it is almost funny.

#%% Create arrays and lists
thisBand = 'Theta'
channels = [i for i in range(64)]
times = [i for i in range(len(tfr_bands[str(thisBand+"_COI_times")]))]

p_values = np.zeros(shape=(len(channels),len(times),9))

#%% And now the big loop...

for thisChannel in channels:
    for tf in times:
           
        # Create df with the relevant data
        tmp = {}
        for subjID in const.subjIDs:
            pickle_path_in = os.path.join(const.thisDir[:const.thisDir.find(
                'Scripts')] + 'Data', 'SiN','analysis', 'eeg', const.taskID,'features',subjID,subjID + const.inputPickleFileEnd)
            
            print('opening dict:',pickle_path_in)
            with open(pickle_path_in, 'rb') as f:
                tfr_bands = pickle.load(f)
                
            df = tfr_bands['epoch_metadata']
            df['data'] = tfr_bands[str(thisBand+'_data')][:,thisChannel,tf]
        
            del tfr_bands
            
            # re-code and delete unneeded data
            df['subjID'] = [subjID for i in range(len(df))]
            df['levels'].replace('Lv1', 1, inplace=True)
            df['levels'].replace('Lv2', 2, inplace=True)
            df['levels'].replace('Lv3', 3, inplace=True)
            df['accuracy'].replace('inc', 0, inplace=True)
            df['accuracy'].replace('cor', 1, inplace=True)
            df['block'].replace('NV', 0, inplace=True)
            df['block'].replace('SSN', 1, inplace=True)
            df.drop(labels=['tf','stim_code','stimtype','stimulus','voice'], axis = 1, inplace = True)
            
            tmp[subjID]=df
            del df
        
        # Combine all subject's data to one df
        df = pd.concat(tmp.values(), axis=0)
        del tmp
        
        # calculate LMM
        md = smf.mixedlm("accuracy ~ levels * data * block", df, groups = df["subjID"]) 
        del df
        
        # record p-Values
        p_values[thisChannel,tf,:] = md.fit().pvalues
        del md
  
"""

#%% Alright! Let's optimise!

#%% Create arrays and lists
thisBand = 'Theta'
channels = [i for i in range(64)] # list of channels
times = [i for i in range(len(tfr_bands[str(thisBand+"_COI_times")]))] #list of timepoints

p_values = np.zeros(shape=(len(channels),len(times),9)) # empty array for the p_values

#%% First, create a dict of all subj data of thisBand to store in the memory
data_dict = {}
metadata_dict = {}

for subjID in const.subjIDs:
    pickle_path_in = os.path.join(const.thisDir[:const.thisDir.find(
        'Scripts')] + 'Data', 'SiN','analysis', 'eeg', const.taskID,'features',subjID,subjID + const.inputPickleFileEnd)
    
    print('opening dict:',pickle_path_in)
    with open(pickle_path_in, 'rb') as f:
        tfr_bands = pickle.load(f)
    
    data_dict[subjID]=tfr_bands[str(thisBand+'_data')]
    metadata_dict[subjID] = tfr_bands['epoch_metadata']
    
    # re-code and delete unneeded data
    metadata_dict[subjID]['subjID'] = [subjID for i in range(len(metadata_dict[subjID]))]
    metadata_dict[subjID]['levels'].replace('Lv1', 1, inplace=True)
    metadata_dict[subjID]['levels'].replace('Lv2', 2, inplace=True)
    metadata_dict[subjID]['levels'].replace('Lv3', 3, inplace=True)
    metadata_dict[subjID]['accuracy'].replace('inc', 0, inplace=True)
    metadata_dict[subjID]['accuracy'].replace('cor', 1, inplace=True)
    metadata_dict[subjID]['block'].replace('NV', 0, inplace=True)
    metadata_dict[subjID]['block'].replace('SSN', 1, inplace=True)
    metadata_dict[subjID].drop(labels=['tf','stim_code','stimtype','stimulus','voice'], axis = 1, inplace = True)
    
    del tfr_bands



#%% And now loop over that...

for thisChannel in channels:
    print('running channel',thisChannel,'of', len(channels))
    
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
        md = smf.mixedlm("accuracy ~ levels * eeg_data * block", df, groups = df["subjID"])        
        mdf = md.fit()
        
        # record p-Values
        p_values[thisChannel,tf,:] = mdf.pvalues
        
index_p_values = mdf.pvalues.index
formula_LMM = md.formula


#%%
md = smf.mixedlm("accuracy ~ levels + eeg_data + block", df, groups = df["subjID"]) 
mdf = md.fit()
print(mdf.summary())
print(mdf.pvalues)
pvals = mdf.pvalues.index

#%%

md2 = smf.mixedlm('accuracy ~ eeg_data + levels * block', groups = 'subjID', data = df)
mdf2 = md2.fit()
print(mdf2.summary())


###################################################################################################################
#%% And  now let's do that with EEG amplitude instead of tfr-band

epo = mne.read_epochs(epo_path)
epo = epo._get_data(tmax=0)

#%% First, create a dict of all subj data to store in the memory
data_dict = {}
metadata_dict = {}

for subjID in const.subjIDs:
    
    # get filepath
    epo_path = glob(os.path.join(dirinput, subjID, str("*" + const.fifFileEnd)), recursive=True)[0]
    epo = mne.read_epochs(epo_path)

    
    data_dict[subjID] = epo._get_data(tmax = 0) # get data
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
    
    del epo
    
#%% Create arrays and lists

channels = [i for i in range(data_dict[subjID].shape[1])] # list of channels
times = [i for i in range(data_dict[subjID].shape[2])] #list of timepoints

p_values = np.zeros(shape=(len(channels),len(times),9)) # empty array for the p_values
#%% And now loop over that...

for thisChannel in channels:
    print('running channel',thisChannel,'of', len(channels))
    
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
        md = smf.mixedlm("accuracy ~ levels * eeg_data * noiseType", df, groups = "subjID")        
        mdf = md.fit()
        
        # record p-Values
        p_values[thisChannel,tf,:] = mdf.pvalues
        
index_p_values = mdf.pvalues.index
formula_LMM = md.formula


#%%
md = smf.mixedlm("accuracy ~ levels + eeg_data + noiseType", df, groups = 'subjID') 
mdf = md.fit()
print(mdf.summary())
print(mdf.pvalues)
pvals = mdf.pvalues.index

#%% Creating Evoked
# epo=mne.read_epochs(epo_path) # read Epoched .fif file
# epo = epo.crop(-0.5,0) # crop epochs to keep only pre-stimulus interval

# evo_inc = epo['Inc'].average() # Average data per timepoint/electrode for incorrect/correct conditions
# evo_cor = epo['Cor'].average()

# ## Attention! Unequal numbers of trials! It may be necessary to first use 
# ## epochs.equalize_event_counts() before averaging. But that depends on how much
# ## data we are okay with losing.

# # evo_cor_df = evo_cor.to_data_frame(copy=False) # if we need the data as pd.dataframe
# #%% 
# """
# But we need the evoked separately for each condition we want to include.
# For example, if we want to look at how degradation levels affect accuracy, 
# we would need to create 3*2 evoked arrays. Doing this manually is a lot of work.

# epochs.average(by_event_type) would create evoked arrays for every event type
# but we have 288 event types and some of them don't matter, so that is not feasible.

# But! Here is the source code for that: 
#     https://github.com/mne-tools/mne-python/blob/maint/1.6/mne/epochs.py#L1060-L1110
 
#     evokeds = list()
#     for event_type in epochs.event_id.keys():
#             ev = epochs[event_type]._compute_aggregate(picks=picks, mode=method)
#             ev.comment = event_type
#             evokeds.append(ev)
    
#     Meaning basically, if I create a dict of what conditions I want to split the data into,
#     and then use that in place of epochs.event_id.keys() - that would work.
#     I can put that into a function.

# """
# accuracy = ['Cor','Inc']
# degradation = ['Lv1','Lv2','Lv3']
# noise = ['NV','SSN']

# # creating a list of every possible combination of accuracy, noise & degradation, separated by /
# conditions = [x + '/' + y + '/' + z for x in noise for y in degradation for z in accuracy]

# evokeds = {}
# for event_type in conditions:
#         evokeds[event_type] = epo[event_type]._compute_aggregate(picks=None)

# n_trial_per_condition = pd.DataFrame([[i , evokeds[i].nave] for i in evokeds ])


# #%% some plots

# # Visualising global amplitude
# evo_inc.plot(gfp=True, spatial_colors=True)
# evo_cor.plot(gfp=True, spatial_colors=True)

# # Comparing amplitude between conditions
# evokeds=dict(cor=evo_cor, inc=evo_inc)
# picks = [1] #which electrode to compare - if None, will compare GFP
# mne.viz.plot_compare_evokeds(evokeds, picks=picks, combine="mean")

# # And here with confidence intervals
# evokeds = dict(
#     cor=list(epo["Cor"].iter_evoked()),
#     inc=list(epo["Inc"].iter_evoked()),
# )
# mne.viz.plot_compare_evokeds(evokeds, combine="mean", picks=None)
# ## Hm... that's interesting. For subj s001, the GFP before correct trials is way less varied / more stable.
# ## ... actually, that reflects the unequal number of trials per condition (918 correct, 234 incorrect)

# # We can also combine evokeds!
# inc_minus_cor = mne.combine_evoked([evo_inc, evo_cor], weights = [1, -1])
# inc_minus_cor.plot(gfp=True, spatial_colors=True)
# inc_minus_cor.plot_joint()




# # #%% to dataframe
# # epo_df = epo.to_data_frame(copy=False)


# #%%
# df_long # Should have the columns Accuracy, Noise, Degradation, [Every electrode] and the rows as timepoints (128 * 2 * 3 * 2)
# #md = smf.mixedlm("accu ~ noise * levels", df_long, groups = df_long["subj"]) 
# #md = smf.mixedlm("accu ~ noise * levels * itemType", df_long, groups = df_long["subj"]) 
# #mdf = md.fit()