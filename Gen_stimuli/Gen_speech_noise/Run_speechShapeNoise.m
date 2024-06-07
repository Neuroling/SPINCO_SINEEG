clear all ; 
%% ========================================================================
%  Generate Speech in Speech-shaped noise   
% ========================================================================
% Author: G.FragaGonzalez 2022(based on snippets from T.Houweling)
% Description
%   - Reads list of .wav files 
%   - Filters signal (butterworth), 
%   - Normalize 
%   - Concatenate 
%   - Generate speech shaped noise-SSN
%   - Adjust speech intensity to different levels
%   - SiSSN: adds the noise (optional:  a head and a tail and ramps)
%
%-------------------------------------------------------------------------
 % Find the index of the "script" folder
folders = strsplit(matlab.desktop.editor.getActiveFilename, filesep);
scriptPathIdx = find(strcmp(folders, 'Scripts'), 1);
baseDir = [fullfile(folders{1:(scriptPathIdx-1)}),filesep];
 % add paths of associated functions and toolbox TSM required by function 
addpath([baseDir, fullfile('Scripts','Gen_stimuli','Gen_speech_noise','functions')])
addpath([baseDir, fullfile('Scripts','Gen_stimuli','Gen_speech_noise')])

% Inputs 
 % paths and files 
dirinput =      [baseDir,fullfile('Stimuli','AudioGens','Experiment2','tts-golang-44100hz','tts-golang-equalisedDuration')] ;
diroutput =      [baseDir,fullfile('Stimuli','AudioGens','Experiment2','tts-golang-44100hz','tts-golang-equalisedDuration-SiSSN')];




% save a 'last run' copy of script 
[filepath,name,ext] = fileparts(matlab.desktop.editor.getActiveFilename);
copyfile(matlab.desktop.editor.getActiveFilename,[diroutput,filesep,name,'_lastRun.txt'])


% find files
% cd (dirinput)
audiofiles =      dir([dirinput,filesep,'*.wav']); % must be more than one 
audiofiles =      fullfile(dirinput, {audiofiles.name}); 
 
%% Filter settings (butterworth filter lower and upper cut freqs in Hz)
filt_low =      70 ;
filt_upper =    5000;

% Length of intro/outro (with ramp in/out)
rampin_length =  0.5;% 0.02; % ramp length in seconds
rampout_length =  0.5;%% 0; % ramp length in seconds

% Parameters for SSN function
nfft =          1000;
noctaves =      6;   % 1/6 octave band smoothing (spectral smoothing in which the bandwidth of the smoothing window is a constant percentage of the center frequency).

% SNR levels
%  target_dB_snr = [-11] %,-9,-7,];%15db used for 'clean condition catch trials
target_dB_snr = [-9];

%% Generate noise from concatenated data
% read signals
[signals, fss] = cellfun(@(x) audioread(x), audiofiles, 'UniformOutput',0);

%% Filter signals
srate = fss{1};
NyqFreq = srate/2;            % fs = 2kHz; Nyquist freq. = 1 kHz
[filt_b,filt_a]=butter(3, [filt_low filt_upper]/NyqFreq); % make butterworth filter
sigs_filt = cellfun(@(x) filtfilt(filt_b,filt_a,x), signals,'UniformOutput',0);


%% concatenate
sigs_filt_concat = vertcat(sigs_filt{:});

%% speech-shape noise 
rng(3) % set up random seed
ssn = speechshapednoise(sigs_filt_concat,nfft,noctaves,srate);
disp('...generated speech-shaped noise from file '); 
audiowrite([diroutput,'/noise/_ssn.wav'],ssn,srate,'BitsPerSample',16,'comment','speech-shaped noise with length of all files in folder concatenated');        

%% Loop thru SNR values and embed  the speech in SSN  
for L=1:length(target_dB_snr)
    disp('....Starting SNR loop');       

   % set up the signal manipulation (see later below)
    dblevel = target_dB_snr(L); 
    target_lin_snr = db2mag(dblevel);  % db2mag matlab func does: 10.^(target_dB_SNR/20);    
    
    
    % Define intro and outro and ramps 
    rampin = linspace(0,1,rampin_length*srate );
    rampout = flip(linspace(0,1,rampout_length*srate));
    
    %Add noise to each file with rampin/out
    %-----------------------------------------
    sigs_filt_adj = cell(length(sigs_filt),1);
    SiSSN= cell(length(sigs_filt),1);    
    for i = 1:length(sigs_filt)               
        % adjust signal intensity
        sigs_filt_adj{i} = sigs_filt{i}.*target_lin_snr;
         
        % Cut noise chunk
        noise2use_points = length(sigs_filt_adj{i});
        seed = randperm(length(ssn)-noise2use_points) ;%find a random data point(prevent out of bounds)
        noise2use = ssn(seed(1):seed(1)+noise2use_points-1); % take that noise segment
      
        % normalize noise to current unadjusted signal rms         
        noise2use_norm = noise2use.*(rms(sigs_filt{i})/rms(noise2use));       
 
        %Speech in Speech-shaped noise:
        noise2use_norm_ramp = (noise2use_norm.*[rampin,ones(1,length(noise2use_norm)-length(rampin)-length(rampout)),rampout]);
        sissn = sigs_filt_adj{i}' + noise2use_norm_ramp;
        disp(['Applying SNR: ', num2str(target_dB_snr(L)) ,'db to file: ' audiofiles{i}])

       %Normalize to perceived loudness            
       target_loudnessDB = -23;
       SiSSN{i,1}=  normalize_by_perceivedLoudness(sissn',fss{i},target_loudnessDB);
        
       %Prevent clipping only if needed 
       if any(SiSSN{i,1}>0.99 | SiSSN{i,1} < -0.99)
          SiSSN{i,1} = SiSSN{i,1}*(0.999999/max(abs(SiSSN{i,1})));  
          disp('preventing clipping')
       end
    end

%% Save audio (and plots if requested)
     audio2save= cell(length(SiSSN),1);
     for i = 1:length(SiSSN)
         
         %%% Save audio (speech in speech-shaped noise
         %--------------------------------------------
         [pathstr, name , ext] = fileparts(audiofiles{i});
         outputfilename = strrep([diroutput,'/SiSSN_',name,'_',num2str(dblevel),'db',ext],'\\','\');
         text = ['Speech in speech-shaped noise with ',num2str(target_dB_snr(L)),' SNR db. Normalized at ',num2str(target_loudnessDB),'db. MinF ',num2str(filt_low),' MaxF ',num2str(filt_upper)];
         audiowrite(outputfilename, SiSSN{i},srate,'BitsPerSample',16,'comment',text);        
         disp(['...saved ',outputfilename]);
        
     end
end

     
 