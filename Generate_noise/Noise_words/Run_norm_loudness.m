clear all; 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Run normalization by perceived loudness function 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
dirinput = 'V:\spinco_data\AudioRecs\LIRI_voice_DF\segments\Take1_all_trimmed\';
diroutput = 'V:\spinco_data\AudioRecs\LIRI_voice_DF\segments\Take1_all_trimmed\trim_loudNorm';
addpath ('V:\gfraga\scripts_neulin\Generate_noise\functions\mp3readwrite')
addpath ('V:\gfraga\scripts_neulin\Generate_noise\functions\')
cd(dirinput)
files = dir('**/*.wav'); 
files = fullfile({files.folder},{files.name});
targetDB = -23;

%% read signals 
[sigs, fss] = cellfun(@(x) audioread(x), files, 'UniformOutput',0);
%%  run normalization  and save 
cd(diroutput)
for i = 1:length(sigs)
        signal = sigs{i};
        sig_loudNorm = normalize_by_perceivedLoudness(signal,fss{i},-23);
        
        % save wav 
         text = ['Normalize to perceived loudness = ', num2str(targetDB),' LUFS'];
         [foldername,filename] = fileparts(files{i});
         outname = strcat(diroutput,'\', filename,'_norm.wav');
         audiowrite(outname , sig_loudNorm,fss{i},'BitsPerSample',16,'comment',text);

        %save mp3
        %mp3write(sig_loudNorm, fss{i},strcat([diroutput,'\',files{i}]));    
           
end
