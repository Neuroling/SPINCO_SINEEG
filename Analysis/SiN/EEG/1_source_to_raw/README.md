
## 1_source_to_raw 

The Biosemi EEG data is recorded in a single **.bdf** file (24-bit) for the entire session, which consists on a main task and two resting state recordings (before and after task). 
The file has an `Erg1` channel with the audio output signal to help correcting for audio delay. Unfortunately, this channel is missing in subjects s201 and s202, and it is wrong in s203.

### Import_01_importBDF_loadLocs_split.m

[most recent commit](https://github.com/Neuroling/SPINCO_SINEEG/blob/main/Analysis/SiN/EEG/1_source_to_raw/Import_01_importBDF_loadLocs_split.m)  
[permalink](https://github.com/Neuroling/SPINCO_SINEEG/blob/034cc5a5a0da078511fc800ce60e6743f164bd9d/Analysis/SiN/EEG/1_source_to_raw/Import_01_importBDF_loadLocs_split.m) to the version of the code used for Exp1  

Import raw data from Source with minimal preprocessing in EEGlab: 
- Adjust triggers. Clicks in the *audio signal* (`Erg1`) are detected for each trial in the task. This is used to adjust the event triggers (target word onsets and start/end of the sentence) accounting for any audio output delay. 
    - **NOTE: This is probably wrong, see issue [#8](https://github.com/Neuroling/SPINCO_SINEEG/issues/8) on github**
- The file is split[^1] into three datasets: `s001_task-rest-pre.set`, `s001_task-rest-post.set`,  `s001_task-sin.set` (event triggers are used to determine the splits)
- Channel locations are loaded 
- Create `.json` metadata files and `.tsv` channel location and event files. 
    - **NOTE:** the event file contains also the accuracy value , this is read from the experimental file (in behavioral folder 'beh')
-   
[^1]: The `.set` format was preferred after previous issues when exporting to formats as bdf or edf with EEGlab and MNE toolboxes. When the `Erg1` channel with digital audio recorded was loaded, there were (what appeared to be) sampling errors in the exported bdf or edf from EEGlab (using `writeeg` from Biosig) and EDF with [mne](https://mne.tools/stable/generated/mne.export.export_raw.html) . These problems were not present when using the Biosemi Actitools software (however this is not a desired step as it requires manual input in GUI)


## Current issues 

### missing trigger 1 (06.06.2024)

- For the second experiment, some of the triggers for the event of code 1 are missing. 
- Event 1 codes the start of the audio presentation screen in psychoPy (+0.08s). It is therefore always followed by the event codes for audio onset (100, 200 or 300)
- Event code 1 is missing in 8 trials in subj s201 and in 12 trials in subj s202. 
- In trials where event code 1 is missing, the event codes for audio onset (100, 200, 300) seem to be shifted backwards in time: When looking at the number of samples between the events coding audio onset (100, 200, 300) and the subsequent event (callSign onset), the difference is much smaller in those trials where event code 1 is missing.
- For some plots and datachecks surrounding this issue, see the script `datachecks_eventCodes.py`

### alignTriggersToAudio.m currently not working (06.06.2024)

- This script is a function to align trigger code 1 to the clicks in the audio channel (channel 73). There are two issues with it
- The first issue is the missing trigger 1 codes, which the audio clicks should be aligned with.
- The second issue is that the EEGlab function `pop_biosig` deletes the channel with the clicks even when `rmeventchan` is set to `off`. This means that there is no way to find the clicks which should be aligned with trigger code 1.
- I tried to read in the data again with `pop_readbdf`, which previously wasn't done due to "Problems reading events when importing with pop_readbdf" (quote from the script), and then removing all channels but the audio channel. Unfortunately, there really do seem to be problems reading the events when importing with that function.
- Can I do that in python?

### gather_accuracies_events.m currently not working (06.06.2024)

- This script is a function that should create the accuracy tsv file.
- Something about the remapping the answers from str to numeric doesn't work.
- Can I do that in python instead?
