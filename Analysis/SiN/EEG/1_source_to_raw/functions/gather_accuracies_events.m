% =========================================================================
% Gather task accuracy 
% =========================================================================
% Author: G.FragaGonzalez
% Description:

% - Get accuracy of each target word within trial and add that to the event file
function gather_accuracies_events(EEG,expfile,newdiroutput) 

    filepath =  fullfile(expfile.folder, expfile.name);
    % Read data frame
    df = readtable(filepath,'Delimiter',',');

    % Exclude last row if the number of rows is more than 388
    if height(df) > 288
        df(end, :) = [];
    end
    if height(df) > 288
        error('The number of rows exceeds 388. Script terminated.');
    end

    % Recode to numeric to compute summary descriptives
    recodeMap = containers.Map({'True', 'False', 'NO_ANSW', 'TRUE', 'FALSE' }, [1, 0, NaN, 1, 0]);
    df.callSignCorrect = cellfun(@(x) num2cell(recodeMap(x)), df.callSignCorrect);
    df.colourCorrect = cellfun(@(x) num2cell(recodeMap(x)), df.colourCorrect);
    df.numberCorrect = cellfun(@(x) num2cell(recodeMap(x)), df.numberCorrect);

    %% Reshape set
    cols2melt = {'noise', 'block', 'levels', 'callSignCorrect', 'colourCorrect', 'numberCorrect'};
    
    % Reshape the table using the 'stack' function
    accuTable = stack(df, cols2melt, 'NewDataVariableName', 'value');
    % leave rows with accu values
    accuTable = accuTable(contains(string(accuTable.value_Indicator),'Correct'),:);

    %remove examples trials (which had a duration value =  nan)
    accuTable = accuTable(~isnan(accuTable.duration),:);
    
    %  Now we have a table that is three times the length of df - so every
    %  trial is represented three times. It also has two new columns: 
    %  one named 'value_indicator' which is 'callSignCorrect', 'colourCorrect' or 'numberCorrect'
    %  and a column named 'value' which is 1, 0 or NaN

    %%   reformat ? 
    df.callSignCorrect = cell2mat(df.callSignCorrect);
    df.colourCorrect = cell2mat(df.colourCorrect);
    df.numberCorrect = cell2mat(df.numberCorrect);

    %%
    %% SAVE EVENTS with accuracy 
    eventsTab.SAMPLES = cell2mat({EEG.event.latency})';
    eventsTab.VALUE = string({EEG.event.type})';
    eventsTab.DURATION = zeros(length(EEG.event),1);
    eventsTab.ACCURACY = strings(length(EEG.event),1);
    %
    eventsTab.ACCURACY = strings(length(EEG.event),1);
    eventsTab.RESPONSE_ITEM = strings(length(EEG.event),1);

    % Fill in responses
    value_list = ["111", "112", "113", "114","115", "116", "117", "118", "211", "212", "213", "214","215", "216", "217", "218","311", "312", "313", "314", "315", "316", "317", "318"];
    idxs_log = find(accuTable.value_Indicator == "callSignCorrect"); % getting the idxs in accuTable for callSignCorrect
    idxs_events = find(contains(eventsTab.VALUE,value_list)); % getting the idxs in eventsTab where the tigger code refers to a callSign
    trialsAccu = accuTable.value(idxs_log); % trialsAccu is now accuTable.value in rows where accuTable.value_Indicator is 'callSignCorrect'
                              % In python this would be:  trialsAccu = [ accuTable['value'][idx] for idx in len(accuTable) if accuTable['value_Indicator'][idx] == "callSignCorrect"]
    eventsTab.ACCURACY(idxs_events) = trialsAccu; % assigning the trialsAccu to the eventsTab ACCURACY column in the idx of idx_events
    eventsTab.RESPONSE_ITEM(idxs_events) = strrep(strrep(accuTable.mouseClickOnCall_clicked_name(idxs_log), "['", ""), "']", "");


    value_list = ["121", "122", "123", "124", "125", "126", "127", "128", "221", "222", "223", "224", "225", "226", "227", "228", "321", "322", "323", "324", "325", "326", "327", "328"];
    idxs_log = find(accuTable.value_Indicator == "colourCorrect");
    idxs_events = find(contains(eventsTab.VALUE,value_list));
    trialsAccu = accuTable.value(idxs_log);
    eventsTab.ACCURACY(idxs_events) = trialsAccu;
    eventsTab.RESPONSE_ITEM(idxs_events) = strrep(strrep(accuTable.mouseClickOnColour_clicked_name(idxs_log), "['", ""), "']", "");

    value_list = ["131", "132", "133", "134", "135", "136", "137", "138", "231", "232", "233", "234", "235", "236", "237", "238", "331", "332", "333", "334", "335", "336", "337", "338"];
    idxs_log = find(accuTable.value_Indicator == "numberCorrect");
    idxs_events = find(contains(eventsTab.VALUE,value_list));
    trialsAccu = accuTable.value(idxs_log);
    eventsTab.ACCURACY(idxs_events) = trialsAccu;
    eventsTab.RESPONSE_ITEM(idxs_events) = strrep(strrep(accuTable.mouseClickOnNumber_clicked_name(idxs_log), "['", ""), "']", "");


    events2write = struct2table(eventsTab);
    writetable(events2write,fullfile(newdiroutput,[EEG.setname,'_events_accu.tsv']),"FileType","text",'Delimiter', '\t')
    
end
