
function signals_nrm = normalize_by_meanrms(signals)
%% Normalize by mean rms 
%Author: GFragaGonzalez 2022
%Input:  a cell with signals 
%Output: a cell with the signals normalized to the mean rms of all input 
allrms  = cellfun(@(x) rms(x),signals);
RMS_mean = mean(allrms);
signals_nrm = cellfun(@(x) x.*RMS_mean/rms(x), signals,'UniformOutput',false);
