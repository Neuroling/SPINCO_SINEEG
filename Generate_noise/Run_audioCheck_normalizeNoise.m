clear all 
close all
cd ('V:\spinco_data\SINON\VolumeCheck\')
addpath('V:\gfraga\scripts_neulin\Generate_noise\functions')
%% Read files 
dirinput = 'V:\spinco_data\SINON\VolumeCheck';
files = dir([dirinput,'/*.flac']);
files = {files.name};
cd(dirinput)
%%

for i = 1:length(files)
        currfile = files{i};
        [sig, srate] = audioread(currfile);
        sig = sig(:,1);
        
          %Normalize to perceived loudness            
          target_loudnessDB = -23;
          sig_normal =  normalize_by_perceivedLoudness(sig,srate,target_loudnessDB);

         % prevent clipping only if needed 
           if any(sig_normal>0.99 | sig_normal < -0.99)
                 sig_normal = sig_normal*(0.999999/max(abs(sig)));  
                 disp('preventing clipping')
           end
           
         % Save  
         outputfilename = strrep(currfile,'.flac',['_norm',num2str(target_loudnessDB),'db.wav']);
         audiowrite(outputfilename,sig_normal,srate,'BitsPerSample',16);        
         disp(['...saved ',outputfilename]);
        
 
end
