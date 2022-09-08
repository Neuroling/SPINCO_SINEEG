
clear all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% PLOT AUDIO FILES RMS 



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dirinput = 'V:\spinco_data\SINON\Spreadsheets\2ForcedChoice\files_TrialSequences_2FC';
parts = strsplit(dirinput,'\');
foldername = parts{end};
cd (dirinput)

files = dir('*.mp3');
files = {files.name};

% read sig
[signals, fss] = cellfun(@(x) audioread(x), files, 'UniformOutput',0);
% get rms 
[sigRMS] = cellfun(@(x) rms(x), signals, 'UniformOutput',0);

%% PLOTS

durs = cell2mat(cellfun(@(x) length(x)/fss{1}, signals, 'UniformOutput',0));
allrms = cell2mat(sigRMS);
%%
close gcf
figure;
tcl = tiledlayout(2,2);
set(gcf,'color','w');

nexttile
histfit(durs)
ylabel('t_{s}')
title('Item durations');


nexttile
histfit(allrms)
ylabel('items')
title('Root Mean Squared');


nexttile
boxplot(durs)
ylabel('t_{s}')

nexttile
boxplot(allrms)
ylabel('arb.unit')

title(tcl,[strrep(foldername,'_',' ')])

% title('Root Mean Squared'); 
% line(xlim, [max(durs), max(durs)], 'Color', 'red', 'LineWidth', 1,'LineStyle','--');
% line(xlim, [min(durs), min(durs)], 'Color', 'red', 'LineWidth', 1,'LineStyle','--');
% line(xlim, [mean(durs), mean(durs)], 'Color', 'red', 'LineWidth', 1,'LineStyle','-');
