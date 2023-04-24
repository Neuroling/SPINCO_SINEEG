
function signals_loudNorm = normalize_by_perceivedLoudness(signal,fs,targetLUFS)
%% Normalize by perceived Loudness
%Author: GFragaGonzalez 2022
%Input:  a signal vector, sampling rate (fs) and target LUFS (e.g., -23)
%Output: a a vector with the signal normalized to the integratedLoudness

    if (length(signal)/fs ) < 0.4
        error('Failed: signal less than 0.4 sec: could not calculate integratedLoudness!')
    end 
    loudness = integratedLoudness(signal,fs);
    gain = targetLUFS - loudness;
    gain = 10^(gain/20);
    signals_loudNorm = signal.*gain;

