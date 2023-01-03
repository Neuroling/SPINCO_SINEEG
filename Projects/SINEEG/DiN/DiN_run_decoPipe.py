"""
 RUN MVPA ANALYSIS 
#--------------------------------------
- Call functions for selecting epochs and labeling classes
- Call function to extract features 
- Call mvpa classification 

Created on Tue Dec 20 09:37:46 2022
@author: gfraga
"""
# Libraries

import sys
sys.path.insert(0,"/home/d.uzh.ch/gfraga/smbmount/gfraga/scripts_neulin/Projects/SINEEG/functions/" )
from functions_for_classification import *
import mne
import numpy as np
import os
from glob import glob
from mne.decoding import Vectorizer

import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold,cross_validate
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support

# Models
from sklearn import svm

#----
#  paths
dirinput  = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/'
os.chdir(diroutput)


 
# list files
files = glob(dirinput + "s*.fif", recursive=True)

# File loop: 
#for thisFile in files: 
thisFile = files[0]

# EEG features 
#~~~~~~~~~~~~~~~~~~~~~~
# % Read epochs 
epochs = mne.read_epochs(thisFile)
epochs.info['description'] = thisFile # store source filename 

# % Select epochs and labels
classBy ='accuracy'
[epochs_sel, y, times] = eeg_epochSelect_relabel(epochs, classify_by= classBy,equalize_epoch_count = True)

# % get features
features_dict = eeg_extract_feat(epochs_sel, power=False, spectral_connectivity =False)

# % Data for classification (shape: samples (e.g., trials) x features(e.g., chans) x times)
X = features_dict['tfr_bands']['Alpha']
times = features_dict['tfr'].times


# %% Classifier selection 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas as pd  
import numpy as np  
from sklearn.svm import SVC  
from sklearn.metrics import classification_report, confusion_matrix  
import matplotlib.pyplot as plt

X_2d = X.reshape(len(X), -1)               
X_train, X_test, y_train, y_test = train_test_split(X_2d, y, test_size = 0.20,shuffle=True)
param_grid = {'C': [0.1,1, 10, 100], 'gamma': [1,0.1,0.01,0.001],'kernel': ['rbf', 'poly', 'sigmoid','linear']}
grid = GridSearchCV(SVC(),param_grid,refit=True,verbose=2)
grid.fit(X_train,y_train)

print(grid.best_estimator_)

grid_predictions = grid.predict(X_test)
print(confusion_matrix(y_test,grid_predictions))
print(classification_report(y_test,grid_predictions))#Output
# %%
import seaborn as sns
sns.pairplot(X,hue='class',palette='Dark2')

# %% Decoding 
#~~~~~~~~~~~~~~~~~~~~~~
# Define an SVM classifier (SVC) 
clf = svm.SVC(C=1, kernel='linear')
cv = 5
scoretype  = 'roc_auc' 
[scores_full, scores, std_scores] = get_crossval_scores(X, y, clf, cv, scoretype)

# % Plot accuracy scores 
title = [str(clf) + '_CV('  + str(cv) + ')' ]
fig  = plot_decoding_scores(scores, std_scores, scores_full, times,title,scoretype)

#%% 

# # define a monte-carlo cross validation generator (to reduce variance) : 
# #  cv = ShuffleSplit(len(X), n_splits = 10, test_size=0.2, random_state=42)
# cv = sklearn.ShuffleSplit(n_splits = 10, test_size=0.2, random_state=42)
# cv = 5 # k-fold validation 
# # This will learn on 80 % of the epochs and evaluate the remaining 20 % (test_size = ) to predict accurcay 

# # % 
# # Classify using all time points 
# X_2d = X.reshape(len(X), -1)
# X_2d = X_2d / np.std(X_2d)
# scores_full = cross_val_score(estimator = clf, 
#                               X = X_2d, 
#                               y= y, 
#                               cv=cv, 
#                               n_jobs=8)

# print("Classification score: %s (std. %s)" % (np.mean(scores_full), np.std(scores_full)))

# # % classify running the decoder at each time point 
# scores = np.empty(n_times)
# std_scores = np.empty(n_times)

# for t in range(n_times):
#     Xt = X[:, :, t]
#     # Standardize features
#     Xt -= Xt.mean(axis=0)
#     Xt /= Xt.std(axis=0)
#     # Run cross-validation
#     scores_t = cross_val_score(clf, Xt, y, cv=cv, n_jobs=8)
#     scores[t] = scores_t.mean()
#     std_scores[t] = scores_t.std()









# # %% 



# train_data_UN, test_data_UN, labels_train_UN, labels_test_UN = train_test_split(X, y, test_size=0.3, random_state=42)
# #svm
# clf_svm_pip = make_pipeline(Vectorizer(),svm.SVC(random_state=42))
# parameters = {'svc__kernel':['linear', 'rbf', 'sigmoid'], 'svc__C':[0.1, 1, 10]}
# gs_cv_svm = GridSearchCV(clf_svm_pip, 
#                          parameters, 
#                          scoring='accuracy', 
#                          cv=StratifiedKFold(n_splits=5),
#                          return_train_score=True)

# # Get info about 
# gs_cv_svm.fit(train_data_UN, labels_train_UN)
# print('Best Parameters: {}'.format(gs_cv_svm.best_params_))
# print('Best Score: {}'.format(gs_cv_svm.best_score_))