#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------------------------
MACHINE LEARNING CLASSIFICATION 
---------------------------------------------------------------------------------------------------------------------  
* Reads MNE epoched objects. 
* Labels epochs acording to different classification targets 
* Extracts features 
* Run a classifier and a cross validation method


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


# mne.set_log_level('WARNING') # set log-level to 'WARNING' so the output is less verbose 

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
                               'difficulty':['corr/clear','corr/easy','corr/mid','corr/hard','incorr/clear','incorr/easy','incorr/mid','incorr/hard']}  
            
            # %%
            for cidx, cset in enumerate(conditions_sets): 
                curEpochs = epochs[conditions_sets[cset]]            
                csetname = list(conditions_sets.keys())[cidx]
                               
                # Recode event depending on conditions of interest
                for ev in range(len(curEpochs.events)):
                        evIdx = int(np.where(list(curEpochs.event_id.values())==curEpochs.events[ev][2])[0]) # for each event numeric code it looks it up in the table of events id                       
                        evLabel = list(curEpochs.event_id.items())[evIdx][0] # find the corresponding label which will indicate correctness/difficulty                                                                   
                        if  csetname == 'difficulty':
                           eventDict = {'clear':0,'easy':1,'mid':2,'hard':3}                       
                           if evLabel.split('/')[1] == 'hard':
                               newVal = 3
                           elif evLabel.split('/')[1] == 'mid':
                               newVal = 2
                           elif evLabel.split('/')[1] == 'easy':
                               newVal = 1                          
                           elif evLabel.split('/')[1] == 'clear':
                               newVal = 0                          
    
                        if csetname== 'accuracy':
                           eventDict = {'corr':1,'incorr':0}
                           if evLabel.split('/')[0] == 'corr':
                               newVal = 1
                           elif evLabel.split('/')[0] == 'incorr':
                                newVal = 0                     
                                
                       #Update the event value with new code 
                        curEpochs.events[ev][2] = newVal             
                        
                # Update labels 
                curEpochs.event_id = eventDict
                print(curEpochs)   
                #del curEpochs
                          
                # Match the number  of epochs if classifying correct/ incorrect trials 
                if csetname== 'accuracy':
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
                freq_bands_of_interest = ['delta','theta','alpha','beta','gamma']                
                df = df[df.band.isin(freq_bands_of_interest)]                
                df['band'] = df['band'].cat.remove_unused_categories()
                    
                
                
                # %%  LOOP thru frequency bands 
                for thisband in freq_bands_of_interest:                     
                    # Mean 
                    curBandDF = df[df.band.isin([thisband])]
                    dfmean = curBandDF.groupby(['epoch','time']).mean() # add mean per time point of all freqs selected across a selected set of channels
                
                    # Save data in arrays formated for mvpa 
                    #----------------------------------------------------------------
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
                    
                    # %% 
                    from sklearn.svm import SVC                    
                    from  sklearn.model_selection import cross_val_score, ShuffleSplit
                    
                    # Define an SVM classifier (SVC) with a linear kernel
                    clf = SVC(C=1, kernel='linear')
                    
                    # define a monte-carlo cross validation generator (to reduce variance) : 
                    #  cv = ShuffleSplit(len(X), n_splits = 10, test_size=0.2, random_state=42)
                    cv = ShuffleSplit(n_splits = 10, test_size=0.2, random_state=42)
                    
                    # This will learn on 80 % of the epochs and evaluate the remaining 20 % (test_size = ) to predict accurcay 
                    
                    # %% 
                    # Classify using all time points 
                    X_2d = X.reshape(len(X), -1)
                    X_2d = X_2d / np.std(X_2d)
                    scores_full = cross_val_score(estimator = clf, 
                                                  X = X_2d, 
                                                  y= y, 
                                                  cv=cv, 
                                                  n_jobs=1)
                    
                    print("Classification score: %s (std. %s)" % (np.mean(scores_full), np.std(scores_full)))
                    
                    # %% classify running the decoder at each time point 
                    scores = np.empty(n_times)
                    std_scores = np.empty(n_times)
                    
                    for t in range(n_times):
                        Xt = X[:, :, t]
                        # Standardize features
                        Xt -= Xt.mean(axis=0)
                        Xt /= Xt.std(axis=0)
                        # Run cross-validation
                        scores_t = cross_val_score(clf, Xt, y, cv=cv, n_jobs=8)
                        scores[t] = scores_t.mean()
                        std_scores[t] = scores_t.std()
                    
                    
                    # %%  Some rescaling
                    times = 1e3 * times # to have times in ms
                    scores *= 100  # make it percentage accuracy
                    std_scores *= 100
                    
                    # %% Plotting 
                    import matplotlib.pyplot as plt
                    
                    plt.plot(times, scores, label="Classif. score")
                    plt.axhline(50, color='k', linestyle='--', label="Chance level")
                    plt.axvline(0, color='r', label='stim onset')
                    plt.axhline(100 * np.mean(scores_full), color='g', label='Accuracy full epoch')
                    plt.legend()
                    hyp_limits = (scores - std_scores, scores + std_scores)
                    plt.fill_between(times, hyp_limits[0], y2=hyp_limits[1], color='b', alpha=0.5)
                    plt.xlabel('Times (ms)')
                    plt.ylabel('CV classification score (% correct)')
                    plt.ylim([30, 100])
                    plt.title('Sensor space decoding')
                    
                    # %% [save] ---------------------------------------------------                       
                    dict2save = {'X':X, 'y':y, 'times':times}                 
                    
                    newdiroutput = diroutput + 'epochs_labels_' + csetname[0:4] 
                    if not os.path.exists(newdiroutput):
                        os.mkdir(newdiroutput)
                        os.mkdir(newdiroutput + '/' + thisband)
                        
                    outputfilename = thisSubject + '_epochLabels_' + csetname[0:4] + '_' + thisband  + '.mat'
                    sio.savemat(newdiroutput + '/' +  outputfilename,dict2save)                                                    
                    
                    dict2save_results = {'scores':scores,'scores_full':scores_full,'scores_t':scores_t}
                    sio.savemat(newdiroutput + '/' +  outputfilename.replace('.mat','_results.mat'),dict2save_results)                                                    
                    
                    # 
                    plt.savefig(newdiroutput + '/' +  outputfilename.replace('.mat','_decoAccu.jpg') )
                    plt.close()

                    
                    
            del df, curEpochs,power, X, y, epochs


# %% 
# import datetime as dt
# import re

# filename = diroutput +'/script'
# timestamp = str(dt.datetime.now())[:19]
# timestamp = re.sub(r'[\:-]','', timestamp) # replace unwanted chars 
# timestamp = re.sub(r'[\s]','_', timestamp) # with regex and re.sub
# print('{}_{}'.format(filename,timestamp))
# # not included in output file
# out_filename = ('{}_{}'.format(filename,timestamp))
# with open(__file__, 'r') as f:
#     with open(out_filename, 'w') as out:
#         for line in (f.readlines()): #remove last 7 lines
#             print(line, end='', file=out)
