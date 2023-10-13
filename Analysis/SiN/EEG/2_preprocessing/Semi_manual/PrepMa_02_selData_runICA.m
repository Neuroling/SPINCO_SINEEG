clear all; close all; 

% Preprocessing step 02
% ======================================================================
% - select data to exclude are around breaks
% - Run ICA

% Paths
thisDir = mfilename('fullpath');
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
addpath(fullfile(baseDir,'Tools','eeglab_current','eeglab2023.0'));

taskID = 'task-sin';
dirinput = fullfile(baseDir, 'Data','SiN','derivatives_SM',taskID) ;
diroutput = dirinput;


  

%% find data 
files = dir([dirinput,filesep,'**',filesep,'*',taskID,'*avgRef.set']) 

%% loop thru files 
%for f = 1:length(files)
for f= 1 

    % input file 
    fileinput = fullfile(files(f).folder, files(f).name); 

    %% Load set and run ICA 
    
    % load set  
    [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
    EEG = pop_loadset('filename',fileinput);
    % 
    EEG.comments = pop_comments(EEG.comments,'','prepma preproc script applied for inspection',1);
    
    %% 
    %Exclude EOGs 
    EEG = pop_select( EEG, 'rmchannel',{'EXT1','EXT2','EXT3','EXT4'});

    %% 
    % run ICA reducing the dimension by 1 to account for average reference     
    EEG = pop_runica(EEG, 'icatype','runica','chanind',[1:64]);
    
    % Filter 
    % highpass (aggressive for ICA) 
    

    %% save before downsampling
    newsetname = [ursetname, '_filt_avgRef'];
    pop_saveset (EEG, newsetname,files(f).folder);

    %% Downsample 
    EEG = pop_resample(EEG, 128);

    %% Save 
    newsetname = [ursetname, '_filt_avgRef_ds'];
    pop_saveset (EEG, newsetname,files(f).folder);

end

