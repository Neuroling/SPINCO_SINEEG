function Y = shufflewins(X,W,R)
% function Y = shufflewins(X,W,R)
%    X is a waveform, which is chopped into W-point windows 
%    which are then hanning-windowed and 50%-overlapped.  These 
%    windows are shuffled over a radius of R points and
%    ovelap-added to construct Y, a version of X with approximately
%    the same average spectrum over R point windows, but scrambled
%    structure over a W-point timescale.
% 2010-11-13 Dan Ellis dpwe@ee.columbia.edu

% Force W even
W = W + rem(W,2);
% Hop between windows - 50% overlap
H = W/2;

% Build 50% overlapped, windowed windows
Yw = diag(hanning(W)')*frame(X,W,H);

% Calculate reordering
%rpx = 1:size(Yw,2);  % debug - identity
rpx = localperm(size(Yw,2),R/H);

% Reorder columns
Yw = Yw(:,rpx);

% Overlap-add
Y = overlapadd(Yw,H);
Y = Y(1:length(X));
