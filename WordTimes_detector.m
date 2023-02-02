%%
% ANOTHER APPROACH
fs = 24e3;
[speech,fileFs] = audioread(afile);
speech = resample(speech,fs,fileFs);
speech = speech/max(abs(speech));
sound(speech,fs)

%
close all 
win = hamming(50e-3*fs,"periodic");
detectSpeech(speech,fs,Window=win)

