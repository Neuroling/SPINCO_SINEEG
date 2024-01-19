[[_TOC_]]

# Speech-in-noise comprehension: SINEEG
Speech-in-noise comprehension (SPINCO) subproject: sentence-in-noise EEG (SINEEG) studies at the Neurolinguistics group (University of Zurich). 

Experiments:
- SiN: sentence-in-noise (**main**) 
- (drafts based on previous work from THouweling ) DiN: digits-in-noise and WiN: words-in-noise

The data and metadata  organization is heavily based on  [BIDS](https://bids-standard.github.io/)
 
## Project Location
At date 19.01.2024 the entire project contents is stored in the NAS: _\idnas12.d.uzh.ch\G_PSYNEULIN_DATA\Projects\Spinco\SINEEG_ >> requires access permissions with UZH user
This code repository is cloned at  _\idnas12.d.uzh.ch\G_PSYNEULIN_DATA\Projects\Spinco\SINEEG\Scripts_

## Metadata
- JSON files at the level of the raw data files containing details of each recording.
- README.txt at the main subfolders explaining content
 
## Script folders content
- Analysis: all needed for preprocessing (including import of source data) and analysis. Includes, Dynamic Reports (the main outputs with code, visualizations code, text) 
- Experiments: psychopy scripts. The audio files are not pushed into github (too many). The files are in the 'Stimuli'  folder ~\Projects\Spinco\SINEEG\Stimuli\AudioGens\selected_audio_psychoPy_click
- Gen_stimuli: generate stimuli sentences and add noise / vocode 
- Misc: miscelanea, including _fromRobertBecker: collection of scripts shared by R.B
- utils: various generic utilities 

# Data organization 
See README.txt files within each subfolder for more information. The main folders are: 

Folder tree 
````
./spinco_data
    ├──SINEEG
    │	├── README.md
    │	├──SIN/    
    │	│   ├──sourcedata/
    │	│   │	├── dataset_description.json
    │	│   │	├── s01
    │	│   │  		├── s001.bdf
    │	│   │      	├── s001_SentenceInNoise_2023-06-22_09h55.59.129.csv
    │	│   │   	└── s001.json
    │	│   ├──rawdata/
    │	│   │	├── s01
			├── task-*  			
				├── eeg
				│	├── s001_task-sin_eeg.json
				│	│── s001_task-sin.set
    				│	├── s001_electrodes.tsv
				│	├── s001_coordsystem.json
				│	└── s001_task-sin_events.csv
				├── beh
					└── s001_SentenceInNoise_2023-06-22_09h55.59.129.csv
    
* if the optional 'electrodes.tsv' file is provided, with the electrode locations, then the coordsystem.json file should be provided specifying units and position system used. 
````

## sourcedata
Single **.bdf** file (24-bit) file with unedited recording. Contains the entire session, which consists on a main task and two resting state recordings (before and after task). 
The file has an  'ergo1' channel with the audio output signal to help correcting for audio delay.

## rawdata  
.set EEGlab datasets after minimal preprocessing of source data to: correct audio delay in triggers, load channel locations and split resting and task recordings from file)
> this is the raw data to be used for preprocessing and analysis

## Derivatives (preprocessed at multiple stages)
This contains the main preprocessing pipeline using Automagic 

## Derivatives_SM
The alternative pipeline used by Sibylle Meier's Master Thesis. 


