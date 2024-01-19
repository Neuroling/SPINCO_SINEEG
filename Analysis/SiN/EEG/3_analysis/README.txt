MVPA is done in MNE python toolbox. 
We first need to read the epoched EEGlab data set and adding some informatin to 
the trial events to encode all conditions of interest ('relabelling' )

Scripts named with 'constants' are have variables that do not change in 
the different steps (e.g., subj IDs)  and are used by other scripts and functions. 
'function' scripts have functions called by 'runner' scripts. 
Script function names will usually describe what they do (e.g., 'writing') 