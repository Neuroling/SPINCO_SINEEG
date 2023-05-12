function fn = BIF(cfs, category)
% fn = BIF(cfs, category) returns the band importance functions of given centre frequencies.
%
% input:
%        cfs            Centre frequencies (Hz) in an array   
%        category       An integer between 1 and 7 indicating the type of BIF that is used.
%                       1 - For average speech given in Table 3 of ANSI S3.5-1997
%                       2 - Nonsense syllable test of CV, VC and CVC type where most of the English
%                           phonemes occurring equally often
%                       3 - Phonetically-balanced words of CID-W22 test             
%                       4 - Monosyllables of the NU6 test
%                       5 - Words of the two alternative Diagnostic Rhyme Test (DRT) material 
%                       6 - Short passages of easy reading material
%                       7 - Monosyllables of the Speech in the Presence of Noise (SPIN) test.
% 
% output:
%        fn             Band importance functions of the given centre frequencies in an array. The
%                       sum of fn is 1.
%
%
% Author:   Yan Tang
% Date:     Sep 16, 2012

if ~isscalar(category) || ~ismember(category, 1:7)
   error('Flag of BIF type must be an integer between 1 and 7');
end;

% if length(cfs) < 15
%    error('Not enough bands, 15 bands are required at minimal.');
% end

if ((min(cfs)<20) || (max(cfs)>12500))
   error('Centre frequency must be in the range of [20 12500] Hz');
end

cb = [160 200 250 315 400 500 630 800 1000 1250 1600 2000 2500 3150 4000 5000 6300 8000];

CBI = [
   0.0083	0        0.0365	0.0168	0        0.0114	0
   0.0095	0        0.0279	0.0130   0.0240   0.0153	0.0255
   0.0150   0.0153	0.0405	0.0211	0.0330   0.0179	0.0256
   0.0289	0.0284	0.0500   0.0344	0.0390   0.0558	0.0360
   0.0440   0.0363	0.0530   0.0517	0.0571	0.0898	0.0362
   0.0578	0.0422	0.0518	0.0737	0.0691	0.0944	0.0514
   0.0653	0.0509	0.0514	0.0658	0.0781	0.0709	0.0616
   0.0711	0.0584	0.0575	0.0644	0.0751	0.0660   0.0770
   0.0818	0.0667	0.0717	0.0664	0.0781	0.0628	0.0718
   0.0844	0.0774	0.0873	0.0802	0.0811	0.0672	0.0718
   0.0882	0.0893	0.0902	0.0987	0.0961	0.0747	0.1075
   0.0898	0.1104	0.0938	0.1171	0.0901	0.0755	0.0921
   0.0868	0.112    0.0928	0.0932	0.0781	0.0820   0.1026
   0.0844	0.0981	0.0678	0.0783	0.0691	0.0808	0.0922
   0.0771	0.0867	0.0498	0.0562	0.0480   0.0483	0.0719
   0.0527	0.0728	0.0312	0.0337	0.0330   0.0453	0.0461
   0.0364	0.0551	0.0215	0.0177	0.0270   0.0274	0.0306
   0.0185	0        0.0253	0.0176	0.0240   0.0145	0
   ];

fn = interp1(cb, CBI(:, category), cfs, 'PCHIP');
fn(fn < 0) = 0;

% normalised to a summation of 1
fn = fn ./ sum(fn);
