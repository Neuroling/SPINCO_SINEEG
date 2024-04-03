#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test/writing Script for the MVPA
===============================================================================
author: samuemu
Created on Fri Jan 12 13:24:52 2024



"""
import os
import pickle
thisDir = os.path.dirname(__file__)

from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold, cross_validate, KFold
from sklearn import metrics
from sklearn import svm
import numpy as np
import pandas as pd

import MVPA_constants as const
import MVPA_functions as functions
MVPAManager = functions.MVPAManager()


conditionInclude = ['Lv3', 'NV'] 
conditionExculde = []
response_variable = 'accuracy'
timewindow = "_prestim" # other option : '_poststim'
thisBand = 'Alpha'


#%% setting filepaths 
subjID = 's001'
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','analysis', 'eeg',
                        const.taskID,'features',subjID)
pickle_path_in = os.path.join(dirinput, subjID + timewindow + const.inputPickleFileEnd)


#%% Open the dict 
print('opening dict:',pickle_path_in)
with open(pickle_path_in, 'rb') as f:
    tfr_bands = pickle.load(f)
    
#%% Filter conditions using the user inputs
idx = list(MVPAManager.getFilteredIdx(
    tfr_bands['epoch_conditions'], 
    conditionInclude=conditionInclude, 
    conditionExclude=conditionExculde))

#%%

#%% Get crossvalidation scores
y = tfr_bands['epoch_metadata'][response_variable][idx] # What variable we want to predict (set in the user inputs) - these are the class labels
true_accuracy = y.value_counts().iloc[0]/len(y) # percentage of correct responses by the subj. 
# If the classifier always predicts "cor" then it will be correct in this much.

X = tfr_bands[str(thisBand +'_data')][idx,:,:] # Get only the trials that are in the specified conditions (user inputs)
# X_2d = X.reshape(len(X), -1)

#%%
# clf = svm.SVC(C=1, kernel = 'linear')
# clf_params = clf.get_params()

# estim = clf.fit(X_2d, y)
# estim.score(X_2d,y)
# estim.predict(X_2d)

#%% Get Crossvalidation scores
# scoretype=['accuracy','roc_auc', 'balanced_accuracy']
# cv = None
# all_scores_full = cross_validate(estimator = clf, # So this basically runs clf.fit(x, y)
#                                   X = X_2d, # the data to fit the model
#                                   y = y,  # target variable to predict
#                                   cv = cv, # cross-validation splitting strategy
#                                   n_jobs = const.n_jobs,
#                                   scoring = scoretype)  


#%% Grid search for optimal parameters
# param_grid = [
#   {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
#   {'C': [1, 10, 100, 1000], 'gamma': ['auto', 'scale', 0.001, 0.0001], 'kernel': ['rbf','poly','sigmoid']},
#  ]  

# gslf = GridSearchCV(estimator = clf, param_grid = param_grid)
# # gslf.get_params()
# gslf = gslf.fit(X_2d, y)
# print(gslf.best_params_)

# # Now take a look at glsf.cv_results_.rank_test_score - the different options are now ranked from best to worst
# # and in glsf.best_params_ you can find the best parameters
# # Which... in this case was always the same across options. Weird. # TODO

#%%
# idx_train = list(MVPAManager.getFilteredIdx(
#     tfr_bands['epoch_conditions'], 
#     conditionInclude=['Lv1'], 
#     conditionExclude=[]))

# y_train = tfr_bands['epoch_metadata'][response_variable][idx_train]

# X_train = tfr_bands[str(thisBand +'_data')][idx_train,:,:] # Get only the trials that are in the specified conditions (user inputs)
# X_2d_train = X_train.reshape(len(X_train), -1)

# idx_test = list(MVPAManager.getFilteredIdx(
#     tfr_bands['epoch_conditions'], 
#     conditionInclude=['Lv3'], 
#     conditionExclude=[]))

# y_test = tfr_bands['epoch_metadata'][response_variable][idx_test]

# X_test = tfr_bands[str(thisBand +'_data')][idx_test,:,:] # Get only the trials that are in the specified conditions (user inputs)
# X_2d_test = X_test.reshape(len(X_test), -1)

#%%
# clf = svm.SVC(C=1, kernel = 'linear')
# clf.fit(X_2d_train, y_train)

# clf.score(X_2d_test, y_test)

#%%
# y_train_pred = clf.predict(X_2d_train)
# y_test_pred = clf.predict(X_2d_test)

# f1_cor_train = metrics.f1_score(y_true = y_train, y_pred = y_train_pred, pos_label = 'cor')
# f1_inc_train = metrics.f1_score(y_true = y_train, y_pred = y_train_pred, pos_label = 'inc')


# f1_cor_test = metrics.f1_score(y_true = y_test, y_pred = y_test_pred, pos_label = 'cor')
# f1_inc_test = metrics.f1_score(y_true = y_test, y_pred = y_test_pred, pos_label = 'inc')

#%% Confusion Matrix [[TP, FN],[FP, TN]]
# confusion_matrix_train = metrics.confusion_matrix(y_true = y_train, y_pred = y_train_pred)
# confusion_matrix_test = metrics.confusion_matrix(y_true = y_test, y_pred = y_test_pred)


#%% Grid search over timepoints
param_grid = [
  {'kernel': ['linear'],'C': [1, 10, 100, 1000]},
  {'kernel': ['rbf','poly','sigmoid'],'C': [1, 10, 100, 1000], 'gamma': ['auto', 'scale', 0.001, 0.0001] },
  ]  

scoretype = ('balanced_accuracy')
clf = svm.SVC(C=1, kernel = 'linear')

n_times = X.shape[2] # get number of timepoints

ranks = np.zeros(shape = (n_times, 52))
mean_score = np.zeros(shape = (n_times, 52))

for t in range(n_times): # for each timepoint...
    Xt = X[:, :, t] # get array of shape (n_epochs, n_channels) for this timepoint
    
    # Standardize features
    Xt -= Xt.mean(axis=0) # subtracts the mean of the row from each value
    Xt /= Xt.std(axis=0) # divides each value by the SD of the row

    gslf = GridSearchCV(estimator = clf, param_grid = param_grid, scoring = scoretype)
    # gslf.get_params()
    gslf = gslf.fit(Xt, y)
    print(gslf.best_params_)
    ranks[t,:] = gslf.cv_results_['rank_test_score']
    mean_score[t, :] = gslf.cv_results_['mean_test_score']

last_results = gslf.cv_results_
params = [ str(item) for item in gslf.cv_results_['params']]
data = { 'mean_rank' : ranks.mean(axis = 0), 'mean_score' : mean_score.mean(axis = 0)}
df = pd.DataFrame(data, index = params)
