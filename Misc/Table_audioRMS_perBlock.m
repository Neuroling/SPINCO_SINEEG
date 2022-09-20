
clear all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Save AUDIO FILES info  
%[GFragaGonzalez 2022]
%- Read audiofiles, calculate RMS, and save table 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dirinput = 'V:\spinco_data\SINON\Spreadsheets\2ForcedChoice\files';
diroutput = 'V:\spinco_data\SINON\Spreadsheets\2ForcedChoice\';
% spreasheet with stimuli list and block info
spreadsheet = readtable('V:\spinco_data\SINON\Spreadsheets\2ForcedChoice\TrialSequences_2FC_Gorilla.xlsx');
tab2save = spreadsheet(contains(spreadsheet.block,'block'),{'block','snr','type','audio'});

% read files 
parts = strsplit(dirinput,'\');
foldername = parts{end};
cd (dirinput)

files = dir([dirinput,'/*.mp3']);
files = {files.name};

% read sig
[signals, fss] = cellfun(@(x) audioread(x), files, 'UniformOutput',0);
% get rms 
[sigRMS] = cellfun(@(x) rms(x), signals, 'UniformOutput',0);
allrms = cell2mat(sigRMS);

% durations 
durs = cell2mat(cellfun(@(x) length(x)/fss{1}, signals, 'UniformOutput',0));

% get loudness in Loudness Units relative to Full Scale (LUFS)
loudnessLUFS = cell2mat(cellfun(@(x) integratedLoudness(x,fss{1}), signals, 'UniformOutput',0));

%%  Save info to table 
tab2save = sortrows(tab2save,"audio"); % important! sort by audio, that is the order of 'files' where cellfun was applied
tab2save.rms = allrms';
tab2save.duration = durs';
tab2save.loudness = loudnessLUFS';
tab2save = sortrows(tab2save,"block");
%save 
writetable(tab2save,[diroutput, '/audio_info.xlsx'])

 