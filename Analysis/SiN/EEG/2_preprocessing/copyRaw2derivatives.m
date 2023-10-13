clear all; close all; 
% Run Automagic project
% ======================================================================
% - Reads parameters from a template-project created in GUI (project_state.mat file)
% - Adjusts name and directories of the project

% Paths
thisDir = mfilename('fullpath');
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
taskID = 'task-sin';
pipeID = 'trimbreaks_pipeline-01';
subjects = {'s001'};

%% 
for i = 1:length(subjects)
  
    subjID = subjects{i};
    % find data 
    rawdataFolder = fullfile(baseDir, 'Data','SiN','rawdata',subjID,taskID,'eeg') ;
    resultsFolder = fullfile(baseDir, 'Data','SiN','derivatives',pipeID,taskID,subjID);
    mkdir(resultsFolder)
  
    %% Copy raw to derivatives folder 
    % events
    eventsfile = dir([rawdataFolder,filesep,'*_accu.tsv']);
    if length(eventsfile)==1 
        copyfile (fullfile(eventsfile.folder,eventsfile.name), fullfile(resultsFolder,eventsfile.name))
    else;   error('check Event files'); 
    end 

    rawdatafile = dir([rawdataFolder,filesep,'*.set']);
    if length(rawdatafile)==1 
        copyfile (fullfile(rawdatafile.folder,rawdatafile.name), fullfile(resultsFolder,rawdatafile.name))
        % copyfile
        % (fullfile(rawdatafile.folder,strrep(rawdatafile.name,'.set','.fdt')), fullfile(resultsFolder,strrep(rawdatafile.name,'.set','.fdt'))) 
        
    else
        error('check rawdata files')
    end  



 end 