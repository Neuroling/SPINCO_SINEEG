%function [wave]= speechshapednoise(listwavs, rmsnorm, varargin)
% ==========================================================
%  Create Speech-shaped noise   
% ==========================================================
% Author: G.FragaGonzalez 2022(based on snippets from T.Houweling)
%
% Description
%   Reads wav file and if more than one is input it concatenates them.
%   Generates Gaussian white noise and filters filters the data and noise
%   and does RMS-based normalization. Last, it computes spectrum (LTAS) and
%   uses it to filters the noise (with some smoothing)
%
%   Requires SoundZone_Tools
%   https://github.com/JacobD10/SoundZone_Tools/archive/master.zip Add
%   the downloaded files in a package folder named: +Tools and add it to
%   matlab search path
%
%Usage:
%  Inputs 
%       path - path to your files
%       wavfiles - a list of '.wav' files e.g., {'sound1.wav','word2.wav'}
%       normalized - choose 1 for root mean squared normalization or 0. 
%       nfft - The number of FFT points used to compute the LTASS
%       noctaves - e.g., 6. Value to use in 1/nOctaves band smoothing (spectral smoothing in which the bandwidth of the smoothing window is a constant percentage of the center frequency).
%       srate - sampling rate (must be the equal in all files)
%       
%   Outputs 
%       SSN - speech-shaped noise 
%%

    addpath('C:\Users\gfraga\scripts_neulin\Noise_generator\functions')
    addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')
    path = 'C:\Users\gfraga\scripts_neulin\Noise_generator' ;
    wavfiles = {'yummy.wav','unbelievable.wav','please.wav'};   
    wavfiles = {'yummy.wav','unbelievable.wav'};   
    nNfft = 1000; 
    noctaves = 6;   % 1/6 octave band smoothing (spectral smoothing in which the bandwidth of the smoothing window is a constant percentage of the center frequency).
    
