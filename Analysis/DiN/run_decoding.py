"""
 RUN MVPA ANALYSIS 
#--------------------------------------
- Selects epochs and labels classes
- Call function to extract features (time-freq, or other options)
- Calls mvpa classification  (whole epoch & time-resolved decoding)

Created on Tue Dec 20 09:37:46 2022
@author: gfraga
"""

""" 
TO DOs : 
   - Insert time-window selection for decoding (crop epoch, after COI extract- WARNING: time idxs differ across freq bands!)
   - Optional selection of classifier type by cross-validation (based on what though, time-window-based decoding?)   
   - Optional tunning of hyperparameters by cross-validation (based on what though, time-window-based  decoding?)
   - Stats on CV scores (function + call )
   - Compare decoding across freq bands
   - 

TO Think: 
    - Standardization of features when using time-freq?
    - Choice of cross validation 

""" 

# Libraries
import sys
import numpy as np
import os
from glob import glob
import mne
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

# %% paths 
homedir = 'V:/' if os.name == 'nt' else '/home/d.uzh.ch/gfraga/smbmount/'
sys.path.append(homedir + "gfraga/scripts_neulin/Projects/SINEEG/functions/")
from mvpa_funs import EEG_epochSelect_relabel,EEG_extract_feat, EEG_tfr_cone_of_influence, EEG_tfr_extract_freqBands,get_crossval_scores, plot_decoding_scores
dirinput  = homedir + 'spinco_data/SINEEG/DiN/data_preproc_ep_ICrem/epochs/' 
diroutput = homedir + 'spinco_data/SINEEG/DiN/mvpa/'
os.chdir(diroutput)
 
# list files
files = glob(dirinput + "s*.fif", recursive=True)
thisFile = files[0]

# Option to run without saving
saveme = False

# %% File loop: 
for thisFile in files:         

    # %% 
    # EEG features 
    #======================================================================
    # % Read epochs 
    epochs = mne.read_epochs(thisFile)
    epochs.info['description'] = thisFile # store source filename 
    
    # % Select and get class labels  [FUN]
    classBy ='accuracy'
    [epochs_sel, y, times] = EEG_epochSelect_relabel(epochs, classify_by= classBy,equalize_epoch_count = True, crop_epoch_times=None)  
        
    
    # % Time-frequency analysis
    freqs = np.logspace(*np.log10([1, 48]), num=56)
    n_cycles = 3
    features_dict = EEG_extract_feat(epochs_sel, TFR=True,power=False, spectral_connectivity=False)        
    
    # Cone of influence (for tfr. ACHTUNG! each freq band will have different time idxs!)
    featureType='tfr'
    feat_df = EEG_tfr_cone_of_influence(features_dict[featureType])    
    
    # Extract power per freq bands        
    feat_bands = EEG_tfr_extract_freqBands(feat_df)    #feat_bands should be a dict with keys like 'Alpha' and 'times_Alpha' 
    
    
    # band loop
    for freqBand in feat_bands['freqbands']:                
#    for freqBand in feat_bands['Alpha']:                       
        
    # %% Decoding 
        #=========================        
        #  data prep. Shape: samples (e.g., trials) x features(e.g., chans) x times
        X = feat_bands[freqBand]
        times = feat_bands['times_'+freqBand]
        
        
        # Define classifier, cross validation and score types
        clf = svm.SVC(C=1, kernel='linear')
        cv = 5       
        scoretype = ['accuracy','f1','roc_auc']
        
        #Get cross validation vals [FUN]        
        [scores_full, scores, std_scores] = get_crossval_scores(X, y, clf, cv, scoretype)
        
               
        # %% Plot classification scores 
        #---------------------------------- 
        title = [str(clf) + '_CV('  + str(cv) + ')' ]
        figures = [] # This will yield a list of figures
        for score2plot in scoretype:
            sc = scores[score2plot]
            ss = std_scores[score2plot]
            sf = scores_full['test_'+ score2plot]
            figures.append(plot_decoding_scores(sc, ss,sf, times,title,score2plot))        
            
        
        # %% Save (optional)
        if saveme:
            # informative outputdirectory per model  
            decodeInf = str(clf).split('(')[0] + '_' +  str(clf.kernel) + '_c' + str(clf.C) + '_cv' + str(cv)
            newdir = diroutput + featureType + '_' + decodeInf + '/' + os.path.basename(thisFile).split('_')[0] + '_labels-' + classBy
            os.makedirs(newdir, exist_ok=True)
            os.chdir(newdir)
            #File suffix
            outputSuffix = '_' + featureType + '_' + freqBand + '.npy'
            
            # data matrix, labels and figures
            np.save('X'+outputSuffix, X)
            np.save('Y.npy',y)
            np.save('Figs'+outputSuffix,figures)
            for i, fig in enumerate(figures):
                 fig.savefig('FIG_' + scoretype[i] + outputSuffix.replace('.npy','.jpg') )
            
            # Log file 
            with open('README.txt', 'w') as f:      
                 f.write("Trials labeled by: " + classBy + ".\n")
                 f.write("Feature: " + featureType + ".\n")    
                 f.write("Classifier: " + str(clf) + ".\n")
                 f.write("Cross-validation: " + str(cv) + ".\n")
        
            
        
# %%%%%%%%%%%%%%% 
       
        

### SKETCHES:         
# %% [just testing]  Print tree view 
#for root, dirs, files in os.walk(diroutput_curr):
 #   print(root)
 #   for subdir in dirs:
 #       print(f'\t{subdir}')
 #   for file in files:
 #       print(f'\t\t{file}')

    #
    #sns.pairplot(X,hue='class',palette='Dark2')

