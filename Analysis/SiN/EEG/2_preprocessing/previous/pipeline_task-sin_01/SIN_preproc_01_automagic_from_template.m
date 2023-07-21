clear all; close all; 
% Run Automagic project
% ======================================================================
% - Reads parameters from a template-project created in GUI (project_state.mat file)
% - Adjusts name and directories of the project

dirinput = 'V:\Projects\Spinco\SINEEG\Data\SiN\derivatives\pipeline_task-sin_01\p005\' ;
diroutput = 'V:\Projects\Spinco\SINEEG\Data\SiN\derivatives\pipeline_task-sin_01\p005_resauto\' ;
template_project = 'V:\Projects\Spinco\SINEEG\Scripts\Analysis\SiN\EEG\2_preprocessing\pipeline_task-sin_01\project_state.mat';

%% Project definition
load(template_project) 

% %% Define new project 
 name =  'SIN_PIPE01'; 
 dataFolder = dirinput;
 resultsFolder = diroutput;
 ext = '.set';
 Params = self.params; % param from previous
 VisualisationParams = struct();
 samplingrate = 2048; 
 

%% Run project       
eeglab nogui
addAutomagicPaths();
project = Project(name, dataFolder, resultsFolder, ext, Params, VisualisationParams);
project.preprocessAll();
