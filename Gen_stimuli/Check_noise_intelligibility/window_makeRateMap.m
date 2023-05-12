function [ratemap,bm,cf] = window_makeRateMap(x,fs,lowcf,highcf,numchans,frameshift,ti,compression, outermiddle, reflevel)
% ratemap = makeRateMap(x,fs,lowcf,highcf,numchans,frameshift,ti,compression) generates the
% spectro-temporal excitation pattern (STEP) representation for given signal. This is to model
% smoothed and compressed representation of the envelope of the basilar membrane response to sound.
% The wavform is was initially processed by gammatone filterbankds using a pole-mapping procedure
% described in (Cooke, 1993). The Hilbert envelope in each channel of the filterbank was computed
% and smoothed with a leaky integrator with a ti ms (in default) time constant (Moore et al., 1988).
% The smoothed envelope was further downsampled.
%
% input:
%        x             input signal
%        fs            sampling frequency in Hz (8000 in default)
%        lowcf         centre frequency of lowest filter in Hz (100 in default)
%        highcf        centre frequency of highest filter in Hz
%                      (1/2 sampling freqeuency in default)
%        numchans      number of channels in filterbank (34 in default)
%        frameshift    interval between successive frames in ms (10 in default)
%        ti            temporal integration in ms (8 in default)
%        compression   type of compression ['cuberoot','log','none'] (no compression in default)
% output:
%        ratemap       STEP representation of the input signal x
%        cf            central frequences for each band
%
% Author: Martin Cooke
% modified by Yan Tang
% Commented out the whos in line 71.

diary

if nargin < 2
    fs = 8000; %Hz
end

if nargin < 3
    lowcf = 100; %Hz
end

if nargin < 4
    highcf = round(fs / 2); %Hz
end

if nargin < 5
    numchans = 34;
end

if nargin < 6
    frameshift = 10; %ms
end

if nargin < 7
    ti = 8; %ms
end

if nargin < 8
    compression = 'none';
end

if nargin < 9
    outermiddle = 'none';
end

if nargin < 10
    reflevel = 0; %dB
end

cf = MakeErbCFs(lowcf,highcf,numchans);
frameshift_samples = round(frameshift*fs/1000);
framecentres = 1:frameshift_samples:length(x);
numframes = length(framecentres);
x = x(:)';
% whos
xx=zeros(1,numframes*frameshift_samples);
xx(1:length(x))=x;

ratemap = zeros(numchans,numframes);
tp = 2*pi;
tpt = tp/fs;
wcf = 2*pi*cf;
kT = (0:length(xx)-1) / fs;
bw = erb(cf)*bwcorrection;
as = exp(-bw*tpt);

gain = ((bw*tpt).^4)/3;
% outermiddle ear transfer function integration
switch lower(outermiddle)
    case 'iso'
        gain = gain .* db2amp(-outerMiddleEar(cf),reflevel);
    case 'terhardt'
        gain = gain .* db2amp(-terhardt_treshold(cf), reflevel);
    case 'none'
end

bm = zeros(numchans, length(xx));

intdecay=exp(-(1000/(fs*ti)));
intgain=1-intdecay;

for c=1:numchans
    a = as(c);
    q = exp(-1i*wcf(c)*kT).*xx;
    p = filter([1 0],[1 -4*a 6*a^2 -4*a^3 a^4],q);     % filter: part 1
    u = filter([1 4*a a^2 0],[1 0],p);                % filter: part 2

    % compute displacement of basal membrane
    bm(c, :) = (gain(c)*real(exp(1i*wcf(c)*kT).*u))';
    % extract envelope
    env = gain(c)*abs(u);

    smoothed_env = filter(1,[1 -intdecay],env);         % temporal integration
    tmp = intgain.*mean(reshape(smoothed_env,frameshift_samples,numframes)); % downsampling
    tmp = max(tmp,1e-10); % avoid zero amplitude which causes -inf value when doing log compression
    ratemap(c,:) = tmp;
end

