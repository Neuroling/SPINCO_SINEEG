function [X,opix] = overlapadd(Y,H)
% X = ola(Y,H)
%   Overlap-add columns of Y, offset by H.
%   There's no windowing (i.e. scaling by a tapered window) in here. 
% 2010-11-14 Dan Ellis dpwe@ee.columbia.edu

[W,nw] = size(Y);

% The approach is to build an index matrix, where each row pulls 
% in successive, nonoverlapping windows from the original data.
% This matrix then has as many rows as needed to get all the
% overlapping windows.  We can then index the input with it, and 
% simply sum up.

% Upper bound on the the number of windows that overlap for each
% point = the number of rows we'll need in our index matrix
ovf = ceil(W/H);

% How many windows will there be in each row?
nwonf = ceil(nw/ovf);

% Unravel Y, then add a zero on the end.  Any indices we don't need
% in our index will point here, so they have no contribution to the
% final sum
Ywz = [Y(:)',0];
% (index for the final zero value)
leny = length(Ywz);

% Here's the indexing magic.  Create one row of the final index
% matrix that pulls out every ovf'th window from the original
% matrix in its unravelled form.  Pad any gaps with the zero index.
opix = reshape(repmat([[1:W],leny*ones(1,ovf*H - W)]', 1, nwonf) ...
               + repmat(ovf*W*[0:(nwonf-1)], ovf*H, 1), ...
               1, ovf*H*nwonf);

lopix = length(opix);
% Add in the following rows, which are offset by H points, and with
% indices that are shifted to pick up the interleaving windows
for i = 2:ovf
  opix = [opix;[leny*ones(1,(i-1)*H),W+opix(1,1:(lopix-(i-1)*H))]];
end

% Any points off the end get set to the zero value
opix(opix > leny) = leny;

% Now, the big payoff - index by the rows, including pulling in the
% zeros, in such a way that it's all ready to sum up to get OLA
X = sum(Ywz(opix))';
