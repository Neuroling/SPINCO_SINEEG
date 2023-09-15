%% script for behavioural accuracy

clear all; close all;

%% find files
thisDir = matlab.desktop.editor.getActiveFilename;
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
taskID = 'task-sin';
dirinput = fullfile(baseDir, 'Data','SiN','rawdata') ;

% find data 
files = dir([dirinput,filesep,'*',filesep,taskID, filesep,'beh',filesep,'*','.csv']); 

%%
f= 1
fileinput = fullfile(files(f).folder, files(f).name); 
ds=datastore(fileinput,'Type','tabulartext','FileExtensions','.csv','TextType','string');
ds.SelectedVariableNames= {'voice','words','levels','trigger_call',...
    'trigger_col','trigger_num','block','callSignCorrect','colourCorrect',...
    'numberCorrect','mouseClickOnCall_clicked_name',...
    'mouseClickOnColour_clicked_name','mouseClickOnNumber_clicked_name'};
preview(ds);
T=readall(ds);
T2=table2array(T);
data=T2(5:end-1,:);
%%
AT=[];
AT(1:3,1)=c('correctCallNV1','correctColNV1','correctNumNV1')
AT(1:3,2)=sum(data(:,7)=='NV1'&data(:,8:10)=='True')

%%
sum(data(:,7)=='NV2'&data(:,8:10)=='True')/sum(data(:,7)=='NV2')
sum(data(:,7)=='NV2'&data(:,8:10)=='True')
sum(data(:,7)=='SSN1'&data(:,8:10)=='True')/sum(data(:,7)=='SSN1')
sum(data(:,7)=='SSN1'&data(:,8:10)=='True')
sum(data(:,7)=='SSN2'&data(:,8:10)=='True')/sum(data(:,7)=='SSN2')
sum(data(:,7)=='SSN2'&data(:,8:10)=='True')