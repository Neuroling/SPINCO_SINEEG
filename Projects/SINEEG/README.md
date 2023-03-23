# SINEEG
Experiments
- SiN: sentence-in-noise (main) 
- (previous from TH ) DiN: digits-in-noise
- (just some initial tests ) WiN: words-in-noise

Folders
- utils: various generic utilities 
- functions: main functions for analyses
- Experiment: scripts to generate experiments (e.g. psychopy)
- _fromRobertBecker: collection of scripts shared by R.B 



# Data organization
(BIDS) Data set available at *tbd*

Folders
````
./spinco_data
    ├──SINEEG
    |	├── README.md
    |	├──SIN/    
    |	|   ├── README.md
    |	│   ├──raw/
    |	│   │   ├── README.md
    |	│   │   ├── s01
    |	│   │   │   ├── s01_rest_eeg.bdf 
    |	│   │   │   ├── s01_sin_eeg.bdf
    |	│   │   │   ├── s01_rest_eeg.json        
    |	│   │   │   ├── s01_sin_eeg.json
    |	│   │   │   ├── s01_electrodes.tsv
    |	│   │   │   └── s01_sin_exp-data.csv
    └──	└── └── └── ...
````

Metadata (JSON)
Example *s01_sin_eeg.json*
````
{
	"TaskName": "SentenceInNoise",
	"TaskDescription": ".describe task here..",
	"InstitutionName": "...",
	"InstitutionAddress": "...",
	"EEGChannelCount": 64,
	"EEGReference": "xxxx",
	"EOGChannelCount": 4,  
	"EMGChannelCount": 0,
	"ECGChannelCount": 0	
	"MiscChannelCount": 73,
	"TriggerChannelCount": 1,
	"PowerLineFrequency": 50,
	"EEGPlacementScheme": "xxx",
	"Manufacturer": "BioSemi",
	"ManufacturersModelName": "ActiveTwo",
	"HardwareFilters": "n/a",
	"SoftwareFilters": "n/a",
	"SoftwareVersions": "xxx",
	"CapManufacturer": "xxxx",
	"CapManufacturersModelName": "xxxxx",
	"RecordingType": "continuous",
	"RecordingDuration": xxxx,
	"SamplingFrequency": xxx,	
}
````
