clear all ; 
% ========================================================================
%  Generate Vocoded speech 
% ========================================================================
% Author: G.FragaGonzalez 2022(based on snippets from T.Houweling)
% Description
%  BLABlahblah
%
%-------------------------------------------------------------------------
% add paths of associated functions and toolbox TSM required by function 
addpath('V:\gfraga\scripts_neulin\Generate_noise\functions')
addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')
addpath('C:\Users\gfraga\Documents\MATLAB\')

%% Inputs 
% paths and files 
dirinput =      'V:\gfraga\SPINCO\Sound_files\Digits_16k\' ;
diroutput =     'V:\gfraga\SPINCO\Sound_files\Digits_16k_vocoded\';
wavfiles =      dir([dirinput, 'Speaker*.wav']);
wavfiles =      fullfile(dirinput, {wavfiles.name});

% Filter settings (butterworth filter lower and upper cut freqs in Hz)
 
srate =         16000;

% Parameters for Vocoding function 
exc =           'noise' ; 
mapping=        'n'; 
filters =       'greenwood'; % Greenwood
EnvelopeExtractor = 'half'; 
smooth=          30 ; 
nCh =           4; 
MinFreq =       50;
MaxFreq =        5000;

% Degradation levels
target_nchannels = [4,8,12,16,20];
 
%% Call vocoder function (save in structure array)

% read signals
[signals, freqs] = cellfun(@(x) audioread(x), wavfiles, 'UniformOutput',0);

% Loop and vocode for each degradation level
nvStimuli = struct(); 
for i = 1:length(signals)     
    [pathstr, name , ext] = fileparts(wavfiles{i});
    nvStimuli(i).filename = name;
    nvStimuli(i).ursignal = signals{i};
    nvStimuli(i).srate = srate;
    
   for ii = 1:length(target_nchannels)       
       nvStimuli(i).vocoded(ii).filename= strrep([diroutput,'NoiseVocoded_',name,'_',num2str(target_nchannels(ii)),'chans',ext],'\\','\');
       nvStimuli(i).vocoded(ii).channels = target_nchannels(ii);
       nvStimuli(i).vocoded(ii).nvsignal = vocode_2022(exc, mapping, filters, EnvelopeExtractor, smooth, nvStimuli(i).vocoded(ii).channels, nvStimuli(i).ursignal, srate, MinFreq, MaxFreq);            
        
        
    end
end

%% Saving 
% Matlab 
save([diroutput,'stimuli_nv'],'nvStimuli')
% Audio
for i = 1:length(nvStimuli)
   for ii = 1:length(nvStimuli(i).vocoded)       
        audiowrite(nvStimuli(i).vocoded(ii).filename, nvStimuli(i).vocoded(ii).nvsignal,srate)
         disp(['...saved ',nvStimuli(i).vocoded(ii).filename]);
   end
    
end

%% Summary figures 
for i = 1:length(target_nchannels) 

       %%% Save summary plot 
       footnote = ['Vocoder_2022 run for ',name,' (srate: ',num2str(srate),' Hz) with arguments: exc (', exc, '), mapping (',mapping, '), filters(',...
           filters ,'), min-max freqs(',num2str(MinFreq),'-',num2str(MaxFreq),'), channels (',num2str(target_nchannels(i)),'), smooth (',num2str(smooth),')'];
       
       signal_nv2plot = signal_nv{ii};
       original2plot = signals{ii}';
       variables2plot = {'original2plot','signal_nv2plot'};
       %
       figure ('position', [1 1 800 800],'color','white');
       annotation('textbox', [0, 0.075, 1, 0], 'string',footnote)
       % Amplitude x  time
       titles = {'speech','signal NV'};
       for p = 1:2
           subplot(3,2,p);
           plot(eval(variables2plot{p}))
           title(titles{p});  ylabel('Amplitude (a.u.)');  xlabel('Time (ms)');
       end
       % Spectral plots
       titles = {'LTAS speech ','LTAS signal NV '};
       for p = 1:2
           subplot(3,2,2+p);
           iosr.dsp.ltas(eval(variables2plot{p}),srate,'noct',6,'graph',true,'units','none','scaling','max0','win',srate/10);  % requires the IoSR Matlab Toolbox
           xline(50, '--k'); xline(5000, '--k');
           title(titles{p});
       end
       % Surf plots
       titles = {'Spectrogram speech', 'Spectrogram signal NV'};
       for p = 1:2
           subplot(3,2,4 + p);
           parameter = [];
           parameter.fsAudio = srate;
           parameter.zeroPad = srate/10;
           [spec2plot,f,t] = stft(eval(variables2plot{p})',parameter);
           surf(t,f,abs(spec2plot));
           hold on; set(gcf,'renderer','zbuffer'); shading interp; view(0,90); axis tight; caxis([0 50])
           title(titles{p});
       end
       
       print(gcf, '-djpeg', strrep(outputfilename,'.wav','.jpg'));
       disp(['....saved figure for ',outputfilename]);
       %
       close gcf
end

 