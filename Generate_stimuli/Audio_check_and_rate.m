%% Quick aid for checking the audio recordings
%-----------------------------------------------------
% Loop thru wav files, button press log 1 = good; 0 = bad; 2= undecided
% Enter rater name, save output 
addpath('C:\Users\gfraga\Documents\MATLAB\')
addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')% tool for plot
dirinput= 'V:\gfraga\SPINCO\Sound_files\LIRI_voice_SM\segmented_v1';
diroutput = 'V:\gfraga\SPINCO\Sound_files\LIRI_voice_SM\';
outputfilename = 'audio_check.xlsx';
files = dir([dirinput,'/*.wav']);
folders = {files.folder};
files = {files.name};
srate = 48000;
%%  Log rater 
ratername = input('Enter rater name: ','s');
%% Main loop Loop 
qa_score = num2cell(zeros(length(files),1));
i = 1;
rate=0;
while i < length(files)   
    
    % read data 
    [dat, srate] = audioread(files{i});
    dat = dat(:,1);
    % play audio 
     sound(dat,srate);     
     disp(['Word played: ', files{i}])    
    % plots
    subplot(3,1,1)
        plot(dat)
    subplot(3,1,2)
        iosr.dsp.ltas(dat,srate,'noct',6,'graph',true,'units','none','scaling','max0','win',srate/10);  % requires the IoSR Matlab Toolbox
    subplot(3,1,3)
        parameter = [];
        parameter.fsAudio = srate;
        parameter.zeroPad = srate/10;
        [spec2plot,f,t] = stft(dat,parameter);
        surf(t,f,abs(spec2plot));
        set(gcf,'renderer','zbuffer'); shading interp; view(0,90); axis tight; caxis([0 1]);
    
    %Request input    
    rate = inputdlg(['Rate sound:',files{i},':',],'s');
    rate = str2double(rate);
    if rate > 2
        disp('Type a valid value: 0, 1 or 2')
    else 
         % save rate 
        qa_score{i}= rate;
        % move on to next
        i = i + 1;
    end
   
end
 

tbl = cell2table([ratername,folders',files',qa_score]);

tbl.Properties.VariableNames = {'ratername','folder','file','rate'};
writetable(tbl,['audiocheck_',ratername,'.xlsx'])
disp(['file saved'])
 
