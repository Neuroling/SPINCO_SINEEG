 % =========================================================================
% Audio Trigger adjust 
% =========================================================================
% Author: G.FragaGonzalez
% Description:
% - Align trial event latencies (target word onsets, offsets) to clicks 
% - Clicks embeded in start of audio file. Sent to last EEG channel 'ergo1'
% - Uses EEG.event from eeglab dataset 
%
% Inputs:
% - EEG variable (loaded dataset in EEGlab)
%
% Outputs: 
% - EEG_mod: dataset with adjusted triggers
% - trial_delays_set: array with delays in seconds for each trial 

function [EEG_mod, trial_delays_sec] = alignTriggersToAudio(EEG, event_chan)
    
    EEG_mod = EEG; 

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

    triggers = (cell2mat({EEG_mod.event.type}));
    for i = 1:length(triggers)
        if triggers(i) <= 83 && triggers(i)>= 44
            if (triggers(i) == 55 && triggers(i-1) == 300) || triggers(i) ~= 55  
                if (triggers(i) == 60 && triggers(i-1) == 300) || triggers(i) ~= 60  
                    triggers(i) = triggers(i) + 256;
                    EEG_mod.event(i).type = triggers(i);
                end
            end

        end
    end

%     %%
%     for i = 1:length(triggers)
%         if triggers(i) == 100 | triggers(i) == 200  | triggers(i) == 300 
% %             triggers(i)
%             triggers(i-1)
%             EEG_mod.event(i).latency - EEG_mod.event(i-1).latency
%         end
%     end
%%   
    
    %Normalize audio signal so that max value is 1 
    erg1_norm = event_chan.data(end,:,:)*(1/max(abs(event_chan.data(end,:,:))));

    % Event trigger coded 1 indicate start of the file     
    idxs_1 = (find(cell2mat({EEG_mod.event.type})==1));

    % Check we have the correct number. We expect 96 x 4 (4 blocks for 96 trials)
    if length(idxs_1) ~= 288
        error(['[ERROR!] Unexpected number of trial onset triggers: ',  num2str(length(idxs_1))])      
    else
        
        disp(['OK >>> '  num2str(length(idxs_1)), '  trial onset detected'])
        
       %% Trial loop 
        trial_delays_sec = zeros(1,length(idxs_1));
        
        for i= 1:length(idxs_1)
           % current trial index in the array of all events
           currIdx = idxs_1(i);
           disp(['--> Finding triggers in trial #', num2str(i)])

           % Search in next events for trigger '7' indicating response grid ( search in 10 subsequent events)
           currIdx_resp = find(cell2mat({EEG_mod.event(currIdx : currIdx+10).type})==7,1, 'first')-1;    
           currTrialEvents  = currIdx : (currIdx + currIdx_resp); % all triggers for this trial (global index in array for all events)

           %% find click in this trial(latencies in data points)
           clickThreshold = 0.9; 
           points2search = EEG_mod.event(currTrialEvents(1)).latency : EEG_mod.event(currTrialEvents(end)).latency;
           clickLatency = points2search(find(erg1_norm(points2search) > clickThreshold,1,'first')); % assuming the audio signal in the last channel 

%         % Optional plots to test clicks were well detected
%           showfigs = 1 
%            if showfigs == 1
%                figure('Renderer', 'painters', 'Position', [400 400 900 600]);
%                plot(points2search,erg1_norm(points2search));
%                title(['Detecting click in trial ',num2str(i)])
%                hold on;
%                xline(clickLatency,'red','LineWidth',1,'LineStyle','--')        
%                pause(1) % 
%                close gcf
%            end
           
           %% adjust target onset triggers to the audio trigger
           delay = clickLatency - EEG_mod.event(currIdx).latency;
           trial_delays_sec(i) = delay/EEG_mod.srate; % save this in output vector with delays for all trials
           
           % From the events for this trial: find triggers to targets (coded between 100 and 340) 
           targets_idx = currTrialEvents(cell2mat({EEG_mod.event(currTrialEvents).type}) >= 100 & cell2mat({EEG_mod.event(currTrialEvents).type}) < 340);
        
           % Add delay to trial start trigger and all targets 
            EEG_mod.event(currIdx).latency = EEG_mod.event(currIdx).latency + delay;
            for ii = 1:length(targets_idx)            
                    EEG_mod.event(targets_idx(ii)).latency = EEG_mod.event(targets_idx(ii)).latency + delay;
                    disp(['[->] Added ' num2str(delay) ' data points ',num2str(delay/EEG_mod.srate),' (sec) to ' num2str(EEG_mod.event(targets_idx(ii)).type), ' latency'])
            end                

        end 
    end % close if
