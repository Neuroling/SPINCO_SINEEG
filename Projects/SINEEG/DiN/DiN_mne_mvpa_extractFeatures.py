#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------------------------
MVPA MACHINE LEARNING CLASSIFICATION 
[CLASS LABELING AND FEATURE SELECTION] 
---------------------------------------------------------------------------------------------------------------------  
* Reads MNE epoched objects. 
* Labels epochs acording to different classification targets 
* Extracts features 
* Saves X (channel data) and y (labels) and times (time info)

@author: gfraga based on Alexandre Gramfort's demo  https://natmeg.se/mne_multivariate/mne_multivariate.html
Created on Wed Nov 30 10:40:32 2022
"""
import mne
from mne.time_frequency import tfr_morlet
import os
from glob import glob
import scipy.io as sio
import numpy as np
import pandas as pd

# %%  Access epoched data
dirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/'
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/mvpa/25subj_TFR/' 
if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
    
files = glob(dirinput + "s*ICrem.fif", recursive=True)
subjects = [f.split('/')[-1].split('_')[0] for f in files ]

for thisSubject in subjects:
            
            # %% Epoch selection and labeling for classification
            #-----------------------------------------------------------------------------------------            
            # read epoched data 
            epochs = mne.read_epochs(glob(dirinput + thisSubject +'_DiN_epoched_ICrem.fif')[0])
                     
            # take sets of the original events for labeling. Depends what to classify            
            conditions_sets = {'accuracy': ['corr/easy','corr/mid','corr/hard','incorr/easy','incorr/mid','incorr/hard'],
                               'difficulty':['corr/easy','corr/mid','corr/hard','incorr/easy','incorr/mid','incorr/hard']}  
            
            # %% Class (epoch) Labeling 
            for cidx, cset in enumerate(conditions_sets): 
                curEpochs = epochs[conditions_sets[cset]]            
                csetname = list(conditions_sets.keys())[cidx]
                               
                # Recode event depending on conditions of interest
                for ev in range(len(curEpochs.events)):
                        evIdx = int(np.where(list(curEpochs.event_id.values())==curEpochs.events[ev][2])[0]) # for each event numeric code it looks it up in the table of events id                       
                        evLabel = list(curEpochs.event_id.items())[evIdx][0] # find the corresponding label which will indicate correctness/difficulty                                                                   
                        
                        if csetname== list(conditions_sets.keys())[0]:
                           eventDict = {'corr':1,'incorr':0}
                           if evLabel.split('/')[0] == 'corr':
                               newVal = 1
                           elif evLabel.split('/')[0] == 'incorr':
                                newVal = 0                     
                                
                        if  csetname == list(conditions_sets.keys())[1]:
                           eventDict = {'clear':0,'easy':1,'mid':2,'hard':3}                       
                           if evLabel.split('/')[1] == 'hard':
                               newVal = 3
                           elif evLabel.split('/')[1] == 'mid':
                               newVal = 2
                           elif evLabel.split('/')[1] == 'easy':
                               newVal = 1                          
                                
                       #Update the event value with new code 
                        curEpochs.events[ev][2] = newVal             
                        
                # Update labels 
                curEpochs.event_id = eventDict
                print(curEpochs)   
                #del curEpochs
                          
                # Match the number  of epochs if classifying correct/ incorrect trials 
                if csetname== list(conditions_sets.keys())[0]:
                    epochs_list = [curEpochs[k] for k in curEpochs.event_id]
                    print('Equalizing number of epochs' )
                    mne.epochs.equalize_epoch_counts(epochs_list)
                    print('--------')
                
           
                # %% FEATURE SELECTION 
                #-----------------------------------------------------------------------------------------
                # Time-frequency power per epoch for some bands 
                freqs = np.logspace(*np.log10([1, 48]), num=56)
                n_cycles = freqs / 2.  # different number of cycle per frequency
                power = tfr_morlet(curEpochs, freqs=freqs, decim= 3, n_cycles=3, average=False, use_fft=True, return_itc=False,n_jobs=4)
                                    
                                    
                # Extract frequency bands:
                df = power.to_data_frame(time_format=None)  
                freq_bounds = {'_': 0,
                               'delta': 4,
                               'theta': 8,
                               'alpha': 13,
                               'beta': 35,
                               'gamma': 140}
                
                df['band'] = pd.cut(df['freq'], list(freq_bounds.values()),labels=list(freq_bounds)[1:])
            
                # Filter to retain only relevant frequency bands:
                #freq_bands_of_interest = ['alpha']                
                freq_bands_of_interest = ['delta','theta','alpha','beta','gamma']                
                df = df[df.band.isin(freq_bands_of_interest)]                
                df['band'] = df['band'].cat.remove_unused_categories()
                    
                
                #  LOOP thru frequency bands 
                for thisband in freq_bands_of_interest:                     
                    # Mean 
                    curBandDF = df[df.band.isin([thisband])]
                    dfmean = curBandDF.groupby(['epoch','time']).mean() # add mean per time point of all freqs selected across a selected set of channels
                
                    # Save data in arrays formated for mvpa                     
                    x = []
                    epIds = dfmean.index.get_level_values('epoch').unique()
                    for ep in epIds:
                        thisEpoch = dfmean.filter(regex='^E.*',axis = 1 ).loc[ep].to_numpy().transpose()
                        x.append(thisEpoch)
                        del thisEpoch  
                    X = np.dstack(x)  
                                                                              
                    # X shape must be :  Trials x Channels x TimePoints
                    X = X.transpose(2,0,1)
                    n_times= X.shape[2]
                    
                    # Condition labels (vector of length = X[0])
                    y = np.array([e[2] for e in curEpochs.events])# epochs codes should have dimensions [ n_trials , ]
                    times = power.times
                                
                    # %% [save] ---------------------------------------------------                       
                    dict2save = {'X':X, 'y':y, 'times':times}                 
                    
                    newdiroutput = diroutput # + 'epochs_labels_' + csetname[0:4] 
                    if not os.path.exists(newdiroutput):
                        os.mkdir(newdiroutput)
                        
                    outputfilename = thisSubject + '_epochLabels_' + csetname[0:4] + '_' + thisband  + '.mat'
                    sio.savemat(newdiroutput + '/' +  outputfilename,dict2save)                                                    
                    
                    del df, curEpochs,power, X, y, epochs
                        
# %% Save script
import datetime as dt
import re
filename = newdiroutput +'/script'
timestamp = str(dt.datetime.now())[:19]
timestamp = re.sub(r'[\:-]','', timestamp) # replace unwanted chars 
timestamp = re.sub(r'[\s]','_', timestamp) # with regex and re.sub
print('{}_{}'.format(filename,timestamp))
# not included in output file
out_filename = ('{}_{}'.format(filename,timestamp))
with open(__file__, 'r') as f:
     with open(out_filename, 'w') as out:
         for line in (f.readlines()): #remove last 7 lines
           print(line, end='', file=out)
                    
       



