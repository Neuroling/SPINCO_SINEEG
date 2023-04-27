function frq = mm2frq(mm)
% MM2FRQ Greenwood's function for mapping place on the basilar membrane to frequency
% Usage: function frq = mm2frq(mm)

a= .06; % appropriate for measuring basilar membrane length in mm
k= 165.4;

frq = 165.4 * (10.^(a * mm)- 1);




