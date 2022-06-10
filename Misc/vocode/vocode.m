function [wave,varargout]=vocode(exc, mapping, filters, EnvelopeExtractor, smooth, nCh, x, Srate, MinFreq, MaxFreq, varargin)
%  This function has been heavily modified by A.H-A since 2003, and now
%  does more, and worse than it was ever intended to.
%
%  OUTPUTS: wave is the vocoded/processed wav file; varargout: max one
%  output, will be the Theta envelope, for visualisation purposes

%  VOCODE - This program reconstructs speech as a sum of 'nCh'
%  noise bands, sinusoids, or filtered harmonic complexes.
%  The speech input is filtered into a nCh bands, and the envelope in each band
%  is used to modulate a noise band, harmonic complex, or sinusoid, which
%  is then bandpass filtered into that region
%
% It was mostly written by Stuart Rosen (stuart@phon.ucl.ac.uk) based on the
% work of Philip  Loizou. Bob Carlyon persuaded Johannes Lyzenga
% (j.lyzenga@azvu.nl) to add the harmonic complex bit, as a possible acoustic
% analogue of the modulated pulse trains used to code speech in some cochlear
% implants. See complexes.txt or complexes.doc for the rationale and for further
% instructions. Philip Loizou's original notes are in readme.doc
%
%
% function vocode_64bits(exc, mapping, filters, EnvelopeExtractor, smooth, nCh, InFile, OutFile)
%
%  exc - 'noise', 'sine', 'F0_value', or '-F0_value', in quotes
%   for: white noise, sinusoid, sine-, or alternating-phase harm. complexes
%   as excitation for the temporal envelopes of the filtered waveforms
%  mapping of channels - 'n'(ormal) or 'i'(nverted)
%  filters - 'greenwood', 'linear', 'mel' or 'log'
%  EnvelopeExtractor - How is the amplitude envelope extracted? 'half' or
%  'full', or 'hilbert' or 'hilbertNoTheta'
%  smooth - filter cutoff frequency
%  nCh - the number of channels
%  x - input filename in quotes, e.g., 'heed.wav'
%  wave - output filename in quotes, e.g., 'heed2.wav'
%
% For example, to get an interesting variety of outputs with 6 channels,
% do the following commands:
% vocode('noise','n','greenwood','half',320,6,'sent.wav','nn320.wav')
% vocode('noise','i','greenwood','half',320,6,'sent.wav','ni320.wav')
% vocode( 'sine','n','greenwood','half',320,6,'sent.wav','sn320.wav')
% vocode( 'sine','i','greenwood','half',320,6,'sent.wav','si320.wav')
% vocode('noise','n','greenwood','half', 30,6,'sent.wav', 'nn30.wav')
% vocode('noise','i','greenwood','half', 30,6,'sent.wav', 'ni30.wav')
% vocode( 'sine','n','greenwood','half', 30,6,'sent.wav', 'sn30.wav')
% vocode( 'sine','i','greenwood','half', 30,6,'sent.wav', 'si30.wav')
% These commands are contained in file 'run.m'
%
% For harmonic complexes, e.g. sine and alternating phase with F0= 100 Hz, type:
% vocode(  '100','n','greenwood','half', 30,6,'sent.wav', 'csn30.wav')
% vocode( '-100','n','greenwood','half', 30,6,'sent.wav', 'can30.wav')
% To specify the F0 and phase for each band separately you can do this:
% vocode( '-100 72 55 200 144 72','n','greenwood','half', 30,6,'sent.wav',
% 'mixed30.wav')
% You can produce one or more "empty" channels by specifying an F0 of 0:
%  vocode( '-100 72 0 200 144 72','n','greenwood','half', 30,6,'sent.wav',
% '1empty.wav')
% The output file is in .WAV format and can be played using whatever
% package you like, or just type: play filename
%

%yes, globals are terrible
%SORRY
%Debug mode, off or on
DEBUG=0;
FILTER_BEFORE=1;
FILTER_AFTER=1;
%  Verify nargout:
% if nargout>=2 && ~(strcmp(EnvelopeExtractor,'hilbertNoTheta') ...
%             | strcmp(EnvelopeExtractor,'hilbertNoThetaNoLowp') ...
%             | strcmp(EnvelopeExtractor,'hilbertNoThetaRB') ...
%             | strcmp(EnvelopeExtractor,'Ghitza'))
%     warndlg('Your second output will be empty, it is only meaningful for the hilbertNoTheta case','warndialogue');
%     varargout{1}=[];
% end

