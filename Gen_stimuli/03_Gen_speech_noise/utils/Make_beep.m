%% Directories
% Find the index of the "script" folder
folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
scriptPathIdx = find(strcmp(folders, 'Scripts'), 1);
baseDir = [fullfile(folders{1:(scriptPathIdx-1)}),filesep]
diroutput =  [baseDir,fullfile('Stimuli','AudioGens','Experiment2', 'utils')];


%% 
fs = 48000;
f = 200;
dur = 1;
t = 0:1/fs:dur-1/fs;
y = sin(2*pi*f*t);

y=y*0.7;
y = [ones(1,100),y]

audiowrite([diroutput,'/click_beep.wav'],y,fs) 