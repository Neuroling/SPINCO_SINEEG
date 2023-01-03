import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mne 
from mne.time_frequency import tfr_morlet
from mne_connectivity import spectral_connectivity_epochs
from mne.epochs import equalize_epoch_counts
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold,cross_validate

# % ----------------------------------------------------------

def eeg_epochSelect_relabel(epochs,
                                classify_by,
                                equalize_epoch_count = True):
 
    """Select and relabel epochs for classification
    =================================================================
    Created on Wed Dec 21 13:16:09 2022
    @author: gfraga\n Study-specific function to label classes. 
    - Selects epochs and relabels event names depending on our classification choice
    - Returns selected epochs and an 'y' array with their labels for classification
       
    Parameters
    ----------
    epochs: Instance of 'Epochs'
        Epoched Object from mne. Contains event info
    
    classify_by: str 
        A string indicating your target classification to relabel classes:
            'accuracy' will take epochs correct/incorrect labels (and take only epochs that had noise) 
            
            'difficulty' will use the easy,mid , hard labels (ignoring accuracy and clear epochs)
    
    equalize_epoch_count: bool | Default True 
        If True it will run the mne equalize the number of epochs to classify using mne.epochs.equalize_epoch_counts()                
    
           
    Returns
    -------
    y_epochLabels : dictionary
        A dictionary containing several arrays for the different sets of labels we are interested in 
         
    """      
           
    # sets of the original events for labeling. Depends what to classify            
    conditions_sets = {'accuracy': ['corr/easy','corr/mid','corr/hard','incorr/easy','incorr/mid','incorr/hard'],
                       'difficulty':['corr/easy','corr/mid','corr/hard','incorr/easy','incorr/mid','incorr/hard']}  
    
   
    # Select events depending on conditions of interest
    print('d[0_0]b selecting epochs for classification of [' + classify_by + ']')           
    n_urepoch = len(epochs)    
    epochs_sel = epochs[conditions_sets[classify_by]]         
    print('.....' + str(len(epochs_sel)-n_urepoch) + ' epochs excluded from initial ' + str(n_urepoch) + ' epochs. \n New epoched object has ' + str(len(epochs_sel)) + ' epochs')              
    
    for ev in range(len(epochs_sel.events)):
            evIdx = int(np.where(list(epochs_sel.event_id.values())==epochs_sel.events[ev][2])[0]) # for each event numeric code it looks it up in the table of events id                       
            evLabel = list(epochs_sel.event_id.items())[evIdx][0] # find the corresponding label which will indicate correctness/difficulty                                                                   
            
            if classify_by== list(conditions_sets.keys())[0]:
               eventDict = {'corr':1,'incorr':0}
               if evLabel.split('/')[0] == 'corr':
                   newVal = 1
               elif evLabel.split('/')[0] == 'incorr':
                    newVal = 0                     
               #epochs_sel.event_id={'corr':1, 'incorr':0}
                
            if  classify_by == list(conditions_sets.keys())[1]:
               eventDict = {'clear':0,'easy':1,'mid':2,'hard':3}                       
               if evLabel.split('/')[1] == 'hard':
                   newVal = 3
               elif evLabel.split('/')[1] == 'mid':
                   newVal = 2
               elif evLabel.split('/')[1] == 'easy':
                   newVal = 1                          
               #epochs_sel.event_id={'hard':3, 'mid':2,'easy':1}
            
           #Update the event value with new code 
            epochs_sel.events[ev][2] = newVal             
    # Update labels 
    epochs_sel.event_id = eventDict
    print(epochs_sel)   
    
    if equalize_epoch_count==True:
        print('....equalizing number of epochs between ' + classify_by + ' conditions')
        epochs_sel.equalize_event_counts()     
    
        
    # Save labels in vector
    y = np.array([e[2] for e in epochs_sel.events])# epochs codes should have dimensions [ n_trials , ]
    times = epochs.times

    return epochs_sel,y, times

####################################################################################    
# % ----------------------------------------------------------
    
