%read all files
AudioFiles=dir('C:/Users/Hervais-Adelman/Documents/Stimuli/Auditory_Corpora/Swiss_CRM/Swiss_CRM/*.wav');
OutDir=dirmake('C:/Users/Hervais-Adelman/Documents/Stimuli/Auditory_Corpora/Swiss_CRM/Swiss_CRM_RMS_eq/'); %where will they go once processed
Prefix='';
for AF=1:size(AudioFiles,1)
    FileName{AF}=AudioFiles(AF).name;
    [wave{AF},Fs(AF)]=audioread(fullfile(AudioFiles(AF).folder,AudioFiles(AF).name));
    %mean here makes it mono
    wave{AF}=mean(wave{AF},2);
    %get rms amplitude
    RMSamp(AF)=rms(wave{AF});
end
 
%make an output directory:
mkdir(OutDir)
 
%set all to same rms
MeanRMS=mean(RMSamp);
 
for AF=1:length(wave)
    ScaleFactor=MeanRMS/RMSamp(AF);%Ratio of mean to actual
    adjustedsignal=wave{AF}*ScaleFactor; %scale the signal
    audiowrite(fullfile(OutDir,[Prefix,FileName{AF}]),adjustedsignal,Fs(AF)); %save the file
end

