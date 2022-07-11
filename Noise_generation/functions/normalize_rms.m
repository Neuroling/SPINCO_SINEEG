function [wavenorm]=normalize_rms(sourceSignal,signal2normal) 
% ==========================================================
%  Use RMS to normalize two signals 
% ==========================================================
%Author: G.FragaGonzalez 2022 from T.Houweling
%Description
%   Simple matching of rms of two signal vectors  
%
%Usage:
%  Inputs 
%    sourceSignal - vector with signal e.g.,output of audioread(speech.wav)
%    signal2normal - vector with signal to be normalized to source a e.g., a noise 
%
%   Outputs 
%      Normalized noise 

%% Format check 
% make them row vectors
 if ~isrow(sourceSignal)
     sourceSignal = sourceSignal';
 end 
 
 if ~isrow(signal2normal)
     signal2normal = signal2normal' ;
 end 
 
%% Normalize using Root mean square 
    
    RMS_sig = rms(sourceSignal);      
    RMS_noise = rms(signal2normal);
    
    wavenorm = signal2normal.*(RMS_sig/RMS_noise);
    disp(['normalizing [' inputname(2) ']']);  
       
    
  if ~isequal(round(rms(sourceSignal),3),round(rms(wavenorm),3))
      error ('check if something went wrong with RMS normalization')
  end
end

