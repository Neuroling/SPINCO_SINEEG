# Sentence-in-noise 
## Audio levels
The audio mixer snapshot is in the file:  _SIN_AUDIOMIX_snapshot.tmss
See the SOP of this project for more details - You can find it in `SINEEG/Docs/Procedures/SINEEG_lab_SOP_v01.docx`

## Flow 
The 'flow' folder contains the files for each block of trials (2 NV and 2 SiSSN) the block presentation order is defined by the files order1.csv, order2.csv....order10.csv  
The blocks always alternate types of noise (NV or SISSN). The 'order' files with odd number suffix specify sequences starting with SiSSN blocks, 'order' files with even number specify sequence starting with NV blocks (*Note: it is the other way around for experiment1*)

Check 'docs' folders for papers in which this task is based on

## Triggers codes

Triggers mark onset/offset of audio file and onset/offset of target items (3 targets per sentence). The triggers codes the type of noise and item position in the sentence and word [^1]

[^1]: Triggers are only allowed to be between 1 and 255. Triggers 256 and over will overflow back to 1. Unfortunately, I haven't realised that until after I coded the clear trials with 300-339. This means that triggers 55 (end of instruction screen) and 60 (end of block) are now the same as the codes that originally were 311 and 316. The preprocessing scripts for experiment2 therefore recodes triggers that should be 300-339 by adding +256 to the triggers between 44 and 83. For codes 55 and 60, it will only recode them to 311 and 316 if they were immediately preceded by code 300. Since 311 and 316 refer to onset of callSign (`token_1_tmin`), they always have to follow 300, which refers to audio onset (`firstSound_tmin`)

- 1st digit indicates type: 1 (NV), 2 (SiSSN), 3 (clear/non-degraded)
- 2nd digit indicates position: 0 (first word: `firstSound_tmin`), 1 (CallSign: `token_1_tmin`), 2 (colour: `token_2_tmin`), 3 (number: `token_3_tmin`) 
- 3rd digit indicates word in sorted alphabetically or ordinally when numbers: 1 (adler | gelb | eins) , 2 (drossel | gruen | zwei) , 3 (kroete | rot | drei), 4 (tiger | weiss | vier) # TODO
- 3rd digit = 0 indicates the offset of the target
- Clicks and block intial screens are also coded. See table below
 


| code	| Description
|-------|-------------------------------|
| 8	| Start resting state PRE task	|
| 9 	| Start resting state POST task	|
| 1 	| Click to first target         |
| 2 	| Click to second target	|
| 3 	| Click to third target		|
|	|				|
| 5	| Main task Instruction screen		|
| 55	| Post-task resting-state Instruction screen		|
|	|				|
| 6	| Start of block screen		|
| 7	| Start of response grid	|
| 60	| End of a block |
|	|				|
| 100 	| NV starts			| 
| 101 	| NV ends			| 
| 200 	| SiSSN starts			| 
| 201 	| SiSSN ends			| 
|target onsets	|				|
| 111 	| NV onset 1:Adler 		| 
| 121 	| NV onset 2:gelb	 	| 
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
|target offsets|				|
| 110 	| NV offset 1			| 
| 120 	| NV offset 2			| 
| 130 	| NV offset 3			| 
| 210 	| SiSSN offset 1		| 
| 220 	| SiSSN offset 2		| 
| 230 	| SiSSN offset 3		|
