#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 10:40:32 2022



 
@author: gfraga based on Alexandre Gramfort's demo  https://natmeg.se/mne_multivariate/mne_multivariate.html
"""
import os
from glob import glob
#import mne
import scipy.io as sio
import numpy as np
# mne.set_log_level('WARNING') # set log-level to 'WARNING' so the output is less verbose 

# %%  Access epoched data

dirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/mvpa/25subj_TFR/'
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/mvpa/25subj_TFR/results/' 
if not os.path.exists(diroutput): 
    os.mkdir(diroutput)
    
files = glob(dirinput + "s*info_trials_mvpa.mat", recursive=True)
subjects = [f.split('/')[-1].split('_')[0] for f in files ]

for thisSubject in subjects:

            # EEG channel data in format Trials x Channel x Data Point 
            X = sio.loadmat(glob(dirinput + thisSubject +'_prep4mvpa.mat')[0])['x']
            X = np.transpose(X,[2,0,1])
            n_times= X.shape[2]
            
            # Condition labels (vector of length = X[0])
            info =  sio.loadmat(glob(dirinput  + thisSubject +'_info_trials_mvpa.mat')[0])
            y = np.transpose(info['Y']).ravel()  # should have dimensions [ n_trials , ]
            S = info['S'] # subject info
            times = np.transpose(info['times']).ravel()
            # %% 
            from sklearn.svm import SVC
            #from sklearn.cross_validation import cross_val_score, ShuffleSplit
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
                scores_t = cross_val_score(clf, Xt, y, cv=cv, n_jobs=1)
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
            
            # %% save ---------------------------------------------------
            plt.savefig(diroutput + thisSubject + '_decoAccu.jpg')
            plt.close()
