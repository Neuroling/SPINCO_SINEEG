# Sentence-in-noise 
## Flow 
The 'flow' folder contains the files for each block of trials (2 NV and 2 SiSSN) the block presentation order is defined by the files order1.csv, order2.csv....order8.csv. 
The blocks always alternate types of noise (NV or SISSN). The 'order' files with odd number suffix specify sequences starting with NV blocks, 'order' files with even number specify sequence starting with SiSSN blocks. 

Check 'docs' folders for papers in which this task is based on

## Triggers codes

Triggers mark onset/offset of audio file and onset/offset of target items (3 targets per sentence). The triggers (possible values 1 to 256) codes the type of noise item position in the sentence and word 

- 1st digit indicates type: 1(NV), 2(SiSSN) 
- 2nd digit indicates position: 0 (entire file), 1(1st target) 2 (2nd target), 3(3rd target) 
- 3rd digit indicates word in sorted alphabetically or ordinally when numbers: 1 (adler | gelb | eins) , 2 (drossel | gruen | zwei) , 3 (kroete | rot | drei), 4 (tiger | weiss | vier) 
- 3rd digit = 0 indicates the offset of the target
- Clicks and block intial screens are also coded. See table below
- 


| code	| Description
|-------|-------------------------------|
| 1 	| Click to first target		|
| 2 	| Click to second target		|
| 3 	| Click to third target		|
| 5	| Instruction screen		|
| 6	| Start of block screen		|
| 7	| Start of response grid	|
|	|				|
| 100 	| NV starts			| 
| 101 	| NV ends			| 
| 200 	| SiSSN starts			| 
| 201 	| SiSSN ends			| 
|onsets	|				|
| 111 	| NV onset 1:Adler 		| 
| 121 	| NV onset 2:gelb	| 
| 131 	| NV onset 3:eins		| 
|	|				|
| 211 	| SiSSN onset 1:Adler 		| 
| 221 	| SiSSN onset 2:gelb		| 
| 231 	| SiSSN onset 3:eins		| 
|	|				|
| 112 	| NV onset 1: Drossel		| 
| 122 	| NV onset 2:gruen		| 
| 132 	| NV onset 3:zwei		| 
| 212 	| SiSSN onset 1:Drossel		| 
| 222 	| SiSSN onset 2:gruen		| 
| 232 	| SiSSN onset 3:zwei		|
|	|				| 
| 113 	| NV onset 1:Kroete		| 
| 123 	| NV onset 2:rot		| 
| 133 	| NV onset 3:drei		| 
| 213 	| SiSSN onset 1:Kroete		| 
| 223 	| SiSSN onset 2:rot		| 
| 233 	| SiSSN onset 3:drei		|
|	|				| 
| 114 	| NV onset 1:Tiger		| 
| 124 	| NV onset 2:weiss		| 
| 134 	| NV onset 3:vier		| 
| 214 	| SiSSN onset 1:Tiger		| 
| 224 	| SiSSN onset 2:weiss		| 
| 234 	| SiSSN onset 3:vier		|
|offsets|				|
| 110 	| NV offset 1			| 
| 120 	| NV offset 2			| 
| 130 	| NV offset 3			| 
| 210 	| SiSSN offset 1		| 
| 220 	| SiSSN offset 2		| 
| 230 	| SiSSN offset 3		|

