function [wave]=vocode_aller(nCh,morph,smooth,InputSignal,Srate,MinFreq,MaxFreq)

% Vocode according to Aller et al. J Neuroscience 2022, modified from
% Zoefel et al. 2020

% Algorithm:
% divide signal into 16 log-spaced channels
% 70 - 5000 Hz
% Half-wave rectification of envelope
% LP filtering of HW rectified envelope <30Hz
% morph is the p factor for manipulating difficulty:
    % Manipulation of difficulty is achieved using a ratio of broad to
    % narrowband envelope: env_final(b) = env(b)*p + env(broadband)*(1-p)

nSmp=length(InputSignal);
srat2=Srate/2;

%broadband filter:
[BfilterB,BfilterA]=butter(4,[MinFreq MaxFreq]/srat2,"bandpass");

filters='greenwood'; % could also do log, but stick with this for the moment

%---------------------Design the filters ----------------
[filterB,filterA,center]=estfilt(nCh,filters,Srate,MinFreq,MaxFreq);

% --- design low-pass envelope filter ----------
[blo,alo]=butter(4, smooth/srat2);

% create buffers for the necessary waveforms
% 'y' contains a single output waveform,
%     the original after filtering through a bandpass filter
% 'ModC' contains the complete set of nChannel modulated white noises
%        or sine waves, created by low-pass filtering the 'y' waveform,
%        and multiplying the resultant by an appropriate carrier
% 'band' contains the waveform associated with a single output channel,
%        the modulated white noise or sinusoid after filtering
% 'wave' contains the final output waveform constructing by adding together
%        the ModC, which are first filtered by a filter matched to
%        the input filter
%

%ModC=zeros(nCh,nSmp);
y=zeros(1,nSmp);
wave=zeros(1,nSmp);
band=zeros(1,nSmp);

% rms levels of original filter-bank outputs are stored in the vector 'levels'

% ----------------------------------------------------------------------%
% First construct the component modulated carriers for all channels      %
% ----------------------------------------------------------------------%
%THERE IS A LOT OF LEGACY STUFF HERE MANIPULATING ENVELOPE DEPTH, IT'S NOT
%NECESSARY (PROBABLY)
fcnt=1; fold=0;

%Get broadband envelope:
y=filtfilt(BfilterB,BfilterA,InputSignal);
%smooth broadband envelope:
broadband_envelope = filtfilt(blo,alo,0.5*(abs(y)+y))'; %transpose! 

% here we multiply y - the envelope, by some noise

for i=1:nCh
    %filter the signal into a narrow band for the channel
    y=filtfilt(filterB(i,:),filterA(i,:),InputSignal)';
    % get the level fo the channel (to normalise later)
    level=norm(y,2);
    %Smooth the half-wave rectified signal: gives the band envelope
    y=filtfilt(blo,alo,0.5*(abs(y)+y));

%%%MORPHING AS IMPLEMENTED BY MATT DAVIS:

  % mix channel envelope (y) and 1-channel envelope (envelope) in different proportions 
  % according to morph percentage
  y = (y .* (morph)) + (broadband_envelope.* (1 - (morph)));
  

    % here we multiply y - the envelope, by some noise
    % -- excite with noise -- 
    % generate and filter noise:
    noise = sign(rand(1,nSmp)-0.5);
    bandnoise = filtfilt(filterB(i,:),filterA(i,:),noise);
    %multiply by envelope
    band=y.*bandnoise;
    %refilter noise:
    band=filtfilt(filterB(i,:),filterA(i,:),band);
    %Equalise RMS to input level
    band = band*level/norm(band,2); % band = band*level(i)/norm(band,2);
    wave = wave + band;
end


function [filterB,filterA,center]=estfilt(nChannels,type,Srate,LowFreq,UpperFreq)

%  ESTFILT - This function returns the filter coefficients for a
%	filter bank for a given number of channels
%	and with a variety of filter spacings. Also returned are
%	the filter centre frequencies,

