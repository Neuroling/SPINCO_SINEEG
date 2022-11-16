clear ; close all; 
% ========================================================================
%  Filter preprocessed epochs to alpha band 
% ========================================================================
% Author: G.FragaGonzalez 2022
% Description
%  Loads .set datasets and filter them to alpha band (8-13Hz)using EEGlab
%
%-------------------------------------------------------------------------
dirinput = '/mnt/nfs/din_v1/experimentData';
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_merged';
mkdir (diroutput)
cd(dirinput)


%%
files = dir([dirinput,'/SUBJECT_*/EEG_DATA/DOWNSAMPLED/*merged.set'])
%%
%files = {files.name};
cd (diroutput)
for f = 1 :length(files)
    tmp = strsplit(files(f).name,'_downsampled')
    mkdir(tmp{1})
        copyfile([files(f).folder,'/',files(f).name], [cd '/',tmp{1}])
end





%% look for src files 

files = dir([dirinput,'/SUBJECT_*/EEG_DATA/DOWNSAMPLED/DiN/*epoched.set']);

for f = 1:length(files)

copyfile([files(f).folder,'/',files(f).name],diroutput)

end 

%%
% set some eeglab options
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;

%%
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