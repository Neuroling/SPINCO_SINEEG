clear; close all ;
% =========================================================================
% Import raw bdf files 
% =========================================================================
% Author: G.FragaGonzalez
% Description:
% - Read raw .bdf files
% - Create and save eeglab dataset 
%% user inputs
subjID = 'p003';
taskID = 'task-sin';

% Paths and files (Use relative path to 'scripts' Folder to find data)
folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
baseDir = fullfile(folders{1:(find(strcmp(folders, 'Scripts'), 1)-1)});
dirinput = [baseDir,filesep,fullfile('Data','SiN','raw',subjID,taskID,'eeg')];
% find raw eeg
files  = dir([dirinput,filesep,'*.bdf']);
%% 

for i = 1:length(files)
   % define current subject input and output dir 
   fullFileInput = [files(i).folder,filesep,files(i).name];   
   diroutput = strrep([files(i).folder],'raw','preproc'); % Assuming only one 'raw' folder is present in the full path 
   mkdir(diroutput)   
   
   %% EEGLAB ------------------------------------------------------
   eeglab nogui 
   pop_editoptions( 'option_storedisk', 1); % Process only one dataset at a time   
   
   % import 
   %EEG = pop_readbdf(fullFileInput); % using thoe older function: %EEG = pop_biosig(fullFileInput, 'importannot','off');
   EEG = pop_biosig(fullFileInput, 'importannot','off','ref', 48, 'refoptions',{ 'keepref' 'on' }, 'rmeventchan','off');
   
   % load channel locations
   chanLocsFile = [files(i).folder,filesep,[subjID,'_electrodes.tsv']];
   EEG = pop_chanedit(EEG,'load',chanLocsFile); 
   
   % downsample    
   EEG = pop_resample( EEG, 512);
   
   %% save dataset 
   newSetName = strrep(files(i).name,'.bdf','_imp');
   EEG  = pop_newset(ALLEEG, EEG, 0,'setname',newSetName,'gui','off','overwrite','on'); 
   EEG = pop_saveset (EEG, newSetName,diroutput);   
   
   
end 
   
   
   
   
    



