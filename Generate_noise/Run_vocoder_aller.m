clear all ; 
%%
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
makeplots = 0;
% paths and files 
dirinput =      'V:\spinco_data\AudioRecs\LIRI_voice_DF\segments\Take1_all_trimmed\trim_loudNorm-23LUFS';
diroutput =     'V:\spinco_data\AudioRecs\LIRI_voice_DF\segments\Take1_all_trimmed\trim_loudNorm-23LUFS_NV3';
cd (dirinput)
audiofiles =      dir([dirinput, '\*.wav']);
audiofiles =      fullfile(dirinput, {audiofiles.name});
mkdir(diroutput)
% Filter settings (butterworth filter lower and upper cut freqs in Hz)
 
 
% Parameters for Vocoding function 
exc =           'noise' ; 
mapping=        'n'; 
filters =       'log'; % greenwood
EnvelopeExtractor = 'half'; 
smooth=          30 ; 
nCh =           64; 
MinFreq =       70;
MaxFreq =        5000;
% Degradation levels
target_proportions = [0.2, 0.4, 0.6, 0.75, 0.8, 0.85, 0.9, 0.95, 1];
 
 
%% Call vocoder function (save in structure array)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% read signals
[signals, freqs] = cellfun(@(x) audioread(x), audiofiles, 'UniformOutput',0);

% Loop and vocode for each degradation level
nvStimuli = struct(); 
for i = 1:length(signals)     
    [pathstr, name , ext] = fileparts(audiofiles{i});
    nvStimuli(i).filename = name;
    nvStimuli(i).srate = freqs{i};
    
    tmp = signals{i};
    tmp = tmp(:,1);
    nvStimuli(i).ursignal = tmp;
    
    
   for ii = 1:length(target_proportions)       
       nvStimuli(i).vocoded(ii).filename= strrep([diroutput,'\NV_',name,'_',num2str(target_proportions(ii)),'p',ext],'\\','\');
       nvStimuli(i).vocoded(ii).proportions = target_proportions(ii);
       %call function 
       morph = target_proportions(ii); 
       InputSignal =  nvStimuli(i).ursignal;
       Srate = nvStimuli(i).srate;
       nvStimuli(i).vocoded(ii).nvsignal =  vocode_aller(nCh,morph,smooth,InputSignal,Srate,MinFreq,MaxFreq);
       
       disp(['I just vocoded:  NV_',name,'_',num2str(target_proportions(ii)),'proportions'])        
       
      %Normalize to perceived loudness            
       target_loudnessDB = -23;
       nvStimuli(i).vocoded(ii).nvsignal =  normalize_by_perceivedLoudness(nvStimuli(i).vocoded(ii).nvsignal', nvStimuli(i).srate,target_loudnessDB);
       
   end
    
end
srate =freqs{1}
%% Saving vododed audio 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 cd (diroutput)

% Audio
for i = 1:length(nvStimuli)
   for ii = 1:length(nvStimuli(i).vocoded)       
       
       % save to wav file  (output commented )
        text = ['Noise vocoded with ',num2str(nvStimuli(i).vocoded(ii).proportions),' p, normalized for loudness -23 LUFS']; 
        audiowrite(nvStimuli(i).vocoded(ii).filename, nvStimuli(i).vocoded(ii).nvsignal,srate,'BitsPerSample',24,'comment',text);
        disp(['...saved ',nvStimuli(i).vocoded(ii).filename]);
   end
    
end

%% Summary figures
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if makeplots==1
    for i = 1:length(nvStimuli)
       for ii = 1:length(nvStimuli(i).vocoded)       
                   %%% Save summary plot 
                   footnote = ['Vocoder_2022 run for ', nvStimuli(i).filename,' (srate: ',num2str(nvStimuli(i).srate),' Hz) with arguments: exc (', exc, '), mapping (',mapping, '), filters(',...
                       filters ,'), min-max freqs(',num2str(MinFreq),'-',num2str(MaxFreq),'), proportions (',num2str(target_proportions(ii)),'), smooth (',num2str(smooth),')'];

                   signal_nv2plot = nvStimuli(i).vocoded(ii).nvsignal;
                   original2plot = nvStimuli(i).ursignal';
                   variables2plot = {'original2plot','signal_nv2plot'};
                   %
                   figure ('position', [1 1 800 800],'color','white');
                   annotation('textbox', [0, 0.075, 1, 0], 'string',footnote)
                   % Amplitude x  time
                   titles = {'original','signal NV'};
                   for p = 1:2
                       subplot(3,2,p);
                       plot(eval(variables2plot{p}))
                       title(titles{p});  ylabel('Amplitude (a.u.)');  xlabel('Time (ms)');
                   end
                   % Spectral plots
                   titles = {'LTAS original ','LTAS signal NV '};
                   for p = 1:2
                       subplot(3,2,2+p);
                       iosr.dsp.ltas(eval(variables2plot{p}),srate,'noct',6,'graph',true,'units','none','scaling','max0','win',srate/10);  % requires the IoSR Matlab Toolbox
                       xline(50, '--k'); xline(5000, '--k');
                       title(titles{p});
                   end
                   % Surf plots
                   titles = {'Spectrogram original', 'Spectrogram signal NV'};
                   for p = 1:2
                       subplot(3,2,4 + p);
                       parameter = [];
                       parameter.fsAudio = srate;
                       parameter.zeroPad = srate/10;
                       [spec2plot,f,t] = stft(eval(variables2plot{p})',parameter);
                       surf(t,f,abs(spec2plot));
                       hold on; set(gcf,'renderer','zbuffer'); shading interp; view(0,90); axis tight; caxis([0 0.2]); ylim([0 10000])
                       title(titles{p});
                   end
                   outputfilename = nvStimuli(i).vocoded(ii).filename;
                   print(gcf, '-djpeg', strrep(outputfilename,'.wav','.jpg'));
                   disp(['....saved figure for ',outputfilename]);
                   %
                   close gcf
      end
    end
end
 