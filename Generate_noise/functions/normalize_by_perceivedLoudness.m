
function signals_loudNorm = normalize_by_perceivedLoudness(signal,fs,targetDB)
%% Normalize by mean rms 
%Author: GFragaGonzalez 2022
%Input:  a signal vector, sampling rate (fs) and targetDB (e.g., -23)
%Output: a a vector with the signal normalized to the integratedLoudness

    
    loudness = integratedLoudness(signal,fs);
    gaindB = targetDB - loudness;
    gain = 10^(gaindB/20);
    signals_loudNorm = signal.*gain;

