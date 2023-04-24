import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold,cross_validate  
from sklearn import metrics
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
       Define classifier . e.g., clf = svm.SVC(C=1, kernel='linear')
    
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
    
    
    # #[MVPA] Decoding based on entire epoch
    # ---------------------------------------------
    X_2d = X.reshape(len(X), -1)               
    all_scores_full = cross_validate(estimator = clf,
                                     X = X_2d,
                                     y= y, 
                                     cv=cv, 
                                     n_jobs=8,
                                     scoring=scoretype)
    
    all_scores_full = {key: all_scores_full[key] for key in all_scores_full if key.startswith('test')} #get only the scores from output (also contains times)
    print('--> run classification on the full epoch')
    
    
    
    #[MVPA] Time-resolved decoding 
    # ---------------------------------------------
    n_times = X.shape[2]       
    
    #Use dictionaries to store values for each score type 
    scores = {name: [] for name in scoretype}
    std_scores = {name: [] for name in scoretype}
    
    print('[--> starting classification per time point....')
    for t in range(n_times):
        Xt = X[:, :, t]
        
        # Standardize features
        Xt -= Xt.mean(axis=0)
        Xt /= Xt.std(axis=0)
        
        #[O_O] Run cross-validation 
        scores_t = cross_validate(clf, Xt, y, cv=cv, n_jobs=8,scoring=scoretype)     
        
        #Add CV mean and std of this time point to my output dict 
        for name in scoretype:
            scores[name].append(scores_t['test_' + name].mean()) 
            std_scores[name].append(scores_t['test_' + name].std())
    
    #from lists to arrays 
    scores = {key: np.array(value) for key, value in scores.items()}
    std_scores = {key: np.array(value) for key, value in std_scores.items()}
      
    print('Done <--]')
    return all_scores_full, scores, std_scores 


#### BELOW some unorganized copies of codes for future recycling
# %% Confusion matrix

    # from sklearn.metrics import confusion_matrix
    # X_train, X_test, y_train, y_test = train_test_split(X_2d, y)
    # #train model
    # clf.fit(X_train, y_train)
    # #predict test data
    # y_pred = clf.predict(X_test)
    # y_true = y_test  
    # cm= confusion_matrix(y_true, y_pred)
    
    # metrics.f1_score(y_test, clf.predict(X_test), average="macro")
    # print(metrics.classification_report(y_test, y_pred))
    
    # scores = cross_validate(estimator = clf,
    #                                 X = X_2d,
    #                                 y= y, 
    #                                 cv=cv, 
    #                                 n_jobs=8,
    #                                 scoring=scoretype)

    # % Classifier selection 
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
    
    
    #%% 

    # # define a monte-carlo cross validation generator (to reduce variance) : 
    # #  cv = ShuffleSplit(len(X), n_splits = 10, test_size=0.2, random_state=42)
    # cv = sklearn.ShuffleSplit(n_splits = 10, test_size=0.2, random_state=42)
    # cv = 5 # k-fold validation 
    # # This will learn on 80 % of the epochs and evaluate the remaining 20 % (test_size = ) to predict accurcay 


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