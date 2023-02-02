%% Quick aid for checking the audio recordings
%-----------------------------------------------------
% Loop thru wav files, button press log 1 = good; 0 = bad; 2= undecided
% Enter rater name, save output 
addpath('C:\Users\gfraga\Documents\MATLAB\')
addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')% tool for plot
addpath('V:\gfraga\scripts_neulin\Generate_noise\functions\')
dirinput= 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\items_OK';
diroutput = 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\items_OK_norm'; 


%% Read signal of all files 
files = dir([dirinput,'/*.wav']);
folders = {files.folder};
files = {files.name};

% little fix for some filename issue
files(find(contains(files,"Äsleyre.2_OK.wav"))) = {'Äsleyre.2_OK.wav'};
files(find(contains(files,"Ässchnauner_OK.wav"))) = {'Ässchnauner_OK.wav'};

%
cd(dirinput)
signals = cell(1,length(files));
fss = cell(1,length(files));
for i = 1:length(files)
   [sig, fs] = audioread(files{i});
   signals{i}= sig(:,1);
   fss{i}= fs(1);
   disp(['read ',files{i}]);
end

 %% Main loop Loop 
%cd(dirinput)
signals_nrm = normalize_by_meanrms(signals);

for i =1:length(signals_nrm)
    itm = strsplit(files{i},'_');
    itm = itm{1};
   outputname = [itm,'_norm.wav'];
    %
   audiowrite(strcat(diroutput,'\',outputname),signals_nrm{i},fss{i},'BitsPerSample',24,'comment','cut normalized to mean rms of all items in this folder'); % comments can be read by reading file with audioinfo('file.wav')
end
 