% ====================================================================
% ------------------ greenwood spacing of filters -------------------------
if strcmp(type,'greenwood')  %

    FS=Srate/2;
    %%%%nOrd edited to 4 from 6.
    nOrd=6;
    %case of [G] changed in greenwud
    [lower1,center,upper1]=greenwud(nChannels,LowFreq,UpperFreq);

    if FS<upper1(nChannels), useHigh=1;
    else			 useHigh=0;
    end

    filterA=zeros(nChannels,nOrd+1);
    filterB=zeros(nChannels,nOrd+1);

    for i=1:nChannels
        W1=[lower1(i)/FS, upper1(i)/FS];
        if i==nChannels
            if useHigh==0
                [b,a]=butter(nOrd/2,W1);
            else
                [b,a]=butter(nOrd,W1(1),'high');
            end
        else
            [b,a]=butter(nOrd/2,W1);
        end
        filterB(i,1:nOrd+1)=b;   %----->  Save the coefficients 'b'
        filterA(i,1:nOrd+1)=a;   %----->  Save the coefficients 'a'
    end

    % ------------------ linear filter spacing  -------------------------
    %
elseif strcmp(type,'linear') % ============== linear spacing ==============

    FS=Srate/2;

    nOrd=6;
    range=(UpperFreq-LowFreq);
    interval=range/nChannels;

    center=zeros(1,nChannels);

    for i=1:nChannels  % ----- Figure out the center frequencies for all channels
        upper1(i)=LowFreq + (interval*i);
        lower1(i)=LowFreq + (interval*(i-1));
        center(i)=0.5*(upper1(i)+lower1(i));
    end

    if FS<upper1(nChannels), useHigh=1;
    else			 useHigh=0;
    end

    filterA=zeros(nChannels,nOrd+1);
    filterB=zeros(nChannels,nOrd+1);

    for i=1:nChannels
        W1=[lower1(i)/FS, upper1(i)/FS];
        if i==nChannels
            if useHigh==0
                [b,a]=butter(3,W1);
            else
                [b,a]=butter(6,W1(1),'high');
            end
        else
            [b,a]=butter(3,W1);
        end

        filterB(i,1:nOrd+1)=b;   %----->  Save the coefficients 'b'
        filterA(i,1:nOrd+1)=a;   %----->  Save the coefficients 'a'
    end


    % ------------------ logarithmic filter spacing  -------------------------
    %
elseif strcmp(type,'log') % ============== Log spacing ==============

    FS=Srate/2;

    nOrd=6;
    range=log10(UpperFreq/LowFreq);
    interval=range/nChannels;

    center=zeros(1,nChannels);

    for i=1:nChannels  % ----- Figure out the center frequencies for all channels
        upper1(i)=LowFreq*10^(interval*i);
        lower1(i)=LowFreq*10^(interval*(i-1));
        center(i)=0.5*(upper1(i)+lower1(i));
    end

    if FS<upper1(nChannels), useHigh=1;
    else			 useHigh=0;
    end

    filterA=zeros(nChannels,nOrd+1);
    filterB=zeros(nChannels,nOrd+1);

    for i=1:nChannels
        W1=[lower1(i)/FS, upper1(i)/FS];
        if i==nChannels
            if useHigh==0
                [b,a]=butter(3,W1);
            else
                [b,a]=butter(6,W1(1),'high');
            end
        else
            [b,a]=butter(3,W1);
        end
        filterB(i,1:nOrd+1)=b;   %----->  Save the coefficients 'b'
        filterA(i,1:nOrd+1)=a;   %----->  Save the coefficients 'a'
    end

    % ====================================================================
    % ------------------ Shannon filter spacing  -------------------------
