
# Sentence-in-noise preprocessing and analysis
## Import Raw data to BIDs
Recorded raw EEG data ise expected to be  a single **.bdf** file containing the main task and two resting state recordings (before and after task). 
### 1. Raw bdf split 
> ISSUES when cropping the files and exporting as bdf or edf with EEGlab and MNE toolboxes:
> - Toolbox: export problems when all channels are loaded as they include Ergo1 with digital audio recorded (non-voltage channel). This is a problem when exporting bdf or edf from EEGlab (uses writeeg) and EDF with mne (https://mne.tools/stable/generated/mne.export.export_raw.html)
> - Bisemi tools: This problem is solved if converting to EDF using ActiTools converted OR if cropping the files with ActiTools. This is not a desired step as it is a manual step. 
The main bdf `s001_task.bdf` is splitted in three files named `s001_task-rest-pre.bdf`, `s001_task-rest-post.bdf`,  `s001_task-sin.bdf`. 
This 




### 2. w

### 3. 
