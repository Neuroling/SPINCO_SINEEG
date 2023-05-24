# Speech-in-noise comprehension: SINEEG
Speech-in-noise comprehension (SPINCO) subproject: sentence-in-noise EEG (SINEEG) studies at the Neurolinguistics group (University of Zurich). 
Visit https://gorkafraga.github.io/guidesbook for a collection of notes, documentation and resources


Experiments
- SiN: sentence-in-noise (main) 
- (drafts and previous work TH ) DiN: digits-in-noise and WiN: words-in-noise

Folders
- utils: various generic utilities 
- Analysis: main functions for analyses
- Experiment: psychopy scripts: local version contains the .wav files, also stored in the data location
- Gen_stimuli: generate stimuli sentences and add noise / vocode 
- Misc: miscelanea, including _fromRobertBecker: collection of scripts shared by R.B 


# Data organization
(BIDS) Dataset will be made available in a public data repo *tbd*

Folders
````
./spinco_data
    ├──SINEEG
    |	├── README.md
    |	├──SIN/    
    |	│   ├──raw/
    |	│   │   ├── dataset_description.json
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
Example of EEG data from https://openneuro.org/datasets/ds001787/versions/1.1.0/file-display/sub-015:ses-01:eeg:sub-015_ses-01_task-meditation_eeg.json: 
````
{
  "InstitutionAddress": "Centre de Recherche Cerveau et Cognition, Place du Docteur Baylac, Pavillon Baudot, 31059 Toulouse, France",
  "InstitutionName": "Paul Sabatier University",
  "InstitutionalDepartmentName": "Centre de Recherche Cerveau et Cognition",
  "PowerLineFrequency": 50,
  "ManufacturersModelName": "ActiveTwo",
  "TaskName": "meditation",
  "EEGReference": "CMS/DRL",
  "Manufacturer": "BIOSEMI",
  "EEGChannelCount": 64,
  "MiscChannelCount": 15,
  "RecordingType": "continuous",
  "RecordingDuration": 2718,
  "SamplingFrequency": 256,
  "EOGChannelCount": 0,
  "ECGChannelCount": 0,
  "EMGChannelCount": 0,
  "SoftwareFilters": "n/a"
}
````

Metadata (JSON)
Example from BIDS dataset_description.json
Only the fields 'Name' and 'BIDSVersion' are marked as required in the documentation:
https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html
````
{
  "Name": "The mother of all experiments",
  "BIDSVersion": "1.6.0",
  "DatasetType": "raw",
  "License": "CC0",
  "Authors": [
    "Paul Broca",
    "Carl Wernicke"
  ],
  "Acknowledgements": "Special thanks to Korbinian Brodmann for help in formatting this dataset in BIDS. We thank Alan Lloyd Hodgkin and Andrew Huxley for helpful comments and discussions about the experiment and manuscript; Hermann Ludwig Helmholtz for administrative support; and Claudius Galenus for providing data for the medial-to-lateral index analysis.",
  "HowToAcknowledge": "Please cite this paper: https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
  "Funding": [
    "National Institute of Neuroscience Grant F378236MFH1",
    "National Institute of Neuroscience Grant 5RMZ0023106"
  ],
  "EthicsApprovals": [
    "Army Human Research Protections Office (Protocol ARL-20098-10051, ARL 12-040, and ARL 12-041)"
  ],
  "ReferencesAndLinks": [
    "https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
    "Alzheimer A., & Kraepelin, E. (2015). Neural correlates of presenile dementia in humans. Journal of Neuroscientific Data, 2, 234001. doi:1920.8/jndata.2015.7"
  ],
  "DatasetDOI": "doi:10.0.2.3/dfjj.10",
  "HEDVersion": "8.0.0",
  "GeneratedBy": [
    {
      "Name": "reproin",
      "Version": "0.6.0",
      "Container": {
        "Type": "docker",
        "Tag": "repronim/reproin:0.6.0"
      }
    }
  ],
  "SourceDatasets": [
    {
      "URL": "s3://dicoms/studies/correlates",
      "Version": "April 11 2011"
    }
  ]
}
````
