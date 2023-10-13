% script to check if the accuracy reports in the .tsv files are correct.

% By checking first if the number in "RESPONSE_ITEM" (which indicates which
% response was given) matches the last number of the trigger in the "VALUE"
% column (which indicated which stimulus was presented), and then checking 
% whether the "ACCURACY" column states True ("1") if they match and 
% "0" if they do not match. It gives an error if the ACCURACY column
% reports a mismatch as True or a match as False


clear all; close all;

%%
thisDir = mfilename('fullpath');
% if above returns a temp file, use the line below instead
% thisDir = matlab.desktop.editor.getActiveFilename;
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
taskID = 'task-sin';
dirinput = fullfile(baseDir, 'Data','SiN','rawdata') ;

%% find data 
files = dir([dirinput,filesep,'*',filesep,taskID, filesep,'eeg',filesep,'*','accu.tsv']); 

%%
for f = 1:length(files)
    
    fileinput = fullfile(files(f).folder, files(f).name); 
    table=readtable(fileinput,'FileType','text','Delimiter','\t');
    table2 = table2cell(table);
    sprintf("now checking %s",files(f).name)
    errormarker = 0;
    for i= 1:length(table2)
        if isnan(cell2mat(table2(i,4)))
            continue % skip rows where the ACCURACY column is nan, since those are other triggers
        else
            if extract(string(table2(i,2)),3) == extract(string(table2(i,5)),strlength(string(table2(i,5))))
                %if the answ and the stim match
                if string(table2(i,4)) == '1' %if the accuracy says it is true
                    continue
                else
                    sprintf("ERROR: false positive at %i in subj nr %d",i,f)
                    errormarker = errormarker+1;
                end
            else %if ans and stim do not match
                if string(table2(i,4)) == '0'  %if accuracy says it is wrong
                    continue
                else
                    sprintf("ERROR: false negative at %i in subj nr %d",i,f)
                    errormarker = errormarker+1;
                end
            end
        end
    end
    %sprintf("errors found in subject nr %d: %d",f,errormarker)
end
