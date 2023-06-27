
# Sentence-in-noise preprocessing
## Source and Raw data import 

- Source data (unedited recording)
- Raw (minimally preprocessed with only trigger adjustment and file split )
- Derivatives (preprocessed at multiple stages)
  
See : https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#source-vs-raw-vs-derived-data

**Steps**
### 0. Source data
The Biosemi EEG data is recorded in a single **.bdf** file (24-bit) for the entire session, which consists on a main task and two resting state recordings (before and after task). 
The file has an  'ergo1' channel with the audio output signal to help correcting for audio delay.

### 1. Raw data from Source
Minimal processing is done (in *Matlab*):

#### Adjust triggers
Click's in the *audio signal* are detected for each trial in the task. This is used to adjust the event triggers (target word onsets and start/end of the sentence) accounting for any audio output delay.

#### Split and export as EDF 
- The source bdf `s001.bdf` is splitted in three `EDF` files named `s001_task-rest-pre.edf`, `s001_task-rest-post.edf`,  `s001_task-sin.edf`. 
- Audio channel is removed leaving scalp channels, EOG, mastoids [^1]

  
[^1]: Previous issues when cropping the files and exporting as bdf or edf with EEGlab and MNE toolboxes (1) Export problems when all channels are loaded as they include Ergo1 with digital audio recorded. This is a problem when exporting bdf or edf from EEGlab (uses writeeg) and EDF with mne (https://mne.tools/stable/generated/mne.export.export_raw.html). (2) Biosemi recorded bdf files are 24-bits, edf are 16-bits. However the problem here is more serious (scrolling channels show sampling problems) 
(3) Bisemi tools: This problem is solved if converting to EDF using ActiTools converted OR if cropping the files with ActiTools. This is not a desired step as it is a manual step. 

### 2. BIDs folder structure and meta-data
A python script generates `.json` files with meta data and `.tsv ` channel locations and event files.
Uses MNE to read file duration (included in json file) and events to create a .tsv event file. 
Source to Raw conversion steps are logged in .json eeg file. 




