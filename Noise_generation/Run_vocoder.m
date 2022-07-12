clear all ; 
%% ========================================================================
%  Generate Vocoded speech 
% ========================================================================
% Author: G.FragaGonzalez 2022(based on snippets from T.Houweling)
% Description
%  BLABlahblah
%
%-------------------------------------------------------------------------
% add paths of associated functions and toolbox TSM required by function 
addpath('V:\gfraga\scripts_neulin\Noise_generation\functions')
addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')
addpath('C:\Users\gfraga\Documents\MATLAB\')

%% Inputs 
% paths and files 
dirinput =      'V:\gfraga\SPINCO\Sound_files\Digits_16k\' ;
diroutput =     'V:\gfraga\SPINCO\Sound_files\Digits_16k_in_SSN\';
wavfiles =      dir([dirinput, 'Speaker01*.wav']);
wavfiles =      fullfile(dirinput, {wavfiles.name});

% Filter settings (butterworth filter lower and upper cut freqs in Hz)
filt_low =      50 ;
filt_upper =    5000;
srate =         16000;
% Parameters for Vocoding function 
exc = 'noise' ; 
mapping= 'n'; 
filters = 'linear';
EnvelopeExtractor = 'half'; 
smooth= 1 ; 
nCh = 16; 
MinFreq = filt_low;
MaxFreq = filt_upper;

noctaves =      6;   % 1/6 octave band smoothing (spectral smoothing in which the bandwidth of the smoothing window is a constant percentage of the center frequency).

% SNR levels
target_dB_snr = -10:5:10;

%% Read normalize, filter and concatenate 
disp('...normalizing speech (rms) and filtering')

% Filter
signals = cellfun(@(x) audioread(x), wavfiles, 'UniformOutput',0);
NyqFreq = srate/2;            % fs = 2kHz; Nyquist freq. = 1 kHz
[filt_b,filt_a]=butter(3, [filt_low filt_upper]/NyqFreq);
sigs_filt = cellfun(@(x) filtfilt(filt_b,filt_a,x), signals,'UniformOutput',0);


%Normalize signal to median rms in the set of files (after filtering)
allrms  = cellfun(@(x) rms(x),sigs_filt);
RMS_median = median(allrms);
sigs_filt_norm = cellfun(@(x) x.*RMS_median/rms(x), sigs_filt, 'UniformOutput', 0);


%% Generate noise and normalize it
 disp('...generate speech-shaped noise');
 
 % Concatenate speech signal to generate noise
 sigs_filt_norm_concat = vertcat(sigs_filt_norm{:});
 
 % speech-shape noise
 ssn = speechshapednoise(sigs_filt_norm_concat,nfft,noctaves,srate);
 
 %% Loop thru SNR values 
  for L=1:length(target_dB_snr)
     disp(['Start SNR loop']);
     
     dblevel = target_dB_snr(L); 
     target_lin_snr = db2mag(dblevel);  % db2mag matlab func does: 10.^(target_dB_SNR/20);
     
     %% Add noise to each file  with intro and outro noise and ramps
     disp('...introducing startup noise + ramp in in SiSSN words')
     
     sigs_filt_norm_adj = cell(length(sigs_filt_norm),1);
     SiSSN= cell(length(sigs_filt_norm),1);
     for i = 1:length(sigs_filt_norm)
             
      %%%% get a noise segment
         % Define intro and outro and ramps
         head_points = head_length * srate;
         tail_points = tail_length * srate;
         rampin = [linspace(0,1,rampin_length*srate ),ones(1,head_points-rampin_length*srate)];
         rampout = [flip(linspace(0,1,rampout_length*srate)),zeros(1,tail_points-rampout_length*srate)];
         
         if head_points + tail_points + length(sigs_filt_norm_adj{i}) > length(ssn)
             error('You try to add too long head/tail noise periods');
         end
         
         % normalize noise
         disp('normalizing SSN to the individual signal rms');
         ssn_norm = ssn.*(rms(sigs_filt_norm{i})/rms(ssn));
         
       
      %%%% noise to signal
         % adjust signal intensity
         sigs_filt_norm_adj{i} = sigs_filt_norm{i}.*target_lin_snr;
         
         %Cut noise chunk
         noise2use_points = head_points +length(sigs_filt_norm_adj{i})+ tail_points;
         seed= randperm(length(ssn_norm)-noise2use_points) ;%find a random data point(prevent out of bounds)
         noise2use = ssn_norm(seed(1):seed(1)+noise2use_points); % take that noise segment
         
         %Speech in Speech-shaped noise:
         tmpSiSSN = sigs_filt_norm_adj{i}' + noise2use(1+head_points:head_points+length(sigs_filt_norm_adj{i}));
         ssn_head = noise2use(1:head_points);
         ssn_tail = noise2use((end-tail_points)+1:end);
         SiSSN{i,1} = [ssn_head.*rampin, tmpSiSSN, ssn_tail.*rampout];
         
         %Normalize the combined signal + noise to avoid clipping 
         SiSSN{i,1} = normalize(SiSSN{i,1}, 'range',[-1 1]);
     end
     
     %% Plot and save    
     for i = 1:length(SiSSN)
         
         % Save audio
         [pathstr, name , ext] = fileparts(wavfiles{i});
         outputfilename = strrep([diroutput,'SiSSN_',name,num2str(dblevel),'db',ext],'\\','\');
         audiowrite(outputfilename, SiSSN{i},srate)
         disp(['...saved ',outputfilename]);
         
         % Figures
         %-------------------------
         SiSSN2plot = SiSSN{i};
         original2plot = audioread(wavfiles{i})';
         variables = {'original2plot','SiSSN2plot'};
         
         %
         infotext = ['SSN from ', num2str(length(wavfiles)),' files (',num2str(srate),' Hz) concat and filt (',num2str(filt_low),...
             ' ',num2str(filt_upper),' Hz). Extra noise intro (', num2str(head_length),' s), outro (', num2str(tail_length),' s) with ramps.',...
             ' Noct ',num2str(noctaves),'. NFFT ',num2str(nfft),'. SSN norm-',num2str(dblevel),'db'];
         
         figure ('position', [1 1 800 800],'color','white');
         annotation('textbox', [0, 0.075, 1, 0], 'string',infotext)
         % Amplitude x  time
         titles = {'speech (filt)','SiSSN(norm)'};
         for p = 1:2
             subplot(3,2,p);
             plot(eval(variables{p}))
             title(titles{p});  ylabel('Amplitude (a.u.)');  xlabel('Time (ms)');
         end
         % Spectral plots
         titles = {'LTAS speech (filt)','LTAS SiSSN (norm)'};
         for p = 1:2
             subplot(3,2,2+p);
             iosr.dsp.ltas(eval(variables{p}),srate,'noct',noctaves,'graph',true,'units','none','scaling','max0','win',srate/10);  % requires the IoSR Matlab Toolbox
             xline(50, '--k'); xline(5000, '--k');
             title(titles{p});
         end
         % Surf plots
         titles = {'Spectrogram speech(filt)', 'Spectrogram SiSSN(norm)'};
         for p = 1:2
             subplot(3,2,4 + p);
             parameter = [];
             parameter.fsAudio = srate;
             parameter.zeroPad = srate/10;
             [spec2plot,f,t] = stft(eval(variables{p})',parameter);
             surf(t,f,abs(spec2plot));
             hold on; set(gcf,'renderer','zbuffer'); shading interp; view(0,90); axis tight; caxis([0 50])
             title(titles{p});
         end
         
         print(gcf, '-djpeg', strrep(outputfilename,'.wav','.jpg'));
         disp(['...saved figure for ',outputfilename]);
         %
         close gcf
     end
 end % close noise level loop