if smooth<=0, ['Smoothing filter low pass cutoff must be greater than 0.']
    return;
end

if nCh<1, ['The number of channels has to be greater than 0.']
    return;
end



x=mean(x,2); %Make signal average of both channels if stereo
nSmp=length(x);

meen=mean(x);
x=x-meen; %----------remove any DC bias---
%figure(1), plot(x)             %###

%---------------------Design the filters ----------------
[filterA,filterB,center]=estfilt(nCh,filters,Srate,MinFreq,MaxFreq,DEBUG);
srat2=Srate/2;

% --- design low-pass envelope filter ----------
[blo,alo]=butter(3, smooth/srat2);

% --- design low-pass envelope 10Hz filter for Ghitza Control----------
[Ghitzablo,Ghitzaalo]=butter(3, 10/srat2);
% --- design window for Ghitza Bursts----------
WindowDuration=0.1;
Window=hanning(Srate*WindowDuration);
MaxAllowedRate=8;
MaxAudioVal=0.9;%0;
%design bandstop filter for Theta removal
% alexis filter order:
[Bstop,Astop] = butter(2,[2/srat2 9/srat2],'stop');

%design bandpass filter for theta envelope extraction:
[Btheta,Atheta] = butter(2,[2/srat2 9/srat2]);



% --- in case sampling freq > 12 kHz, bandlimit signal to 6 kHz ----
% if srat2>6000,  % in case sampling freq > 12 kHz, limit input signal to 6 kHz
%   LPF=1;
%   [blpf, alpf]=ellip(6,0.5,50,6000/srat2);
%   x=filter(blpf,alpf,x);
% else LPF=0;
% end;


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

ModC=zeros(nCh,nSmp);
y=zeros(1,nSmp);
wave=zeros(1,nSmp);
band=zeros(1,nSmp);
cmpl=zeros(1,nSmp);
            ChTheta=zeros(1,nSmp);

% rms levels of original filter-bank outputs are stored in the vector 'levels'
levels=zeros(1, nCh);

%figure(2), plot(0,0), hold on  %###
% ----------------------------------------------------------------------%
% First construct the component modulated carriers for all channels      %
% ----------------------------------------------------------------------%
%THERE IS A LOT OF LEGACY STUFF HERE MANIPULATING ENVELOPE DEPTH, IT'S NOT
%NECESSARY (PROBABLY)
fcnt=1; fold=0;

% figure(1);title('Modulation spectrum for all chs')
% idx = 300;
% Nfft = 1024;


