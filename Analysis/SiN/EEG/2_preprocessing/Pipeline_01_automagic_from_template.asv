clear all; close all; 
% Run Automagic project
% ======================================================================
% - Reads parameters from a template-project created in GUI (project_state.mat file)
% - Adjusts name and directories of the project

% Paths
thisDir = matlab.desktop.editor.getActiveFilename;
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
 
dataFolder = fullfile(baseDir, 'Data','SiN','derivatives','pipeline-01','task-sin') ;
resultsFolder = fullfile(baseDir, 'Data','SiN','derivatives','pipeline-01','task-sin_res');
template_project = fullfile(fileparts(thisDir),'project_state.mat');
mkdir(resultsFolder)
%% Project definition
load(template_project) 

% %% Define new project 
 name =  'PIPE01';  
 ext = '.set';
 Params = self.params; % param from previous
 VisualisationParams = struct();
 samplingrate = 2048; 
 
eeglab nogui
%% Run project       
addAutomagicPaths();
project = Project(name, dataFolder, resultsFolder, ext, Params, VisualisationParams,samplingrate); % won't work without giving all these inputs including srate
project.preprocessAll()
