clear all; close all; 
%% Run Automagic project
% ======================================================================
% - Reads parameters from a project created in GUI (project_state.mat file)
% - ...


%% CREATE PROJECT FROM SCRATCH
% user intput 
subjID = 'p004';

% Paths (Find data folder using location relative to Scripts folder)
folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
baseDir = fullfile(folders{1:(find(strcmp(folders, 'Scripts'), 1)-1)});
dirinput = [baseDir,filesep,fullfile('Data','SiN','derivatives', subjID,'task-sin')];
diroutput = [baseDir,filesep,fullfile('Data','SiN','derivatives', subjID,'task-sin','pipeline_task-sin_01')];
%
automagic_project_file = 'V:\Projects\Spinco\SINEEG\Data\SiN\derivatives\p004_task-sin_res\project_state.mat';


% Input template, name 
% project_template = [baseDir,filesep,fullfile('Data','SiN','preproc_automagic','project_state.mat')];
mkdir(diroutput)

% 
% Load template 
eeglab nogui
addAutomagicPaths();
load(automagic_project_file); % This loads object self of class 

%% 
% Define new project 
name = 'taskSin'; 
dataFolder = dirinput;
resultsFolder = diroutput;
Params = self.params; % param from previous
ext = '.set';
VisualisationParams = struct();
samplingrate = 2048; %WhY hardcoding this ? 

project = Project(name, dataFolder, resultsFolder, ext, samplingrate, Params, VisualisationParams);
project.preprocessAll();
project.interpolateSelected();
