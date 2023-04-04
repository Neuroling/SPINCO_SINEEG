clear all 
%% Summary plot of all wav files in folder 
%-----------------------------------------------------
% Desc: 
% - Plot wav files (time x amplitude, PSD, spectra) 
% - Run detectSpeech function with default settings and mark its boundaries
% - Option to add some extended head/tail to the boundaries from detectSpeech
addpath('C:\Users\gfraga\Documents\MATLAB\')
addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')% tool for plot
dirinput= 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\';
diroutput = dirinput; 
mkdir(diroutput)
% find files 
files = dir([dirinput,'/*.wav']);
folders = {files.folder};
files = {files.name};
cd (dirinput)
 
 
%% Read all files
signals = cell(1,length(files));
fss = cell(1,length(files));
for i = 1:length(files)
   [sig, fs] = audioread(files{i});
   signals{i}= sig(:,1);
   fss{i}= fs(1);
   disp(['read ',files{i}]);
end

%% Main loop  
cd (diroutput)
for i = 1:length(signals)   

    % read data 
    dat=signals{i};
    srate = fss{i};
    times = (0:length(dat)-1)/srate;     
    
        % plots
        figure('color','white');
        subplot(3,1,1)
        plot(times,dat); hold on; 
%        title(['detectSpeech + ', num2str(headms),' ms head and ',num2str(tailms),' ms tail (win: default)'])
       ylabel('amp')
     
        subplot(3,1,2)
            iosr.dsp.ltas(dat,srate,'noct',6,'graph',true,'units','none','scaling','max0','win',srate/10);  % requires the IoSR Matlab Toolbox
            ylabel('PSD')
        subplot(3,1,3)
            parameter = [];
            parameter.fsAudio = srate;
            parameter.zeroPad = srate/10;
            [spec2plot,f,t] = stft(dat,parameter);
            surf(t,f,abs(spec2plot));
            set(gcf,'renderer','zbuffer'); shading interp; view(0,90); axis tight; caxis([0 1]);
          ylabel('freqs')

       % title          
        sgtitle(files{i}) 
        disp(files{i})
   
      %Save
      print(gcf, '-djpeg', [diroutput,'/',strrep(files{i},'.wav','.jpg')]);
      close gcf
end
  
   
