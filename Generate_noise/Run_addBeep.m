clear all 
close all
cd ('V:\spinco_data\AudioRecs\')
addpath('V:\gfraga\scripts_neulin\Generate_noise\functions')
%% Read files 
dirinput = 'V:\spinco_data\AudioRecs\LIRI_voice_DF\segments\Take1_all_trimmed\trim_loudNorm-23LUFS_SiSSN2';
diroutput = 'V:\spinco_data\AudioRecs\LIRI_voice_DF\segments\Take1_all_trimmed\trim_loudNorm-23LUFS_SiSSN2_cued';
files = dir([dirinput,'/*.wav']);
files = {files.name};
%% read beep
beepfile = 'V:\spinco_data\AudioRecs\beep.wav';
[beep, beeprate] = audioread(beepfile);
target_loudnessDB = -23;

beep2 = repmat(beep,8,1);
tmp =  normalize_by_perceivedLoudness(beep2,beeprate,target_loudnessDB);
beep2 = tmp(1:length(beep));

cd(dirinput)
%%

for i = 1:length(files)
        currfile = files{i};
        [sig, srate] = audioread(currfile);
        %sig = sig(:,1);
        if contains(currfile(1:2),'NV')
            newsig = [beep2;repmat(0,(srate*0.1),1);sig];
        else  contains(currfile(1:2),'SiSSN')
           newsig = [beep2;sig];
        end
         
         outputfilename = currfile;
         audiowrite([diroutput,'/',outputfilename],newsig,srate,'BitsPerSample',16);        
         disp(['...saved ',outputfilename]);
        
 
end
