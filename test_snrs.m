function test_snrs
%Formula:
%dBSNR = 20∗log10(rms(Signal)/rms(Noise))
%dBSNR/20 = log10(rms(Signal)/rms(Noise))
%10^(dBSNR/20) = rms(Signal)/rms(Noise)
%(10^(dBSNR/20)) * rms(Noise) = rms(Signal)
%from this we derive: (if Noise and Signal are ==RMS to start)
%Correctly_Scaled_Noise = (10^(dBSNR/20)) * Noise
%Noisy_Signal = Signal + Correctly_Scaled_Noise
%Verify:
fs = 16e3; % Sampling frequency (samples per second) 
 dt = 1/fs; % seconds per sample 
 StopTime = 5; % seconds 
 t = (0:dt:StopTime)'; % seconds 
 F = 10; % Sine wave frequency (hertz) 
Signal = sin(2*F*pi*t);
Noise = rand([size(Signal)])-0.5;
%Match RMSs
Target_RMS = 0.5
Noise = Noise * Target_RMS/rms(Noise);
Signal = Signal * Target_RMS/rms(Signal);
Target_Loudness = -10; %whatever??
%try some SNRs
for dBSNR = [-10:5:10]
    Correctly_Scaled_Noise = (10^(dBSNR/20)) * Noise;
    Noisy_Signal = Signal + Correctly_Scaled_Noise;
    testedSNR = 20*log10(rms(Signal)/rms(Correctly_Scaled_Noise));
    %normalise level

    loudnessvalue = integratedLoudness(Noisy_Signal,fs)
    while loudnessvalue~=Target_Loudness
    Noisy_Signal = (Target_Loudness\loudnessvalue) * Noisy_Signal;
    loudnessvalue= integratedLoudness(Noisy_Signal,fs)
    end
    plot_signal(Noisy_Signal,fs,t)
end

function normalise_loudness(signals)

function plot_signal(insig,fs,t)
h=figure(111);
j=figure(112);
win_size = 0.5;
fft_overlap = 0.1;
hop_size = fs*win_size;
nfft = hop_size/fft_overlap;
noverlap = nfft-hop_size;
w = sqrt(hann(nfft));
  figure(h);
    plot(t(1:fs),insig(1:fs),'LineWidth',2);
 %%set properties
 set(gca,'Visible','on','Position',[0 0 1 1],'color',[0 0 0]);
 set(gcf,'Color',[0 0 0]);
 figure(j);
spectrogram(insig, w ,noverlap, nfft, fs, 'yaxis' );
ax=gca;
%ax.YScale = 'log';
ylim(ax, [0,50]); %kHz
set(gca,'Visible','off','Position',[0 0 1 1],'color',[0 0 0],'Xlim',[0,length(insig)/fs]);
set(gcf,'Color',[0 0 0]);
colorbar('off');colormap('default')