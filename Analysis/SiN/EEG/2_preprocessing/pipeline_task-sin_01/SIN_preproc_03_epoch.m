clear all; close all; 
%% EPOCH Data
% ======================================================================
% - Load preprocessed datasets
% - Epoch around onset of the target words 

%% ---------------------------------------------------------------------------
% user input
subjID = 'p004';
pipelineID = 'pipeline_task-sin_01';
taskID = 'task-sin';


% Paths 
folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
baseDir = fullfile(folders{1:(find(strcmp(folders, 'Scripts'), 1)-1)});

dirinput = fullfile(baseDir,'Data','SiN','derivatives', subjID,taskID) ;
diroutput = fullfile(baseDir,'Data','SiN','derivatives', subjID, taskID, pipelineID);

% list triggers : 1st digit = type , 2nd digit = target position , 3rd digit = word 
% Ref https://github.com/Neuroling/SPINCO_SINEEG/tree/main/Experiments/SiN/SiN_task#readme
target_codes = {'111','112','113','114','211','212','213','214','121','122','123','124','221','222','223','224','131','132','133','134','231','232','233','234'};

%%  find files 
file_event = dir([dirinput, filesep, '**',filesep,'*_events_accuracy.csv']);
file_eeg = dir([dirinput, filesep, '*.set']); %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%>>>>>> Expect change in file pattern to load preprocessed files

% Read targets accuracy 
tabEvent = readtable(fullfile(file_event.folder,file_event.name))


%% Add accuracy to target events in the EEG dataset 
for e = 1:height(tabEvent)
    %if it is a target use its unique latency to find it in the eeg dataset 
    istarget = find(contains(target_codes,num2str(tabEvent.VALUE(e))));
    if length(istarget) == 1
        eventIdx = find(cell2mat({EEG.event.latency}) == tabEvent.SAMPLES(e))             
        
        %rename the event to include accuracy info  
        if tabEvent.RESPONSE(e) == 1
            EEG.event(eventIdx).type = ['cor_',EEG.event(eventIdx).type] ;           
        
        elseif tabEvent.RESPONSE(e) == 0 
            EEG.event(eventIdx).type = ['incor_',EEG.event(eventIdx).type]; 
            
        end
    end    
   
    
end
[ALLEEG, EEG] = eeg_store(ALLEEG,EEG, CURRENTSET);
EEG = eeg_checkset(EEG);

%% 





% comprehension response onset are discarded
    EEG = pop_epoch(EEG, {'DI24'}, [-4.3  1], 'newname', ... 
        ['sbj_' num2str(sbj) '_DiN_epoched.set'], ...
        'epochinfo', 'yes');
    EEG = eeg_checkset(EEG);
    [ALLEEG EEG CURRENTSET] = eeg_store(ALLEEG, EEG, CURRENTSET);
    eeglab redraw

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


% comprehension response onset are discarded
    EEG = pop_epoch(EEG, {'DI24'}, [-4.3  1], 'newname', ... 
        ['sbj_' num2str(sbj) '_DiN_epoched.set'], ...
        'epochinfo', 'yes');
    EEG = eeg_checkset(EEG);
    [ALLEEG EEG CURRENTSET] = eeg_store(ALLEEG, EEG, CURRENTSET);
    eeglab redraw




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
