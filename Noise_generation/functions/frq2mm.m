function mm = frq2mm(frq)
% FRQ2MM Greenwood's function for mapping frequency to place on the basilar membrane
%
% Usage: mm = frq2mm(frq)

a= .06; % appropriate for measuring basilar membrane length in mm
k= 165.4;

mm = (1/a) * log10(frq/k + 1);
