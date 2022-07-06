clear all ; 
% ========================================================================
%  Generate Speech-shaped noise   
% ========================================================================
% Author: G.FragaGonzalez 2022(based on snippets from T.Houweling)
% Description
%   - Reads single wav or list of .wav files (concatenate if multiple)
%   - Uses signal to create speech shaped noise (calls function)
%   - Normalization: matches Root Mean Square of noise to signal RMS
%   - Several plots signal and noise (in one figure)
%
%-------------------------------------------------------------------------
% add paths of associated functions and toolbox TSM required by function 
addpath('C:\Users\gfraga\scripts_neulin\Noise_generator\functions')
addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')

%% Inputs 
dirinput = 'C:\Users\gfraga\scripts_neulin\Noise_generator\samples\' ;
diroutput = 'C:\Users\gfraga\scripts_neulin\Noise_generator\samples\' ;

% files full path
wavfiles = {'yummy.wav','unbelievable.wav'};   
wavfiles= strcat(path,wavfiles);% add full filepath

% Inputs for SSN generation 
nfft = 1000;
srate = 48000;
noctaves = 6;   % 1/6 octave band smoothing (spectral smoothing in which the bandwidth of the smoothing window is a constant percentage of the center frequency).
    
%% Read inputs
% check files 
tmp = contains(wavfiles,'.wav','ignorecase',true);
if (~isempty(find(tmp~=1,1)))
    error('your input list must contain only .wav filenames !') 
end

% Read wavs and concatenate
amps = cell(length(wavfiles),1);
frqs = cell(length(wavfiles),1);
for i=1:length(wavfiles)        
    [amps{i},frqs{i}] = audioread(wavfiles{i});
    if size(amps{i},2)>1 
        tmp = amps{i};
        amps{i} = tmp(:,1);
    end 
end
sourceSignal = vertcat(amps{:});
if ~isrow(sourceSignal); sourceSignal=sourceSignal';end 


%  CHECK: are sampling rates the same ? 
if ~isempty(find(diff(cell2mat(frqs))~=0,1))
    error ('sampling rates seem to differ!') 
end

%% Filter 


%% Create speech shaped noise 
 ssn = speechshapednoise(sourceSignal,nfft,noctaves,srate);     

 %normalize 
 ssn_norm = normalize_rms(sourceSignal, ssn);

 % Add to speech: speech in speech-shaped noise 
 SiSSN = sourceSignal + ssn_norm;

 %% Plots  
 % Amplitude x time plots 
 %
    figure ('position', [1 1 800 800]); 
    
    subplot(3,3,1);
    plot(sourceSignal)
    title(['Speech signal']);
    ylabel('Amplitude (a.u.)');
    xlabel('Time (s)');
    
    subplot(3,3,2);
    plot(ssn_norm)
    title(['SSN norm']);
    ylabel('Amplitude (a.u.)');
    xlabel('Time (s)');
    
    subplot(3,3,3);
    plot(SiSSN)
    title(['Speech in SSN']);
    ylabel('Amplitude (a.u.)');
    xlabel('Time (s)');
    
% Spectral plots
%
    subplot(3,3,4);
    iosr.dsp.ltas(sourceSignal,srate,'noct',noctaves,'graph',true,'units','none','scaling','max0','win',srate/10);  % requires the IoSR Matlab Toolbox
    xline(50, '--k'); xline(5000, '--k'); 
    title('LTAS of speech');
    
    subplot(3,3,5);
    iosr.dsp.ltas(ssn_norm,srate,'noct',noctaves,'graph',true,'units','none','scaling','max0','win',srate/10);  % requires the IoSR Matlab Toolbox
    xline(50, '--k'); xline(5000, '--k'); 
    title('LTAS of SSN norm');
    

    subplot(3,3,6);
    iosr.dsp.ltas(SiSSN,srate,'noct',noctaves,'graph',true,'units','none','scaling','max0','win',srate/10);  % requires the IoSR Matlab Toolbox
    xline(50, '--k'); xline(5000, '--k'); 
    title('LTAS of SiSSN');
    
% Surf plots 
%
    subplot(3,3,7);
    parameter = [];
    parameter.fsAudio = srate;
    parameter.zeroPad = srate/10;
    [spec2plot,f,t] = stft(sourceSignal',parameter);
    surf(t(2:end-3),f(1:round(length(f)/2)+1),abs(spec2plot(1:round(length(f)/2)+1,2:end-3)));
    hold on; set(gcf,'renderer','zbuffer');
    shading interp; view(0,90); axis tight;
    caxis([0 50])
    title('Spectrogram of speech');
  
    subplot(3,3,8);
    parameter = [];
    parameter.fsAudio = srate;
    parameter.zeroPad = srate/10;
    [spec2plot,f,t] = stft(ssn_norm',parameter);
    surf(t(2:end-3),f(1:round(length(f)/2)+1),abs(spec2plot(1:round(length(f)/2)+1,2:end-3)));
    hold on; set(gcf,'renderer','zbuffer');
    shading interp; view(0,90); axis tight;
    caxis([0 50])
    title('Spectrogram of SSN norm');
    
    subplot(3,3,9);
    parameter = [];
    parameter.fsAudio = srate;
    parameter.zeroPad = srate/10;
    [spec2plot,f,t] = stft(SiSSN',parameter);
    surf(t(2:end-3),f(1:round(length(f)/2)+1),abs(spec2plot(1:round(length(f)/2)+1,2:end-3)));
    hold on; set(gcf,'renderer','zbuffer');
    shading interp; view(0,90); axis tight;
    zlim([0 70])
    caxis([0 50])
    title('Spectrogram of SiSSN');
    ylabel('Freqs (Hz)');
    xlabel('Time (s)');
    