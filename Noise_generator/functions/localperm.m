function I = localperm(N,R)
% I = localperm(N,R)
%    I is a random permutation of the integers from 1:N.  However,
%    unlike RANDPERM, the indices remain somewhat local.
%    Specifically, the displacement I(x) - x has a gaussian
%    distribution with standard deviation R.
% 2010-11-13 Dan Ellis dpwe@ee.columbia.edu

I = zeros(1,N) - 1;

D = round(R*randn(1,N));

remaining = ones(1,N);

% Assign them randomly, to avoid systematic problems with the last few
for i = randperm(N)
  % Ideal placement - offset by D(i) from start pos
  ipos = i + D(i);
  % Find the nearest unused slot to put it in
  frem = find(remaining);
  [err,posix] = min(abs(frem - ipos));
  % OK, there it goes
  pos = frem(posix);
  I(pos) = i;
  remaining(pos) = 0;
end
