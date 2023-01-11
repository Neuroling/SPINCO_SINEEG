import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold,cross_validate  
####################################################################################    
# % ----------------------------------------------------------      
def get_crossval_scores(X,y,clf,cv,scoretype):    
    """ Get classification scores with a scikit classifier 
    =================================================================
    Created on Thu Dec 22 13:44:33 2022
    @author: gfraga\n
    Ref: visit documentation in https://scikit-learn.org/stable/modules/classes.html
    
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
    
    
    # #[MVPA]------Use entire epoch
    X_2d = X.reshape(len(X), -1)               
    all_scores_full = cross_validate(estimator = clf,
                                     X = X_2d,
                                     y= y, 
                                     cv=cv, 
                                     n_jobs=8,
                                     scoring=scoretype)
    
    all_scores_full = {key: all_scores_full[key] for key in all_scores_full if key.startswith('test')} #get only the scores from output (also contains times)
    
    # %%
    from sklearn.metrics import confusion_matrix
    X_train, X_test, y_train, y_test = train_test_split(X_2d, y)
    #train model
    clf.fit(X_train, y_train)
    #predict test data
    y_pred = clf.predict(X_test)
    y_true = y_test  
    cm= confusion_matrix(y_true, y_pred)
    
    cross_validate(estimator = clf,
                                    X = X_2d,
                                    y= y, 
                                    cv=cv, 
                                    n_jobs=8,
                                    scoring=scoretype)
    
    # %% 
    
    ## alternative line with only one type of scoring: 
    #scores_full = cross_val_score(estimator = clf, X = X_2d, y= y, cv=cv,n_jobs=8)        
    
    
    print('--> run classification on the full epoch')
    #[MVPA]------ running the decoder at each time point 
    n_times = X.shape[2]       
    #Use dictionaries to store values for each score type 
    scores = {name: [] for name in scoretype}
    std_scores = {name: [] for name in scoretype}
    print('[--> starting classification per time point....')
    #loop thru time points
    for t in range(n_times):
        Xt = X[:, :, t]
        # Standardize features
        Xt -= Xt.mean(axis=0)
        Xt /= Xt.std(axis=0)
        
        #[O_O] Run cross-validation 
        scores_t = cross_validate(clf, Xt, y, cv=cv, n_jobs=8,scoring=scoretype)     
        ##alternative line with only one type of scoring:
        # scores_t = cross_val_score(clf, Xt, y, cv=cv, n_jobs=8)        
        
        #Add CV mean and std of this time point to my output dict 
        for name in scoretype:
            scores[name].append(scores_t['test_' + name].mean()) 
            std_scores[name].append(scores_t['test_' + name].std())
    
    #transform lists to arrays 
    scores = {key: np.array(value) for key, value in scores.items()}
    std_scores = {key: np.array(value) for key, value in std_scores.items()}
      
    print('Done <--]')
    return all_scores_full, scores, std_scores 