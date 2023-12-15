
%% EPOCH Data
% ======================================================================
% - Load preprocessed datasets
% - Epoch around onset of the target words 

%% ---------------------------------------------------------------------------
clear all; close all; 
% Use subject list if you want to epoch several subjects at once 
subjectList = {'s001','s002','s003','s004','s005','s006','s007','s008','s009','s010','s011','s012','s013','s015'};
subjectList = {'s001'};

%%
for s = 1:length(subjectList)
    % % user input
     subjID = subjectList{s};

    pipelineID = 'pipeline-01';
    taskID = 'task-sin';
    epoch_t0 = -0.5; % start time in seconds  
    epoch_t1 = 0.5;  % end time in seconds  

    % Paths 
    folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
    baseDir = fullfile(folders{1:(find(strcmp(folders, 'Scripts'), 1)-1)});
    addpath(fullfile(baseDir,'Tools','eeglab_current','eeglab2023.0'))

    dirinput_raw = fullfile(baseDir,'Data','SiN','derivatives', pipelineID, taskID,subjID) ;
    dirinput_deriv = fullfile(baseDir,'Data','SiN','derivatives', pipelineID, [taskID,'_preproc'],subjID) ;
    diroutput = fullfile(baseDir,'Data','SiN','derivatives',  pipelineID, [taskID,'_preproc_epoched'],subjID);

    %  find files - won't work if "current folder" is anything but the root
    fileinput = dir([dirinput_deriv,filesep,'*p_',subjID,'_',taskID,'*.mat']); % find preproc file

    %% Load preprocessed file 
    eeglab ;
    preproc_data = load(fullfile(fileinput.folder,fileinput.name));
    EEG = preproc_data.EEG;
    
    %% Remove channels deleted by automagic (they are NaN after automagic)   
     EEG  = pop_select( EEG, 'rmchannel',preproc_data.automagic.tobeInterpolated);

    %% Re-reference to average of all available scalp electrodes        
    % --------------------------------------------------------------------    
    %re reference to average 
     EEG = pop_reref( EEG, []);
    
    %% Interpolate (this option may be commented if interpolating is done with Automagic)
    % ---------------------------------------------------------------------
    
    preproc_data.automagic.tobeInterpolated
    EEG = pop_interp(EEG, preproc_data.automagic.tobeInterpolated,'spherical');
    pop_comments(EEG.comments,'','chans interpolated after automagic',1);
    
    %% Add accuracy to target events in the EEG dataset 
    % ----------------------------------------------------------------------
    % Read targets accuracy 
    file_event = dir([dirinput_raw,filesep,'*_events_accu.tsv']);
    tabEvent = readtable(fullfile(file_event.folder,file_event.name),'FileType','delimitedtext');

    % list triggers : 1st digit = type , 2nd digit = target position , 3rd digit = word 
    % REF: https://github.com/Neuroling/SPINCO_SINEEG/tree/main/Experiments/SiN/SiN_task#readme
    target_codes = {'111','112','113','114','211','212','213','214','121','122','123','124','221','222','223','224','131','132','133','134','231','232','233','234'};

    % find event index for target events in both EEG.event and tsv file 
    idx_targets_in_tsv = find(ismember(cellstr(num2str(tabEvent.VALUE)),target_codes));

    % replace 1 and 0 by string
    accu_str = replace(string(tabEvent.ACCURACY), {'1', '0'}, {'cor', 'inc'});

    % Combine target code and accuracy (from .tsv table) in the same event label   
    accu_str(idx_targets_in_tsv) = strcat(accu_str(idx_targets_in_tsv),'/',string(tabEvent.VALUE(idx_targets_in_tsv)));
    
    % Replaced separator '_' by '/' for being able to filter in MNE
    accu_str = replace(accu_str,{'/11','/12','/13','/21','/22','/23'},{'/NV/CallSign/','/NV/Colour/','/NV/Number/','/SSN/CallSign/','/SSN/Colour/','/SSN/Number/'});

    %% Add it to the EEG events, add 'miss' if response was missing 
    for i = 1:length(idx_targets_in_tsv)
        if ismissing(accu_str(idx_targets_in_tsv(i)))        
            EEG.event(idx_targets_in_tsv(i)).type = string(strcat('miss/',EEG.event(idx_targets_in_tsv(i)).type));
        else 
            EEG.event(idx_targets_in_tsv(i)).type = accu_str(idx_targets_in_tsv(i));
        end 

    end 

    EEG = eeg_checkset(EEG); 

    %% Resample 
    EEG = pop_resample( EEG, 256);

    %% Epoch    
    % --------------------------------------
      %Define events to epoched 
      targets_with_missing_resp = find(~cellfun('isempty', regexp({EEG.event.type}, '^(miss/)')));
      targets_with_resp = find(~cellfun('isempty', regexp({EEG.event.type}, '^(cor/|inc/)')));

      event_types_to_epoch = unique({EEG.event(targets_with_resp).type});

       % print info 
      disp(['>>-> ' , num2str(length(targets_with_resp) + length(targets_with_missing_resp) ), ' target events found '])
      disp(['>>---> ' , num2str(length(targets_with_resp)), ' target events found with a response'])
      disp(['>>-----> ',num2str(length(targets_with_missing_resp)), ' target events missed a response'])

    % do epoching
      EEG =  pop_epoch(EEG, event_types_to_epoch, [epoch_t0 epoch_t1], 'newname', ... 
             strrep(fileinput.name,'.mat','_avgRef_epo'), ...
            'epochinfo', 'yes');
      
%       % Remove events that are not target item onset (filters out those
%       with labels with less than 7 characters) --> this was done to facilitate import in MNE 
%         event_types={EEG.event.type};
%         n=1;
%         indxs=[];
%         for i = 1:length(event_types)
%             if length(event_types{i}) <= 7
%                 indxs(n)=i;
%                 n=n+1;
%             end
%         end
% 
%         EEG = pop_editeventvals(EEG, 'delete', indxs);

    %% Save and  Export 
    mkdir(diroutput)
    pop_saveset (EEG, [EEG.setname,'.set'], diroutput);
    clear EEG ALLEEG
end
