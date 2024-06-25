# Manupulation of epoched data
author: samuelmull

## Folder organisation

**1_Read_epochs_relabel** folder is for all scripts and files handling epoched data

**EPO_runner.py** is the main script for finished code
**EPO_functions.py** is a collection of functions for handling epoching
**EPO_constants.py** contains variables that do not change across files, such as subject IDs
**sketch_EPO_writing.py** is for trying out and debugging code before putting it in EPO_helper.py


## Package Requirements

[mne](https://mne.tools/stable/install/index.html)
Some plotting functions of mne are bugged in matplotlib version 3.7.2 and earlier. Update matplotlib to at least 3.7.3 to ensure smooth operation.


----- Event Labels -----

NoiseType / StimulusType / DegradationLevel / Accuracy / Voice
    
    
    X_____ NoiseType: NV = 1, SSN = 2
    _X____ Stimulus Type: Call = 1, Colour = 2, Number = 3
    __X___ Stimulus: Adler/Gelb/Eins = 1, Drossel/Grün/Zwei = 2, Kröte/Rot/Drei = 3, Tiger/Weiss/Vier = 4
    ___X__ Degradation Level: Lv1 = 1, Lv2 = 2, Lv3 = 3
    ____X_ Accuracy: Incorrect = 0, Correct = 1
    _____X Voice: Feminine (Neural2-F) = 1, Masculine (Neural2-D) = 2
  
  
This allows you to filter the epochs using the event labels, i.e. by:
    epochs.__getitem__('NV') --------> will return all epochs with NV
    epochs.__getitem__('Lv1/call') --> will return all epochs with Lv1 degradation and CallSign


----- List of event codes -----

---- Noise Vocoded ----
    	      			| -------- Incorrect --------  |  -------- Correct  --------  |
    	       			| Female Voice | Male Voice    | Female Voice  | Male Voice   |
CallSign	Adler	Lv1	  111101	    111102  		 111111	      	 111112	 	
        	  		Lv2	  111201        111202	    	 111211		     111212
        	 		Lv3   111301        111302           111311          111312
            Drossel	Lv1	  112101	    112102  		 112112	      	 112112	 	
         	  		Lv2	  112201        112202	    	 112211		     112212
         	 		Lv3   112301        112302           112311          112312
            Kröte	Lv1	  113101	    113102  		 113113	      	 113112	 	
        	  		Lv2	  113201        113202	    	 113211		     113212
        	 		Lv3   113301        113302           113311          113312
            Tiger   Lv1	  114101	    114102  		 114114	      	 114112	 	
         	  		Lv2	  114201        114202	    	 114211		     114212
         	 		Lv3   114301        114302           114311          114312
         	 		
Colour  	Gelb	Lv1	  121101	    121102  		 121111	      	 121112	 	
        	  		Lv2	  121201        121202	    	 121211		     121212
        	 		Lv3   121301        121302           121311          121312
            Grün	Lv1	  122101	    122102  		 122112	      	 122112	 	
         	  		Lv2	  122201        122202	    	 122211		     122212
         	 		Lv3   122301        122302           122311          122312
            Rot 	Lv1	  123101	    123102  		 123113	      	 123112	 	
        	  		Lv2	  123201        123202	    	 123211		     123212
        	 		Lv3   123301        123302           123311          123312
            Weiss   Lv1	  124101	    124102  		 124114	      	 124112	 	
         	  		Lv2	  124201        124202	    	 124211		     124212
         	 		Lv3   124301        124302           124311          124312     
         	 		
Number  	Eins	Lv1	  131101	    131102  		 131111	      	 131112	 	
        	  		Lv2	  131201        131202	    	 131211		     131212
        	 		Lv3   131301        131302           131311          131312
            Zwei	Lv1	  132101	    132102  		 132112	      	 132112	 	
         	  		Lv2	  132201        132202	    	 132211		     132212
         	 		Lv3   132301        132302           132311          132312
            Drei 	Lv1	  133101	    133102  		 133113	      	 133112	 	
        	  		Lv2	  133201        133202	    	 133211		     133212
        	 		Lv3   133301        133302           133311          133312
            Vier    Lv1	  134101	    134102  		 134114	      	 134112	 	
         	  		Lv2	  134201        134202	    	 134211		     134212
         	 		Lv3   134301        134302           134311          134312           	 		    	 		
 
---- Speech Shaped Noise ----
    	      			| -------- Incorrect --------  |  -------- Correct  --------  |
    	       			| Female Voice | Male Voice    | Female Voice  | Male Voice   |
CallSign	Adler	Lv1	  211101	    211102  		 211111	      	 211112	 	
        	  		Lv2	  211201        211202	    	 211211		     211212
        	 		Lv3   211301        211302           211311          211312
            Drossel	Lv1	  212101	    212102  		 212112	      	 212112	 	
         	  		Lv2	  212201        212202	    	 212211		     212212
         	 		Lv3   212301        212302           212311          212312
            Kröte	Lv1	  213101	    213102  		 213113	      	 213112	 	
        	  		Lv2	  213201        213202	    	 213211		     213212
        	 		Lv3   213301        213302           213311          213312
            Tiger   Lv1	  214101	    214102  		 214114	      	 214112	 	
         	  		Lv2	  214201        214202	    	 214211		     214212
         	 		Lv3   214301        214302           214311          214312
         	 		
Colour  	Gelb	Lv1	  221101	    221102  		 221111	      	 221112	 	
        	  		Lv2	  221201        221202	    	 221211		     221212
        	 		Lv3   221301        221302           221311          221312
            Grün	Lv1	  222101	    222102  		 222112	      	 222112	 	
         	  		Lv2	  222201        222202	    	 222211		     222212
         	 		Lv3   222301        222302           222311          222312
            Rot 	Lv1	  223101	    223102  		 223113	      	 223112	 	
        	  		Lv2	  223201        223202	    	 223211		     223212
        	 		Lv3   223301        223302           223311          223312
            Weiss   Lv1	  224101	    224102  		 224114	      	 224112	 	
         	  		Lv2	  224201        224202	    	 224211		     224212
         	 		Lv3   224301        224302           224311          224312     
         	 		
Number  	Eins	Lv1	  231101	    231102  		 231111	      	 231112	 	
        	  		Lv2	  231201        231202	    	 231211		     231212
        	 		Lv3   231301        231302           231311          231312
            Zwei	Lv1	  232101	    232102  		 232112	      	 232112	 	
         	  		Lv2	  232201        232202	    	 232211		     232212
         	 		Lv3   232301        232302           232311          232312
            Drei 	Lv1	  233101	    233102  		 233113	      	 233112	 	
        	  		Lv2	  233201        233202	    	 233211		     233212
        	 		Lv3   233301        233302           233311          233312
            Vier    Lv1	  234101	    234102  		 234114	      	 234112	 	
         	  		Lv2	  234201        234202	    	 234211		     234212
         	 		Lv3   234301        234302           234311          234312     
