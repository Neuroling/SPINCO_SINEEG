%% Summary plot of all wav files in folder 
%-----------------------------------------------------
addpath('C:\Users\gfraga\Documents\MATLAB\')
addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')% tool for plot
dirinput= 'V:\gfraga\SPINCO\Sound_files\LIRI_voice_SM\segmented_v2';
diroutput = [dirinput,'_figs']
mkdir(diroutput)
outputfilename = 'audio_check.xlsx';
files = dir([dirinput,'/*.wav']);
folders = {files.folder};
files = {files.name};

%% Main loop Loop 

for i = 1:length(files)   
    
    % read data 
    [dat, srate] = audioread(files{i});
    srate = srate(1);
    dat = dat(:,1);
    times = (0:length(dat)-1)/srate; 
    % plots
    subplot(3,1,1)
        plot(times,dat)
    subplot(3,1,2)
        iosr.dsp.ltas(dat,srate,'noct',6,'graph',true,'units','none','scaling','max0','win',srate/10);  % requires the IoSR Matlab Toolbox
    subplot(3,1,3)
        parameter = [];
        parameter.fsAudio = srate;
        parameter.zeroPad = srate/10;
        [spec2plot,f,t] = stft(dat,parameter);
        surf(t,f,abs(spec2plot));
        set(gcf,'renderer','zbuffer'); shading interp; view(0,90); axis tight; caxis([0 1]);
   
   disp(files{i})
   
  %Save 
  %savefig([diroutput,'/',strrep(files{i},'.wav','.fig')])
  print(gcf, '-djpeg', [diroutput,'/',strrep(files{i},'.wav','.jpg')]);
   close all
end
