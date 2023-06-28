
% =========================================================================
% Import SOURCE bdf files 
% =========================================================================
% Author: G.FragaGonzalez
% Description:
% - Read source .bdf file (1 file expected for the entire session)
% - Adjust triggers per trial relative to audio-output
% - Divide the data using triggers to split resting state(s) and task 
% - Read channel locations 
% - Create and save 'raw' eeglab datasets

%% user inputs
clear all; close all ;
subjID = 'p004'; 


%% Paths and files
addpath([fileparts(matlab.desktop.editor.getActiveFilename),filesep,'functions'])

%% 
folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
baseDir = fullfile(folders{1:(find(strcmp(folders, 'Scripts'), 1)-1)});

%
dirinput = [baseDir,filesep,fullfile('Data','SiN','sourcedata',subjID)];
chanLocsFile = [baseDir,filesep,fullfile('Data','SiN','_acquisition','_electrodes','Biosemi_73ch_EEGlab_xyx.tsv')];

% find raw eeg
file  = dir([dirinput,filesep,'*.bdf']);

% Define current subject input and output dir 
fullFileInput = [file.folder,filesep,file.name];   
diroutput = strrep([file.folder],'sourcedata','rawdata'); % Assuming only one 'raw' folder is present in the full path 
mkdir(diroutput)   

%% EEGLAB ------------------------------------------------------
if length(file)~= 1
   error('Eror. More than one source .bdf file found. Revise your paths') 
else 
   eeglab nogui 

   % import 
   EEG = pop_biosig(fullFileInput, 'importannot','off','ref', 48, 'refoptions',{ 'keepref' 'on' }, 'rmeventchan','off'); % Problems reading events when importing with pop_readbdf 

   % load channel locations
   EEG = pop_chanedit(EEG,'load',chanLocsFile); 

   %% Correct events 
   [EEG, trial_delays] = alignTriggersToAudio(EEG);

   %% split resting-state tasks and save 
   UREEG = EEG; % COpy of dataset before split        
   % Resting state parts         
    splits = struct('segment_name', {'task-rest-pre','task-rest-post'},... 
                    'segment_duration', {240,240},...% duration in seconds 
                    'onset_trigger',{8, 9},...
                    'head', {1 ,1},...% seconds before onset trigger  
                    'tail',{1, 1}); % seconds after offset trigger  

    % Loop thru desired output files 
    for i = 1:length(splits)
        % Overwrite with original dataset (no split)  
        EEG = UREEG; 

        % Find unique onset trigger   
        triggerIdx = find(cell2mat({EEG.event(:).type})== splits(i).onset_trigger);
        if length(triggerIdx) ~= 1    
            error (['[error] It seems you have more than one event with code ', num2str(splits(i).onset_trigger), '. Check why']) 
        else 

           % Find data point to the relevant event +/- defined number of seconds before and after
           segment_t0 = EEG.event(triggerIdx).latency - (splits(i).head*EEG.srate) ; 
           segment_t1 = EEG.event(triggerIdx).latency + (splits(i).segment_duration*EEG.srate) + (splits(i).tail*EEG.srate);

           % select data    
            EEG = pop_select( EEG, 'point',[segment_t0 segment_t1]  );

           % save dataset 
            newSetName = strrep(file.name,'.bdf',['_', splits(i).segment_name]);
            EEG  = pop_newset(ALLEEG, EEG, 0,'setname',newSetName,'gui','off','overwrite','on'); 
            pop_saveset (EEG, newSetName,diroutput);                  

            clear EEG
        end
    end % close splits loop 


%% split Main task and save 
   
   % Resting state parts         
    split = struct('segment_name', {'task-sin'},... 
                    'onset_trigger',{5},... % unique onset trigger 
                    'offset_trigger', {55},...% trigger to resting state after task instructions                    
                    'head', {1},...% seconds before onset trigger  
                    'tail',{1}); % seconds after offset

    EEG = UREEG; 
    
    % Find unique onset trigger   
    triggerIdx = find(cell2mat({EEG.event(:).type})== split.onset_trigger);
    if length(triggerIdx) ~= 1    
        error (['[error] It seems you have more than one event with code ', num2str(split.onset_trigger), '. Check why']) 
    else 

       % Find data point to the relevant event +/- defined number of seconds before and after
       segment_t0 = EEG.event(triggerIdx).latency - (split.head*EEG.srate) ; 
       segment_t1 = EEG.event(triggerIdx).latency + (split.segment_duration*EEG.srate) + (split.tail*EEG.srate);

       % select data    
        EEG = pop_select( EEG, 'point',[segment_t0 segment_t1]  );

       % save dataset 
        newSetName = strrep(file.name,'.bdf',['_', split.segment_name]);
        EEG  = pop_newset(ALLEEG, EEG, 0,'setname',newSetName,'gui','off','overwrite','on'); 
        pop_saveset (EEG, newSetName,diroutput);                  

        clear EEG
    end


end % close if length(files)





   
    



