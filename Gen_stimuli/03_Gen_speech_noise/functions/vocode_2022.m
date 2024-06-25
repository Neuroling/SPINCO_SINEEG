function [wave]=vocode_2022(exc, mapping, filters, EnvelopeExtractor, smooth, nCh, InputSignal, Srate, MinFreq, MaxFreq, varargin)
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
% function vocode(exc, mapping, filters, EnvelopeExtractor, smooth, nCh, x, Srate, MinFreq, MaxFreq, varargin)
%
%  exc - 'noise', 'sine', 'F0_value', or '-F0_value', in quotes
%   for: white noise, sinusoid, sine-, or alternating-phase harm. complexes
%   as excitation for the temporal envelopes of the filtered waveforms

%  mapping of channels - 'n'(ormal) or 'i'(nverted), inverted creates
%   spectrally rotated signal

%  filters - 'greenwood', 'linear', 'mel' or 'log', the spacing of the
%   frequency bands 

%  EnvelopeExtractor - How is the amplitude envelope extracted? 'half' or
%   'full', or 'hilbert' 

%  smooth - filter cutoff frequency, typically 30Hz, can be 50, more,
%  less...

%  nCh - the number of channels

%  InputSignal - input signal, as vector, created by reading an input file.
%   i.e. what will be vocoded; can also be pointer to a file but this
%   feature is messy as an Srate is currently still required as an argument
%   to this function
%   
%  Srate - sample rate of signal

%  MinFreq - high-pass cutoff for bandpass filtering of signal. Defines
%   lower limit of bands

%  MaxFreq - low-pass cutoff for bandpass filtering of signal. Defines
%   upper limit of bands

%  wave - output signal (vector), for writing. Function DOES NOT AUTOMATICALLY 
%   save files in order to enable maximum user flexibility in naming
%   outputs, if you want saivng automatically, provide a single additional
%   argument:

%  varargin: add an optional output filename
%
% For example, to get an interesting variety of outputs with 6 channels,
% do the following commands:
% vocode('noise','n','greenwood','half',320,6,'sent.wav',[],50,5000,'nn320.wav')
% vocode('noise','i','greenwood','half',320,6,Signal,44100,50,5000,'ni320.wav')
% vocode( 'sine','n','greenwood','half',320,6,'sent.wav',[],50,5000,'sn320.wav')
% vocode( 'sine','i','greenwood','half',320,6,'sent.wav',[],50,5000,'si320.wav')
% vocode('noise','n','greenwood','half', 30,6,'sent.wav',[],50,5000, 'nn30.wav')
% vocode('noise','i','greenwood','half', 30,6,'sent.wav',[],50,5000, 'ni30.wav')
% vocode( 'sine','n','greenwood','half', 30,6,'sent.wav',[],50,5000, 'sn30.wav')
% vocode( 'sine','i','greenwood','half', 30,6,'sent.wav',[],50,5000,'si30.wav')

%
% For harmonic complexes, e.g. sine and alternating phase with F0= 100 Hz, type:
% vocode(  '100','n','greenwood','half', 30,6,'sent.wav',[],50,5000, 'csn30.wav')
% vocode( '-100','n','greenwood','half', 30,6,'sent.wav',[],50,5000, 'can30.wav')
% To specify the F0 and phase for each band separately you can do this:
% vocode( '-100 72 55 200 144 72','n','greenwood','half', 30,6,'sent.wav',[],50,5000,
% 'mixed30.wav')
% You can produce one or more "empty" channels by specifying an F0 of 0:
%  vocode( '-100 72 0 200 144 72','n','greenwood','half', 30,6,'sent.wav',
%  [],50,5000,'1empty.wav')
% The output file is in .WAV format and can be played using whatever
% package you like, or just type: play filename
%


%User monitoring with figures mode, off or on
DOFIGURES=0; %preferably set to 0
FILTER_BEFORE=1;
FILTER_AFTER=1;


if smooth<=0, ['Smoothing filter low pass cutoff must be greater than 0.']
    return;
end

if nCh<1, ['The number of channels has to be greater than 0.']
    return;
end

% 
%Check form of input signal,
%Feature request: Handle inputs as strings, read file. Find efficient way
%to deal with the Srate input under those circumstances
if ischar(InputSignal)
    [InputSignal,Srate] = audioread(InputSignal);
end
InputSignal=mean(InputSignal,2); %Make signal average of both channels if stereo
%Make sure signal is oriented correctly (N * 1 vector)
if size(InputSignal,1)<size(InputSignal,2)
    InputSignal=transpose(InputSignal);
end
nSmp=length(InputSignal);

meen=mean(InputSignal);
InputSignal=InputSignal-meen; %----------remove any DC bias---
if DOFIGURES
figure(1), plot(InputSignal)             %###
end

%---------------------Design the filters ----------------
[filterA,filterB,center]=estfilt(nCh,filters,Srate,MinFreq,MaxFreq);
srat2=Srate/2;

% --- design low-pass envelope filter ----------
[blo,alo]=butter(3, smooth/srat2);

% --- design low-pass envelope 10Hz filter for Ghitza Control----------
[Ghitzablo,Ghitzaalo]=butter(3, 10/srat2);

% --- design window for Ghitza Bursts----------
Window=hanning(Srate*BurstDuration);
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

if DOFIGURES
figure(2), plot(0,0), hold on  %###
end
% ----------------------------------------------------------------------%
% First construct the component modulated carriers for all channels      %
% ----------------------------------------------------------------------%
%THERE IS A LOT OF LEGACY STUFF HERE MANIPULATING ENVELOPE DEPTH, IT'S NOT
%NECESSARY (PROBABLY)
fcnt=1; fold=0;
% if DOFIGURES
%  figure(1);title('Modulation spectrum for all chs')
% end
% idx = 300;
% Nfft = 1024;


for i=1:nCh
    % h1=fvtool(filterB(i,:),filterA(i,:))
    y=filtfilt(filterB(i,:),filterA(i,:),InputSignal)';
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
    end
    
    % here we multiply y - the envelope, by some noise
    if strcmp(exc,'noise')==1
        % -- excite with noise ---
        noise=sign(rand(1,nSmp)-0.5);
        if FILTER_BEFORE %filter the noise carrier prior to modulating with signal envelope
            %filter the noise
            noise=filtfilt(filterB(i,:),filterA(i,:),noise);
            ModC(i,:)=y.*noise; 
        else %modulate broadband noise with signal
            ModC(i,:)=y.*noise;
        end
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
   if DOFIGURES
       figure(2);plot(y);
   end
end
if DOFIGURES; figure(2), hold off; figure(3), plot(ModC'); end

% ----------------------------------------------------------------------%
% Now filter the components (whatever they are), and add together
% into the appropriate order, scaling for equal rms per channel
% ----------------------------------------------------------------------%
for i=1:nCh
    if sum(abs(ModC(i,:)))>0
        if strcmp(mapping,'n')==1
                
            if FILTER_AFTER
               band=filtfilt(filterB(i,:),filterA(i,:),ModC(i,:) );
            else
                band=ModC(i,:);
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
if DOFIGURES
figure(4), plot(wave)          %###
end

if ~isempty(varargin)
    outfilename=varargin{1}
    audiowrite(outfilename,wave,Srate);
end

 

