dirinput = 'V:\Projects\Spinco\SINEEG\Scripts\Experiments\SiN\PsychoPy_LAB\audio' ;
diroutput = 'V:\Projects\Spinco\SINEEG\Scripts\Experiments\SiN\PsychoPy_LAB\audio_click' ;
mkdir(diroutput)

%% 
cd(dirinput)
files = dir([dirinput,'/*.wav'])
files = {files.name}
%% 
for f= 1:length(files);
    fileinput= files{f};
    [sig, fs] = audioread([dirinput,'/',fileinput]);
    
    %% Add click   
    sig2 = sig;
    clickdur = 0.1;  % dur in sec of the click signal
    clicklength = fs*clickdur; % dur in sec of the click signal
    sig2(1:clicklengh) = ones(1, clicklengh);
    
    %% 
    cd (diroutput)
    newsig = [sig,sig2];
    audiowrite([diroutput,'/',fileinput],newsig, fs, 'Comment', 'Click added at start of channel 2')    
end 




