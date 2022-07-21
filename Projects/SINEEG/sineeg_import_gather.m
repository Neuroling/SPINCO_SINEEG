clear all
% Input settings
dirinput = 'W:\share_gfraga\SINEEG\Data\Pilot_October_2021';
diroutput = 'W:\share_gfraga\SINEEG\Analysis\Pilot_October_2021';


% Find files 
cd(dirinput)

measurement = 'Measurement 11' ;
filename = 'processed.vhdr';

% Import eeg 
EEG = pop_loadbv([dirinput, '\', measurement,'\'], filename,[], []);
EEG.setname = ['eegset_',extractBefore(filename,'.vhdr')];

newsrate = 200;
for i=1:length(EEG.event)
        EEG.event(i).latency = EEG.event(i).latency / EEG.srate * newsrate;
end;
EEG.srate = newsrate

%load channel location 
EEG =pop_chanedit(EEG, 'load',{'W:\\share_gfraga\\SINEEG\\sample32chs.sph','filetype','sph'});
EEG = eeg_checkset( EEG );
%[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
eeglab redraw

