clear; close all ;
% =========================================================================
% Import raw bdf files 
% =========================================================================
% Author: G.FragaGonzalez
% Description:
% - Read raw .bdf files
% - Create and save eeglab dataset 
% 
%% Define paths (Use relative path to 'scripts' Folder to find data)
folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
baseDir = fullfile(folders{1:(find(strcmp(folders, 'Scripts'), 1)-1)});
dirinput = [baseDir,filesep,fullfile('Data','SiN','raw','p001','eeg')];

%% find raw eeg
eeglab;
files  = dir([dirinput,filesep,'*.bdf']);
for i = 1:length(files)
   
   % define inputs and output dir 
   fullFileInput = [files(i).folder,filesep,files(i).name];
   chanLocsFile = 'V:\Projects\Spinco\SINEEG\Data\Biosemi_73ch_ThetaPhi.elp'
   diroutput = strrep(files(i).folder,'raw','preproc'); % Assuming only one 'raw' folder is present in the full path 
   mkdir(diroutput)   
   
   
   % EEGLAB ------------------------------------------------------
   pop_editoptions( 'option_storedisk', 1); % Process only one dataset at a time   
   
   % import 
   EEG = pop_biosig(fullFileInput, 'importannot','off');% import function options may vary   
   
   % load channel locations
  % EEG = pop_chanedit(EEG,'load',chanLocsFile,'besa'); 
   
   % downsample 
   
   
   
   
   % save dataset 
   newSetName = strrep(files(i).name,'.bdf','');
   EEG  = pop_newset(ALLEEG, EEG, 0,'setname',newSetName,'gui','off','overwrite','on'); 
   EEG = pop_saveset (EEG, newSetName,diroutput);   
   
   
   
end 
   
   
   
   
    



