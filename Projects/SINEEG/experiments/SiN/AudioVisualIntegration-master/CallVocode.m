clear; %close all
%BWD = base working directory, this is where your processed files will be
%output
BWD='C:\Users\Becker\Documents\AudioVisualIntegration';

% if on windows, please change to your ffmpeg folder 
if isunix || ismac
    path2ffmpeg= '/usr/local/bin/';
else 
   path2ffmpeg= 'C:\Users\becker\Documents\ffmpeg\bin\';
end

%Stimpath is the path to the stimuli
StimPath=BWD;
%Processed files saved to OutPath (automaticlaly created)
OutPath=dirmake(fullfile(BWD,'ProcessedStimuli'));
SoundFiles=myls(fullfile(StimPath,'*wav'));
%just take a random few:
NumToProcess=5;
randsel=SoundFiles(randperm(length(SoundFiles)));

% use video compression?
use_vidcodecs_comp = 1;

CircleSize=0.6

%randsel=randsel(1:NumToProcess)

for SoundFile=SoundFiles
    [p,filename,e]=fileparts(SoundFile{:});
    
    v = '.avi';
    v1D = '_1D.avi';
    
    %CALL:
    
    smooth=32;
    nChannels=16;
    [Y, fs] = audioread(SoundFile{:});
    MinFreq=50;
    MaxFreq=5000; %Maybe less?
    
    Prefix='NoTheta_';
    PrefixNoLowp='NoTheta_NoLowp_';
    Prefix2='NoiseVoc_';
    
    OutAudioFileName=fullfile(OutPath,[Prefix,filename,e]);
    OutVideoFileName=fullfile(OutPath,[Prefix,filename,v]);
    OutVideoFileName1D =fullfile(OutPath,[Prefix,filename,v1D]);
    
    % if you want to try - this one here does not do low-pass filtering of
    % the signal before removing the theta:
    
    %[NoTheta,ThetaEnvs,centerfreqs] = vocode('noise', 'n', 'greenwood', 'hilbertNoThetaRB', smooth, ...
     %   nChannels, Y, fs,MinFreq,MaxFreq,OutAudioFileName);
    
    [NoTheta,ThetaEnvs,centerfreqs] = vocode('noise', 'n', 'greenwood', 'hilbertNoTheta', smooth, ...
        nChannels, Y, fs,MinFreq,MaxFreq,OutAudioFileName);
 
    %Now feed into the visualisation function:
    OutAudioVideoFileName1D=fullfile(OutPath,[Prefix,filename,'_AV_1D.avi']);
    OutAudioVideoFileNameMulti= fullfile(OutPath,[Prefix,filename,'_AV_Multi.avi']);
    OutAudioVideoFileNameMultiGrad = fullfile(OutPath,[Prefix,filename,'_AV_MultiGrad.avi']);
    
    % resampling of theta to 60Hz
    fs_video = 60;
    ThetaEnvs=resample(ThetaEnvs',1,fs/fs_video)';
    
    PCs=pca(ThetaEnvs);
    ThetaPC1=PCs(:,1);
    
    
    % the 'global' theta case for visualization
    %visualise(NoTheta,ThetaPC1,fs,centerfreqs,OutAudioVideoFileName1D,'circle','gray',2.7,use_vidcodecs_comp)
    
    % visusalise can be launched with diff visualisation options, see help
    % right now: 'bouncing' or 'circlesize' or 'brightness' 
     VisType = 'bouncing'  
    visualise(NoTheta(1:end),ThetaPC1,fs,centerfreqs,OutAudioVideoFileName1D,VisType,'gray',2.7,1,CircleSize,path2ffmpeg)
    
    VisType = 'brightness'  
    visualise(NoTheta,ThetaPC1,fs,centerfreqs,OutAudioVideoFileName1D,VisType,'gray',2.7,1,CircleSize,path2ffmpeg)
    
    % the multidimensional or ch-theta case for visualization
    visualise(NoTheta,ThetaEnvs,fs,centerfreqs,OutAudioVideoFileNameMulti,'circleMulti','gray',2.7,1,CircleSize,path2ffmpeg)

    
   

    % the multidimensional or ch-theta case for visualization, with
    % gradients encoding the envelope, rather than discretized flashes /
    % rings
    %visualise(NoTheta,ThetaEnvs,fs,centerfreqs,OutAudioVideoFileNameMultiGrad,'circleMulti','gray',[])
    
   
end
