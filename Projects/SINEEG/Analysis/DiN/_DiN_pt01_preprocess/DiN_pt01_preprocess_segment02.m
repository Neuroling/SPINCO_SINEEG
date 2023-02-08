function DiN_pt01_preprocess_segment02(thisPath, theseSbj)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function simply merges the .set files obtained as result of the
% previous step and saves the data as '...merged.set'. After this step, it
% is possible to remove the intermediate files obtained previously.
%
% Inputs:
% - thisPath: path to original (.raw) files
% - theseSbj: vector of subject IDs
%
% This function calls functions from both the EEGLAB (Delorme & 
% Makeig, 2004) version 2020.0 toolboxe running under Matlab 2018b.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

eeglab;

nSbj = length(theseSbj);

for subject = 1:nSbj
    sbj = theseSbj(subject);
    disp(' ');
    disp('********************************************************');
    disp(['                   SUBJECT ' num2str(sbj)]);
    disp('********************************************************');
    
    sbjDir = [thisPath 'SUBJECT_' num2str(sbj) '/EEG_DATA/'];
    inDir = [sbjDir 'DOWNSAMPLED/'];
    
    files = dir(fullfile(inDir, '*downsampled.set'));
    nParts = size(files,1);

    backupEvents = cell([1 nParts]);
    for part = 2:nParts
        if part == 2
            OUTEEG1 = pop_loadset('filename',files(part-1).name,'filepath',inDir);
%             for i = 1:length(OUTEEG1.event)
%                 OUTEEG1.event(i).urevent = OUTEEG1.urevent(i); 
%             end
            OUTEEG2 = pop_loadset('filename',files(part).name,'filepath',inDir);
%             for i = 1:length(OUTEEG2.event)
%                 OUTEEG2.event(i).urevent = OUTEEG2.urevent(i); 
%             end
            FULLEEG = pop_mergeset(OUTEEG1,OUTEEG2);
            backupEvents{part-1}=OUTEEG1.event;
            backupEvents{part}=OUTEEG2.event;
            clear OUTEEG1 OUTEEG2
        else
            OUTEEG = pop_loadset('filename',files(part).name,'filepath',inDir);
            FULLEEG = pop_mergeset(FULLEEG,OUTEEG);
            backupEvents{part}=OUTEEG.event;
            clear OUTEEG
        end 
    end
    
%     [ALLEEG, EEG, CURRENTSET] = eeg_store(ALLEEG,FULLEEG);
    FULLEEG.setname = ['sbj_' num2str(sbj) '_downsampled_merged'];
    EEG = FULLEEG;
    clear FULLEEG
    pop_saveset(EEG,'filename',[EEG.setname '.set'],'filepath',inDir);
    eeglab redraw
       
    save([inDir 'backupEvents.mat'],'backupEvents');
end
end