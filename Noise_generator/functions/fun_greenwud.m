function [lower,center,upper]= fun_greenwud(N, low, high)
%

% [lower,center,upper] = greenwud(N,low,high)
%
% This function returns the lower, center and upper freqs
% of the filters equally spaced according to Greenwood's equation
% Input: N - number of filters
% 	 low - (left-edge) 3dB frequency of the first filter
%	 high - (right-edge) 3dB frequency of the last filter
%
% Stuart Rosen -- June 1998
%

% Set up equally spaced places on the basilar membrane
places = [0:N]*(fun_mm2frq(high)-fun_mm2frq(low))/N + fun_mm2frq(low);
% Also calculate centre frequencies according to the same mapping
centres = zeros(1,N);
centres = (places(1:N) + places(2:N+1))/2;
% convert these back to frequencies
freqs = fun_mm2frq(places);
center = fun_mm2frq(centres);

lower=zeros(1,N); upper=zeros(1,N);
lower(1:N)=freqs(1:N);
upper(1:N)=freqs(2:N+1);
