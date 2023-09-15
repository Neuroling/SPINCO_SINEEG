%% script to check if the accuracy in the psychopy output is reported correctly

%thisDir = mfilename('fullpath');
thisDir = matlab.desktop.editor.getActiveFilename;
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
taskID = 'task-sin';
dirinput = fullfile(baseDir, 'Data','SiN','rawdata') ;

% find data 
files = dir([dirinput,filesep,'*',filesep,taskID, filesep,'beh',filesep,'*','.csv']); 

%%
for f= 1:length(files)
    fileinput = fullfile(files(f).folder, files(f).name); 
    table=readcell(fileinput);

    
    table2=table(:,[2,3,4,13,14,15,122,123,124,189,198,207]);
    % emptyCol=cell(length(table2),3)
    % table3 = table2
    f

    for i=6:length(table2)-1
        if string(table2(i,7)) ~= 'NO_ANSW'
            if extract(string(table2(i,4)),3) == extract(string(table2(i,10)),7) %If the answ is true
                if string(table2(i,7)) == 'True' %and if the accuracy says it is true
                    continue
                else
                    'error call'
                    i
                    f
                end
            else %if the ans is false
                if string(table2(i,7)) == 'False' %and if the accuracy says it is false
                    continue
                else
                    'error call'
                    i
                    f
                end
            end
        else
            continue
        end
        if string(table2(i,8)) ~= 'NO_ANSW'
            if extract(string(table2(i,5)),3) == extract(string(table2(i,11)),9) %If the answ is true
                if string(table2(i,8)) == 'True' %and if the accuracy says it is true
                    continue
                else
                    'error col'
                    i
                    f
                end
            else %if the ans is false
                if string(table2(i,8)) == 'False' %and if the accuracy says it is false
                    continue
                else
                    'error col'
                    i
                    f
                end
            end
        else
            continue
        end
        if string(table2(i,9)) ~= 'NO_ANSW'
            if extract(string(table2(i,6)),3) == extract(string(table2(i,12)),9) %If the answ is true
                if string(table2(i,9)) == 'True' %and if the accuracy says it is true
                    continue
                else
                    'error num'
                    i
                    f
                end
            else %if the ans is false
                if string(table2(i,9)) == 'False' %and if the accuracy says it is false
                    continue
                else
                    'error num'
                    i
                    f
                end
            end
        else
            continue
        end
    end
end