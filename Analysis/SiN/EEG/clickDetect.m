% Find Clicks in the last EEG channel 
%------------------------------------------------------
% Input: eeglab data set with audio signal in the last channel
% -Returns the index (data point in EEG data)  for the start of each click
% Author: G.FragaGonzalez
 
function  clickOnsets = clickDetect(EEG)
% intensity threshold 
threshold = 0.8;
% Duration of the click (sec)
clickDur = 0.1 ;

%Normalize audio signal so that max value is 1 
erg1_norm = EEG.data(end,:,:)*(1/max(abs(EEG.data(end,:,:))));
 
%% Find onsets of clicks 
boundaries = find(erg1_norm > threshold);
clickOffsets = boundaries(diff(boundaries) > floor(clickDur*EEG.srate));
clickOnsets = clickOffsets - floor(clickDur*EEG.srate);
disp(['----->', num2str(length(clickOnsets)),' clicks detected'])

%%  visual check
%y = zeros(1,length(erg1_norm));
%y(clickOnsets) = 1;
%plot(erg1_norm, 'Color', [0.5 0.5 0.5]); hold on; plot(y, 'Color', 'red');