%% Basic input checks
    tmp = contains(wavfiles,'.wav','ignorecase',true);
    if (~isempty(find(tmp~=1,1)))
        error('your input list must contain only .wav filenames !') 
    end 

    %% Read wavs and concatenate
    amps = cell(length(wavfiles),1);frqs = cell(length(wavfiles),1);
    for i=1:length(wavfiles)        
        [amps{i},frqs{i}] = audioread(wavfiles{i});
        if size(amps{i},2)>1 
            tmp = amps{i};
            amps{i} = tmp(:,1);
        end 
    end
    sourceSignal = vertcat(amps{:});

    % are sampling rates the same ? 
    if ~isempty(find(diff(cell2mat(frqs))~=0,1))
        error ('sampling rates seem to differ!') 
    end 
        
    %% Make noise 
    
    % white noise
    rng('default');
    whiteNoise = randn(1,length(sourceSignal));
    
    %Normalize
    RMS_noise = rms(whiteNoise);
    scalingFact = rms(sourceSignal);
    ScaleFact = RMS_noise./RMS_signal;
    whiteNoise_norm = whiteNoise./scalingFact;
    
    
    OctaveBandSpace = 1/nOctaves;
    
    [spect, frqs] = Tools.LTASS(S_filt, nfft, fsS );        %Compute LTASS spectrum
    SSN = Tools.ArbitraryOctaveFilt(whiteNoise_filt, spect, frqs, nfft, srate, OctaveBandSpace);   % Generate Speech shaped noise
    
    
          %% Appli
            actual_dB_SNR = 20*log10(RMS_S/new_RMS_N);
    actual_lin_SNR = 10^(actual_dB_SNR/20);
    for j = 1:length(target_dB_SNR)
        scaleFact_S = target_lin_SNR(j)/actual_lin_SNR;  
        scaled_S{:,j} = S_filt * scaleFact_S;
        SiSSN{:,j} = SSN' + scaled_S{:,j};
        SiSSN_scaled{:,j} = SiSSN{:,j} ./ (rms(SiSSN{:,j})./new_RMS_N);
        % add ramps (10ms) to avoid annoying auditory glitches
        SiSSN{:,j}(1:fsS/100) = SiSSN{:,j}(1:fsS/100) .* linspace(0,1,fsS/100)';
        SiSSN{:,j}(end-fsS/100+1:end) = SiSSN{:,j}(end-fsS/100+1:end) .* linspace(1,0,fsS/100)';
        SiSSN_scaled{:,j}(1:fsS/100) = SiSSN_scaled{:,j}(1:fsS/100) .* linspace(0,1,fsS/100)';
        SiSSN_scaled{:,j}(end-fsS/100+1:end) = SiSSN_scaled{:,j}(end-fsS/100+1:end) .* linspace(1,0,fsS/100)';
    end 

    %%
        %%
            % now we add up S & N and we equalize the rms of the SiN snippets
            target_dB_SNR = -10:5:10;
            target_lin_SNR = 10.^(target_dB_SNR/20);
         %% Plot 
         if printplot == 'true' 
            figure
            subplot(2,2,1)
                plot(sourceSignal);hold on;
                plot(scrambledsig);hold on;
                plot(SSN); 
                title ('Time series');
                legend({'ur signal', 'scrambbled', 'SSN'}, 'Location', 'SW');

            subplot(2,2,2)
                iosr.dsp.ltas(sourceSignal,fs,'noct',6,'graph',true,'units','none','scaling','max0','win',fs/10);hold on; 
                iosr.dsp.ltas(SSN,fs,'noct',6,'graph',true,'units','none','scaling','max0','win',fs/10); hold on;  % requires the IoSR Matlab Toolbox
                iosr.dsp.ltas(scrambledsig,fs,'noct',6,'graph',true,'units','none','scaling','max0','win',fs/10);
                title ('Long-term average spectrum');
                legend({'ur signal', 'scrambbled', 'SSN'}, 'Location', 'SW'); 

            subplot(2,2,3)
                    parameter = [];
                    parameter.fsAudio = fs;
                    parameter.zeroPad = fs/10;
                    [spec,f,t] = stft(SSN,parameter);

                    surf(t(2:end-3),f(1:round(length(f)/2)+1),abs(spec(1:round(length(f)/2)+1,2:end-3)));
                    hold on; set(gcf,'renderer','zbuffer');
                    shading interp; view(0,90); axis tight;
                    title ('Spectrum (SSN)');

               subplot(2,2,4)
                    parameter = [];
                    parameter.fsAudio = fs;
                    parameter.zeroPad = fs/10;
                    [spec,f,t] = stft(scrambledsig,parameter);

                   surf(t(2:end-3),f(1:round(length(f)/2)+1),abs(spec(1:round(length(f)/2)+1,2:end-3)));
                     hold on; set(gcf,'renderer','zbuffer');
                    shading interp; view(0,90); axis tight;
                    title ('Spectrum (scrambledsigd)');
                   % yticks([0 2500 5000]);
                   % yticklabels(yticks/1000);
    
  end
% 
% function Y = shufflewins(X,W,R)
% % function Y = shufflewins(X,W,R)
% % X is a waveform, which is chopped into W-point windows
% % which are then hanning-windowed and 50%-overlapped. These
% % windows are shuffled over a radius of R points and
% % ovelap-added to construct Y, a version of X with approximately
% % the same average spectrum over R point windows, but scrambledsigd
% % structure over a W-point timescale.
% % 2010-11-13 Dan Ellis dpwe@ee.columbia.edu
% 
% 
% 
% % Force W even
% W = W + rem(W,2);
% % Hop between windows - 50% overlap
% H = W/2;
% 
% 
% 
% % Build 50% overlapped, windowed windows
% Yw = diag(hanning(W)')*frame(X,W,H);
% 
% 
% 
% % Calculate reordering
% %rpx = 1:size(Yw,2); % debug - identity
% rpx = localperm(size(Yw,2),R/H);
% 
% 
% 
% % Reorder columns
% Yw = Yw(:,rpx);
% 
% 
% 
% % Overlap-add
% Y = ola(Yw,H);
% Y = Y(1:length(X));.
