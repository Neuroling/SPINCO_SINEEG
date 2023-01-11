function DiN_pt01_preprocess_segment01(thisPath, theseSbj)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reads in EGI '.RAW' files from 'path/SUBJECT_ID/EEG_DATA/', performs some
% initial preprocessing, and stores and saves output in EEGLAB's '.set'
% format in 'path/DOWNSAMP/'.
% RAW files contain EEG recordings (sampled at 1kHz) of multiple tests.
%
% Inputs:
% - thisPath: see above
% - theseSbj: vector of subject IDs to convert to .set format
%       final set of subjects included = [4:6 8:10 12 14:19 21 22 25:30 32 33 35:36];
%
% Preprocessing steps carried out:
% 1. Import data
% 2. Add channel locations and measurement unit
% 3. Downsample (from 2kHz to 200Hz)
% 4. Filter (highpass: 0.1Hz, lowpass: 48Hz)
% 5. Remove line noise
% 6. Remove bad channels & data segments
% 7. Interpolate the removed channels
% 8. Re-reference to average
% ... continues in part 3 of preprocessing.
%
% This function calls functions from both the FieldTrip (Oostenveld, Fries,
% Maris, & Schoffelen, 2011) version 20210614, and EEGLAB (Delorme &
% Makeig, 2004) version 2020.0 toolboxes running under Matlab 2018b.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% poolSize = feature('GpuAllocPoolSizeKb', 0);
% turn off the pooling of memory

% add EEGLAB to path
eeglab;

nSbj = length(theseSbj);


