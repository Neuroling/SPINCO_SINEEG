
%% Morlet wavelet
srate = 1000;
time = -2:1/srate:2;
frex = 10; 
% complex sine wave 
sine_wave = exp(1i*2*pi*frex.*time);
% gaussian window
s = 3/(2*pi*frex); %stdev of the Gaussian
gaus_win = exp( (-time.^2)./ (2*s^2));

%now make the wavelet 
cmw = sine_wave .*gaus_win


% plot 
%figure(1),clf
subplot(211)
plot(time,real(cmw))
subplot(212)
plot(time,imag(cmw))
%%
figure(2),clf
plot3(time,real(cmw),imag(cmw),'linew',3)
axis image 
rotate3d









