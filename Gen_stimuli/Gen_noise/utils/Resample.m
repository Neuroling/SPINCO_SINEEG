clear all 

% Resample files in folder  
dirinput = 'V:\spinco_data\AudioGens\tts-golang-44100hz\tts-golang-selected-SiSSN';
diroutput = [dirinput,'_resamp'];
mkdir (diroutput)
%% 
 new_fs = 48000;
files = dir ([dirinput, '\*.wav']);
files = {files.name};
cd (dirinput)
for f=1:length(files)
    % read 
    target_file= files{f};            
    [audio, audio_fs] = audioread(target_file);
    % resampling
    [P,Q] = rat(new_fs/audio_fs);    
    resampled_audio = resample(audio(:,1), P, Q);
    
    % save 
     audiowrite([diroutput,'\',target_file], resampled_audio, new_fs);

end