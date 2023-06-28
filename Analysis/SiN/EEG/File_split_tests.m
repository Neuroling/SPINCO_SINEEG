clear all
close all 

eeglab nogui 
fileinput = 'p004_task.bdf';
EEG = pop_biosig(fileinput,  'channels', 1:72, 'importannot','off','ref', 48, 'refoptions',{ 'keepref' 'on' }, 'rmeventchan','on');
%% data select 
%chanLocsFile = 'V:\Projects\Spinco\SINEEG\Data\SiN\_acquisition\_electrodes\Biosemi_73ch_EEGlab.elp';
%EEG = pop_chanedit(EEG,'load',chanLocsFile); 
segment_t0 = EEG.event(8).latency - (1*EEG.srate) ;
segment_t1 = EEG.event(8).latency + (240*EEG.srate) + (1*EEG.srate);

EEG = pop_select( EEG, 'point',[segment_t0 segment_t1]  );

%% export and save 
EEG = eeg_checkset(EEG)

fileoutput = strrep(fileinput,'.bdf','_exp72_sel.bdf');
pop_writeeeg(EEG,fileoutput,'TYPE','BDF');


%% read exported 
% clear EEG
EEG = pop_biosig(fileoutput, 'importannot','off','ref', 48, 'refoptions',{ 'keepref' 'on' }, 'rmeventchan','off');
%%
pop_eegplot( EEG, 1, 1, 1);

% 
%inf  = openbdf(fileoutput)
%inf.Head.PhysMin
%inf.Head.DigMin