%% 
load('Adults_all.mat')

plot(times, mean(X,3))
%%
%% 
load('Adults_all.mat')

channel = string(1:29);
ch = str2double(channel(1));
data = squeeze(mean(X(:,:,:),3));



