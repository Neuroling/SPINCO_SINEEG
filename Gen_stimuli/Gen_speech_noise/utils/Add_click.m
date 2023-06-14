clear all 
dirinput = 'V:\Projects\Spinco\SINEEG\Stimuli\AudioGens\selected_audio_psychoPy' ;
diroutput = 'V:\Projects\Spinco\SINEEG\Stimuli\AudioGens\selected_audio_psychoPy_click' ;
mkdir(diroutput)

%% 
cd(dirinput)
files = dir([dirinput,'/*.wav'])
files = {files.name}
%% 
for f= 1:length(files);
    fileinput= files{f};
    [sig, fs] = audioread([dirinput,'/',fileinput]);
    
    %% Create a second channel with a click 
    sig2 = sig;
    % Keep intensity of audio wave low to avoid unwanted triggers
    sig2 = sig2*(0.2/max(abs(sig2)));       
    clickdur = 0.1;  % dur in sec of the click signal (long enough to avoid undesired miss)
    clicklength = fs*clickdur; % dur in sec of the click signal
    sig2(1:clicklength) = ones(1, clicklength);        
    
    %% 
    cd (diroutput)
    newsig = [sig,sig2];
    audiowrite([diroutput,'/',fileinput],newsig, fs, 'Comment', 'Click added at start of channel 2')    
end 