% do compression
switch compression
    case 'log'
        ratemap = 20 * log10 (ratemap);
    case 'cuberoot'
        ratemap = ratemap .^ 0.3;
    case 'none'
end



function y=MakeErbCFs(lfhz,hfhz,n)
% y=MakeErbCFs(lfhz,hfhz,n) makes central frequencies in Hz with the given lower and upper boundaries
% in n channels on the ERB scale.
%
% input:
%        lfhz:        central frequency of low end
%        hfhz:        central frequency of high end
%        n:           number of filters
% output:
%        y:           central frequencies of the output of the filterbanks
%
% Author: Martin Cooke

y=ErbRateToHz(linspace(HzToErbRate(lfhz),HzToErbRate(hfhz),n));



function y=ErbRateToHz(x)
% y=ErbRateToHz(x) computes the frequency in Hz with the given number of ERBs
%
% input:
%        x:       number of ERBs
% output:
%        y:       corresponding Hz
%
% Author: Martin Cooke

y=(10.^(x/21.4)-1)/4.37e-3;



function y=HzToErbRate(x)
% y = HzToErbRate(x) computes the number of ERBs of a given frequency in Hz
%
% input:
%        x:       frequency in Hz that will be converted to ERB rate
% output:
%        y:       corresponding number of ERBs
%
% Author: Martin Cooke

y=(21.4*log10(4.37e-3*x+1));



function y=erb(x)
% y = erb(x) converts the given frequency in Hz to ERB rate.
%
% input:
%        x:       frequency in Hz that will be converted to ERB
% output:
%        y:       corresponding ERB rate
%
% Author: Martin Cooke

y=24.7*(4.37e-3*x+1);



function thrsd = terhardt_treshold(cfs)
% y = terhardt_treshold(CFs) computes hearing threshold for given central frequencies using equation
% supplied in "Calculating virtual pitch", Hearing Research, vol. 1 pp. 155-182, 1979. by E. Terhardt
%
% input:
%        cfs       a vector of central frequencies in Hz
% output:
%        thrsd     a vector of corresponding thresolds of give frequencies
%
% Author: Yan Tang


cfs = cfs ./ 1000; % convert Hz to kHz
thrsd = 3.64*(cfs.^(-0.8))-6.5*exp(-0.6*((cfs-3.3).^2))+ 10e-3*(cfs.^4);



function thrsd = outerMiddleEar(cfs)
% h=outerMiddleEar(cfs) returns the outer-middle ear transfer function at the given central frequency
% using the data from ISO 387-9 (1996). Acoustics -- Reference zero for the calibration of audimetric
% equipment. Part 7: Reference threshold of hearing under free-filed and diffuse-field listening conditions
% Note, only defined for frequencies between 20 and 12,500 Hz.
%
% input:
%        cfs       a vector of central frequencies in Hz
% output:
%        thrsd     a vector of corresponding thresolds of give frequencies
%

if ((min(cfs)<20) || (max(cfs)>12500))
    error('Central frequency out of range');
end

f=[20 25 31.5 40 50 63 80 100 125 160 200 250 315 400 500 630 800 ...
    1000 1250 1600 2000 2500 3150 4000 5000 6300 8000 10000 12500];
tf=[74.3 65 56.3 48.4 41.7 35.5 29.8 25.1 20.7 16.8 13.8 11.2 8.9 ...
    7.2 6 5 4.4 4.2 3.7 2.6 1 -1.2 -3.6 -3.9 -1.1 6.6 15.3 16.4 11.6];

thrsd = interp1(f,tf,cfs,'PCHIP');



function amp=db2amp(level,ref)
% amp=db2amp(level,ref) converts decibels to amplitude with optional reference level
%
% input:
%        level       sound level in decibels
%        ref         reference level in decibels. It is useful to adopt a standard reference level
%                    of 80 dB to represent an amplitude of 1 for MATLAB sound output purposes.
% output:
%        amp         corresponding amplitude value
%
% Author: Martin Cooke


if nargin < 2
    amp=10.^(level./20);
else
    amp=10.^((level-ref)./20);
end


function y=bwcorrection
y=1.019;


