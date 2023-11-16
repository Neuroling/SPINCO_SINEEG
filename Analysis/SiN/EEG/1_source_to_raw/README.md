
## 1_source_to_raw 
The Biosemi EEG data is recorded in a single **.bdf** file (24-bit) for the entire session, which consists on a main task and two resting state recordings (before and after task). 
The file has an  'ergo1' channel with the audio output signal to help correcting for audio delay.

Import raw data from Source with minimal preprocessing in EEGlab: 
- Adjust triggers. Click's in the *audio signal* are detected for each trial in the task. This is used to adjust the event triggers (target word onsets and start/end of the sentence) accounting for any audio output delay.
- The file is splitted[^1] in three datasets: `s001_task-rest-pre.set`, `s001_task-rest-post.set`,  `s001_task-sin.set` (event triggers used to determine the splits)
- Channel locations are loaded 
- Create `.json` metadata files and `.tsv` channel location and event files. **NOTE** the event file contains also the accuracy value , this is read from the experimental file (in behavioral folder 'beh')
-   
[^1]: The .set format was preferred after previous issues when exporting to formats as bdf or edf with EEGlab and MNE toolboxes. When the 'Ergo1' channel with digital audio recorded was loaded, there were (what appeared to be) sampling errors in the exported bdf or edf from EEGlab (using *writeeg* from Biosig) and EDF with mne (https://mne.tools/stable/generated/mne.export.export_raw.html).These problems were not present when using the Biosemi Actitools software (however this is not a desired step as it requires manual input in GUI)