elseif strcmp(type,'shannon') % ============== Shannon ==============


    srat2=Srate/2;
    rp=1.5;          % Passband ripple in dB
    rs=20;


    %----Preemphasis filter and Low-pass envelop filter -------------

    [bls,als]=ellip(1,rp,rs,1150/srat2,'high');
    [blo,alo]=butter(2,160/srat2);



    rs=15.0;
    nOrd=2;		% Order of filter = 2*nOrd
    nOrd2=2*nOrd+1; % number of coefficients
    nchan=nChannels;

    if nchan==2

        filt2b=zeros(nchan,nOrd2);
        filt2a=zeros(nchan,nOrd2);
        [b,a]=ellip(nOrd,rp,rs,[50/srat2 1500/srat2]);
        filt2b(1,:)=b; filt2a(1,:)=a;
        [b,a]=ellip(nOrd,rp,rs,[1500/srat2 4000/srat2]);
        filt2b(2,:)=b; filt2a(2,:)=a;

        filtroA=zeros(nchan,nOrd2); filtroB=zeros(nchan,nOrd2);
        filtroA=filt2a; filtroB=filt2b;
    elseif nchan==3

        filt3b=zeros(nchan,2*nOrd+1);
        filt3a=zeros(nchan,2*nOrd+1);
        crsf=[50 800 1500 4000];
        for i=1:3
            lf=crsf(i)/srat2; ef=crsf(i+1)/srat2;
            [b,a]=ellip(nOrd,rp,rs,[lf ef]);
            filt3b(i,:)=b; filt3a(i,:)=a;
        end

        filtroA=zeros(nchan,2*nOrd+1); filtroB=zeros(nchan,2*nOrd+1);
        filtroA=filt3a; filtroB=filt3b;
    elseif nchan==4

        filt4b=zeros(nchan,2*nOrd+1);
        filt4a=zeros(nchan,2*nOrd+1);
        crsf4=[50 800 1500 2500 4000];
        for i=1:4
            lf=crsf4(i)/srat2; ef=crsf4(i+1)/srat2;
            [b,a]=ellip(nOrd,rp,rs,[lf ef]);
            filt4b(i,:)=b; filt4a(i,:)=a;
        end


        filtroA=zeros(nchan,2*nOrd+1); filtroB=zeros(nchan,2*nOrd+1);
        filtroA=filt4a; filtroB=filt4b;

    end

    % ====================================================================
    % ------------------ Mel spacing of filters -------------------------
elseif strcmp(type,'mel')  % ============= use Mel spacing ==========

    FS=Srate/2;
    nOrd=6;
    [lower1,center,upper1]=mel(nChannels,UpperFreq,LowFreq);

    if FS<upper1(nChannels), useHigh=1;
    else			 useHigh=0;
    end

    filterA=zeros(nChannels,nOrd+1);
    filterB=zeros(nChannels,nOrd+1);


    for i=1:nChannels
        W1=[lower1(i)/FS, upper1(i)/FS];
        if i==nChannels
            if useHigh==0
                [b,a]=butter(3,W1);
            else
                [b,a]=butter(6,W1(1),'high');
            end
        else
            [b,a]=butter(3,W1);
        end
        filterB(i,1:nOrd+1)=b;   %----->  Save the coefficients 'b'
        filterA(i,1:nOrd+1)=a;   %----->  Save the coefficients 'a'

    end


else error('ERROR! filters must be log, greenwood, mel, linear or Shannon');

end
% ----------------------

function [lower,center,upper]= greenwud(N, low, high)
%

% [lower,center,upper] = greenwud(N,low,high)
%
% This function returns the lower, center and upper freqs
% of the filters equally spaced according to Greenwood's equation
% Input: N - number of filters
% 	 low - (left-edge) 3dB frequency of the first filter
%	 high - (right-edge) 3dB frequency of the last filter
%
% Stuart Rosen -- June 1998
%

% Set up equally spaced places on the basilar membrane
places = [0:N]*(frq2mm(high)-frq2mm(low))/N + frq2mm(low);
% Also calculate centre frequencies according to the same mapping
centres = zeros(1,N);
centres = (places(1:N) + places(2:N+1))/2;
% convert these back to frequencies
freqs = mm2frq(places);
center = mm2frq(centres);

lower=zeros(1,N); upper=zeros(1,N);
lower(1:N)=freqs(1:N);
upper(1:N)=freqs(2:N+1);


function mm = frq2mm(frq)
% FRQ2MM Greenwood's function for mapping frequency to place on the basilar membrane
%
% Usage: mm = frq2mm(frq)

a= .06; % appropriate for measuring basilar membrane length in mm
k= 165.4;

mm = (1/a) * log10(frq/k + 1);


function frq = mm2frq(mm)
% MM2FRQ Greenwood's function for mapping place on the basilar membrane to frequency
% Usage: function frq = mm2frq(mm)

a= .06; % appropriate for measuring basilar membrane length in mm
k= 165.4;

frq = 165.4 * (10.^(a * mm)- 1);


function audiowriteandscale(Filename,wave,Srate,MaxVal)
if MaxVal==0 %don't scale it
    audiowrite(Filename,wave,Srate); %
else
    max_sample=max(abs(wave));
    ratio=MaxVal/max_sample;
    wave=wave * ratio;
    audiowrite(Filename,wave,Srate);
end


