#Sentence-in-noise 
## Flow 
The 'flow' folder contains the files for each block of trials (2 NV and 2 SiSSN) the block presentation order is defined by the files order1.csv, order2.csv....order8.csv. 
The blocks always alternate types of noise (NV or SISSN). The 'order' files with odd number suffix specify sequences starting with NV blocks, 'order' files with even number specify sequence starting with SiSSN blocks. 


## Triggers code

Stimuli: onset/offset of audio file and onset/offset of target items (3 targets per sentence) 

| code	| Description
|-------|-----------------------|
| 100 	| Audio file starts	| 
| 101	| Audio file ends	| 
| 10	| Target one starts	| 
| 11 	| Target one ends 	| 
| 20 	| Target two starts	| 
| 21 	| Target two ends 	| 
| 30 	| Target three starts 	| 
| 31 	| Target tree ends 	|
| 1 	| First response	|
| 2 	| Second response	|
| 3 	| Third response	|

Naming trigger variables (psychopy):
pp_t1_start = parallel port target 1 starts