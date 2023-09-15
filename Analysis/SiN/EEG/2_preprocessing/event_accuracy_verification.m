%script to check if the .tsv files read the accuracy correctly from the
%.csv file

clear all; close all;

%%
% thisDir = mfilename('fullpath')
% above somehow returns 'C:\Users\User\AppData\Local\Temp\Editor_rlgcp\LiveEditorEvaluationHelperE1105333385'
% to fix #abcde
thisDir = matlab.desktop.editor.getActiveFilename;
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
    sprintf("now checking subject nr %d",f)
    errormarker = 0;
    for i= 1:length(table2)
        if isnan(cell2mat(table2(i,4)))
            continue
        else
            if extract(string(table2(i,2)),3) == extract(string(table2(i,5)),strlength(string(table2(i,5))))
                %if the answ and the stim match
                if string(table2(i,4)) == '1' %if the accuracy says it is true
                    continue
                else
                    sprintf("false positive at %i in subj nr %d",i,f)
                    errormarker = errormarker+1;
                end
            else %if ans and stim do not match
                if string(table2(i,4)) == '0'  %if accuracy says it is wrong
                    continue
                else
                    sprintf("false negative at %i in subj nr %d",i,f)
                    errormarker = errormarker+1;
                end
            end
        end
    end
    sprintf("errors found in subject nr %d: %d",f,errormarker)
end
