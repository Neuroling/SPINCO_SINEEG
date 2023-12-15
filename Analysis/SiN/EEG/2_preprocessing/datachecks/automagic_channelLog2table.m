%% Script to save the automagic channel logs of each subj into a single df
clear all; close all;
save = 1; % set to 1 to save the output

%%

chanLabels = readtable('V:\Projects\Spinco\SINEEG\Data\SiN\_acquisition\_electrodes\Biosemi_71ch_EEGlab_xyz.tsv',"Delimiter",'\t','FileType','delimitedtext');
chanLabels = chanLabels.Electrode; 
thisDir = mfilename('fullpath');
% if above returns a temp file, use the line below instead
% thisDir = matlab.desktop.editor.getActiveFilename;

%% Set Dirs
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
taskID = 'task-sin';
dirinput = fullfile(baseDir, 'Data','SiN','derivatives','pipeline-01', 'task-sin_preproc') ;
%filenameOutput 
% find data 
files = dir([dirinput,filesep,'*',filesep,'*','p_s0','*',taskID,'.mat']); 

%% create empty struct
%array=['file','badChans','n_interpolated','reject_components', 'n_rejC'];
data = struct('file',[],'subjID',[],'n_interpolated',[],'autoBadChans',[],'n_rejectedComponents',[],'rejectedComponents',[]);
data.file=num2str(data.file);
data.subjID=num2str(data.subjID);
data.n_interpolated=num2cell(data.n_interpolated);
data.autoBadChans=num2str(data.autoBadChans);
data.n_rejectedComponents=num2cell(data.n_rejectedComponents);
data.rejectedComponents=num2str(data.rejectedComponents);

dataTemp= struct('autoBadChansTemp',[],'rejectedComponentsTemp',[]);
dataTemp.autoBadChansTemp=num2cell(dataTemp.autoBadChansTemp);
dataTemp.rejectedComponentsTemp=num2cell(dataTemp.rejectedComponentsTemp);

%% read data and fill struct
for f = 1:length(files)
    fileinput = fullfile(files(f).folder, files(f).name);
    load(fileinput, 'automagic');
    data.file{f}=fileinput;
    data.subjID{f}=files(f).name(4:7);
    data.n_interpolated(f)={length(automagic.tobeInterpolated)};
    
    badchans = chanLabels(automagic.autoBadChans)';
    badchans = sprintf('%s,',badchans{1:end})
    badchans = badchans(1:end-1)
    data.autoBadChans{f}= badchans  
    
    %    dataTemp.autoBadChansTemp(f)={automagic.autoBadChans};
    % tmp = sprintf('%.0f, ',dataTemp.autoBadChansTemp{f});
    % data.autoBadChans{f}= tmp(1:end-2);
    data.n_rejectedComponents(f)={length(automagic.iclabel.rejectComponents)};
    dataTemp.rejectedComponentsTemp(f)={automagic.iclabel.rejectComponents}; 
	data.rejectedComponents{f}=sprintf('%.0f, ',dataTemp.rejectedComponentsTemp{f});
	tmp = data.rejectedComponents{f};
	data.rejectedComponents{f} = tmp(1:end-2);
end


%% transpose the struct and convert to table
data.file=transpose(data.file);
data.subjID=transpose(data.subjID);
data.n_interpolated=transpose(data.n_interpolated);
data.autoBadChans=transpose(data.autoBadChans);
data.n_rejectedComponents=transpose(data.n_rejectedComponents);
data.rejectedComponents=transpose(data.rejectedComponents);
table = struct2table(data);

%% save table
if save == 1
    writetable(table, fullfile(dirinput,'automagic_chanLogs.csv'));
    sprintf('file saved!')
else
    sprintf("file not saved because save != 1")
end

