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

%% Read table  with badchannels (SAM)
chanCheck= readtable(fullfile(baseDir, 'Data','SiN','derivatives_SM','QualityAssessment.xlsx'));
rowlabels=chanCheck.SUBJ;
chanCheck=table(chanCheck.all_3, 'RowNames',rowlabels);

%% find data 
files = dir([dirinput,filesep,'**',filesep,'*',taskID,'*_ds.set']);

%% loop thru files 
for f = 1:length(files)
%for f= 1 

    % input file 
    fileinput = fullfile(files(f).folder, files(f).name); 
    subjID=files(f).name(1:4);

    %% Load set and run ICA 
    
    % load set  
    [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
    EEG = pop_loadset('filename',fileinput);
    % 
    EEG.comments = pop_comments(EEG.comments,'','prepma preproc script applied for inspection',1);
    
    %% 
    %Exclude EOGs 
    EEG = pop_select( EEG, 'rmchannel',{'EXT1','EXT2','EXT3','EXT4','EXT5','EXT6','erg1'});

    %% EXCLUDE BAD CHANNELS (SAM)
     % Compare subjID in filename and in table with bad channels
     badChans = chanCheck(subjID,:);
     badChans=split(badChans.Var1, ',');
 
     % exclude from eeg    
      EEG = pop_select( EEG, 'rmchannel',badChans);
    
     
    
    %% 
    % run ICA reducing the dimension by 1 to account for average reference     
     EEG = pop_runica( EEG, 'runica', 'extended', 1);


    %% Save 
    newsetname = [EEG.setname, '_ICA'];
    pop_saveset (EEG, newsetname,files(f).folder);

end

