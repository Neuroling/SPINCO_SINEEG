# -*- coding: utf-8 -*-
"""
Functions used in the MVPA_runner.py script
===============================================================================
@author : samuemu
Created on Tue Jan 16 15:48:30 2024

# TODO

"""

from sklearn.model_selection import  StratifiedKFold, cross_validate, GridSearchCV
from sklearn import svm, metrics
from sklearn import __version__ as sklearn_version
import numpy as np
import pandas as pd
from functools import reduce

import MVPA_constants as const
    
class MVPAManager:
    """
    CLASS OBJECT FOR HANDLING MVPA
    ===========================================================================
    MVPAManager contains functions needed to perform an MVPA.
    It also collects metadata while the functions are run, which is stored in
    MVPAManager.metadata
    """
    
    def __init__(self):
        self.metadata = {}
        self.metadata['sklearn_version'] = sklearn_version

    def getSubsetIdx(self, event_labels, 
                        conditionExclude = None,
                        conditionInclude = None):
        """
        SUBSETTING THE DATA BY CONDITION & RETURN INDEXES
        =======================================================================
        
        This function will return the indices of all epochs in a specified set of 
        conditions. This can then be used to filter the data.
        
        It does that by comparing the items in conditionExclude / conditionInclude
        with the items of event_labels and saving the indices where the two do not
        overlap / do overlap.

        Parameters
        ----------
        event_labels : list of str
            the event labels as str, organised like 'NV/Call/Stim4/Lv2/Inc/F'
            given for example by tfr_bands['epoch_conditions']
            or from the event_id/events of mne's epoch object
            
        conditionExclude : list of str, optional
            Epochs in these conditions will be excluded. The default is None.
            
        conditionInclude : list of str, optional
            Epochs NOT in this condition will be excluded. The default is None.


        Raises
        ------
        ValueError
            conditionExclude and conditionInclude must not overlap. You cannot both 
            include and exclude the same condition at the same time.


        Returns
        -------
        filt_idx : set
            a set of all indexes of epochs in the desired conditions.

        """

        if conditionExclude is not None and conditionInclude is not None:
            if set(conditionExclude) & set(conditionInclude):
                raise ValueError(f"Cannot both include and exclude condition {conditionExclude & conditionInclude}")
            
        # Create a set of all indexes. Items that are not in the desired conditions will be removed
        filt_idx = set(range(len(event_labels)))
        
        # For any condition that should be excluded, get the indices and remove them from filt_idx
        # (technically, it gets the indices of every epoch NOT in the condition and keeps only those. Same difference)
        if conditionExclude is not None: 
            for cond in conditionExclude: 
                idx = [i for i, x in enumerate(event_labels) if cond not in x]
                filt_idx = filt_idx & set(idx) # keep only common elements
                print("--> excluding epochs in the", cond+'-condition')

        # For each specified condition, get the indices of the desired condition
        # and then compare them to filt_idx. From filt_idx, remove all elements not in the desired condition
        if conditionInclude is not None:
            for cond in conditionInclude:
                idx = [i for i, x in enumerate(event_labels) if cond in x]
                filt_idx = filt_idx & set(idx) # Keep only the common elements
                print("--> excluding epochs NOT in the", cond+"-condition")
                
        self.metadata['conditionInclude'] = conditionInclude
        self.metadata['conditionExclude'] = conditionExclude
        self.metadata['includedTrialsByIdx'] = filt_idx
                
        return filt_idx
        
    
    
    def gridSearch_classifierParams(self,
                                    X,
                                    y,
                                    param_grid,
                                    scoretype = ('balanced_accuracy'),
                                    clf = svm.SVC(C=1, kernel = 'linear')
                                    ):
        """
        # TODO
        see https://scikit-learn.org/stable/modules/grid_search.html#grid-search
        

        Parameters
        ----------
        X : TYPE
            DESCRIPTION.
            
        y : TYPE
            DESCRIPTION.
            
        param_grid : TYPE
            DESCRIPTION.
            example:
                param_grid = [
                  {'kernel': ['linear'],'C': [1, 10, 100, 1000]},
                  {'kernel': ['rbf','poly','sigmoid'],'C': [1, 10, 100, 1000], 
                   'gamma': ['auto', 'scale', 0.001, 0.0001] },
                  ]  

        scoretype : str, optional
            DESCRIPTION. The default is ('balanced_accuracy').
            
        clf : TYPE, optional
            DESCRIPTION. The default is svm.SVC(C=1, kernel = 'linear').

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Get number of possible combinations of params to check for
        if type(param_grid) is list:
            n_param_combinations = 0
            for i, entry in enumerate(param_grid):
               n_param_combinations += reduce(lambda x, y: x * y, [len(values) for values in param_grid[i].values()])
        elif type(param_grid) is dict:
            n_param_combinations = reduce(lambda x, y: x * y, [len(values) for values in param_grid.values()])
        else:
            raise ValueError('param_grid needs to be list of dicts or dict')
            
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

        params = [ str(item) for item in gslf.cv_results_['params']]
        data = { 'mean_rank' : ranks.mean(axis = 0), 'mean_score' : mean_score.mean(axis = 0)}
        df = pd.DataFrame(data, index = params)
        # df.to_csv(dirinput+'_thisBand_gridsearch_MVPA_params.csv') # TODO
        return df
    
        
    def get_crossval_scores(self,
                            X,
                            y,
                            clf = svm.SVC(C=1, kernel='linear'),
                            cv = StratifiedKFold(n_splits = 5, random_state = None, shuffle = False),
                            scoretype = ['accuracy']
                            ):    
        """ Get classification scores with a scikit classifier 
        =================================================================
        Created on Thu Dec 22 13:44:33 2022
        @author: gfraga & samuemu
        Reference: visit documentation in https://scikit-learn.org/stable/modules/classes.html
        https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html
        https://scikit-learn.org/stable/modules/svm.html
        
        Parameters
        ----------
        X: array of shape (n_epochs, n_channels, n_timepoints)
           feature vector (e.g., epochs x [channels x times]) 
        
        y: array-like of shape (n_samples,) or (n_samples, n_outputs)
            The target variable to try to predict in the case of supervised learning.
            For instance, the accuracy labels of the epochs (y = epo.metadata['accuracy'])
        
        clf: estimator object implementing 'fit' | optional 
            Default: clf = svm.SVC(C=1, kernel='linear')
            
            Define classifier, i.e. the object used to fit the data. 
            
            The used classifier gets stored in MVPAManager.metadata['classifier']
            and the exact parameters in MVPAManager.metadata['classifier_parameters']
        
        cv: int | cross-validation generator | iterable | None | optional
            Default: cv = StratifiedKFold(n_splits=5, random_state=None, shuffle=False)
            
            cross validation splitting strategy. Possible inputs are:
            - int to specify the number of folds.
            - None will use default 5-fold cross validation.            
                - If int/None input, and if clf is a classifier and y is either binary or multiclass,
                  then StratifiedKFold is used. Otherwise, KFold is used. Both will be instantiated with
                  shuffle=False, so the splits will be the same across all calls.
            - iterable yielding (train, test) splits as arrays of indices
            - A CV splitter, such as KFold or StratifiedKFold, ShuffleSplit.
              example: cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
              
            The used cv gets stored in MVPAManager.metadata['crossval_splitting_strategy']
 
        scoretype: str | callable | list | tuple | dict | optional
            Default: scoretype = ['accuracy']
            
            How to evaluate the performance of the cross-validated model
            (e.g., 'roc_auc','accuracy','balanced_accuracy')
            see https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
            
            The used scoretype gets stored in MVPAManager.metadata['crossval_scoretype']
        
        
        Returns
        -------       
        
        # TODO
        
        """  
        
        output_dict = {}
        self.metadata['classifier'] = str(clf)
        self.metadata['classifier_parameters'] = clf.get_params()
        self.metadata['crossval_scoretype'] = scoretype
        self.metadata['crossval_splitting_strategy'] = str(cv)
        
        # If single scoretype, convert str to list
        if type(scoretype) is str:
            scoretype = [scoretype]
           
    
    
        # #[MVPA] Decoding based on entire epoch ------------------------------
        # ---------------------------------------------------------------------
        print('---> run classification on the full epoch')
        
        if len(X.shape) != 3:
            raise ValueError(f'Array X needs to be 3-dimensional, not {len(X.shape)}')
        X_2d = X.reshape(len(X), -1) # Now it is epochs x [channels x times]
        # or in other words: epochs x features
        # so every electrode and every timepoint is treated as a different feature.
        
            
        
        #% see https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
        all_scores_full = cross_validate(estimator = clf, # So this basically runs clf.fit(x,y)
                                         X = X_2d, # the data to fit the model
                                         y = y,  # target variable to predict
                                         cv = cv, # cross-validation splitting strategy
                                         n_jobs = const.n_jobs,
                                         scoring = scoretype)                                    
                                      
        #get only the scores from output ( not the fitting times)
        output_dict['crossval_score_FullEpoch'] = {key: all_scores_full[key] for key in all_scores_full if key.startswith('test')} 
        
        
        
        #[MVPA] Time-resolved decoding ----------------------------------------
        # ---------------------------------------------------------------------
        n_times = X.shape[2] # get number of timepoints
 
        # Use dictionaries to store values for each score type
        scores = {name: np.zeros(shape = (n_times, 5)) for name in scoretype}
        
        
        f1_cor = np.zeros(shape = (n_times, 5))
        f1_inc = np.zeros(shape = (n_times, 5))

        
        print('----> starting classification per time point....')
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
            for name in scoretype:
                scores[name][t,:]=scores_t['test_' + name]
                # std_scores[name][t,:]=scores_t['test_' + name].std()
                
            i = 0
            for train_index, test_index in cv.split(Xt, y):
                clf.fit(Xt[train_index], y.iloc[train_index])
                y_pred = clf.predict(Xt[test_index])
                f1_cor[t,i] = metrics.f1_score(y.iloc[test_index], y_pred, pos_label='cor')
                f1_inc[t,i] = metrics.f1_score(y.iloc[test_index], y_pred, pos_label='inc')
                i += 1

        scores['f1_cor'] = f1_cor
        scores['f1_inc'] = f1_inc
        
        keys = [key for key in scores]
        for key in keys:
            scores[key + '_mean'] = scores[key].mean(axis = 1)
            scores[key + '_std'] = scores[key].std(axis = 1)

        output_dict['crossval_scores_timewise'] = scores

        print('-----> Done.')
        return output_dict
    
    def random_subsample_accuracy(self, 
                                  trial_info = None):
        """
        # !!! copied straight from PreStim_functions, needs to be adapted to be usable
        
        RANDOMLY SUBSAMPLES TRIALS TO EQUALISE ACCURACY COUNTS
        =======================================================================
        
        This function counts how many trials were correct and how many incorrect.
        It will then get the lower of those two numbers (let's call it minumum)
        and then it will randomly select [minumum] correct and incorrect trials
        and return their indices ("subsample_idx").
        The length of subsample_idx is therefore = 2*minimum.
        Half the indices are from correct, and half from incorrect trials.
        
        Parameters
        ----------
        trial_info : dict or pandas DataFrame, optional
            The trial information - for instance condition_dict or condition_df. 
            The default is None, in which case the function will try to use the
            condition-dict stored in the PreStimManager object. If there is none, it
            will try to use the condition_df stored in the PreStimManager object.
            
        Raises
        ------
        AttributeError
            if no trial information was provided and none could be found.
            
        Returns
        -------
        subsample_idx : indexes
            the subsampled indices, which can be applied to the df by calling 
            `df = df.iloc[subsample_idx]`
            Note : if the df has non-sequential indices (which can happen when filtering or
                 concatentaing), this will not work.
            
        """
        raise NotImplementedError

        if trial_info is None: 
        # TODO : account for if input is dict - 
        # maybe take the concat out of the if loop and do another if-loop outside, i.e. `if trial_info.type=dict: concat`
            try:
                trial_info = self.condition_dict
                # combine all subj condition dataframes to get across-subj accuracy
                # TODO for within-subj (see comment in sketch_PreStim_writing)
                tmp_df = pd.concat(trial_info.values(), axis=0, ignore_index=True)
            except AttributeError:
                try:
                    tmp_df = self.condition_df
                except AttributeError:
                    raise AttributeError("cannot subsample data - no trial information (condition_dict or condition_df) found")
        else:
            tmp_df = trial_info.copy()
            
            
        # counting total correct and incorrect
        count_cor = tmp_df['accuracy'].value_counts()[1]
        count_inc = tmp_df['accuracy'].value_counts()[0]
        
        idx_cor = tmp_df.index[tmp_df['accuracy'] == 1]
        idx_inc = tmp_df.index[tmp_df['accuracy'] == 0]
        
        minimum = min(count_cor, count_inc)
        subsample_idx = random.sample(list(idx_cor), minimum) + random.sample(list(idx_inc), minimum)
        
        
        return subsample_idx












