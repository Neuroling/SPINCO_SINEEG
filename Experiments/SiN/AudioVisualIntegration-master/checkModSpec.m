x=Y;

x = NoTheta;

x = NoThetaNoLowp;

%x =WithTheta;

FS = fs;

if FS~=16e3

    x=resample(x,16e3,FS);

end

%pad to be 6s identical lengths?

L=length(x);

targetlength = 6

% new target length
targetlength = 3


if L<targetlength*16e3

    pad=zeros(1,targetlength*16000);

    pad(1:L)=x;

    x=pad;

elseif L>targetlength*16e3

    x=x(1:targetlength*16000);

end

[v,cf]=wav2aud2(x,[5 8 -2 0]);

% compute the narrow-band modulation spectrum

%sample rate 200Hz because 8ms integration window demanded in call to

%wav2aud2 immediately above here.
clear ms
[ms(:),~,f]=Modulation_Spectrum_Resolved(v,200,'log');

ms_rms=sqrt(ms.^2);

ms_rms=ms_rms/max(ms_rms([f<32 & f>=.5]));

% plot the modulation spectrum averaged over chunks

figure;

plot(f,ms_rms)

xlim([.5 32]);

set(gca,'xscale','log')

set(gca,'xtick',[.5 1 2 4 8 16 32])

xlabel('frequency (Hz)')

ylabel('normalized amplitude')

title('Modulation Spectrum')