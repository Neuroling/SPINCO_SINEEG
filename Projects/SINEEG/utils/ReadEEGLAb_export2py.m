
addpath('/home/d.uzh.ch/gfraga/eeglab2022.1')

% read data set 
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
EEG = pop_loadset('filename','s9_DiN_epoched_ICrem.set','filepath','/mnt/nfs/din_v1/experimentData/SUBJECT_9/EEG_DATA/DOWNSAMPLED/DiN/');
[ALLEEG, EEG, CURRENTSET] = eeg_store( ALLEEG, EEG, 0 );
