 % =========================================================================
% Audio Trigger adjust 
% =========================================================================
% Author: G.FragaGonzalez
% Description:
% - Align trigger latencies to the trigger '256' sent by biosemi using the click in audiofiles 
% - This deals with delays (jittered or not) in audio output
% - Uses EEG.event from eeglab dataset 


%EEG = pop_biosig('p003_task-sin.bdf', 'importannot','off','ref', 48, 'refoptions',{ 'keepref' 'on' }, 'rmeventchan','off');

function EEG = alignTriggersToAudio(EEG)

%% Detect click Onsets to use them for alignment
threshold = 0.8; % intensity threshold 
clickDur = 0.1 ;% Duration of the click (sec)

%Normalize audio so that max value is 1 
erg1_norm = EEG.data(end,:,:)*(1/max(abs(EEG.data(end,:,:))));

% Find clicks
boundaries = find(erg1_norm > threshold);
clickOffsets = boundaries(diff(boundaries) > floor(clickDur*EEG.srate));
clickOnsets = clickOffsets - floor(clickDur*EEG.srate);
disp(['-->--> ', num2str(length(clickOnsets)),' clicks detected in audiochannel ergo1'])

%%  Find Psychopy triggers indicating trial start
idxs_1 = (find(cell2mat({EEG.event.type})==1));

% Check we have the correct number. We expect 96 x 4 (4 blocks for 96 trials)
if length(idxs_1) ~= 384
    error(['[ERROR!] Unexpected number of trial starting trigger: ',  num2str(length(idxs_1))])      
else 
   disp(['-->>--> '  num2str(length(idxs_1)), ' task trials detected'])    
    
   %% Loop thru each trial 
    for i= 1:length(idxs_1)
      
       currIdx = idxs_1(i); % current index in the array of all events
       
       %Find click Onset that is closest (following) to the current latency
       timeDiffs = clickOnsets-EEG.event(currIdx).latency;
       delay = min(timeDiffs(timeDiffs>0)); 
        
        % Search next 15 events for trigger '7' at the response grid (thus, end of this trial)         
        nextRespGridIdx = find(cell2mat({EEG.event(currIdx : currIdx+15).type})==7,1, 'first')-1;    
        thisTrialTriggers_idx  = currIdx : (currIdx + nextRespGridIdx); % all triggers for this trial (index relative to the all events array)
        
        % Find events correspond to target items (200 : 240) 
        targets_idx = thisTrialTriggers_idx(cell2mat({EEG.event(thisTrialTriggers_idx).type}) > 100 & cell2mat({EEG.event(thisTrialTriggers_idx).type}) < 240);
        
        % Add delay to trial start trigger and all targets 
        EEG.event(currIdx).latency = EEG.event(currIdx).latency + delay;
        for ii = 1:length(targets_idx)            
                EEG.event(targets_idx(ii)).latency = EEG.event(targets_idx(ii)).latency + delay;
                disp(['[->] Added ' num2str(delay) ' data points to ' num2str(EEG.event(targets_idx(ii)).type), ' latency'])
        end
                      
    end % close trial loop
    
end % close if 
