function [ms,f]=Modulation_Spectrum(Nenv,fs,fscale)
% Nenv (time by frequency channel) is the narrowband envelope.
% fs is the sampling rate of Nenv in Hz
% fscale, the scale of the modulation frequency, is 'log' or 'lin'.
% ms, the modulation spectrum, is normalized by its maximal value 
% between 0.5 Hz and 32 Hz

% Nai Ding
% gahding@gmail.com
% 6.16.2014

f=1:size(Nenv,1)/2;f=f-1;f=fs*f'/size(Nenv,1);
vs=abs(fft(Nenv.^2)); % fourier transform
vs=sqrt(mean(vs.^2,2)); % average over carrier frequency channels
ms=single(vs(1:end/2)); % keep only 0 - fs/2

if fscale=='log'
  ms=sqrt(f).*ms;
end
