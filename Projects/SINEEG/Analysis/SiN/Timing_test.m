clear all 
close all 
%% 
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
EEG = pop_biosig('V:\spinco_data\SINEEG\SiN\Test_triggers.bdf', 'ref',73);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'gui','off'); 

EEG.data = EEG.data(1,:,:)/10000

%pop_eegplot( EEG, 1, 1, 1);
%EEG = eeg_checkset( EEG );


% 

for e=1:length(EEG.event)
    
    if contains(EEG.event(e).type,'101')
        disp('This')
        %EEG.event(e).latency =  EEG.event(e).latency-(0.08*EEG.srate)
        
    end
end

eeglab redraw
pop_eegplot( EEG, 1, 1, 1);