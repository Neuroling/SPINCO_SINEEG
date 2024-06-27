
%% EPOCH Data
% ======================================================================
% gfraga & samuelmull
% - Load preprocessed datasets
% - Epoch around onset of the target words 

%% ---------------------------------------------------------------------------
clear all; close all; 
% Use subject list if you want to epoch several subjects at once 
% subjectList = {'s001','s002','s003','s004','s005','s006','s007','s008','s009','s010','s011','s012','s013','s015'};
subjectList = {'s201','s202', 's203', 's204'};

taskID = 'task-sin';
pipelineID = 'pipeline-automagic-01-unalignedTriggers';
derivativesFolder = 'derivatives_exp2-unalignedTriggers';
epoch_t0 = -0.5; % start time in seconds  
epoch_t1 = 0.5;  % end time in seconds  

%%
for s = 1:length(subjectList)
    % % user input
     subjID = subjectList{s}


    % Paths 
    folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
    baseDir = fullfile(folders{1:(find(strcmp(folders, 'Scripts'), 1)-1)});
    
%     addpath(fullfile(baseDir,'Tools','eeglab_current','eeglab2023.0')) %
% %     Because this adds the folder AND subfolders to the path, and EEGlab
% %     keeps giving a warning that you shouldn't do that, it is better to
% %     instead manually add it to the path (Only selected Folder, not
% %     selected folder and subfolders)

    dirinput_raw = fullfile(baseDir,'Data','SiN',derivativesFolder, pipelineID, taskID,subjID) ;
    dirinput_deriv = fullfile(baseDir,'Data','SiN',derivativesFolder, pipelineID, [taskID,'_preproc'],subjID) ;
    diroutput = fullfile(baseDir,'Data','SiN',derivativesFolder,  pipelineID, [taskID,'_preproc_epoched'],subjID);
    chanLocsFile = fullfile(baseDir,'Data','SiN','_acquisition','_electrodes','Biosemi_64ch_EEGlab_xyz.tsv');

    %  find files - won't work if "current folder" is anything but the root
    fileinput = dir([dirinput_deriv,filesep,'*p_',subjID,'_',taskID,'*.mat']); % find preproc file

    %% Load preprocessed file 
    eeglab ;
    preproc_data = load(fullfile(fileinput.folder,fileinput.name));
    EEG = preproc_data.EEG;
    

    %% load channel locations
    % Note: This shouldn't be necessary. It wasn't in Exp1, but it is in Exp2. 
    % Otherwise, the interpolation won't work because of missing channel
    % locations. (Maybe I did something wrong in the settings for automagic
    % and they were removed? Is that all that happened or did that also
    % cause some other issues? I mean, if I add the locations now, will it
    % be okay, or did I already screw up?)
    % Also, because the External channels have already been removed, you cannot 
    % load the locations from the file 'Biosemi_71ch_EEGlab_xyz.tsv'. So I created 
    % the file 'Biosemi_64ch_EEGlab_xyz.tsv' which is the exact same but the
    % additional channels not included.
    EEG = pop_chanedit(EEG,'load',chanLocsFile);
    
    %% Interpolate electrodes marked for interp in Automagic
    % ---------------------------------------------------------------------  
    EEG = pop_interp(EEG, preproc_data.automagic.tobeInterpolated,'spherical');
    pop_comments(EEG.comments,'','chans interpolated after automagic',1);
        
    
    %% Re-reference to average of all available scalp electrodes        
    % --------------------------------------------------------------------    
    %re reference to average 
    EEG = pop_reref( EEG, []);
    
    %% Add accuracy to target events in the EEG dataset 
    % ----------------------------------------------------------------------
    % Read targets accuracy 
    file_event = dir([dirinput_raw,filesep,'*_events_accu.tsv']);
    tabEvent = readtable(fullfile(file_event.folder,file_event.name),'FileType','delimitedtext');

    % list triggers : 1st digit = type , 2nd digit = target position , 3rd digit = word 
    % REF: https://github.com/Neuroling/SPINCO_SINEEG/tree/main/Experiments/SiN/SiN_task#readme
    target_codes = {'111', '112', '113', '114','115', '116', '117', '118', '211', '212', '213', '214','215', '216', '217', '218','311', '312', '313', '314', '315', '316', '317', '318', '121', '122', '123', '124', '125', '126', '127', '128', '221', '222', '223', '224', '225', '226', '227', '228', '321', '322', '323', '324', '325', '326', '327', '328', '131', '132', '133', '134', '135', '136', '137', '138', '231', '232', '233', '234', '235', '236', '237', '238', '331', '332', '333', '334', '335', '336', '337', '338'};
%     target_codes = {'111','112','113','114','211','212','213','214','121','122','123','124','221','222','223','224','131','132','133','134','231','232','233','234'};

    % find event index for target events in both EEG.event and tsv file 
    idx_targets_in_tsv = find(ismember(cellstr(num2str(tabEvent.VALUE)),target_codes));

    % replace 1 and 0 by string
    accu_str = replace(string(tabEvent.ACCURACY), {'1', '0'}, {'cor', 'inc'});

    % Combine target code and accuracy (from .tsv table) in the same event label   
    accu_str(idx_targets_in_tsv) = strcat(accu_str(idx_targets_in_tsv),'/',string(tabEvent.VALUE(idx_targets_in_tsv)));
    
    % Replaced separator '_' by '/' for being able to filter in MNE
    accu_str = replace(accu_str,{'/11','/12','/13','/21','/22','/23','/31','/32','/33'},{'/NV/CallSign/','/NV/Colour/','/NV/Number/','/SSN/CallSign/','/SSN/Colour/','/SSN/Number/', '/clear/CallSign/', '/clear/Colour/', '/clear/Number/'});

    % Add it to the EEG events, add 'miss' if response was missing 
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