try
    for subject = 1:nSbj
        sbj = theseSbj(subject);
        disp(' ');
        disp('********************************************************');
        disp(['                   SUBJECT ' num2str(sbj)]);
        disp('********************************************************');
        
        sbjDir = [thisPath 'SUBJECT_' num2str(sbj) '/EEG_DATA/'];
        files = dir(fullfile(sbjDir, '*.raw'));
        nParts = size(files,1);
        
        outDir = [sbjDir 'DOWNSAMPLED/'];
        mkdir(outDir);
        tmpDir = [outDir 'TEMPORARY/'];
        mkdir(tmpDir);
        
        % Signal was checked between the different .raw files. In most cases,
        % here we attempted to restore channels with bad signal. Therefore,
        % preprocessing is carried on each part file separately. Below we keep
        % a record of the channels interpolated at each segment.
        interpChans = cell([1 nParts]);
        
        for part = 1:nParts
            disp(' ');
            disp(['PART ' num2str(part)])
            
            %% 1. Import data
            % if no memory issue, just load (fread), otherwise need to use memory mapping
            % (https://ch.mathworks.com/help/matlab/import_export/overview-of-memory-mapping.html)
            try
                EEG = pop_fileio([sbjDir files(part).name],'dataformat','auto');
            catch
                EEG = pop_fileio([sbjDir files(part).name],'dataformat','auto','memorymapped','on');
            end
            EEG = eeg_checkset(EEG);
            eeglab redraw
            
            
            %% 2. add channel locations and measurement unit
            EEG = pop_chanedit(EEG,'load',{[thisPath 'GSN-HydroCel-129.sfp'],'filetype','sfp'},...
                'changefield',{132,'datachan',0});
            EEG.unit = 'uV';
            EEG = eeg_checkset(EEG);
            eeglab redraw
            
            
            %% 2. downsample
            EEG = pop_resample(EEG, 200);
            EEG = eeg_checkset(EEG);
            %         [ALLEEG, EEG] = eeg_store(ALLEEG,EEG, CURRENTSET);
            eeglab redraw
            
            
            %% 4. filter
            EEG = pop_eegfiltnew(EEG, 'locutoff',0.1);
            EEG = pop_eegfiltnew(EEG, 'hicutoff',48);
            EEG = eeg_checkset(EEG);
            eeglab redraw
            
            
            %% 5. Remove line noise
            % https://github.com/sccn/cleanline/blob/master/pop_cleanline.m
            EEG = pop_cleanline(EEG, 'Bandwidth',2,'ChanCompIndices',[1:EEG.nbchan],                  ...
                'SignalType','Channels','ComputeSpectralPower',true,             ...
                'LineFrequencies',50  ,'NormalizeSpectrum',false,           ...
                'LineAlpha',0.01,'PaddingFactor',2,'PlotFigures',false,          ...
                'ScanForLines',true,'SmoothingFactor',100,'VerboseOutput',1);
            %         [ALLEEG, EEG] = eeg_store(ALLEEG,EEG, CURRENTSET);
            eeglab redraw
            
            
            %% 6. Remove flatline channels, low-frequency drifts, noisy channels, short-time bursts, and incompletely repaird segments from the data.
            % https://github.com/sccn/clean_rawdata/blob/master/clean_artifacts.m
            
            % ... &
            %% 7. interpolate removed channels
            
            chanlocs = EEG.chanlocs;
            
            clear ALLEEG ans
            
            %         sampleThreshold = 50000; % try-catch does not work because of non-standard error message;
            %         % datasets need to be splitted for clean_artifacts to work.
            %         % a sample threshold needs to be hard-coded; could be higher or
            %         % lower depending on system memory
            %
            %         nSubParts = ceil(size(EEG.data,2) / sampleThreshold);
            %         %         thisEEGsubPart = cell([1 nSubParts]);
            %         intChans = cell([1 nSubParts]);
            %
            %         pop_saveset(EEG,'filename','EEG_TMP.set','filepath',tmpDir);
            %
            %         clear ans
            %
            %         if nSubParts > 1
            %             disp(['splitting dataset in ' num2str(nSubParts) ...
            %                 ' sub-parts and running clean_artifact on each before merging'])
            %
            %             for subPart = 1:nSubParts
            %                 disp(['Subject ' num2str(sbj) ', ' ...
            %                     'part ' num2str(part) '/' num2str(nParts) ', sub-part ' ...
            %                     num2str(subPart) '/' num2str(nSubParts) ':'])
            %
            %                 if subPart > 1
            %                     EEG = pop_loadset('filename','EEG_TMP.set','filepath',tmpDir);
            %                 end
            %
            %                 if subPart ~= nSubParts
            %                     thisEEGsubPart = pop_select(EEG, 'point', ...
            %                         [(subPart*sampleThreshold)-(sampleThreshold-1) subPart*sampleThreshold]);
            %                 else
            %                     thisEEGsubPart = pop_select(EEG, 'point', ...
            %                         [(subPart*sampleThreshold)-(sampleThreshold-1) EEG.pnts]);
            %                 end
            %
            %                 clear EEG ans
            %
            %                 thisEEGsubPart = clean_artifacts(thisEEGsubPart);
            %                 intChans{subPart} = setdiff({chanlocs.labels},{thisEEGsubPart.chanlocs.labels});
            %                 thisEEGsubPart = pop_interp(thisEEGsubPart, chanlocs, 'spherical');
            %
            %                 pop_saveset(thisEEGsubPart,'filename',...
            %                     ['EEG_part_' num2str(part) '_subpart_' num2str(subPart) '_tmp.set'],'filepath',tmpDir);
            %
            %                 if subPart > 1
            %                     clear ans
            %                     if subPart == 2
            %                         disp('merging subparts 1 and 2...');
            %                         previousEEGsubPart = pop_loadset('filename',...
            %                             ['EEG_part_' num2str(part) '_subpart_' num2str(subPart-1) '_tmp.set'],'filepath',tmpDir);
            %                         FULLEEG = pop_mergeset(previousEEGsubPart,thisEEGsubPart);
            %                         pop_saveset(FULLEEG,'filename',...
            %                             'EEG_updating.set','filepath',tmpDir);
            %                         intChansFull = union(intChans{subPart-1},intChans{subPart});
            %                         %                         EEG = eeg_checkset(FULLEEG);
            %                     elseif subPart > 2
            %                         disp(['merging subpart ' num2str(subPart) ' with previous ones...']);
            %                         FULLEEG = pop_loadset('filename',...
            %                             'EEG_updating.set','filepath',tmpDir);
            %                         FULLEEG = pop_mergeset(FULLEEG,thisEEGsubPart);
            %                         pop_saveset(FULLEEG,'filename',...
            %                             'EEG_updating.set','filepath',tmpDir);
            %                         intChansFull = union(intChansFull,intChans{subPart});
            %                         %                         EEG = eeg_checkset(FULLEEG);
            %
            %                         if subPart == nSubParts
            %                             EEG = pop_loadset('filename','EEG_TMP.set','filepath',tmpDir);
            %                             FULLEEG.newEvent = FULLEEG.urevent;
            %                             FULLEEG.urevent = EEG.urevent;
            %                             EEG = FULLEEG;
            %                             pop_saveset(EEG,'filename',...
            %                                 'EEG_full.set','filepath',tmpDir);
            %                         end
            %                     end
            %                     clear FULLEEG thisEEGsubPart previousEEGsubPart ans
            %                 end
            %             end
            %             interpChans{part} = intChansFull;
            %         else
            EEG = clean_artifacts(EEG);
            interpChans{part} = setdiff({chanlocs.labels},{EEG.chanlocs.labels});
            EEG = pop_interp(EEG, chanlocs, 'spherical');
            %         end
            
            
            
            %% 8. re-reference to average
            EEG = pop_reref(EEG,[]);
            %         [ALLEEG, EEG] = eeg_store(ALLEEG,EEG, CURRENTSET);
            EEG = eeg_checkset(EEG);
            eeglab redraw
            
            pop_saveset(EEG,'filename',['sbj_' num2str(sbj) '_part_' ...
                num2str(part) '_downsampled.set'],'filepath',outDir);
            
            clear EEG ALLEEG
            
        end
        save([outDir 'interpChans.mat'],'interpChans')
        % feature('GpuAllocPoolSizeKb', poolSize);
    end
    
catch
    save(['wrkspc_sbj_' num2str(sbj) '_up2part_' num2str(part) '_' date '.mat']);
end

