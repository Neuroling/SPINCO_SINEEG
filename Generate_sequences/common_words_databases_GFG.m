clear all

%% Loading data
 multipic = readtable('Y:\Neuroling_SINON_stimuli.xlsx', 'Sheet','Multipic');
 subtlex = readtable('Y:\Neuroling_SINON_stimuli.xlsx', 'Sheet','Subtlex');
 clearpond = readtable('Y:\Neuroling_SINON_stimuli.xlsx', 'Sheet','Clearpond');
 wuggy = readtable('Y:\Neuroling_SINON_stimuli.xlsx', 'Sheet','Wuggy');
 wuggy_selected_alt = readtable('Y:\Neuroling_SINON_stimuli.xlsx', 'Sheet','Wuggy_selected_alt');
 
 
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
tbl2merge = merged_clean(ismember(merged_clean.Word,wuggy_selected_alt.Word),:);
ismember(merged_clean.Word,wuggy_selected_alt.Word)
allmerged = join(tbl2merge,wuggy_selected_alt,'keys','Word');

writetable(allmerged,"C:\Users\gfraga\scripts_neulin\SINON_experiment\all_merged.xls")
%% 
%writetable(wuggy_selected,"C:\Users\gfraga\scripts_neulin\SINON_experiment\Wuggy_selected.xls")

