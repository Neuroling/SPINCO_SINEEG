clear; close all
path2ffmpeg = 'C:\Users\aherva\Documents\NoThetaAV\ffmpeg\bin\'%;'/usr/local/bin/';%'C:\Users\becker\Documents\ffmpeg\bin\';
fs_video = 60;
BurstScaleFactor=0.125;
SELECTEDVISUALISATIONS = {'radius'}; %{'bouncing','radius'}
%cd to AudioVisalIntegration Directory - File paths etc are now all
%identical except for ffmpeg installation which is still system specific
cd(fileparts(mfilename('fullpath')));
%StimPath='C:/Users/Hervais-Adelman/Documents/Stimuli/Auditory_Corpora/Swiss_CRM/Swiss_CRM_RMS_eq/';
%StimPath='/Users/diana/STUDY/UZH/SpringSemester2019/MA/PsychoPy/MA_Theta_Exp/video/ExpTest/equalized';
StimPath='Swiss_CRM_RMS_eq_all/';
SoundFiles=myls(fullfile(StimPath,'zh*wav'));
[~,fs]=audioread(SoundFiles{1});
%BWD='C:\Users\Hervais-Adelman\Documents\Teaching\MasterProjects\AV_Theta_Restoration';
%timepointsdir='C:\Users\Hervais-Adelman\Documents\Teaching\MasterProjects\AV_Theta_Restoration\MidpointsOfVowels';
timepointsdir='MidpointsOfVowels';

%OutPath=dirmake(fullfile(BWD,'Ghitza_Like_Stimuli'));
%OutPath='C:\Users\Hervais-Adelman\switchdrive\Diana_MSc_project\DemoStimuli';
%OutPath='/Users/diana/STUDY/UZH/SpringSemester2019/MA/Stimuli/AudioVisualStimuliGeneration/eq';
OutPath=dirmake('Final_Stimuli_93ms_lags/');
%
TestSignalName='TestPulse_final_30.avi';
%
%  if ~exist(fullfile(OutPath,TestSignalName),'file')
%
%  %Make a test stimulus also:
%  %$Generate an audio signal of the desired type:
%  Duration=30;
%  DutyCycle=0.5
%  BurstDur=2;
%  SilDur=2*BurstDur*DutyCycle;
%  Window=[zeros(1,SilDur*fs),ones(1,BurstDur*fs)];
%  Nwindows=round(Duration/(BurstDur+SilDur));
%  Cycles=[repmat(Window,1,Nwindows)];
%  Noise=0.99*sign(rand(1,length(Cycles))-0.5);
%  Pulses=Noise.*Cycles;
%  %Resample Cycles to fps
%  Window=[zeros(1,SilDur*fs_video),ones(1,BurstDur*fs_video)];
%  Cycles=[repmat(Window,1,Nwindows)];
%  visualise(Pulses,Cycles,fs,[],TestSignalName,'radius','gray',[],0,1,path2ffmpeg,fs_video,15)
% end

%%%None of the rest is worth doing until we know LAGinSec

