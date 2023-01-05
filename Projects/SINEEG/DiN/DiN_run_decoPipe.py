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
import numpy as np
import os
from glob import glob
import mne
#----
#  paths and custom functions
homedir = 'V:/' if os.name == 'nt' else '/home/d.uzh.ch/gfraga/smbmount/'
sys.path.append(homedir + "gfraga/scripts_neulin/Projects/SINEEG/functions/")

from mvpa_funs import EEG_epochSelect_relabel,EEG_extract_feat, get_crossval_scores, plot_decoding_scores
#%%
dirinput  = homedir + 'spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 
diroutput = homedir + 'spinco_data/SINEEG/DiN/mvpa/'
os.chdir(diroutput)
 
# list files
files = glob(dirinput + "s*.fif", recursive=True)

# %% File loop: 
#thisFile = files[0]
for thisFile in files:         

    # %% 
    # EEG features 
    #======================================================================
    # % Read epochs 
    epochs = mne.read_epochs(thisFile)
    epochs.info['description'] = thisFile # store source filename 
    
    # % Select epochs and labels  [FUN]
    classBy ='accuracy'
    [epochs_sel, y, times] = EEG_epochSelect_relabel(epochs, classify_by= classBy,equalize_epoch_count = True, crop_epoch_times=None)  
        
    # % get features [FUN]
    features_dict = EEG_extract_feat(epochs_sel, TFR=True,power=False, spectral_connectivity=False) 
    
    
    # % Select Data for classification (shape: samples (e.g., trials) x features(e.g., chans) x times)
    #---------------------------------
    measure = 'tfr_bands'
    
    #freqBand = 'Alpha' # Select band of interest     
    for freqBand in features_dict['tfr_bands'].keys():        
        
        X = features_dict[measure][freqBand]
        times = features_dict['tfr'].times
        
        # %% Decoding 
        #---------------------------------
        # Define an SVM classifier (SVC)  
        clf = svm.SVC(C=1, kernel='linear')
        cv = 5
        scoretype = ['accuracy','f1','roc_auc']
        
        #Get cross validation scores [FUN]
        [scores_full, scores, std_scores] = get_crossval_scores(X, y, clf, cv, scoretype)
        
        # %% Plot accuracy scores 
        #---------------------------------- 
        title = [str(clf) + '_CV('  + str(cv) + ')' ]
        figures = [] # This will yield a list of figures
        for score2plot in scoretype:
            sc = scores[score2plot]
            ss = std_scores[score2plot]
            sf = scores_full['test_'+ score2plot]
            figures.append(plot_decoding_scores(sc, ss,sf, times,title,score2plot))        
            
        
        # %% Save 
        # Create Output dir 
        decodeInf = str(clf).split('(')[0] + '_' +  str(clf.kernel) + '_c' + str(clf.C) + '_cv' + str(cv)
        newdir = diroutput + measure + '_' + decodeInf + '/' + os.path.basename(thisFile).split('_')[0] + '_labels-' + classBy
        os.makedirs(newdir, exist_ok=True)
        os.chdir(newdir)
        
        #File suffix
        outputSuffix = '_' + measure + '_' + freqBand + '.npy'
        
        # Save data matrix, labels and figures
        np.save('X'+outputSuffix, X)
        np.save('Y.npy',y)
        np.save('Figs'+outputSuffix,figures)
        for i, fig in enumerate(figures):
            fig.savefig('FIG_' + scoretype[i] + outputSuffix.replace('.npy','.jpg') )
        
        
        #%%  Log file 
        with open('README.txt', 'w') as f:
            # Write the desired text to the file
            f.write("Trials labeled by: " + classBy + ".\n")
            f.write("Feature: " + measure + ".\n")    
            f.write("Classifier: " + str(clf) + ".\n")
            f.write("Cross-validation: " + str(cv) + ".\n")
        
            
        
# %%%%%%%%%%%%%%% 
""" 
TO DO NOW : 
    -make a separate function to split the tfr in freq bands
    - checkthe times in the feature dictionary are correct 
    -TFR: 
        - On the TFR object, calculate the cone of influence and use it as a mask 
        - Then allow time window selection for the freq band averaging and X output for classification 
    
What about: 
- Further separate functions? 
- Cross validation based 
- Training set classification scores (not saved currently)

To do: 
    - Stats on CV scores (function + call )

"""        
        
        

# %% [just testing]  Print tree view 
#for root, dirs, files in os.walk(diroutput_curr):
 #   print(root)
 #   for subdir in dirs:
 #       print(f'\t{subdir}')
 #   for file in files:
 #       print(f'\t\t{file}')
 




# %% Classifier selection 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# X_2d = X.reshape(len(X), -1)               
# X_train, X_test, y_train, y_test = train_test_split(X_2d, y, test_size = 0.20,shuffle=True)
# param_grid = {'C': [0.1,1, 10, 100], 'gamma': [1,0.1,0.01,0.001],'kernel': ['rbf', 'poly', 'sigmoid','linear']}
# grid = GridSearchCV(SVC(),param_grid,refit=True,verbose=2)
# grid.fit(X_train,y_train)

# print(grid.best_estimator_)

# grid_predictions = grid.predict(X_test)
# print(confusion_matrix(y_test,grid_predictions))
# print(classification_report(y_test,grid_predictions))#Output

# %%
#sns.pairplot(X,hue='class',palette='Dark2')

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