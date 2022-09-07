clear all 
close all
cd ('V:\spinco_data\SINON')

addpath('V:\gfraga\scripts_neulin\Generate_noise\functions\mp3readwrite')


%% Read mean RMs of our files
        cd('V:\spinco_data\SINON\Spreadsheets\LexicalDecision\files')
        
        expfiles = dir('*.mp3');
        expfiles = {expfiles.name};
        [signals, fss] = cellfun(@(x) audioread(x), expfiles, 'UniformOutput',0);
        
        allrms  = cellfun(@(x) rms(x),signals);
        RMS_mean = mean(allrms);
        
%%
dirinput = 'V:\spinco_data\SINON\VolumeCheck';
files = dir([dirinput,'/*.flac']);
files = {files.name};
cd(dirinput)
%%

for i = 1:length(files)
        currfile = files{i};
        [sig, srate] = audioread(currfile);
        
        %%
        mp3write(sig,srate,strrep(currfile,'.flac','.mp3'));    
        
        %%
       signal_nrm = sig.*RMS_mean/rms(sig(:,1));
       mp3write(signal_nrm,srate,strrep(currfile,'.flac','_norm.mp3'));    

end
