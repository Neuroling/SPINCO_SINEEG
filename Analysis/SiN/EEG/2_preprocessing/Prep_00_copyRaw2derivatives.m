clear all; close all; 
% Copy raw files into the Derivatives folder
% ======================================================================
% - Copy Raw eeg files and .tsv with events to the derivatives folder for preprocessing

% Paths
thisDir = mfilename('fullpath');
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
taskID = 'task-sin';
pipeID = 'pipeline-automagic-02';
derivativesFolder = 'derivatives_exp2';
subjects = {'s204'};

%% 
for i = 1:length(subjects)
  
    subjID = subjects{i};
    % find data 
    rawdataFolder = fullfile(baseDir, 'Data','SiN','rawdata',subjID,taskID,'eeg') ;
    resultsFolder = fullfile(baseDir, 'Data','SiN',derivativesFolder,pipeID,taskID,subjID);
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