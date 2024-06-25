clear all 

folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
scriptPathIdx = find(strcmp(folders, 'Scripts'), 1);
baseDir = [fullfile(folders{1:(scriptPathIdx-1)}),filesep]

% Resample files in folder  
dirinput =  [baseDir,fullfile('Stimuli','AudioGens','Experiment2', 'tts-golang-44100Hz', 'tts-golang')]
% dirinput = 'V:\spinco_data\AudioGens\tts-golang-44100hz\tts-golang-selected-SiSSN';
% diroutput = [dirinput,'_resamp'];
% mkdir (diroutput)
%% 
 new_fs = 48000;
files = dir ([dirinput, '/*.wav']);
files = {files.name};
% cd (dirinput)
for f=1:length(files)
    fileinput= files{f};
    [audio, audio_fs] = audioread([dirinput,'/',fileinput]);

    audio_fs
    % resampling
%     [P,Q] = rat(new_fs/audio_fs);    
%     resampled_audio = resample(audio(:,1), P, Q);
%     
%     % save 
%      audiowrite([diroutput,'\',target_file], resampled_audio, new_fs);

end