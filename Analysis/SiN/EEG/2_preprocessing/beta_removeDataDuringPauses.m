
%% Remove data around the pauses  
% ======================================================================
% - Load dataset
% - There were 4 blocks, so 3 period of pauses between blocks that could be
% noise. Exclude data around these time points

%% ---------------------------------------------------------------------------
clear all; close all; 

% Use subject list if you want to epoch several subjects at once 
subjectList = {'s001'};
taskID = 'task-sin'

%%
for s = 1:length(subjectList)
    % user input
    subjID = subjectList{s};
    pipelineID = 'trimbreaks_pipeline-01';
        
    % Paths 
    folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
    baseDir = fullfile(folders{1:(find(strcmp(folders, 'Scripts'), 1)-1)});
    addpath(fullfile(baseDir,'Tools','eeglab_current','eeglab2023.0'))
    
    dirinput = fullfile(baseDir,'Data','SiN','derivatives', pipelineID, taskID,subjID) ;    
    diroutput = dirinput ;
    

    %  find files 
    fileinput = dir([dirinput,filesep,[subjID,'*.set']]); 
    %% Load preprocessed file 
    [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
    EEG = pop_loadset('filename',fileinput.name,'filepath',fileinput.folder);
    [ALLEEG, EEG, CURRENTSET] = eeg_store( ALLEEG, EEG, 0 );


    %% Interpolate (this may be temporal in favor of interpolating with Automagic)

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

    % Combine target code and accuracy 
    accu_str(idx_targets_in_tsv) = strcat(accu_str(idx_targets_in_tsv),'_',string(tabEvent.VALUE(idx_targets_in_tsv)));

    % Add it to the EEG events, add 'miss' if response was missing 
    for i = 1:length(idx_targets_in_tsv)
        if ismissing(accu_str(idx_targets_in_tsv(i)))        
            EEG.event(idx_targets_in_tsv(i)).type = string(strcat('miss_',EEG.event(idx_targets_in_tsv(i)).type));
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
      targets_with_missing_resp = find(~cellfun('isempty', regexp({EEG.event.type}, '^(miss)')));
      targets_with_resp = find(~cellfun('isempty', regexp({EEG.event.type}, '^(cor_|inc_)')));

      event_types_to_epoch = unique({EEG.event(targets_with_resp).type});

       % print info 
      disp(['>>-> ' , num2str(length(targets_with_resp) + length(targets_with_missing_resp) ), ' target events found '])
      disp(['>>---> ' , num2str(length(targets_with_resp)), ' target events found with a response'])
      disp(['>>-----> ',num2str(length(targets_with_missing_resp)), ' target events missed a response'])

    % do epoching
     EEG =  pop_epoch(EEG, event_types_to_epoch, [epoch_t0 epoch_t1], 'newname', ... 
             strrep(fileinput.name,'.mat','_epoched'), ...
            'epochinfo', 'yes');

    %% Save and  Export 
    mkdir(diroutput)
    pop_saveset (EEG, [EEG.setname,'.set'], diroutput);
    clear EEG ALLEEG
end
