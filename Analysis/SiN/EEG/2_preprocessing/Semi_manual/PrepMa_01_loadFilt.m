clear all; close all; 

% Preprocessing step 01 
% ======================================================================
% - Remove audiochannel 
% - Basic Filters
% - Downsample 

% Paths
thisDir = mfilename('fullpath');
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
taskID = 'task-sin';
pipeID = 'pipeline-semiManual';
derivativesFolder = 'derivatives_exp2-unalignedTriggers';
dirinput = fullfile(baseDir, 'Data','SiN',derivativesFolder,pipeID,taskID) ;
diroutput = dirinput;

% subjects = {'s201','s202','s203','s204'};

%% find data 
files = dir([dirinput,filesep,'**',filesep,'*',taskID,'.set']); 

%% loop thru files 
for f = 1:length(files)

    % input file 
    fileinput = fullfile(files(f).folder, files(f).name); 

    %% preprocessing 
    % load set  
    [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
    EEG = pop_loadset('filename',fileinput);
    ursetname = EEG.setname;
    
    %Exclude mastoids
    EEG = pop_select( EEG, 'rmchannel',{'EXT5','EXT6'});

    % Filter 
    % highpass (aggressive for ICA) 
    EEG = pop_eegfiltnew(EEG, 'locutoff',1); %1 hz high pass filter 

    %Notch
    EEG = pop_cleanline(EEG, 'bandwidth',2,'chanlist',[],'computepower',1,'linefreqs',50,'newversion',0,'normSpectrum',0,'p',0.01,'pad',2,'plotfigures',0,'scanforlines',0,'sigtype','Channels','taperbandwidth',2,'tau',100,'verb',1,'winsize',4,'winstep',1);

    %re reference to average 
    EEG = pop_reref( EEG, [],'exclude',[65:70] );

    %% save before downsampling
    newsetname = [ursetname, '_filt_avgRef'];
    pop_saveset (EEG, newsetname,files(f).folder);

    %% Downsample 
    EEG = pop_resample(EEG, 128);

    %% Save 
    newsetname = [ursetname, '_filt_avgRef_ds'];
    pop_saveset (EEG, newsetname,files(f).folder);

end