def eeg_extract_feat(epochs, power = True, TFR = True, spectral_connectivity = True):
 
    """Extract features from EEG epochs
    =================================================================
    Created on Tue Dec 13 16:39:45 2022
    @author: gfraga\n
    Refs:  
    https://mne.tools/stable/index.html ;  
    https://mne.tools/mne-connectivity/
    
    Parameters
    ----------
    epochs: Instance of 'Epochs'
        Epoched Object from mne. Features are extracted per epoch
    
    TFR: bool | (default True)
        True = run time frequency analysis (broadband and per band). False = do not run
        
    power: bool | (default True)
         True = run power analysis (spectrum of the entire epoch). False = do not run 
     
    spectral_connectivity: bool | (default True)   
         True = run connectivity analysis in the entire epoch (broadband and per band). False = do not run
        
    Returns
    -------
    features_dict : dictionary
        A dictionary containing mne objects with the selected features
         
    >>>>> Work in progress
    -----------------------
    spectroTemporalConnectivity: bool | (default True)   
         True = run connectivity analysis in the entire epoch (broadband and per band). False = do not run
         
    """      
    #% Some definitions:    
    freqbands = dict(Delta = [1,4],
                     Theta = [4,8],
                     Alpha=[8,13], 
                     Beta= [13,25],
                     Gamma =[25,48])
    
    features_dict = {}
    
    #%  Analysis
    # Power spectrum per epoch
    if power: 
        print(' ¸.·´¯`·.¸><(((º>  Running spectra per epoch')        
        spec = epochs.compute_psd() # Power Spectrum object has power per epoch, preserves event info from Epochs object
        
        print('Done.')        
        features_dict['spec'] = spec
        
    
    #  Time frequency analysis
    if TFR:                
        print(' ¸.·´¯`·.¸><(((º>  Running time frequency analysis')        
        # Time freq
        freqs = np.logspace(*np.log10([1, 48]), num=56)
        tfr = tfr_morlet(epochs, freqs=freqs, decim= 3, n_cycles=3, average=False, use_fft=True, return_itc=False,n_jobs=8)
        print('Done.')        
        features_dict['tfr'] = tfr
        
        print('>> Creating data set with tfr power per frequency band')
        #Create a data frame with TFR power indicating frequency band
        df = tfr.to_data_frame(time_format=None)  
        freq_bounds =  [0] +  [item[1][1] for item in freqbands.items()] 
        df['band'] = pd.cut(df['freq'], list(freq_bounds),labels=list(freqbands))    
        
        #save averaged power per band in a dictionary
        tfr_bands= {}
        print('>> O_o Adding power averages per band to a dictionary')
        for thisband in list(freqbands):                     
            # Mean 
            curBandDF = df[df.band.isin([thisband])]
            dfmean = curBandDF.groupby(['epoch','time']).mean() # add mean per time point of all freqs selected across a selected set of channels
            
            # Save data in arrays formated for mvpa                     
            x = []
            epIds = dfmean.index.get_level_values('epoch').unique()
            for ep in epIds:
                thisEpoch = dfmean.filter(regex='^E.*',axis = 1 ).loc[ep].to_numpy().transpose() # find columns with channel values (start with E*.) for each epoch and transpose 
                x.append(thisEpoch)
                del thisEpoch  
            X = np.dstack(x)                                                                        
            
            # Add to dictionary in shape:  epochs x Channels x TimePoints
            tfr_bands[thisband] = X.transpose(2,0,1)       
            print('>>> ' + thisband + ' avg per epoch added')
            
    # Add to function output dict
    features_dict['tfr_bands'] = tfr_bands
        
    # % Phase connectivity     
    if spectral_connectivity: 
        print(' ¸.·´¯`·.¸><(((º>  Running spectral connectivity per band')
        method = 'pli2_unbiased' #['coh', 'cohy', 'imcoh', 'plv', 'ciplv', 'ppc', 'pli', 'dpli', 'wpli', 'wpli2_debiased'].        
        fmin = [vals[0] for vals in freqbands.values()] # get lower bounds of freq bands
        fmax = [vals[1] for vals in freqbands.values()] 
        conn= spectral_connectivity_epochs(epochs,method=method,fmin=fmin, fmax=fmax, faverage=True)
        
        print('Done.')        
        features_dict['conn'] = conn
        
    return features_dict if features_dict else None
 
