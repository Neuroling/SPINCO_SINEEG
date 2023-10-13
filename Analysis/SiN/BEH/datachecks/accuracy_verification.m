%% script to check if the accuracy in the psychopy output is reported correctly
% The for & if loops do the following for each participant, for each trial and for
% each stimulus (call, colour and number):
% First: Skip this stimulus if no answer was given
% Second: check if the number in response column matches the number in the stimulus 
%       column (meaning if the response is correct)
% Third: Check if the accuracy report correctly states "True" if the
%       response and stimulus match and "False" if they do not
% Fourth:  If the above is not true, gives an error message specifying stimulus, row, and subject

%% 
%thisDir = mfilename('fullpath');
thisDir = matlab.desktop.editor.getActiveFilename;
baseDir = char(thisDir(1:regexp(thisDir,'Scripts')-1));
taskID = 'task-sin';
dirinput = fullfile(baseDir, 'Data','SiN','rawdata') ;

% find data 
files = dir([dirinput,filesep,'*',filesep,taskID, filesep,'beh',filesep,'*','.csv']); 

%%
for f = 1:length(files)
    fileinput = fullfile(files(f).folder, files(f).name); 
    table=readcell(fileinput);

    % Below: would be better to choose the relevant columns based on name
    % instead of index
    table2=table(:,[2,3,4,13,14,15,122,123,124,189,198,207]);
    sprintf("now checking %s",files(f).name)

    for i=6:length(table2)-1 % starting at row 6 because first 5 are practise trials
        if string(table2(i,7)) ~= 'NO_ANSW' % skip if there is no answer
            if extract(string(table2(i,4)),3) == extract(string(table2(i,10)),7)
                if string(table2(i,7)) == 'True' %and if the accuracy says it is true
                    continue
                else
                    sprintf('error in call in row %d in file %s',i,files(f).name)
                end
            else %if the ans is false
                if string(table2(i,7)) == 'False' %and if the accuracy says it is false
                    continue
                else
                    sprintf('error in call in row %d in file %s',i,files(f).name)
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
                    sprintf('error in Color in row %d in file %s',i,files(f).name)
                end
            else %if the ans is false
                if string(table2(i,8)) == 'False' %and if the accuracy says it is false
                    continue
                else
                    sprintf('error in Color in row %d in file %s',i,files(f).name)
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
                    sprintf('error in number in row %d in file %s',i,files(f).name)
                end
            else %if the ans is false
                if string(table2(i,9)) == 'False' %and if the accuracy says it is false
                    continue
                else
                    sprintf('error in number in row %d in file %s',i,files(f).name) 
                end
            end
        else
            continue
        end
    end
end