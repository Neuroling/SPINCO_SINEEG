% =========================================================================
% Import SOURCE bdf files
% =========================================================================
% Author: G.FragaGonzalez
% Description:
% - Read source .bdf file (1 file expected for the entire session)
% - Adjust triggers per trial relative to audio-output
% - Read channel locations
% - Divide the data using triggers to split resting state(s) and task
% - Create and save each part as EEGLAB data

%% Paths
clear all; close all 
thisDir = mfilename('fullpath');
addpath([fileparts(thisDir),filesep,'functions'])
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
% user inputs
subjectlist = {'s204'};
% subjectlist = {'s201','s202','s203','s204'};

%%
for s = 1:length(subjectlist)
    subjID = subjectlist{s};
    
    %% Paths and files

    dirinput = fullfile(baseDir,'Data','SiN','sourcedata',subjID);
    chanLocsFile = fullfile(baseDir,'Data','SiN','_acquisition','_electrodes','Biosemi_71ch_EEGlab_xyz.tsv');
    
    % Find files:
    % source eeg
    file  = dir([dirinput,filesep,'*.bdf']);
    
    % source exp file (log of performance)to copy it into raw folder 
    expfile = dir([dirinput,filesep,'*.csv']);
    expfile = expfile(find(~cellfun(@isempty, regexp({expfile.name}, '\d+\.csv$', 'match')))); % find the one ending in digit + '.csv' 
    
    % Define current subject input and output dir
    fullFileInput = fullfile(file.folder,filesep,file.name);
    diroutput = strrep([file.folder],'sourcedata','rawdata'); % Assuming only one 'rawdata' folder is present in the full path
    mkdir(diroutput)
    
    
    eeglab
    %% EEGLAB ------------------------------------------------------
    if length(file)~= 1
        error('Error. None or more than one source .bdf file found. Revise your paths')
    else
        % Import
        
        pop_editoptions( 'option_storedisk', 0); % Change option to process multiple datasets
        EEG = pop_biosig(fullFileInput,'rmeventchan','off', 'importannot','off','ref', 48, 'refoptions',{ 'keepref' 'on' } ); % Problems reading events when importing with pop_readbdf

        %% Remove external channels 71 & 72  (were not recorded)
        
        EEG = pop_select (EEG, 'channel', [1:70,73]); 

        % load channel locations
        EEG = pop_chanedit(EEG,'load',chanLocsFile);  

