%% Quick aid for checking the audio recordings
%-----------------------------------------------------
% Loop thru wav files, button press log 1 = good; 0 = bad; 2= undecided
% Enter rater name, save output 
addpath('C:\Users\gfraga\Documents\MATLAB\')
addpath('C:\Program Files\MATLAB\R2021a\toolbox\MATLAB_TSM-Toolbox_2.03')% tool for plot
dirinput= 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\macro-output';
diroutputOK = 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\good';
diroutputBAD = 'V:\spinco_data\Audio_recordings\LIRI_voice_DF\segments\bad';
mkdir (diroutputOK)
mkdir (diroutputBAD)
cd(dirinput)
files = dir([dirinput,'/*.wav']);
folders = {files.folder};
files = {files.name};
srate = 44100;

 %% Main loop Loop 
cd(dirinput)
i = 1;
rate=0; 
while i <= length(files)   
    % read data 
    [dat, srate] = audioread(files{i});
    dat = dat(:,1);
    % play audio 
     sound(dat,srate);     
     disp(['item played: ', files{i}])    
 
    %% display image 
    
    %pic2read= strrep(files{i},'wav','jpg');
    %pic = imread(pic2read);
    %imshow(pic)
    %%
    %Request input    
    rate = inputdlg(['Rate sound:',files{i},':',],'s');
    rate = str2double(rate);
    if rate > 1
        disp('Type a valid value: 0 or 1')
    elseif rate ==1 
         audiowrite(strcat(diroutputOK,'\',strrep(files{i},'.wav','_OK.wav')),dat,srate,'BitsPerSample',24,'comment','cut rated as OK'); % comments can be read by reading file with audioinfo('file.wav')
        % save rate      
         i = i + 1;

    elseif rate ==0 
        audiowrite(strcat(diroutputBAD,'\',strrep(files{i},'.wav','_bad.wav')),dat,srate,'BitsPerSample',24,'comment','cut needs revision'); % comments can be read by reading file with audioinfo('file.wav')
       % save rate 
         i = i + 1;
        
    end
   close gcf
end
 
 