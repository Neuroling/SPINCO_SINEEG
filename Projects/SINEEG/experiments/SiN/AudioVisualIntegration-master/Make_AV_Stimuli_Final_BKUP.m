clear; close all
path2ffmpeg = 'C:\Users\studi\Documents\NoThetaAV\ffmpeg\bin\'%;'/usr/local/bin/';%'C:\Users\becker\Documents\ffmpeg\bin\';
fs_video = 60;

%cd to AudioVisalIntegration Directory - File paths etc are now all
%identical except for ffmpeg installation which is still system specific
cd(fileparts(mfilename('fullpath')));
%StimPath='C:/Users/Hervais-Adelman/Documents/Stimuli/Auditory_Corpora/Swiss_CRM/Swiss_CRM_RMS_eq/';
%StimPath='/Users/diana/STUDY/UZH/SpringSemester2019/MA/PsychoPy/MA_Theta_Exp/video/ExpTest/equalized';
StimPath='Swiss_CRM_RMS_eq/';
SoundFiles=myls(fullfile(StimPath,'*wav'));
[~,fs]=audioread(SoundFiles{1});
%BWD='C:\Users\Hervais-Adelman\Documents\Teaching\MasterProjects\AV_Theta_Restoration';
%timepointsdir='C:\Users\Hervais-Adelman\Documents\Teaching\MasterProjects\AV_Theta_Restoration\MidpointsOfVowels';
timepointsdir='MidpointsOfVowels';

%OutPath=dirmake(fullfile(BWD,'Ghitza_Like_Stimuli'));
%OutPath='C:\Users\Hervais-Adelman\switchdrive\Diana_MSc_project\DemoStimuli';
%OutPath='/Users/diana/STUDY/UZH/SpringSemester2019/MA/Stimuli/AudioVisualStimuliGeneration/eq';
OutPath=dirmake('Stimuli/');

make_test_stim = 0;


%if ~exist(fullfile(OutPath,'TestPulse.avi'))

%Make a test stimulus also:
%$Generate an audio signal of the desired type:
%Duration=3;
DutyCycle=0.5
BurstDur=1;
SilDur=1*BurstDur*DutyCycle;
Window=[zeros(1,SilDur*fs),ones(1,BurstDur*fs),zeros(1,SilDur*fs)];
Nwindows=15;

Cycles=[repmat(Window,1,Nwindows)];
Noise=0.99*sign(rand(1,length(Cycles))-0.5);
Pulses=Noise.*Cycles;
OutFile='TestPulse_2s.avi';
%Resample Cycles to fps
t = [1:length(Cycles)]/fs;

%create the video with square pulses for testing
if make_test_stim
    visualise(Pulses,resample(Cycles,1,fs/fs_video,1),fs,[],OutFile,'radius','gray',[],1,1,path2ffmpeg,fs_video)
end
%end

%%%None of the rest is worth doing until we know LAGinSec

VISUALISE=1;
MinVal=0.1;%floor value for visualisation (i.e. never disappear, could be 0 then it would disappear).
LAGinSec=[0.058];%0.077;%positive values mean push the audio back in time (i.e. start later) relative to the video (calibration placed lag at -77ms)

% make window function
WindowDuration=0.1; %duration in seconds