####################################################################################    
# % ----------------------------------------------------------      
def plot_decoding_scores(scores, std_scores, scores_full, times,title,scoretype):
 
    """Plot decoding scores 
    =================================================================
    Created on Thu Dec 22 13:44:33 2022
    @author: gfraga\n
        
    Parameters
    ----------
    scores = classification scores for each time point
    std_scores = std of scores
    scores_full = classification score for the whole epoch
    title = plot main title
    scoretype = to label y-axis
    
    Returns
    -------        
    fig : a matplotlib figure object 
    """  
    # % Some rescaling
    times = 1e3 * times # to have times in ms  
    fig = plt.figure();
    #plt.ioff() #uncomment to suppress interactive plots 
    plt.plot(times, scores, label="Classif. score")
    plt.axhline(0.5, color='k', linestyle='--', label="Chance level")
    plt.axvline(0, color='r', label='stim onset')
    plt.axhline(1* np.mean(scores_full), color='g', label='Accuracy full epoch')
    plt.legend()
    hyp_limits = (scores - std_scores, scores + std_scores)
    plt.fill_between(times, hyp_limits[0], y2=hyp_limits[1], color='b', alpha=0.5)
    plt.xlabel('Times (ms)')
    plt.ylabel('CV classification score (' + scoretype + ')')
    plt.ylim([0.3, 1])
    plt.title(title)
    plt.close()
    return fig


####################################################################################    

# % ----------------------------------------------------------      
def get_crossval_scores(X,y,clf,cv,scoretype):    
    """ Get classification scores with a scikit classifier 
    =================================================================
    Created on Thu Dec 22 13:44:33 2022
    @author: gfraga\n
    Ref: visit scikit-learn.org documentation 
    
    Parameters
    ----------
    X: array
     feature vector (e.g., [epochs x channels] x times)
    
    y: array
        class labels 
    
    clf: str 
       Definition of a classifier . e.g., clf = svm.SVC(C=1, kernel='linear')
    
    cv: int | str
        cross validation choice. If int is a k-fold CV (e.g, 5) or ShuffleSplit or Stratified 5 fold etc 
        or: StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
    scoretype: str
        the type of score (e.g., 'roc_auc','accuracy','f1')
    
    Returns
    -------       
    scores_full: classification score for the whole epoch
    
    scores: classification scores for each time point (time-resolved mvpa)
    
    std_scores: std of scores
    
    """  
    X_2d = X.reshape(len(X), -1)               
    
    # [MVPA] Use entire epoch
    #scores_full = cross_val_score(estimator = clf, X = X_2d, y= y, cv=cv,n_jobs=8)
    all_scores_full = cross_validate(estimator = clf, X = X_2d, y= y, cv=cv,n_jobs=8, scoring=['accuracy','f1','roc_auc'])
    scores_full=all_scores_full['test_' + scoretype] # get your selected score
    print('--> run classification on the full epoch')
    
    #[MVPA]  running the decoder at each time point <~~~
    n_times = X.shape[2]
    scores = np.empty(n_times)
    std_scores = np.empty(n_times)
    print('[--> starting classification per time point....')
    for t in range(n_times):
        Xt = X[:, :, t]
        # Standardize features
        Xt -= Xt.mean(axis=0)
        Xt /= Xt.std(axis=0)
        # Run cross-validation
        #scores_t = cross_val_score(clf, Xt, y, cv=cv, n_jobs=8)
        scores_t = cross_validate(clf, Xt, y, cv=cv, n_jobs=8,scoring=['accuracy','f1','roc_auc'])
        scores_t=scores_t['test_' + scoretype] # get your selected score
        scores[t] = scores_t.mean()
        std_scores[t] = scores_t.std()
    
    print('Done <--]')
    return scores_full, scores, std_scores
        