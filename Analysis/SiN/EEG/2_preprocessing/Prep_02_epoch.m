
%% EPOCH Data
% ======================================================================
% - Load preprocessed datasets
% - Epoch around onset of the target words 

%% ---------------------------------------------------------------------------
clear all; close all; 

% user input
subjID = 'p004';
pipelineID = 'pipeline-01';
taskID = 'task-sin';

% Paths 
folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
baseDir = fullfile(folders{1:(find(strcmp(folders, 'Scripts'), 1)-1)});
dirinput_raw = fullfile(baseDir,'Data','SiN','derivatives', pipelineID, taskID,subjID) ;
dirinput_deriv = fullfile(baseDir,'Data','SiN','derivatives', pipelineID, [taskID,'_res'],subjID) ;
diroutput = fullfile(baseDir,'Data','SiN','derivatives',  pipelineID, [taskID,'_res_epoched'],subjID);


%%  find files 

fileinput = dir([dirinput_deriv,filesep,'*p_',subjID,'*.mat']) % find preproc file

%% Load preprocessed file 

eeglab nogui
preproc_data = load(fullfile(fileinput.folder,fileinput.name));
EEG = preproc_data.EEG;
% Interpolate (this may be temporal , it may be done with Automagic)

preproc_data.automagic.tobeInterpolated
EEG = pop_interp(EEG, preproc_data.automagic.tobeInterpolated,'spherical');


% Add accuracy to target events in the EEG dataset 
% ----------------------------------------------------------------------
% Read targets accuracy 
file_event = dir([dirinput_raw,filesep,'*_events_accu.tsv']);
tabEvent = readtable(fullfile(file_event.folder,file_event.name),'FileType','delimitedtext');

% list triggers : 1st digit = type , 2nd digit = target position , 3rd digit = word 
% REF: https://github.com/Neuroling/SPINCO_SINEEG/tree/main/Experiments/SiN/SiN_task#readme
target_codes = {'111','112','113','114','211','212','213','214','121','122','123','124','221','222','223','224','131','132','133','134','231','232','233','234'};



%%
% find event index for target events in both EEG.event and tsv file 
idx_targets_in_tsv = find(ismember(cellstr(num2str(tabEvent.VALUE)),target_codes));

% replace 1 and 0 by string
accu_str = replace(string(tabEvent.ACCURACY), {'1', '0'}, {'cor', 'inc'});

% Combine target code and accuracy 
accu_str(idx_targets_in_tsv) = strcat(accu_str(idx_targets_in_tsv),'_',string(tabEvent.VALUE(idx_targets_in_tsv)));

% Add it to the EEG events, add 'miss' if response was missing 
for i = 1:length(idx_targets_in_tsv)
    if ismissing(accu_str(idx_targets_in_tsv(i)))        
        EEG.event(idx_targets_in_tsv(i)).type = string(strcat('miss_',EEG.event(idx_targets_in_tsv(i)).type));
    else 
        EEG.event(idx_targets_in_tsv(i)).type = accu_str(idx_targets_in_tsv(i))
    end 
    
end 
    
 
%%
[ALLEEG, EEG] = eeg_store(ALLEEG,EEG, CURRENTSET);
EEG = eeg_checkset(EEG);


% Resample 
EEG = pop_resample( EEG, 256);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1,'gui','off'); 


%% Epoch    
% --------------------------------------
  %Define events to epoched 
  targets_with_missing_resp = find(~cellfun('isempty', regexp({EEG.event.type}, '^(miss)')));
  targets_with_resp = find(~cellfun('isempty', regexp({EEG.event.type}, '^(cor_|inc_)')));
  
  event_types_to_epoch = unique({EEG.event(targets_with_missing_resp).type});
  
   % print info 
  disp(['>>-> ' , num2str(length(targets_with_resp) + length(targets_with_missing_resp) ), ' target events found '])
  disp(['>>---> ' , num2str(length(targets_with_resp)), ' target events found with a response'])
  disp(['>>-----> ',num2str(length(targets_with_missing_resp)), ' target events found with a response'])
  
% do epoching
 EEG =  pop_epoch(EEG, event_types_to_epoch, [-0.5  0.5], 'newname', ... 
         'epoched_set', ...
        'epochinfo', 'yes')
  

%% Save and  Export 
 
