% PLOT AUDIO AND EEG TRIGGERS
% ==========================================
%- Plot audio signal sent to ergo 1 
% - Plot the events after timing correction 
% 


%%
for i = 1:length(idxs_1)

    currIdx = idxs_1(i)
    % Search next 15 events for trigger '7' at the response grid (thus, end of this trial)         
    nextRespGridIdx = find(cell2mat({EEG.event(currIdx : currIdx+15).type})==7,1, 'first')-1;    
    thisTrialTriggers_idx  = currIdx : (currIdx + nextRespGridIdx); % all triggers for this trial (index relative to the all events array)
    markerTimes = EEG.times(cell2mat({EEG.event(thisTrialTriggers_idx).latency}))/1000 
    
    % find which data points should be plotted 
    pnts2plot = EEG.event(thisTrialTriggers_idx(1)).latency:EEG.event(thisTrialTriggers_idx(end)).latency ; 
    times2plot = EEG.times(pnts2plot)/1000     
    
   %% Plot data    
   % normalize ergo channel data 
    erg1_norm = EEG.data(end,pnts2plot,:)*(1/max(abs(EEG.data(end,pnts2plot,:))));
   %signal plot 
    figure; 
    plot(EEG.times(pnts2plot)/1000,erg1_norm,'color',[0.5 0.5 0.5]);
    ylim([-.2,.2])
    hold on;
    % add events
    for m = 1:length(markerTimes)
        xline(markerTimes(m),'red')        
        hold on; 
    end
    
end
        
        