for i=1:nCh
    % h1=fvtool(filterB(i,:),filterA(i,:))
    y=filtfilt(filterB(i,:),filterA(i,:),x)';
    level(i)=norm(y,2);
    switch EnvelopeExtractor
        case 'half'
            
            y=filtfilt(blo,alo,0.5*(abs(y)+y));
           
        case 'full'
            y=filtfilt(blo,alo,abs(y));
        case 'hilbert'
            y=abs(hilbert(y));
            %LP Filter
            y=filtfilt(blo,alo,y); 

        case 'hilbert_nolp'          
             y=abs(hilbert(y));
        case 'hilbertNoTheta'
            % here we get the envelope, i.e. the instantaneous hilbert amps
            y=abs(hilbert(y));       
            % envelope time-series gets low-pass filtered
            %Actually Ghitzastyle is not to do this, so let's not do this?
            y=filtfilt(blo,alo,y);
            % rb: these should get us the theta-filtered modulations of
            % enevelopes across the board
            Theta(i,:)=filtfilt(Btheta,Atheta,y);
            
            % filtered again to remove theta (= stop band filter)
            y=filtfilt(Bstop,Astop,y);
            
        case 'Ghitza'
            % here we get the envelope, i.e. the instantaneous hilbert amps
            y=abs(hilbert(y)); 
            
            % envelope time-series gets low-pass filtered
            %at 10Hz to create Ghitza's envelope stimuli. Then he does an
            %obscure peak picking operation... we'll deal with that
            %outside.
            Theta(i,:)=filtfilt(Ghitzablo,Ghitzaalo,y);
            % rb: these should get us the theta-filtered modulations of
            % enevelopes across the board
            RemovedTheta(i,:)=filtfilt(Btheta,Atheta,y);
            
            % filtered again to remove theta (= stop band filter)
            y=filtfilt(Bstop,Astop,y);
            
            %in addition to this we also need to make the bursty stimuli 
             tmp=zeros(1,size(Theta,2));
             [PeakValues, PeakPoints]=findpeaks(zscore(Theta(i,:)),'MinPeakDistance',round((1/MaxAllowedRate)*Srate),'MinPeakProminence',0.5);
            % [PeakValues, PeakPoints]=findpeaks(zscore(Theta(i,:)),'MinPeakProminence',1);
 
            %Convolve with a little window
             
           % tmp(PeakPoints((PeakValues>0)))=1;
            tmp(PeakPoints)=1;
            Conved=conv(tmp,Window);
            Conved=Conved(ceil(length(Window)/2):end-floor(length(Window)/2));
            
            if FILTER_BEFORE
                 ModZ=(Conved.*filtfilt(filterB(i,:),filterA(i,:),sign(rand(1,nSmp)-0.5)));             
            else
                ModZ=(Conved.*sign(rand(1,nSmp)-0.5));
            end
            if FILTER_AFTER
                 ModZ=filtfilt(filterB(i,:),filterA(i,:),ModZ);
            end
            
            ModZ= ModZ*level(i)/norm(ModZ,2);
           % ModX=
            ChTheta=ChTheta+ModZ;
          
          %  GloTheta(i,:)=filter(filterB(i,:),filterA(i,:),ModX(i,:));
            clear tmp
    
            case 'hilbertNoThetaRB'
            % here we get the envelope, i.e. the instantaneous hilbert amps
         
            y=abs(hilbert(y));
            
           % rb: these should get us the theta-filtered modulations of
            % enevelopes across the board
            Theta(i,:)=filtfilt(Btheta,Atheta,y);
            
            % here we remove theta env dynamics by subtracting it from the
            % total env dynamics
            y = y - Theta(i,:);
           
        case 'hilbertNoThetaNoLowp'
            % here we get the envelope, i.e. the instantaneous hilbert amps
            y=abs(hilbert(y));
            
            % rb: these should get us the theta-filtered modulations of
            % enevelopes across the board
            Theta(i,:)=filtfilt(Btheta,Atheta,y);
            
            % filtered again to remove theta (= stop band filter)
            y=filtfilt(Bstop,Astop,y);
            
            figure(1)
            subplot(2,nCh/2,i, 'XScale', 'log', 'YScale', 'log')
            loglog(F(1:idx),Pxx_tot(1:idx))
            hold on;loglog(F(1:idx),Pxx_noth(1:idx))
           
    end
    
    
    % here we multiply y - the envelope, by some noise
    if strcmp(exc,'noise')==1
        % -- excite with noise ---
        ModC(i,:)=y.*sign(rand(1,nSmp)-0.5);
    elseif strcmp(exc,'sine')==1
        % ---- multiply by a sine wave carrier of the appropriate carrier ----
        if strcmp(mapping,'n')==1
            ModC(i,:)=y.*sin(center(        i)*2.0*pi*[0:(nSmp-1)]/Srate);
        elseif strcmp(mapping,'i')==1
            ModC(i,:)=y.*sin(center((nCh+1)-i)*2.0*pi*[0:(nSmp-1)]/Srate);
        else fprintf('\nERROR! Mapping must be n or i\n');
            return;
        end
    elseif sum(abs(str2num(exc)))~=0   % Check for harmonic complexes
        f0=str2num(exc); fmax=size(f0); fmax=fmax(2);
        % [i fcnt f0(fcnt)]
        if f0(fcnt)~=fold
            cmpl=zeros(1,nSmp);
            if f0(fcnt)>0
                % ---- cmpl is with sine-phase complex of fundamental f0 ----
                for j=(1:fix(srat2/f0(fcnt)))
                    cmpl=cmpl+sin(j*f0(fcnt)*2.0*pi*[0:(nSmp-1)]/Srate);
                end
            elseif f0(fcnt)<0
                % ---- cmpl is alternating-phase complex of fundamental f0 ----
                for j=(1:fix(-srat2/f0(fcnt)))
                    if rem(j,2)==1
                        cmpl=cmpl+sin(-j*f0(fcnt)*2.0*pi*[0:(nSmp-1)]/Srate);
                    else
                        cmpl=cmpl+cos(-j*f0(fcnt)*2.0*pi*[0:(nSmp-1)]/Srate);
                    end
                end
            end
            fold=f0(fcnt);
        end
        if (fcnt<fmax) fcnt=fcnt+1; end
        % ---- multiply with sine- or alt-phase harm. complex ----
        ModC(i,:)=y.*cmpl;
    else fprintf('\nERROR! Excitation must be sine, noise, or +/-F0\n');
        return;
    end
    
