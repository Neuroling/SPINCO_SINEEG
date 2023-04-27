% read wav files and save them as mp3  
% - uses external function 'mp3write' modified (wavread was deprecated,psychtoolbox funct used instead)
% -----------------------------------
clear all

dirinput = 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\words_take1_speechDetect_OK_vocoded';
diroutput = 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\All_mp3s\noise_vocoded';
addpath('V:\gfraga\scripts_neulin\Generate_noise\functions\mp3readwrite')
mkdir(diroutput)
cd(dirinput)
%read all wavs
wavfiles = dir([dirinput,'\*.wav']);
files2read = {wavfiles.name};
cd(dirinput)
[sigs, fss] = cellfun(@(x) audioread(x), files2read, 'UniformOutput',0);

%%
%save as mp3
for i= 1:length(wavfiles)
    mp3write(sigs{i},fss{i},[diroutput,'\',strrep(wavfiles(i).name,'.wav','.mp3')]);    
end 

