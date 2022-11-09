clear ; close all; 
% ========================================================================
%  Filter preprocessed epochs to alpha band 
% ========================================================================
% Author: G.FragaGonzalez 2022
% Description
%  Loads .set datasets and filter them to alpha band (8-13Hz)using EEGlab
%
%-------------------------------------------------------------------------
dirinput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc';
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_alpha';
mkdir (diroutput)
cd(dirinput)

% look for src files 
files = dir([dirinput,'/*ICrem.set']);

% set some eeglab options
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;


% start file loop
for f= 1:length(files)
    fileinput = files(f).name;

    % load file       
    EEG = pop_loadset('filename',fileinput,'filepath',dirinput);  
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
   
    
    %% filter to alpha band
    EEG = pop_eegfiltnew(EEG, 'locutoff',8);
    EEG = pop_eegfiltnew(EEG, 'hicutoff',13); 
    EEG = eeg_checkset(EEG);
    
    newsetname = [EEG.setname,'_alpha'];
    EEG.setname = newsetname;
    eeglab redraw  

    %% Save 
    EEG= pop_saveset(EEG,'filename',[newsetname,'.set'],'filepath',diroutput);
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

end