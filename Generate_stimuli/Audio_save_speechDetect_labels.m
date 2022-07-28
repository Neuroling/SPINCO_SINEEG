%% clear all
%% Save files with manually adjusted labels marking the speech ROI 
%--------------------------------------------------------------------
% Author: G.FragaGonzalez
% Desc: 
%   Reads the workspace variable saved after using audioLabeler app.
%   The variable has the name of the source signal (one or multiple files)
%   Here we expect that each file has a 'SpeechDetected' label indicating one
%   fragment with speech
% In:  just specify the variable (labelSet) and directories 
% Out: saves trimmed files (same name as source files with suffix) in same
% directory as the original files that were used by audioLabeler 

% Specify which label Set you want to use 
labelSet  = labeledSet_122752;

%% Read labels 
for f = 1:length(labelSet.Source)
    % identify source signal
    sourcefile = labelSet.Source{f};
    
    % read the source file and trim it to the selected ROI 
    [sig, fs] = audioread(sourcefile); % expects only one channel
    
    % find label and get indices of ROI    
    idxs  = labelSet.Labels.SpeechDetected{f}.ROILimits(1,:); % expects only one ROI per file! 
    startidx = idxs(1)*fs; %labels are given in secs, convert to datapoint 
    endidx = idxs(2)*fs;
    sig_trim = sig(startidx:endidx);  
   
    %write file 
    outputname = strrep(sourcefile,'.wav','_OK.wav'); % add some suffix to name
    audiowrite(outputname,sig_trim,fs,'BitsPerSample',24,'comment','Manually adjusted the speech detection and trimmed '); % comments can be read by reading file with audioinfo('file.wav')

end
