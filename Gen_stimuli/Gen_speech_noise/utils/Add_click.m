clear all

%% Directories
% Find the index of the "script" folder
folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
scriptPathIdx = find(strcmp(folders, 'Scripts'), 1);
baseDir = [fullfile(folders{1:(scriptPathIdx-1)}),filesep]

% % add paths of associated functions and toolbox TSM required by function 
% addpath([baseDir, fullfile('Scripts','Gen_stimuli','Gen_speech_noise','functions')])
% %addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')
% %addpath('C:\Users\gfraga\Documents\MATLAB\')
% 

% paths and files 
dirinput =   [baseDir,fullfile('Stimuli','AudioGens','Experiment2', 'selected_audio_psychoPy')];
diroutput =  [baseDir,fullfile('Stimuli','AudioGens','Experiment2', 'selected_audio_psychoPy_click')];

if exist(diroutput) ~= 7
    mkdir(diroutput);
    disp(['New folder created: ', diroutput]);
else
    disp(diroutput);
    warntext = 'Output directory already exists. Existing files may be overwritten. You have 5 seconds to abort the script.'
    pause(5)
end

% give write permission to diroutput
fileattrib(diroutput, '+w');

%% 

files = dir([dirinput,'/*.wav']);
files = {files.name};
%% 
for f= 1:length(files);
    fileinput= files{f};
    [sig, fs] = audioread([dirinput,'/',fileinput]);
    
    %% Create a second channel with a click 
    sig2 = sig;
    % Keep intensity of audio wave low to avoid unwanted triggers
    sig2 = sig2*(0.2/max(abs(sig2)));       
    clickdur = 0.1;  % dur in sec of the click signal (long enough to avoid undesired miss)
    clicklength = fs*clickdur; % dur in sec of the click signal
    sig2(1:clicklength) = ones(1, clicklength);        
    
    %% 
    
    newsig = [sig,sig2];
    audiowrite([diroutput,'/',fileinput],newsig, fs, 'Comment', 'Click added at start of channel 2')    
end 




