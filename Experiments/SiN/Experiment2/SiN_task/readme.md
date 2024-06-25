# Sentence-in-noise 
author: samuelmull
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
- 2nd digit indicates position: 0 (first word: `firstSound_tmin`), 1 (callSign: `token_1_tmin`), 2 (colour: `token_2_tmin`), 3 (number: `token_3_tmin`) 
- 3rd digit indicates word: 1 (Adler | gelb | eins) , 2 (Eule | gruen | zwei) , 3 (Ratte | rot | drei), 4 (Tiger | weiss | vier) , 5 (Velo | blau | fuenf) , 6 (Auto | braun | sechs) , 7 (Messer | pink | neun), 8 (Gabel | schwarz | null) 
- 3rd digit = 0 indicates the offset of the target
- Clicks and block intial screens are also coded. See table below
 


| code	| Description                   | PsychoPy component |
|-------|-------------------------------|--------|
| 8	    | Start resting state PRE task	| pp_rest_pre_start |
| 9 	| Start resting state POST task	| pp_rest_pre_start_2 |
|	    |				                |            |
| 55	| Pre-task resting state Instruction screen | pp_instrRest_PRE |
| 55	| Post-task resting state Instruction screen | pp_rest_post |
| 55	| Main task Instruction screen     | pp_instr_start_2 |
| 5 | final Main task Instruction screen   | pp_instrTask |
|	    |			                       |  |
| 6 	| Start of block screen		| pp_blockstart |
| 1 	| audioTrial Routine start + 0.08s (see github issue [#8](https://github.com/Neuroling/SPINCO_SINEEG/issues/8) and [#6](https://github.com/Neuroling/SPINCO_SINEEG/issues/6) ) | pp_start |
| 7	    | Start of response grid	| pp_respGrid  |
| 60	| End of a block            | pp_blockends |
|	    |				            |              |
| 100 	| NV onset first word 			   | pp_t0_start |
| 101 	| NV offset last word [^2]		       | pp_end |
| 200 	| SiSSN onset first word 		   | pp_t0_start |
| 201 	| SiSSN offset last word [^2]			   | pp_end |
| 300 	| clear Trial onset first word 	   | pp_t0_start |
| 301 	| clear Trial offset last word [^2]	   | pp_end |
|target onsets	|				| |
| 111 	| NV onset callSign: Adler 		| pp_t1_start |
| 112 	| NV onset callSign: Eule 		| pp_t1_start |
| 113 	| NV onset callSign: Ratte 		| pp_t1_start |
| 114 	| NV onset callSign: Tiger 		| pp_t1_start |
| 115 	| NV onset callSign: Velo 		| pp_t1_start |
| 116 	| NV onset callSign: Auto 		| pp_t1_start |
| 117 	| NV onset callSign: Messer 		| pp_t1_start |
| 118 	| NV onset callSign: Gabel 		| pp_t1_start |
|       |                               |             |
| 211 	| SiSSN onset callSign: Adler 		| pp_t1_start |
| 212 	| SiSSN onset callSign: Eule 		| pp_t1_start |
| 213 	| SiSSN onset callSign: Ratte 		| pp_t1_start |
| 214 	| SiSSN onset callSign: Tiger 		| pp_t1_start |
| 215 	| SiSSN onset callSign: Velo 		| pp_t1_start |
| 216 	| SiSSN onset callSign: Auto 		| pp_t1_start |
| 217 	| SiSSN onset callSign: Messer 		| pp_t1_start |
| 218 	| SiSSN onset callSign: Gabel 		| pp_t1_start |
|       |                               |             |
| 311 	| clear Trial onset callSign: Adler 		| pp_t1_start |
| 312 	| clear Trial onset callSign: Eule 		| pp_t1_start |
| 313 	| clear Trial onset callSign: Ratte 		| pp_t1_start |
| 314 	| clear Trial onset callSign: Tiger 		| pp_t1_start |
| 315 	| clear Trial onset callSign: Velo 		| pp_t1_start |
| 316 	| clear Trial onset callSign: Auto 		| pp_t1_start |
| 317 	| clear Trial onset callSign: Messer 		| pp_t1_start |
| 318 	| clear Trial onset callSign: Gabel 		| pp_t1_start |
|       |                               |             |
| 121 	| NV onset colour: gelb 		| pp_t2_start |
| 122 	| NV onset colour: gruen 		| pp_t2_start |
| 123 	| NV onset colour: rot 		    | pp_t2_start |
| 124 	| NV onset colour: weiss 		| pp_t2_start |
| 125 	| NV onset colour: blau 		| pp_t2_start |
| 126 	| NV onset colour: braun 		| pp_t2_start |
| 127 	| NV onset colour: pink 		| pp_t2_start |
| 128 	| NV onset colour: schwarz 		| pp_t2_start |
|       |                               |             |
| 221 	| SiSSN onset colour: gelb 		    | pp_t2_start |
| 222 	| SiSSN onset colour: gruen 		| pp_t2_start |
| 223 	| SiSSN onset colour: rot 		    | pp_t2_start |
| 224 	| SiSSN onset colour: weiss 		| pp_t2_start |
| 225 	| SiSSN onset colour: blau 		    | pp_t2_start |
| 226 	| SiSSN onset colour: braun 		| pp_t2_start |
| 227 	| SiSSN onset colour: pink 		    | pp_t2_start |
| 228 	| SiSSN onset colour: schwarz 		| pp_t2_start |
|       |                                   |             |
| 321 	| clear Trial onset colour: gelb 		| pp_t2_start |
| 322 	| clear Trial onset colour: gruen 		| pp_t2_start |
| 323 	| clear Trial onset colour: rot 		| pp_t2_start |
| 324 	| clear Trial onset colour: weiss 		| pp_t2_start |
| 325 	| clear Trial onset colour: blau 		| pp_t2_start |
| 326 	| clear Trial onset colour: braun 		| pp_t2_start |
| 327 	| clear Trial onset colour: pink 		| pp_t2_start |
| 328 	| clear Trial onset colour: schwarz 	| pp_t2_start |
|       |                                       |             |
| 131 	| NV onset number: eins 		| pp_t3_start |
| 132 	| NV onset number: zwei 		| pp_t3_start |
| 133 	| NV onset number: drei 		    | pp_t3_start |
| 134 	| NV onset number: vier 		| pp_t3_start |
| 135 	| NV onset number: fuenf 		| pp_t3_start |
| 136 	| NV onset number: sechs 		| pp_t3_start |
| 137 	| NV onset number: neun 		| pp_t3_start |
| 138 	| NV onset number: null 		| pp_t3_start |
|       |                               |             |
| 231 	| SiSSN onset number: eins 		    | pp_t3_start |
| 232 	| SiSSN onset number: zwei 		| pp_t3_start |
| 233 	| SiSSN onset number: drei 		    | pp_t3_start |
| 234 	| SiSSN onset number: vier 		| pp_t3_start |
| 235 	| SiSSN onset number: fuenf 		    | pp_t3_start |
| 236 	| SiSSN onset number: sechs 		| pp_t3_start |
| 237 	| SiSSN onset number: neun 		    | pp_t3_start |
| 238 	| SiSSN onset number: null 		| pp_t3_start |
|       |                                   |             |
| 331 	| clear Trial onset number: eins 		| pp_t3_start |
| 332 	| clear Trial onset number: zwei 		| pp_t3_start |
| 333 	| clear Trial onset number: drei 		| pp_t3_start |
| 334 	| clear Trial onset number: vier 		| pp_t3_start |
| 335 	| clear Trial onset number: fuenf 		| pp_t3_start |
| 336 	| clear Trial onset number: sechs 		| pp_t3_start |
| 337 	| clear Trial onset number: neun 		| pp_t3_start |
| 338 	| clear Trial onset number: null 	| pp_t3_start |
|       |                                       |             |
|target offsets|				|
| 110 	| NV offset callSign		| pp_t1_end |
| 120 	| NV offset colour			| pp_t2_end |
| 101 	| NV offset number [^2]		| pp_end |
| 210 	| SiSSN offset callSign		| pp_t1_end |
| 220 	| SiSSN offset colour		| pp_t2_end |
| 201 	| SiSSN offset number [^2]  | pp_end |
| 310 	| clear Trial offset callSign		| pp_t1_end |
| 320 	| clear Trial offset colour		    | pp_t2_end |
| 301 	| clear Trial offset number [^2]    | pp_end |


[^2]: Since the last word in the sentence is the Number, the trigger code for the offset of the last word is also the trigger code for the offset of number
