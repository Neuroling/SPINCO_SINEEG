clear all 
%% Summary plot of all wav files in folder 
%-----------------------------------------------------
% Desc: 
% - Plot wav files (time x amplitude, PSD, spectra) 
% - Run detectSpeech function with default settings and mark its boundaries
% - Option to add some extended head/tail to the boundaries from detectSpeech
addpath('C:\Users\gfraga\Documents\MATLAB\')
addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')% tool for plot
dirinput= 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\words_take1';
diroutput = [dirinput,'_speechDetect2']; 
mkdir(diroutput)
% find files 
files = dir([dirinput,'/*.wav']);
folders = {files.folder};
files = {files.name};
%
headms = 100; % ms
tailms = 100;
PLOTME = 1;
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
    
    %  Try automatic detection of speech (show boundaries in time x amp plot) 
       windowDuration= 0.07;
       numWindowSamples = round(windowDuration*srate);
       win = hamming(numWindowSamples,'periodic');
       %mergeDuration = 0.2;
       %mergeDist = round(mergeDuration*srate);
       [idx, thresh] = detectSpeech(dat,srate,"Window",win);
      
    if PLOTME==1 
        % plots
        figure('color','white');
        subplot(3,1,1)
            plot(times,dat); hold on; 
            title(['detectSpeech + ', num2str(headms),' ms head and ',num2str(tailms),' ms tail (win: default)'])
            xline([idx(1)/srate ,idx(2)/srate],"Color","red"); hold on;             
            xline([(idx(1)/srate)- headms/1000,(idx(2)/srate) + tailms/1000 ],"Color","red","LineStyle","--");
            ylabel('amp')
          %  legend({'signal','detectSpeech start','. end',['start-',num2str(headms),'ms'],['end+',num2str(tailms),'ms']},'Location','southwest')     
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
  
  %Save audio       
   if size(idx,1)> 1 
       trimdat = dat;
      outputname = strrep(files{i},'.wav','_badDetect.wav');
   else 
     % setting boundaries to trim 
     % if adding head leads to negative value start from 1st datapoint
       startpoint = idx(1)-((headms/1000)*srate);
       if startpoint < 1 
           startpoint = 1;
       end 
      % if endpoint + tail larger than data, just cut to last data point
      endpoint = idx(2)+ ((tailms/1000)*srate);
      if endpoint > length(dat)
        endpoint = length(dat);
      end
      % trim signal
      trimdat = dat(startpoint:endpoint);
      outputname = strrep(files{i},'.wav','_trim.wav');
   end 
   
      % save to file 
      audiowrite(strcat(diroutput,'\',outputname),trimdat,srate,'BitsPerSample',24,'comment','File trimmed to speechDetect boundaries + some additional ms'); % comments can be read by reading file with audioinfo('file.wav')
   
end


