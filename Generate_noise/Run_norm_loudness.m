clear all; 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Run normalization by perceived loudness function 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
dirinput = 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\Take1_all_trimmed\trim_norm-25db_SiSSN';
diroutput = 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\Take1_all_trimmed\trim_norm-25db_SiSSN_loudnessNorm';
addpath ('V:\gfraga\scripts_neulin\Generate_noise\functions\mp3readwrite')
cd(dirinput)
files = dir('*.mp3'); 
files = {files.name};

%% read signals 
[sigs, fss] = cellfun(@(x) audioread(x), files, 'UniformOutput',0);

%%  run normalization  and save 
cd(diroutput)
for i = 1:length(sigs)
        signal = sigs{i};
        sig_loudNorm = normalize_by_perceivedLoudness(signal,fss{i},-23);
        
        %save mp3
        mp3write(sig_loudNorm, fss{i},strcat([diroutput,'\',files{i}]));    
           
end