%Prevent peaks from being too close together in the theta conditions
MaxAllowedRate=6;
MinFreq=230; %Ghitza 2012 uses 230 - 3800Hz. Very narrow!
MaxFreq=3800; %
%
if ~isempty(LAGinSec);
    for SoundFile=SoundFiles
        [p,filename,e]=fileparts(SoundFile{:});
        
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
        Prefix=[ProcessingMode,'_'];
        PrefixNoLowp='NoTheta_NoLowp_';
        Prefix2='NoiseVoc_';
        
        OutAudioFileName=fullfile(OutPath,[Prefix,filename,e]);
        OutAudioNVFileName=fullfile(OutPath,['NV_',filename,e]);
        GloThetaOutfile=fullfile(OutPath,[Prefix,filename,'_GlobalTheta',e]);
        OutVideoFileName=fullfile(OutPath,[Prefix,filename,v]);
        OutVideoFileName1D =fullfile(OutPath,[Prefix,filename,v1D]);
        
        
        [NoTheta,ThetaEnvs,centerfreqs] = vocode('noise', 'n', 'greenwood', ProcessingMode, smooth, ...
            nChannels, LaggedY, fs,MinFreq,MaxFreq,OutAudioFileName);
        
        %%%UNLAGGING%%%
        %Now correct the NoTheta Envelopes for visualisation by removing initial padding:
        NoTheta=NoTheta(ceil(LAGinSec*fs)+1:end);
        %Create Stimuli using the timecourses provided by Diana:
        
        %read in the timepoints:
        try
            Peaks=load(fullfile(timepointsdir,[filename,'.txt']));
            
            %Convert to samplefrequency
            Peaks=Peaks*fs;
            %turn into timeseries:
            VowelPeaks=zeros(size(NoTheta));
            VowelPeaks(round(Peaks))=1;
            %convolve:
            Window=hanning(fs*WindowDuration);
            %Fill a hanning window with noise
            BPNoise=filtfilt(BandPassB,BandPassA,sign(rand(size(Y))-0.5));
            %Grab an aribtrary segment of noise and multiply by window
            BPThetaBurst=Window.*BPNoise([1000:999+length(Window)]);
            %Make the unfiltered bursts for video
            ThetaBurst=Window.*sign(rand(size(Window))-0.5);
            BPThetaBursts=conv(VowelPeaks,BPThetaBurst); %This way at least the windows are all identical
            %Shift Convolution back by half a cycle because matlab is silly:
            BPThetaBursts=BPThetaBursts(ceil(length(Window)/2):end-floor(length(Window)/2));
            %check Conved for overlap
            [maxTB,maxIdx]=max(BPThetaBursts);
            while maxTB>1
                %rescale somehow:
                %maxIdx will indicate point of maximum overlap between two windows,
                %we need to then find the neighbouring windows and squish them down
                %a bit before regenerating this...
                %look forward:
                Second=maxIdx+min(find(VowelPeaks(maxIdx:end)==1))-1;
                First=max(find(VowelPeaks(1:maxIdx)==1));
                %Attenuate them so they add up to max 1
                VowelPeaks([First,Second])=1/maxTB;
                BPThetaBursts=conv(VowelPeaks,Window);
                BPThetaBursts=[BPThetaBursts(length(Window)/2:end),zeros(1,length(Window)/2)];
                [maxTB,maxIdx]=max(BPThetaBursts);
            end
            %make noise:
            %LEVEL??
            NoThetaMax=max(NoTheta);
            %Match?
            BPThetaBursts=BPThetaBursts*(NoThetaMax/max(BPThetaBursts));
            
            %Add to NoTheta signal:
            %NB That at this moment the stimuli are no longer appropriately
            %lagged for the AV condition
            GlobalTheta=NoTheta+BPThetaBursts;
            %What to do about the relative levels? Add it and see...
            max_sample=max(abs(GlobalTheta));
            
            %ThetaBursts for video:
            ThetaBursts=conv(Window,VowelPeaks);
            ThetaBurst=ThetaBursts(ceil(length(Window)/2):end-floor(length(Window)/2));
            [maxTB,maxIdx]=max(ThetaBursts);
            while maxTB>1
                %rescale somehow:
                %maxIdx will indicate point of maximum overlap between two windows,
                %we need to then find the neighbouring windows and squish them down
                %a bit before regenerating this...
                %look forward:
                Second=maxIdx+min(find(VowelPeaks(maxIdx:end)==1))-1;
                First=max(find(VowelPeaks(1:maxIdx)==1));
                %Attenuate them so they add up to max 1
                VowelPeaks([First,Second])=1/maxTB;
                BPThetaBursts=conv(VowelPeaks,Window);
                BPThetaBursts=[BPThetaBursts(length(Window)/2:end),zeros(1,length(Window)/2)];
                [maxTB,maxIdx]=max(BPThetaBursts);
            end
            ThetaBursts=abs(ThetaBursts);
            ThetaBursts=ThetaBursts*(1/max(abs(ThetaBursts)));
            
            %and write:
            audiowriteandscale(GloThetaOutfile,GlobalTheta,fs,0.9);
        catch ME
        end
        if VISUALISE
            
            [LaggedNV,~,centerfreqs] = vocode('noise', 'n', 'greenwood', 'hilbert', 10, ...
                nChannels, LaggedY, fs,MinFreq,MaxFreq,OutAudioNVFileName);
            LaggedNoTheta=[zeros(1,floor(LAGinSec*fs)),NoTheta(ceil(LAGinSec*fs):end)];
            
            %for VisType={'bouncing','radius'}
            for VisType={'radius'}
                
                switch lower(VisType{:})
                    case 'bouncing'
                        CircleSize=0.3;
                    otherwise
                        CircleSize=0.5;
                end
                %Now feed into the visualisation function:
                Vprfx=[VisType{:},'_'];
                
                try
                    
                    % Visualise NoTheta using GlobalTheta as visual input
                    %Global Theta needs audio to be lagged again :-/
                    OutFile=fullfile(OutPath,[Vprfx,'NoTheta_Audio_',filename,'_GlobalTheta_Video.avi']);
                    %Scale and Rectify, and that means no z-scoring on the other side:
                    
                    ThetaVideoEnvs=resample(ThetaBursts',1,fs/fs_video)';
                    ThetaVideoEnvs=ThetaVideoEnvs*(1/max(abs(ThetaVideoEnvs)));
                    
                    ThetaVideoEnvs=max(ThetaVideoEnvs,0);
                    %set some kind of floor value:
                    ThetaVideoEnvs(ThetaVideoEnvs<MinVal)=MinVal;
                    visualise(LaggedNoTheta,ThetaVideoEnvs,fs,centerfreqs,OutFile,VisType{:},'gray',[],1,CircleSize,path2ffmpeg,fs_video);
                    %delete uncompressed video:
                    delete(OutFile);
                    
                    % Visualise NoTheta using GlobalTheta as visual input;
                    %NB these vocoded stimuli with 10Hz LP envelope filteringare Ghitza-controls
                    OutFile=fullfile(OutPath,[Vprfx,'NV_Audio_',filename,'_GlobalTheta_Video.avi']);
                    visualise(UnlaggedNV,ThetaVideoEnvs,fs,centerfreqs,OutFile,VisType{:},'gray',[],1,CircleSize,path2ffmpeg,fs_video);
                    
                    %delete uncompressed video:
                    delete(OutFile);
                catch ME
                    
                end
                
                close all
            end %end vistypes
        end%end VISUALISE
        
    end %end loop over soundfiles
end