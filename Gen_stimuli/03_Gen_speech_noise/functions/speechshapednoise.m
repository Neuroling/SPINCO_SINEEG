function [ssn]= speechshapednoise(sourceSignal, nfft, noctaves, srate, varargin)
% ==========================================================
%  Function to create  Speech-shaped noise   
% ==========================================================
%Author: G.FragaGonzalez 2022(based on snippets from T.Houweling)
%Description
%   Reads source signal, generates white noise of same length, computes spectrum (LTAS) and
%   uses it to filters the noise (with some smoothing) to create Speech Shaped Noise (SSN)
%
%Requires:
%   SoundZone_Tools
%   https://github.com/JacobD10/SoundZone_Tools/archive/master.zip Add
%   the downloaded files in a package folder named: +Tools and add it to
%   matlab search path
%
%Usage:
%  Inputs 
%    sourceSignal - a vector with the input audio signal (e.g., after reading with audioread)  
%    nfft - The number of FFT points used to compute the LTASS
%    noctaves - e.g., 6. Value to use in 1/nOctaves band smoothing (spectral smoothing in which the bandwidth of the smoothing window is a constant percentage of the center frequency).
%    srate -  sampling rate
%       
%   Outputs 
%       ssn - speech-shaped noise 

 
    % white noise 
    rng('default');
    whiteNoise = randn(1,length(sourceSignal)); % create white noise 
    
   % Speech shape noise 
    OctaveBandSpace = 1/noctaves;
    [spect, frqs] = Tools.LTASS(sourceSignal, nfft, srate);        %Compute LTASS spectrum
    ssn = Tools.ArbitraryOctaveFilt(whiteNoise, spect, frqs, nfft, srate, OctaveBandSpace);   % Generate Speech shaped noise
    
end
       
   