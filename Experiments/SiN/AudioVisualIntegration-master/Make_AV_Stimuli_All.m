clear; close all
StimPath='/Users/diana/STUDY/UZH/SpringSemester2019/MA/PsychoPy/MA_Theta_Exp/video/Training';
% BWD='C:\Users\Hervais-Adelman\Documents\Teaching\MasterProjects\AV_Theta_Restoration';
timepointsdir='/Users/diana/STUDY/UZH/SpringSemester2019/MA/Stimuli/MidpointsOfVowels';
% OutPath=dirmake(fullfile(BWD,'Ghitza_Like_Stimuli'));
OutPath='/Users/diana/STUDY/UZH/SpringSemester2019/MA/Stimuli/AudioVisualStimuliGeneration';
SoundFiles=myls(fullfile(StimPath,'*wav'));
VISUALISE=1;
LAGinSec=0.077;%positive values mean push the audio back in time (i.e. start later) relative to the video (calibration placed lag at -77ms)

% make window function
WindowDuration=0.1; %duration in seconds
%Prevent peaks from being too close together in the theta conditions
MaxAllowedRate=6;
CircleSize=0.6;
MinVal=0.2;%floor value for visualisation (i.e. never disappear, could be 0 then it would disappear).
MaxScale=0.7; %Maximum scaling of circle (max size = CircleSize*MaxScale)
%
for SoundFile={SoundFiles{randi(length(SoundFiles))}};%{'C:\Users\Hervais-Adelman\Documents\Teaching\MasterProjects\AV_Theta_Restoration\4a_7a_Original.wav'}%SoundFiles(randi(length(SoundFiles)))
    [p,filename,e]=fileparts(SoundFile{:});
    
    v = '.avi';
    v1D = '_1D.avi';
    
    %CALL:
    
    smooth=32;
    nChannels=16;
    [Y, fs] = audioread(SoundFile{:});
    [BandPassB,BandPassA]=butter(3,[230,3800]/(0.5*fs));
    
    %Pad all files and adjust here before sending to visualise
    LaggedY = [zeros(round(LAGinSec*fs),1);Y];
    MinFreq=230; %Ghitza 2012 uses 230 - 3800Hz. Very narrow!
    MaxFreq=3800; %Maybe less?
    
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
    Conved=conv(VowelPeaks,Window);
    Conved=Conved(ceil(length(Window)/2):end-floor(length(Window)/2));
    %make noise:
    Noise=(Conved.*filtfilt(BandPassB,BandPassA,sign(rand(size(Conved))-0.5)));
    Noise=(filtfilt(BandPassB,BandPassA,Noise));
    %LEVEL??
    NoThetaMax=max(NoTheta);
    %Match?
    Noise=Noise*(NoThetaMax/max(Noise));
    
    %Add to NoTheta signal:
    %NB That at this moment the stimuli are no longer appropriately
    %lagged for the AV condition
    GlobalTheta=NoTheta+Noise;
    %What to do about the relative levels? Add it and see...
    max_sample=max(abs(GlobalTheta));
    
            %Same business for the Noise:
            Noise=abs(Noise);
            Noise=Noise*(1/max(abs(Noise)));
    
    %and write:
    audiowriteandscale(GloThetaOutfile,GlobalTheta,fs,0.9);
    catch ME
    end
    if VISUALISE
        
        [LaggedNV,~,centerfreqs] = vocode('noise', 'n', 'greenwood', 'hilbert', 10, ...
                nChannels, LaggedY, fs,MinFreq,MaxFreq,OutAudioNVFileName);
            LaggedNoTheta=[zeros(1,floor(LAGinSec*fs)),NoTheta(ceil(LAGinSec*fs):end)];

            UnlaggedNV=LaggedNV(ceil(LAGinSec*fs):end);
            
            
             
            %Take the First Differential of the Envelopes
            diffThetaEnvs=diff(ThetaEnvs,2);
            %Pad with initial 0 to ensure correct length:
            diffThetaEnvs=[zeros(size(diffThetaEnvs,1),1),diffThetaEnvs];
            %Halfwave rectify it (negative slopes are of no interest)
            diffThetaEnvsRect = max( diffThetaEnvs, 0 );
            %Average:
            MeanDiffThetaEnv=mean(diffThetaEnvs);
            %Maybe rather differentiate the mean envelope!
            MeanThetaEnvs=mean(ThetaEnvs);
            DiffThetaMeanEnv=diff(MeanThetaEnvs);
            %Pad:
            DiffThetaMeanEnv=[zeros(size(DiffThetaMeanEnv,1),1),DiffThetaMeanEnv];
            %Scale to max=1?
            DiffThetaMeanEnv=DiffThetaMeanEnv*(MaxScale/max(DiffThetaMeanEnv));
            