%         %% Pilot debug 
%         % Pilot edit for p004
%         if contains(subjID,'p004')
%             disp('added manually events 5 and 55') 
%             EEG = pop_editeventvals(EEG,'insert',{1,[],[],[]},'changefield',{1,'latency',295},'changefield',{1,'type',5});
%             EEG = pop_editeventvals(EEG,'insert',{1,[],[],[]},'changefield',{1,'latency',3650},'changefield',{1,'type',55});
%         end
%         if contains(subjID,'p005')
%             EEG.event(find(cell2mat({EEG.event(:).type})== 6)).type = 5;
%             EEG.event(find(cell2mat({EEG.event(:).type}) == 55)).type = 15; 
%             EEG.event(find(cell2mat({EEG.event(:).type}) == 60,1,'last')).type = 55; 
% 
%         end

        %% Recoding triggers to correct bit-overflow
        % Because event triggers are for some reason stored as a single byte,
        % numbers above 256 overflow back to 1. So triggers 300-339 (which we use
        % for clear trials) are now coded as 44-83. This means that triggers
        % 55 (end of instruction screen) and 60 (end of block) are now the same as
        % the codes that originally were 311 and 316
        %
        % This loop recodes triggers that should be 300-339 by adding +256 to 
        % the triggers between 44 and 83. For codes 55 and 60, it will only recode
        % them to 311 and 316 if they were immediately preceded by code 300.
        % Since 311 and 316 refer to onset of callSign (token_1_tmin), they always 
        % have to follow 300, which refers to audio onset (firstSound_tmin)

        triggers = (cell2mat({EEG.event.type}));
        for i = 1:length(triggers)
            if triggers(i) <= 83 && triggers(i)>= 44
                if (triggers(i) == 55 && triggers(i-1) == 300) || triggers(i) ~= 55  
                    if (triggers(i) == 60 && triggers(i-1) == 300) || triggers(i) ~= 60  
                        triggers(i) = triggers(i) + 256;
                        EEG.event(i).type = triggers(i);
                    end
                end

            end
        end

        %% Realign target events to audio  
        [EEG, trial_delays] = alignTriggersToAudio(EEG);
        EEG.comments = pop_comments(EEG.comments,'','imported,loaded chan locations, NOT realigned triggers',1);
        [ALLEEG EEG CURRENTSET] = eeg_store(ALLEEG, EEG);   % save as a new dataset in ALLEEG

       
       %% SPLIT RESTING STATE  =========================================================
        splits = struct('segment_name', {'task-rest-pre','task-rest-post'},...
            'segment_duration', {300,300},...% duration in seconds
            'onset_trigger',{8, 9},...
            'head', {1 ,1},...% seconds before onset trigger
            'tail',{1, 1}); % seconds after offset trigger

            % Loop thru desired output files
           for i = 1:length(splits)

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
                    EEG.setname = [subjID,'_', splits(i).segment_name];

                    % save dataset
                    newSetName = strrep(file.name,'.bdf',['_', splits(i).segment_name]);
                    newdiroutput = [diroutput,filesep,splits(i).segment_name,filesep,'eeg'];
                    mkdir(newdiroutput)
                    pop_saveset (EEG, newSetName,newdiroutput);
                    [ALLEEG, EEG, CURRENTSET] = eeg_store( ALLEEG, EEG);

                    % Save BIDS metadata 
                    saveBidsMetadata(EEG,newdiroutput,chanLocsFile)

                    %Retrieve dataset before split
                    EEG = eeg_retrieve(ALLEEG, 1); CURRENTSET = 1;

                end      

          end % close splits loop


        %% SPLIT TASK ===========
        split = struct('segment_name', {'task-sin'},...
            'onset_trigger', {55},... % unique onset trigger
            'offset_trigger', {9},...% trigger to instruction of resting state after task 
            'head', {1},...% seconds before onset trigger
            'tail',{1}); % seconds after offset        
            %'onset_trigger',{5},... % unique onset trigge
            %'offset_trigger', {55},...% trigger to resting state after task instructions


        % Find unique onset trigger
        triggerIdx_onset = find(cell2mat({EEG.event(:).type})== split.onset_trigger);
        triggerIdx_offset = find(cell2mat({EEG.event(:).type})== split.offset_trigger);

        % Find data point to the relevant event +/- defined number of seconds before and after
        segment_t0 = EEG.event(triggerIdx_onset).latency - (split.head*EEG.srate);
        segment_t1 = EEG.event(triggerIdx_offset).latency + (split.tail*EEG.srate);


        % select data
        EEG = pop_select(EEG, 'point',[segment_t0 segment_t1]  );
        EEG.setname = [subjID,'_', split.segment_name];


        % save dataset
        newSetName = strrep(file.name,'.bdf',['_', split.segment_name]);
        newdiroutput = fullfile(diroutput,split.segment_name,'eeg');
        mkdir(newdiroutput)
        EEG.filename = fullfile(newdiroutput,newSetName);
        pop_saveset (EEG, newSetName, newdiroutput);
        
        % copy log file 
        newdiroutput_beh = [diroutput,filesep,split.segment_name,filesep,'beh'];
        mkdir(newdiroutput_beh)
        copyfile(fullfile(expfile.folder,expfile.name), newdiroutput_beh)

        %% Gather accuracy
        gather_accuracies_events(EEG,expfile, newdiroutput)

        %% Save BIDS metadata 
        saveBidsMetadata(EEG,newdiroutput,chanLocsFile)

       clear EEG ALLEEG CURRENTSET

     end % close if length(files)

     close all
     disp('0000000000000000000000000000===== next ')
 end
