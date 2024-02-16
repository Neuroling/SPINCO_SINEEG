clear all; close all; 

% Preprocessing step 03
% ======================================================================
% - Reject Independent Components marked as bad 
% - Re-reference to average
% - Downsample
% - Do some additional labeling of the events
% - Epoch 

% Paths
thisDir = mfilename('fullpath');
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
addpath(fullfile(baseDir,'Tools','eeglab_current','eeglab2023.0'));

taskID = 'task-sin';
dirinput = fullfile(baseDir, 'Data','SiN','derivatives_SM',taskID) ;
diroutput = dirinput;

% User INPUT 
epoch_t0 = -0.5; % start time in seconds  
epoch_t1 = 0.5;  % end time in seconds  

%allchansEEG = EEg


%% get chanLocs
f=1;
files = dir([dirinput,filesep,'**',filesep,'*',taskID,'*_ds.set']);

fileinput = fullfile(files(f).folder, files(f).name); 
subjID=files(f).name(1:4);

% load set  
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
EEG = pop_loadset('filename',fileinput);
EEG = pop_select(EEG, 'rmchannel', {'EXT1', 'EXT2','EXT3','EXT4'});
origEEG = EEG;

%% find data 
files = dir([dirinput,filesep,'**',filesep,'*',taskID,'*_marked.set']);
%% 
run = 1;
if run == 1
%% loop thru files 

countEp = []; countICsKept = [];countICsRej=[]; countChans = []; 
for f = 1:length(files)
%for f= 1:2

    % input file 
    fileinput = fullfile(files(f).folder, files(f).name); 
    subjID=files(f).name(1:4);
    
    % load set  
    [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
    EEG = pop_loadset('filename',fileinput);
    
       
    %% Exclude components flagged as bad 
    EEG = pop_subcomp( EEG, find(EEG.reject.gcompreject), 0);
    EEG.comments = pop_comments(EEG.comments,'','rejected ICs manually flagged as bad',1);  
    
    %% Interpolate missing channels
    EEG = pop_interp(EEG, origEEG.chanlocs, 'spherical');
  
    %% Add accuracy to target events in the EEG dataset 
    % ----------------------------------------------------------------------
    % Read targets accuracy 
    file_event = dir([EEG.filepath,filesep,'*_events_accu.tsv']);
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

    % Add it to the EEG events, add 'miss' if response was missing 
    for i = 1:length(idx_targets_in_tsv)
        if ismissing(accu_str(idx_targets_in_tsv(i)))        
            EEG.event(idx_targets_in_tsv(i)).type = string(strcat('miss/',EEG.event(idx_targets_in_tsv(i)).type));
        else 
            EEG.event(idx_targets_in_tsv(i)).type = accu_str(idx_targets_in_tsv(i));
        end 

    end 

    EEG = eeg_checkset(EEG); 
    
 
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
      EEG =  pop_epoch(EEG, event_types_to_epoch, [epoch_t0 epoch_t1],...
            'epochinfo', 'yes');
    %% Save 
    newsetname = strrep(EEG.filename,'_marked','_rej_ep');
    EEG.setname = newsetname; 
    pop_saveset (EEG, newsetname,files(f).folder);
    
    %%
    countEp(f) =  size(EEG.data,3);
    countICsKept(f) =  size(EEG.icaweights,1);                                                   
    countICsRej(f) =  size(EEG.icaweights,2)- size(EEG.icaweights,1);
    countChans(f) = 64-length(EEG.chanlocs);
end

%% Save counts
header= {'subjID','n_epoch','ICs_kept', 'ICs_rej','Chans_rej'} ;
data2save = [string(header)',[string({files.name});countEp;countICsKept;countICsRej;countChans]]; 
data2save = data2save'

%% save in Excel
cd(diroutput);
outputfilename = 'count_badSegs_rejICs.xls';
if exist(outputfilename,'file') == 0;
    writematrix(data2save,outputfilename);
 else disp('CANNOT SAVE FILE, IT ALREADY EXISTS!!');
end 
end
