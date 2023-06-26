eeglab nogui 


fileinput = 'V:\Projects\Spinco\SINEEG\Data\SiN\raw\p004\p004_task.bdf';
EEG = pop_biosig(fileinput, 'importannot','off','ref', 48, 'refoptions',{ 'keepref' 'on' }, 'rmeventchan','off');

%% RESTING-STATE PRE-TASK
%=================================
splits = struct('segment_name', {'task-rest-pre','task-rest-post'},...
                'segment_duration', {240,240},...% duration in seconds 
                'onset_trigger',{8, 9},...
                'head', {1 ,1},...% how many seconds before onset trigger  
                'tail',{1,1}); % how many seconds after offset
%
%for i = 1:length(splits)
for i = 2
    eeglab nogui
    EEG = pop_biosig(fileinput, 'importannot','off','ref', 48, 'refoptions',{ 'keepref' 'on' }, 'rmeventchan','off');

    % Find resting state before task: 
    triggerIdx = find(cell2mat({EEG.event(:).type})== splits(i).onset_trigger);
    
    if length(triggerIdx) ~= 1    
        error (['[error] It seems you have more than one event with code ', num2str(splits(i).onset_trigger), '. Check why']) 
    else 

       % Find data point to the relevant event leaving a couple of seconds before and after
       segment_t0 = EEG.event(triggerIdx).latency - (splits(i).head*EEG.srate) ;
       segment_t1 = EEG.event(triggerIdx).latency + (splits(i).segment_duration*EEG.srate) + (splits(i).tail*EEG.srate);

       % select data    
        EEG = pop_select( EEG, 'point',[segment_t0 segment_t1]  );

        % write bdf
        fileoutput = strrep(fileinput,'task.bdf',[splits(i).segment_name,'.bdf']);   
        pop_writeeeg(EEG,fileoutput,'TYPE','BDF');

    end
end
%% 
filename = {'p004_task.bdf','p004_task-rest-pre.bdf','p004_task-rest-post.bdf'};

for f = 1:length(filename)
    fileinput=filename{f}
    s = openbdf(fileinput);
    disp([ num2str(s.Head.PhysMin(74)),' for ' fileinput] )

end 