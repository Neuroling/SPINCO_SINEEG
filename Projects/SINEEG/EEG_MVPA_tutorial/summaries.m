%% Gather results of MVPA
%------------------------
dirinput  = 'V:\spinco_data\SINEEG\analysis\mvpa';
cd (dirinput);
% read data 
load('Results_Infants_included_decode_within_SVM_22-Sep-2022_44205.mat')
DA = results.DA;

%% Get mean classification accuracy
means_1lv = mean(DA,[3 4],'omitnan');
means_2lv = mean(DA,[1 3 4],'omitnan');

%% PLOT 

plot(results.times,means_1lv); hold on; 
plot(results.times, means_2lv','color', 'black','lineWidth',2)
 



