
clear all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% PLOT AUDIO FILES RMS 
%[GFragaGonzalez 2022]
%- Read audiofiles, calculate RMS, plot and save table 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dirinput = 'V:\spinco_data\AudioRecs\LIRI_voice_DF\segments\Take1_all_trimmed\trim_loudNorm-23LUFS_NV';
diroutput = 'V:\spinco_data\AudioRecs\LIRI_voice_DF\segments\Take1_all_trimmed\';
parts = strsplit(dirinput,'\');
foldername = parts{end};
cd (dirinput)

files = dir('NV*.wav');
files = {files.name};

% read sig
[signals, fss] = cellfun(@(x) audioread(x), files, 'UniformOutput',0);
% get rms 
[sigRMS] = cellfun(@(x) rms(x), signals, 'UniformOutput',0);

%% PLOTS

durs = cell2mat(cellfun(@(x) length(x)/fss{1}, signals, 'UniformOutput',0));
loudnessLUFS = cell2mat(cellfun(@(x) integratedLoudness(x,fss{1}), signals, 'UniformOutput',0));
allrms = cell2mat(sigRMS);
%%
close gcf
overview = figure('units','normalized','outerposition',[0 0 1 1]);
tcl = tiledlayout(3,3);
set(gcf,'color','w');

nexttile
histfit(durs)
ylabel('items')
title('Item durations');


nexttile
histfit(allrms)
ylabel('items')
title('Root Mean Squared');

nexttile
histfit(loudnessLUFS)
ylabel('items')
title('Loudness LUFS');


nexttile
boxplot(durs)
ylabel('t_{s}')

nexttile
boxplot(allrms)
ylabel('arb.unit')

nexttile
boxplot(loudnessLUFS)
ylabel('LUFS')

title(tcl,strrep(foldername,'_',' '))
 
% save summary plot
saveas( tcl, [diroutput, '/PLOT_',foldername,''], 'jpg')
close gcf
%%  Tables 
tab2save = cell2table(files');
tab2save.Properties.VariableNames = {'file'};
tab2save.rms = allrms';
tab2save.duration = durs';
%save 
writetable(tab2save,[diroutput, '/TABLE_',foldername,'.xlsx'])