VISUALISE=1;
MinVal=0.2;%floor value for visualisation (i.e. never disappear, could be 0 then it would disappear).
%LAGinSec=[0.058];%0.077;%positive values mean push the audio back in time (i.e. start later) relative to the video (calibration placed lag at -77ms)
LAGinSec=[0.093];
% make window function
WindowDuration=0.1; %duration in seconds
%Prevent peaks from being too close together in the theta conditions
MaxAllowedRate=6;
MinFreq=230; %Ghitza 2012 uses 230 - 3800Hz. Very narrow!
MaxFreq=3800; %
%
if ~isempty(LAGinSec)
    parfor SoundFileIndex=1:length(SoundFiles)
        SoundFile=SoundFiles(SoundFileIndex); %cumbersome indexing applied in order to make compatible with parfor.
        [p,filename,e]=fileparts(SoundFile{:});
        OutFileCtrl=fullfile(OutPath,[filename,'_GlobalTheta_NoVideo.avi']);
      %  if ~exist(OutFileCtrl,'file')
            v = '.avi';
            v1D = '_1D.avi';
            
            %CALL:
            
            smooth=32;
            nChannels=16;
            [Y, fs] = audioread(SoundFile{:});
            [BandPassB,BandPassA]=butter(3,[MinFreq,MaxFreq]/(0.5*fs));
            
            %Pad all files and adjust here before sending to visualise
            LaggedY = [zeros(round(LAGinSec*fs),1);Y];
            
            
            ProcessingMode = 'Ghitza';% 'Ghitza';% 'hilbert','hilbertNoTheta';
            Prefix=['_',ProcessingMode];
            PrefixNoLowp='_NoTheta_NoLowp';
            Prefix2='_NoiseVoc';
            
            OutAudioFileName=fullfile(OutPath,[filename,Prefix,e]);
            OutAudioNVFileName=fullfile(OutPath,[filename,'_NVoc',e]);
            GloThetaOutfile=fullfile(OutPath,[filename,'_NoTheta_GlobalTheta_Audio',e]);
            OutVideoFileName=fullfile(OutPath,[filename,Prefix,v]);
            OutVideoFileName1D =fullfile(OutPath,[filename,Prefix,v1D]);
            
            
            [NoTheta,ThetaEnvs,centerfreqs] = vocode('noise', 'n', 'greenwood', ProcessingMode, smooth, ...
                nChannels, LaggedY, fs,MinFreq,MaxFreq,OutAudioFileName);
            %At this point NoTheta, which is the audio signal for the video, is
            %lagged by LaginSec
            %This is how it should stay - the video and the audio need to coincide,
            %and we have a delay, such that video is late. Therefore, pushing back
            %the audio solves our issue.
            try
                Peaks=load(fullfile(timepointsdir,[filename,'.txt']));
                %Convert to sample frequency
                Peaks=Peaks*fs;
                %turn into timeseries:
                VowelPeaks=zeros(size(Y));
                VowelPeaks(round(Peaks))=1;
                %convolve:
                Window=hanning(fs*WindowDuration);
                %Fill a hanning window with noise
                BPNoise=filtfilt(BandPassB,BandPassA,sign(rand(size(Y))-0.5));
                %Grab an aribtrary segment of noise and multiply by window
                BPThetaBurst=Window.*BPNoise([1000:999+length(Window)]);
                %Make the unfiltered bursts for video
                BPThetaBurst = BPThetaBurst / max(abs(BPThetaBurst));
                
                ThetaBurst=Window.*sign(rand(size(Window))-0.5);
                BPThetaBursts=conv(VowelPeaks,BPThetaBurst); %This way at least the windows are all identical
                %Shift Convolution back by half a cycle because matlab is silly:
                BPThetaBursts=BPThetaBursts(ceil(length(Window)/2):end-floor(length(Window)/2));
                %check Conved for overlap
                [maxTB,maxIdx]=max(abs(BPThetaBursts));
                
                
                
                % change rb
                % find vowel peaks
                VowelPeakIdxs =find(VowelPeaks);
                % get their distance factor relative to window duration (and video sampling rate)
                factor = (diff(find(VowelPeaks))/fs)/WindowDuration;
                % anything smaller than 1 will addup to more then 1 when
                % convolved
                idxs2clip = find(factor<1);
                %             % go through all peaks that are too close to each other and
                %             % correct by factor (plus some nonlinear extra scaling, since convolution)
                %             for clips = idxs2clip
                %                 VowelPeaks([VowelPeakIdxs(idxs2clip) VowelPeakIdxs(idxs2clip+1)]) = ...
                %                                 VowelPeaks([VowelPeakIdxs(idxs2clip) VowelPeakIdxs(idxs2clip+1)]).* 1 % (1/maxTB);
                %
                %                                 %VowelPeaks([VowelPeakIdxs(idxs2clip) VowelPeakIdxs(idxs2clip+1)]).* factor(idxs2clip)*1.3;
                %
                %             end
                % convolve again with corrected VowelPeaks
                BPThetaBursts=conv(VowelPeaks,BPThetaBurst); %This way at least the windows are all identical
                BPThetaBursts=BPThetaBursts(ceil(length(Window)/2):end-floor(length(Window)/2));
                [maxTB,maxIdx]=max(abs(BPThetaBursts));
                
                
                while maxTB>1
                    maxTB
                    for clips = idxs2clip
                        VowelPeaks([VowelPeakIdxs(idxs2clip) VowelPeakIdxs(idxs2clip+1)]) = ...
                            VowelPeaks([VowelPeakIdxs(idxs2clip) VowelPeakIdxs(idxs2clip+1)]).* 1/maxTB;
                    end
                    % convolve again with corrected VowelPeaks
                    BPThetaBursts=conv(VowelPeaks,BPThetaBurst); %This way at least the windows are all identical
                    BPThetaBursts=BPThetaBursts(ceil(length(Window)/2):end-floor(length(Window)/2));
                    [maxTB,maxIdx]=max(abs(BPThetaBursts));
                end
                %LEVEL??
                NoThetaMax=max(NoTheta);
                %Match?
                BPThetaBursts=BPThetaBursts*(NoThetaMax/max(BPThetaBursts));
                %Reduce the Amplitude of the theta bursts to be less intrusive:
                BPThetaBursts=BurstScaleFactor*BPThetaBursts;
                %Add to NoTheta signal:
                %We need to UNLAG the NoTheta to make it coincident with the
                %ThetaBursts
                UnlaggedNoTheta=NoTheta(1+round(LAGinSec*fs):end)';
                GlobalTheta=UnlaggedNoTheta+BPThetaBursts;
                %What to do about the relative levels? Add it and see...
                max_sample=max(abs(GlobalTheta));
                
                %and write:
                %The scaling factor here is also imposed across the board in
                %the vocode script - all stimuli will have the same mean RMS of 0.9.
                %The signal to burst ratio for these stimuli is approx 1:1
                %(more complicated than that, but the peak RMS values are
                %matched prior to mixing)
                %
                audiowriteandscale(GloThetaOutfile,GlobalTheta,fs,0.9);
                
                %Convert to sample frequency
                Peaks=load(fullfile(timepointsdir,[filename,'.txt']));
                Peaks=Peaks*fs_video;
                Window=hanning(fs_video*WindowDuration);
                
                %Now make ThetaBursts for video, downsampled correctly:
                %turn into timeseries:
                VowelPeaks=zeros(ceil(size(Y,1)*(fs_video/fs)),1);
                VowelPeaks(round(Peaks))=1;
                ThetaBursts=conv(Window,VowelPeaks);
                ThetaBurst=ThetaBursts(ceil(length(Window)/2):end-floor(length(Window)/2));
                [maxTB,maxIdx]=max(ThetaBursts);
                
                % change rb
                % find vowel peaks
                VowelPeakIdxs =find(VowelPeaks);
                
                % get their distance factor relative to window duration (and video sampling rate)
                factor = (diff(find(VowelPeaks))/fs_video)/WindowDuration;
                
                % anything smaller than 1 will addup to more then 1 when
                % convolved
                idxs2clip = find(factor<1);
                % go through all peaks that are too close to each other and
                % correct by factor (plus some nonlinear extra scaling, since convolution)
                %             for clips = idxs2clip
                %                 VowelPeaks(VowelPeakIdxs(idxs2clip):VowelPeakIdxs(idxs2clip+1)) = factor(idxs2clip)^1.75;
                %             end
                %
                %             % convolve again with corrected VowelPeaks
                %             ThetaBursts=conv(Window,VowelPeaks);
                %             ThetaBurst=ThetaBursts(ceil(length(Window)/2):end-floor(length(Window)/2));
                %             [maxTB,maxIdx]=max(ThetaBursts);
                %
                while maxTB>1
                    maxTB
                    %rescale somehow:
                    %maxIdx will indicate point of maximum overlap between two windows,
                    %we need to then find the neighbouring windows and squish them down
                    %a bit before regenerating this...
                    %look forward:
                    %Second=maxIdx+min(find(VowelPeaks(maxIdx:end)==1))-1;
                    %First=max(find(VowelPeaks(1:maxIdx)==1));
                    %Attenuate them so they add up to max 1
                    %VowelPeaks([First,Second])=1/maxTB;
                    for clips = idxs2clip
                        VowelPeaks([VowelPeakIdxs(idxs2clip) VowelPeakIdxs(idxs2clip+1)]) = ...
                            VowelPeaks([VowelPeakIdxs(idxs2clip) VowelPeakIdxs(idxs2clip+1)]).* 1/maxTB;
                        
                        %factor(idxs2clip)^1.75;
                    end
                    
                    % convolve again with corrected VowelPeaks
                    ThetaBursts=conv(Window,VowelPeaks);
                    ThetaBurst=ThetaBursts(ceil(length(Window)/2):end-floor(length(Window)/2));
                    [maxTB,maxIdx]=max(ThetaBursts);
                    
                end
                
                ThetaBursts=abs(ThetaBursts);
                ThetaVideoEnvs=ThetaBursts*(1/max(abs(ThetaBursts)));
                
            catch ME
                ME.getReport
            end
            if VISUALISE
                %Now, in order to produce visualisations, we want to show:
                %1) NV speech + Global Theta
                %2) NoTheta Speech + Global Theta
                
                [LaggedNV,~,centerfreqs] = vocode('noise', 'n', 'greenwood', 'hilbert', 10, ...
                    nChannels, LaggedY, fs,MinFreq,MaxFreq,OutAudioNVFileName);
                %this LaggedNV is the correct, lagged, stimulus to visualise.
                %It is also the correct stimulus to save as an NV only
                %condition
                %If for some reason we wanted an NV+GlobalTheta Audio only
                %condition (do we?) it will be generated as well.
                %Here:
                %Recall from above: BPThetaBursts are the bursts for unlagged
                %stimuli
                %Unlag the NV:
                UnlaggedNV=LaggedNV(1+round(LAGinSec*fs):end)';
                NVGlobalTheta=UnlaggedNV+BPThetaBursts;
                %and write:
                NVGloThetaOutfile=fullfile(OutPath,[filename,'_NV_GlobalTheta_Audio',e]);
                
                audiowriteandscale(NVGloThetaOutfile,NVGlobalTheta,fs,0.9);
                
                for VisType=SELECTEDVISUALISATIONS
                    switch lower(VisType{:})
                        case 'bouncing'
                            CircleSize=0.3;
                        otherwise
                            CircleSize=0.5;
                    end
                    StaticCircleSize=0.1; % when showing no video
                    blurAmount=30;
                    blurAmountFix=3;
                    %Now feed into the visualisation function:
                    Vprfx=['_',VisType{:}];
                    try                   
                        OutFileCtrl=fullfile(OutPath,[filename,'_GlobalTheta_NoVideo.avi']);
                        visualise(GlobalTheta',MinVal*ones(size(GlobalTheta)),fs,centerfreqs,OutFileCtrl,VisType{:},'gray',[],0,...
                            StaticCircleSize,path2ffmpeg,fs_video,blurAmountFix);
                        %delete uncompressed video:
                        %delete(OutFileCtrl);
                        
                    catch ME
                        ME.getReport
                    end
                    close all
                    close all hidden
                end %end vistypes
            end%end VISUALISE
       % end % end check if file already exists
    end  %end loop over soundfiles
    end