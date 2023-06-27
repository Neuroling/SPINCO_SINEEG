
# Sentence-in-noise preprocessing and analysis

## Raw data import 

### 0. Source data
Recorded raw EEG data is a single **.bdf** file (24-bit) containing the recording for the entire session which consists on a main task and two resting state recordings (before and after task). 
The file has an  ergo1 channel with the audio signal to help correcting for audio delay.

### 1. Source to raw data
> ISSUES when cropping the files and exporting as bdf or edf with EEGlab and MNE toolboxes:
> - Toolboxes: export problems when all channels are loaded as they include Ergo1 with digital audio recorded (non-voltage channel). This is a problem when exporting bdf or edf from EEGlab (uses writeeg) and EDF with mne (https://mne.tools/stable/generated/mne.export.export_raw.html).
>   Biosemi recorded bdf files are 24-bits, edf are 16-bits. However the problem here is more serious (scrolling channels show sampling problems) 
> - Bisemi tools: This problem is solved if converting to EDF using ActiTools converted OR if cropping the files with ActiTools. This is not a desired step as it is a manual step. 

One `Matlab` script performs:
#### 1.1 Audio-trigger to adjust event triggers
Click's in the audio signal are detected for each trial in the task. This is used to adjust the event triggers (target word onsets and start/end of the sentence) accounting for any audio output delay.

#### 1.2 Data selection and export voltage channels
- The main bdf `s001_task.bdf` is splitted in three files named `s001_task-rest-pre.bdf`, `s001_task-rest-post.bdf`,  `s001_task-sin.bdf`. 
- Channel locations are loaded
- Only voltage channels are exported

### 2. BIDs folder structure and meta-data
A python script generates `.json` files with meta data and `.tsv ` channel locations and event files.
Uses MNE to read file duration (included in json file) and events to create a .tsv event file. 

