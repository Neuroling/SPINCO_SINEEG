
%%
dat = dat(:,1)
fs = 16e3;
speech = resample(dat,fs,srate);
speech = speech/max(abs(speech));
sound(speech,fs)

win = hamming(50e-3*fs,"periodic");
%%
win = hamming(50e-3*srate,"periodic");
[idx, thresh] = detectSpeech(dat,srate,Window=win);
%%
figure;
plot(1:length(dat),dat);
%
hold on; xline([idx(1)],"Color","red");xline([idx(2)],"Color","red")
%%
sound(dat,srate)
%%
sound(dat(idx(1)-10:idx(2)),srate)