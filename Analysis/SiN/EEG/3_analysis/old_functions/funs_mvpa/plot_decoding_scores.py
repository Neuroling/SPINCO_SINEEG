import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mne 
from mne.time_frequency import tfr_morlet
from mne_connectivity import spectral_connectivity_epochs
from mne.epochs import equalize_epoch_counts
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, StratifiedKFold,cross_validate
####################################################################################    
# % ----------------------------------------------------------      
def plot_decoding_scores(scores, std_scores, scores_full, times,title,scoretype):
 
    """Plot decoding scores 
    =================================================================
    Created on Thu Dec 22 13:44:33 2022
    @author: gfraga\n
        
    Parameters 
    ----------
    Expected input is derived from scikit-learn crossvalidate output
    
    scores: classification scores for each time point
    
    std_scores: std of scores
    
    scores_full: classification score for the whole epoch
    
    title: plot main title
    
    scoretype: label of y-axis e.g., accuracy
    
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

