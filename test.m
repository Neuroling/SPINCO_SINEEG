%%

 addpath('V:\gfraga\scripts_neulin\Generate_noise\functions')

 nchs = 1:10;
for i=1:length(nchs);
    nChannels=nchs(i);
    [lower1,center,upper1]=greenwud(nChannels,50,8000);
    dif = upper1-lower1;
    difs = sum(dif)
    
 plot(difs,'-o'); hold on;
end