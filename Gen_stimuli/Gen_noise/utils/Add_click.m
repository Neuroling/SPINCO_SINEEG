dirinput = 


%% 


fs = 48000;
f = 200;
dur = 1;
t = 0:1/fs:dur-1/fs;
y = sin(2*pi*f*t);

y=y*0.7;
y = [ones(1,100),y]

audiowrite('V:\spinco_data\AudioGens\click_beep.wav',y,fs) 