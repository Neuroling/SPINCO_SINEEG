%% Gather results of MVPA
%------------------------
%dirinput  = 'V:\spinco_data\SINEEG\analysis\mvpa';
%cd (dirinput);
% read data 
load('Results_25subj_alpha_decode_within_SVM_11.10.2022_15.20.11.mat')
DA = results.DA;

%% Get mean classification accuracy
means_1lv = mean(DA,[3 4],'omitnan');
means_2lv = mean(DA,[1 3 4],'omitnan');

%% PLOT 

plot(results.times,means_1lv); hold on; 
plot(results.times, means_2lv','color', 'black','lineWidth',2)
 