%         for VisType={'brightness','bouncing','radius'}
        for VisType={'bouncing','radius'}

            switch lower(VisType{:})
                
                case 'bouncing'
                    CircleSize=0.3;
                otherwise
                    CircleSize=0.6;
            end
            %Now feed into the visualisation function:
            Vprfx=[VisType{:},'_'];
            % OutAudioVideoFileName1D=fullfile(OutPath,[Prefix,filename,'_AV_1D_diffs.avi']);
            OutAudioVideoFileName1Dcont=fullfile(OutPath,[Vprfx,'NoTheta_Audio_',filename,'ThetaDiff_Video.avi']);
            
            % OutAudioVideoFileNameMulti= fullfile(OutPath,[Prefix,filename,'_AV_Multi.avi']);
            % OutAudioVideoFileNameMultiGrad = fullfile(OutPath,[Prefix,filename,'_AV_MultiGrad.avi']);
            
           
            % resampling of theta to 60Hz
            fs_video = 60;
            ThetaVideoEnvs=resample(DiffThetaMeanEnv',1,round(fs/fs_video))';
            %Scale and Rectify, and that means no z-scoring on the other side:
            ThetaVideoEnvs=ThetaVideoEnvs*(MaxScale/max(abs(ThetaVideoEnvs)));
            ThetaVideoEnvs=max(ThetaVideoEnvs,0);
            %set some kind of floor value:
            ThetaVideoEnvs(ThetaVideoEnvs<MinVal)=MinVal;
            % the 'global' theta case for visualization
            %   visualise(NoTheta,ThetaVideoEnvs,fs,centerfreqs,OutAudioVideoFileName1D,'circle','gray',2.7,1)
            % 'global case but with smooth visual stimuli:
%             OutFile=fullfile(OutPath,[Vprfx,'NoTheta_Audio_',filename,'ThetaDiff_Video.avi']);
%             visualise(NoTheta,ThetaVideoEnvs,fs,centerfreqs,OutAudioVideoFileName1Dcont,VisType{:},'gray',[],1,CircleSize);
%             %delete uncompressed video:
%             delete(OutAudioVideoFileName1Dcont);
            
            % Visualise with vocoded case but with smooth visual stimuli
            %NB these vocoded stimuli with 10Hz LP envelope filtering are Ghitza-controls
            
%             OutFile=fullfile(OutPath,[Vprfx,'NV_Audio',filename,'ThetaDiff_Video.avi']);
%             visualise(LaggedNV,ThetaVideoEnvs,fs,centerfreqs,OutFile,VisType{:},'gray',[],1,CircleSize)
%             %delete uncompressed video:
%             delete(OutFile);
            try
            % Visualise NoTheta using GlobalTheta as visual input
            %Global Theta needs audio to be lagged again :-/
            OutFile=fullfile(OutPath,[Vprfx,'NoTheta_Audio_',filename,'_GlobalTheta_Video.avi']);
            %Scale and Rectify, and that means no z-scoring on the other side:

            ThetaVideoEnvs=resample(Noise',1,fs/fs_video)';
            ThetaVideoEnvs=ThetaVideoEnvs*(MaxScale/max(abs(ThetaVideoEnvs)));

            ThetaVideoEnvs=max(ThetaVideoEnvs,0);
            %set some kind of floor value:
            ThetaVideoEnvs(ThetaVideoEnvs<MinVal)=MinVal;   
            visualise(LaggedNoTheta,ThetaVideoEnvs,fs,centerfreqs,OutFile,VisType{:},'gray',[],1,CircleSize)
            %delete uncompressed video:
            delete(OutFile);
            
            % Visualise NoTheta using GlobalTheta as visual input;
            %NB these vocoded stimuli with 10Hz LP envelope filteringare Ghitza-controls
            OutFile=fullfile(OutPath,[Vprfx,'NV_Audio_',filename,'_GlobalTheta_Video.avi']);
            visualise(UnlaggedNV,ThetaVideoEnvs,fs,centerfreqs,OutFile,VisType{:},'gray',[],1,CircleSize)
            
            %delete uncompressed video:
            delete(OutFile);
            catch ME
            end
            close all
        end %end vistypes
    end%end VISUALISE
    
end %end loop over soundfiles


