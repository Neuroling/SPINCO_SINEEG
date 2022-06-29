clear all

%% Loading data
 multipic = readtable('C:\Users\gfraga\Downloads\Neuroling_SINON_stimuli', 'Sheet',1);
 subtlex = readtable('C:\Users\gfraga\Downloads\Neuroling_SINON_stimuli', 'Sheet',2);
 clearpond = readtable('C:\Users\gfraga\Downloads\Neuroling_SINON_stimuli', 'Sheet',3);
 wuggy = readtable('C:\Users\gfraga\Downloads\Neuroling_SINON_stimuli', 'Sheet',4);

%% Merge datasets
tbl1 = join(multipic,subtlex,'keys','ITEM'); % assuming the variable ITEM is common to all sets
merged_database = join(tbl1,clearpond,'keys','ITEM');

%% Remove duplicate names 
merged_database.Word = merged_database.Word_clearpond;
[uniqueName i j] = unique(merged_database.Word,'first');
merged_clean = merged_database(i,:);

%% Wuggy - select words based on ned1_diff (value closest to zero)
wuggy.Word = erase(wuggy.Word, '-');
% loop thru unique wuggy words 
wordsinwuggy = unique(wuggy.Word);

indices = zeros(length(wordsinwuggy),1);
for i=1:length(wordsinwuggy)
    
    idx = find(ismember(wuggy.Word,wordsinwuggy(i)));
    % Find index of minimum ned1_diff (closest to zero)
    [minval, minidx] = min(abs(wuggy.Ned1_Diff(idx)));
    % add to vector with all selected indices 
    indices(i) = idx(minidx);
end
wuggy_selected = wuggy(indices,:); 

%% Add to merged set without duplicates 

merged_clean = outerjoin(merged_clean,wuggy_selected,'Type','Left','MergeKeys',true);

%% 
%writetable(wuggy_selected,"C:\Users\gfraga\scripts_neulin\SINON_experiment\Wuggy_selected.xls")
%writetable(merged_clean,"C:\Users\gfraga\scripts_neulin\SINON_experiment\Merged_clean.xls")