end
%figure(2), hold off            %###
%figure(3), plot(ModC')         %###

% ----------------------------------------------------------------------%
% Now filter the components (whatever they are), and add together
% into the appropriate order, scaling for equal rms per channel
% ----------------------------------------------------------------------%
for i=1:nCh
    if sum(abs(ModC(i,:)))>0
        if strcmp(mapping,'n')==1
            if FILTER_BEFORE
            band=filtfilt(filterB(i,:),filterA(i,:),ModC(i,:));%;filter(filterB(i,:),filterA(i,:),ModC(i,:));
            else
                band=ModC(i,:);
            end
            if FILTER_AFTER
               band=filtfilt(filterB(i,:),filterA(i,:),ModC(i,:) );
            end
                
            % scale component output waveform to have
            % equal rms to input component
            band=band*level(i)/norm(band,2);
        elseif strcmp(mapping,'i')==1
            band=filter(filterB((nCh+1)-i,:),filterA((nCh+1)-i,:),ModC(i,:));
            % scale component output waveform to have
            % equal rms to input component
            band=band*level((nCh+1)-i)/norm(band,2);
            
        end
        wave=wave+band;  % accumulate waveforms
    end
end

%if LPF==1, wave=filter(blpf,alpf,wave); end;
%figure(4), plot(wave)          %###

% ------------ now save output to a file ----------
% --- first check that no sample point leads to an overload

max_sample=max(abs(wave));
Origwave=wave;
 if max_sample > 1    % ---- !! OVERLOAD !! -----
    % figure out degree of attenuation necessary
    ratio=0.9/max_sample;
    wave=wave * ratio;
    %  fprintf('!! WARNING -- OVERLOAD !!');
    fprintf(' File scaled by %f = %f dB\n', ratio, 20*log10(ratio));
 end

    

if nargin==11
    OutFile=varargin{1};
    [pth,fname,e]=fileparts(OutFile);
    NoThetaFile=fullfile(pth,[fname,'_NoTheta',e])
    audiowriteandscale(NoThetaFile,wave,Srate,MaxAudioVal);
    
%
    if strmatch(EnvelopeExtractor,'Ghitza')
    %then also save the GTheta and the ChTheta
        ChThetaWave=Origwave+ChTheta;
        ChThetaWave=(ChThetaWave/max(abs(ChThetaWave)));
        [pth,fname,e]=fileparts(OutFile);
        ChThetaOutFile=fullfile(pth,[fname,'_plus_ChTheta',e]);
        audiowriteandscale(ChThetaOutFile,ChThetaWave,Srate,MaxAudioVal); 
        
        %Save the Thetas alone
        OutFile=varargin{1};
        [pth,fname,e]=fileparts(OutFile);
        ChThetaOutFile=fullfile(pth,[fname,'_ChTheta',e]);
        audiowriteandscale(ChThetaOutFile,ChTheta,Srate,MaxAudioVal); 
    end
    
end
if nargout>2
    if (strcmp(EnvelopeExtractor,'hilbertNoTheta') ...
            | strcmp(EnvelopeExtractor,'hilbertNoThetaNoLowp') ...
            | strcmp(EnvelopeExtractor,'hilbertNoThetaRB') ...
            | strcmp(EnvelopeExtractor,'Ghitza'));
        varargout{1}=Theta;
        varargout{2}=center;
    else
        varargout{1}=0;
        varargout{2}=center;
    end
end
if nargout==4
    varargout{4}=wave;
end

function [filterA,filterB,center]=estfilt(nChannels,type,Srate,LowFreq,UpperFreq,dbg)

%  ESTFILT - This function returns the filter coefficients for a
%	filter bank for a given number of channels
%	and with a variety of filter spacings. Also returned are
%	the filter centre frequencies,

dbg=0;
% ====================================================================
% ------------------ greenwood spacing of filters -------------------------
if strcmp(type,'greenwood')  %
    
    FS=Srate/2;
    %%%%nOrd edited to 4 from 6.
    nOrd=6;
    %case of [G] changed in greenwud
    [lower1,center,upper1]=greenwud(nChannels,LowFreq,UpperFreq,dbg);
    
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
    [lower1,center,upper1]=mel(nChannels,UpperFreq,LowFreq,dbg);
    
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

function [lower,center,upper]= greenwud(N, low, high, dbg)
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

if dbg==1
    f=low:100:high;
    plot(f, frq2mm(f));
    grid
    hold on
end

lower=zeros(1,N); upper=zeros(1,N);
lower(1:N)=freqs(1:N);
upper(1:N)=freqs(2:N+1);

if dbg==1,
    plot(center,ones(1,N),'ro');
    
end;


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





