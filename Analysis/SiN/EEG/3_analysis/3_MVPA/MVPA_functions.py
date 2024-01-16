# -*- coding: utf-8 -*-
"""
Functions used in the MVPA_runner.py script
===============================================================================
@author : samuemu
Created on Tue Jan 16 15:48:30 2024

"""

from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold, cross_validate  
from sklearn import metrics
from sklearn import svm

import MVPA_constants as const
    
class MVPAManager:
    """
    # TODO
    """
    

#%%
    def get_crossval_scores(self,X,y,clf=svm.SVC(C=1, kernel='linear'),cv=None,scoretype=('accuracy')):    
        """ Get classification scores with a scikit classifier 
        =================================================================
        Created on Thu Dec 22 13:44:33 2022
        @author: gfraga & samuemu
        Ref: visit documentation in https://scikit-learn.org/stable/modules/classes.html
        https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
        https://scikit-learn.org/stable/modules/svm.html
        
        Parameters
        ----------
        X: array of shape (n_epochs, n_channels, n_timepoints)
           feature vector (e.g., epochs x [channels x times]) 
        
        y: array-like of shape (n_samples,) or (n_samples, n_outputs)
            The target variable to try to predict in the case of supervised learning.
            For instance, the accuracy labels of the epochs (y = epo.metadata['accuracy'])
        
        clf: str 
           Define classifier, i.e. the object to use to fit the data. 
           Default: clf = svm.SVC(C=1, kernel='linear')
        
        cv: int | cross-validation generator or an iterable | Default=None
            cross validation choice. 
            - int to specify the number of folds.
            - None will use default 5-fold cross validation.
            - iterable yielding (train, test) splits as arrays of indices
            - A CV splitter, such as KFold or StratifiedKFold, ShuffleSplit.
              example: cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            
            - If int/None input, and if clf is a classifier and y is either binary or multiclass,
              then StratifiedKFold is used. Otherwise, KFold is used. Both will be instantiated with
              shuffle=False, so splits will be the same across class.
            
        scoretype: str | callable | list | tuple | dict
            the type of score (e.g., 'roc_auc','accuracy','f1')
            see https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
            Default= ('accuracy')
        
        Returns
        -------       
        scores_full: classification score for the whole epoch
        
        scores: classification scores for each time point (time-resolved mvpa)
        
        std_scores: std of scores
        
        """  
        
        
        # #[MVPA] Decoding based on entire epoch
        # ---------------------------------------------
        if len(X.shape) != 3:
            raise ValueError(f'Array X needs to be 3-dimensional, not {len(X.shape)}')
        X_2d = X.reshape(len(X), -1) # Now it is epochs x [channels x times]   
        
        #% see https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
        all_scores_full = cross_validate(estimator = clf,
                                         X = X_2d, # the data to fit the model
                                         y= y,  # target variable to predict
                                         cv=cv, # cross-validation splitting strategy
                                         n_jobs=const.n_jobs,
                                         scoring=scoretype)
        
        all_scores_full = {key: all_scores_full[key] for key in all_scores_full if key.startswith('test')} #get only the scores from output (also contains times)
        # TODO get only mean and std instead of all 5 (ask Gorka if he wants all 5)
        print('--> run classification on the full epoch')
        
        
        
        #[MVPA] Time-resolved decoding 
        # ---------------------------------------------
        n_times = X.shape[2] # get number of timepoints
        
        #Use dictionaries to store values for each score type
        if type(scoretype) is str:
            scores = np.zeros(shape=(n_times,1))
            std_scores = np.zeros(shape=(n_times,1))
        else:
            scores = {name: np.zeros(shape=(n_times,1)) for name in scoretype}
            std_scores = {name: np.zeros(shape=(n_times,1)) for name in scoretype}
        
        print('[--> starting classification per time point....')
        for t in range(n_times): # for each timepoint...
            Xt = X[:, :, t] # get array of shape (n_epochs, n_channels) for this timepoint
            
            # Standardize features
            Xt -= Xt.mean(axis=0) # subtracts the mean of the row from each value
            Xt /= Xt.std(axis=0) # divides each value by the SD of the row
            
            #[O_O] Run cross-validation for each timepoint
            scores_t = cross_validate(estimator=clf, 
                                      X=Xt, 
                                      y=y, 
                                      cv=cv, 
                                      n_jobs=const.n_jobs,
                                      scoring=scoretype)     
            
            #Add CV mean and std of this time point to my output dict 
            if type(scoretype) is str:
                scores[t]=scores_t['test_score'].mean()
                std_scores[t]=scores_t['test_score'].std()
             # TODO Somehow, all values in scores are the same. Check if there's something wrong
                
            else:
                for name in scoretype:
                    scores[name][t]=scores_t['test_' + name].mean()
                    std_scores[name][t]=scores_t['test_' + name].std()
        
        #from lists to arrays 
        if type(scoretype) is not str:
            scores = {key: np.array(value) for key, value in scores.items()}
            std_scores = {key: np.array(value) for key, value in std_scores.items()}
          
        print('Done <--]')
        return all_scores_full, scores, std_scores 
    
