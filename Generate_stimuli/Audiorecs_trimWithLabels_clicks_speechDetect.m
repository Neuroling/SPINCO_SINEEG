%% clear all
%% Save files with manually adjusted labels marking the speech ROI 
%--------------------------------------------------------------------
% Author: G.FragaGonzalez
% Desc: 
%   Reads the workspace variable saved after using audioLabeler app.
%   The variable has the name of the source signal (one or multiple files)
%   Here we expect that each file has a 'SpeechDetected' label indicating one
%   fragment with speech
%   If if finds a 'click' label it will first turn that segment into zeros
% In:  just specify the variable (labelSet) and directories 
% Out: saves trimmed files (same name as source files with suffix) in same
% directory as the original files that were used by audioLabeler 

% Specify which label Set you want to use 
labelSet  = labeledSet_164154 ;

%% Read labels 
for f = 1:length(labelSet.Source)
    % identify source signal
    sourcefile = labelSet.Source{f};
    
    % read the source file and trim it to the selected ROI 
    [sig, fs] = audioread(sourcefile); % expects only one channel
    
    %% Check if there are regions with clicks 
    colidx = find(contains(labelSet.Labels.Properties.VariableNames,'click','IgnoreCase',true));
    if ~isempty(colidx)
        disp('removing clicks') 
            tbl = labelSet.Labels{f,colidx} ;
            tbl=tbl{1};
            clickIdx = tbl.ROILimits(1,:)*srate ;
            sig(clickIdx(1):clickIdx(2))=0;
            text = 'Manually adjusted the speech detection and trimmed. Manual selection of a click segment replaced by 0s ';
    else
        text = 'Manually adjusted the speech detection and trimmed. No clicks were removed';
    end
      
    %%
    % find label and get indices of ROI    
    idxs  = round(fs*labelSet.Labels.SpeechDetected{f}.ROILimits(1,:)); % expects only one ROI per file! convert from secs to datapoint 
    startidx = idxs(1); 
    if startidx==0
        startidx=1;
    end
    endidx = idxs(2);
    sig_trim = sig(startidx:endidx);  
   %%
    %write file 
    outputname = strrep(sourcefile,'.wav','_OK.wav'); % add some suffix to name
    
    audiowrite(outputname,sig_trim,fs,'BitsPerSample',24,'comment',text); % comments can be read by reading file with audioinfo('file.wav')
    clear sig sig_trim    
end
