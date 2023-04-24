import numpy as np

####################################################################################    
# % ----------------------------------------------------------
def EEG_epochSelect_relabel(epochs,
                                classify_by,
                                equalize_epoch_count = True,
                                crop_epoch_times = None):
 
    """Select and relabel epochs for classification
    =================================================================
    Created on Wed Dec 21 13:16:09 2022
    @author: gfraga\n 
    Project-specific function to label classes. 
    - Selects epochs and relabels event names depending on our classification choice
    - Returns selected epochs and an 'y' array with their labels for classification
       
    Parameters
    ----------
    epochs: instance of mne 'Epochs'
        Epoched Object from mne. Contains event info
    
    classify_by: str 
        A string indicating your target classification to relabel classes:
            'accuracy' will take epochs correct/incorrect labels (and take only epochs that had noise) 
            
            'difficulty' will use the easy, mid, hard labels (ignoring accuracy and clear epochs)
    
    equalize_epoch_count: bool | default True 
        If True it will run the mne equalize the number of epochs to classify using mne.epochs.equalize_epoch_counts()
        
    crop_epoch_times: tuple | default None
        Specify tmin and tmax (in sec) If you want to crop the epoch before feature extraction e.g. (-2, 1). If None the entire epochs will be passed on 
    
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
    
    if crop_epoch_times is None:
        print('--Done. The entire epochs length was selected.')
    else:
        print('--Done. Epochs were cropped to ' + str(crop_epoch_times) + ' (tmax not included)')
        epochs_sel.crop(tmin=crop_epoch_times[0], tmax=crop_epoch_times[1], include_tmax=False)
    
    # Save labels in vector
    y = np.array([e[2] for e in epochs_sel.events])# epochs codes should have dimensions [ n_trials , ]
    times = epochs_sel.times


    return epochs_sel,y, times