# Sentence-in-noise 
## Flow 
The 'flow' folder contains the files for each block of trials (2 NV and 2 SiSSN) the block presentation order is defined by the files order1.csv, order2.csv....order8.csv. 
The blocks always alternate types of noise (NV or SISSN). The 'order' files with odd number suffix specify sequences starting with NV blocks, 'order' files with even number specify sequence starting with SiSSN blocks. 


## Triggers codes

Triggers mark onset/offset of audio file and onset of target items (3 targets per sentence). The triggers (possible values 1 to 256) codifies type of noise item position in the sentence and word 

- 1st digit indicates type: 1(NV), 2(SiSSN) 
- 2nd digit indicates position: 0 (entire file), 1(1st token) 2 (2nd token), 3(3rd token) 
- 3rd digit indicates word in sorted alphabetically or ordinally when numbers: 1 (adler | gelb | eins) , 2 (drossel | gruen | zwei) , 3 (kroete | rot | drei), 4 (tiger | weiss | vier) 

111(2,3,4)  | , 121, 103, 104
1


| code	| Description
|-------|-------------------------------|
| 100 	| NV file starts		| 
| 101 	| NV file ends			| 
| 200 	| SiSSN file starts		| 
| 201 	| SiSSN file ends		| 
|	|				|
| 111 	| NV file token 1:Adler 	| 
| 121 	| NV file token 2:drossel	| 
| 131 	| NV file token 3:eins		| 
| 211 	| SiSSN file token 1:Adler 	| 
| 221 	| SiSSN file token 2:drossel	| 
| 231 	| SiSSN file token 3:eins	| 
|	|				|
| 112 	| NV file token 1:Drossel	| 
| 122 	| NV file token 2:gruen		| 
| 132 	| NV file token 3:zwei		| 
| 212 	| SiSSN file token 1:Drossel	| 
| 222 	| SiSSN file token 2:gruen	| 
| 232 	| SiSSN file token 3:zwei	|
|	|				| 
| 113 	| NV file token 1:Kroete	| 
| 123 	| NV file token 2:rot		| 
| 133 	| NV file token 3:drei		| 
| 213 	| SiSSN file token 1:Kroete	| 
| 223 	| SiSSN file token 2:rot	| 
| 233 	| SiSSN file token 3:drei	|
|	|				| 
| 114 	| NV file token 1:Tiger		| 
| 124 	| NV file token 2:weiss		| 
| 134 	| NV file token 3:vier		| 
| 214 	| SiSSN file token 1:Tiger	| 
| 224 	| SiSSN file token 2:weiss	| 
| 234 	| SiSSN file token 3:vier	|
|	|				| 
| 1 	| First response		|
| 2 	| Second response		|
| 3 	| Third response		|

