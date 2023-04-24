% This code illustrate how to compute and plot the
% auditory spectrogram simulated by a cochlear model
% reference: Yang, Wang, & Shamma. IEEE Trans Information Theory 38.2 (1992): 824-839.
% author: Nai Ding, gahding@gmail.com

clear;clc
% load the sound file, resample it to 16 kHz if necessary
[x,fs]=wavread('Music-Cello.wav');
% generate the auditory spectrogram
[v,cf]=wav2aud2(x,[5 8 -2 0]);
% plot the auditory spectrogram
figure;imagesc([1 size(v,1)]/200,1:128,20*log10(max(v,0))');axis xy
set(gca,'ytick',1:30:128);set(gca,'yticklabel',cf(1:30:128));
xlabel('time (s)');ylabel('frequency (Hz)');title('auditory spectrogram')
l=colorbar;title(l,'dB')

