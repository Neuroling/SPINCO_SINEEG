clear all; close all; 
% Run Automagic project
% ======================================================================
% - Reads parameters from a template-project created in GUI (project_state.mat file)
% - Adjusts name and directories of the project

% Paths
thisDir = mfilename('fullpath');
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
taskID = 'task-sin';
pipeID = 'pipeline-01';
run = 1;

%% find data 
dataFolder = fullfile(baseDir, 'Data','SiN','derivatives',pipeID,taskID) ;
resultsFolder = fullfile(baseDir, 'Data','SiN','derivatives',pipeID,[taskID,'_preproc']);
template_project = fullfile(fileparts(thisDir),'project_state.mat');
mkdir(resultsFolder)

%% Copy raw to derivatives folder 
if run == 1
    %% Project definition
    cd (fileparts(template_project))
    load(template_project)     
    eeglab nogui

    % %% Define new project 
    name =  'PI01';  
    ext = '.set';
    Params = self.params; % param from previous
    VisualisationParams = struct();
    samplingrate = 2048; 

    % fix channelLoc file path
    Params.EEGSystem.locFile = fullfile(baseDir,'Data','SiN','_acquisition','_electrodes','Biosemi_71ch_EEGlab_xyz.tsv');

    %% Run project       
    addAutomagicPaths();
    project = Project(name, dataFolder, resultsFolder, ext, Params, VisualisationParams,samplingrate); % won't work without giving all these inputs including srate
    project.preprocessAll();

end
 