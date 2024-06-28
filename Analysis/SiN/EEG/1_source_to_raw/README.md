
## 1_source_to_raw 

The Biosemi EEG data is recorded in a single **.bdf** file (24-bit) for the entire session, which consists on a main task and two resting state recordings (before and after task). 
The file has an `Erg1` channel with the audio output signal to help correcting for audio delay. Unfortunately, this channel is missing in subjects s201 and s202, and it is wrong in s203, see issue [#7](https://github.com/Neuroling/SPINCO_SINEEG/issues/7)

### Import_01_importBDF_loadLocs_split.m

[most recent commit](/Import_01_importBDF_loadLocs_split.m)  
[permalink](https://github.com/Neuroling/SPINCO_SINEEG/blob/034cc5a5a0da078511fc800ce60e6743f164bd9d/Analysis/SiN/EEG/1_source_to_raw/Import_01_importBDF_loadLocs_split.m) to the version of the code used for Exp1  

Import raw data from Source with minimal preprocessing in EEGlab: 
- Adjust triggers. Clicks in the *audio signal* (`Erg1`) are detected for each trial in the task. This is used to adjust the event triggers (target word onsets and start/end of the sentence) accounting for any audio output delay. 
    - **NOTE: This is probably wrong, see issue [#8](https://github.com/Neuroling/SPINCO_SINEEG/issues/8) on github**
- The file is split[^1] into three datasets: `s001_task-rest-pre.set`, `s001_task-rest-post.set`,  `s001_task-sin.set` (event triggers are used to determine the splits)
- Channel locations are loaded 
- Create `.json` metadata files and `.tsv` channel location and event files. 
    - **NOTE:** the event file contains also the accuracy value , this is read from the experimental file (in behavioral folder 'beh')
    
Additionally, here is a [permalink](https://github.com/Neuroling/SPINCO_SINEEG/blob/4d99d22fbf509624efec3b0745a714742fff0190/Analysis/SiN/EEG/1_source_to_raw/Import_01_Exp2_ImportBDF_split_loadLocs_alignTriggers.py) to an unfinished script that I started to write to do the same thing in python with MNE. However, due to time constraints, I abandoned that project to stick with the matlab EEGlab script. The python script has been deleted by now, but I wanted to save the permalink to it somewhere, in case it becomes useful for someone.
   
[^1]: The `.set` format was preferred after previous issues when exporting to formats as bdf or edf with EEGlab and MNE toolboxes. When the `Erg1` channel with digital audio recorded was loaded, there were (what appeared to be) sampling errors in the exported bdf or edf from EEGlab (using `writeeg` from Biosig) and EDF with [mne](https://mne.tools/stable/generated/mne.export.export_raw.html) . These problems were not present when using the Biosemi Actitools software (however this is not a desired step as it requires manual input in GUI)

### datacheck_eventCodes.py

This script was written for experiment 2 [^2] to do some checks on the event codes

[^2]: For a run down on what 'experiment1' and 'experiment2' means, check the [project report](https://github.com/Neuroling/SPINCO_SINEEG/wiki/Project-Report-June-2024) or this [README](https://github.com/Neuroling/SPINCO_SINEEG/tree/main/Experiments/SiN) file

## Current issues 

### Recoding event triggers to correct bit-overflow (experiment 2)

Because event triggers are stored as a single bit, numbers above 256 overflow back to 1. I forgot that. Now, triggers 300-339 (which we use for clear trials in experiment 2 [^2]) are coded as 44-83. This means that triggers 55 (end of instruction screen) and 60 (end of block) are now the same as the codes that originally were 311 and 316

This loop below is how triggers that should be 300-339 are recoded by adding +256 to the triggers between 44 and 83. For codes 55 and 60, it will only recode them to 311 and 316 if they were immediately preceded by code 300. Since 311 and 316 refer to onset of callSign (token_1_tmin), they always have to follow 300, which refers to audio onset (firstSound_tmin).

```python
for i in range(len(events)):
    if events[i,2] <= 83 and events[i,2]>= 44:
        if (events[i,2] == 55 and events[i-1,2] == 300) or events[i,2] != 55 :
            if (events[i,2] == 60 and events[i-1,2] == 300) or events[i,2] != 60  :
                events[i,2] = events[i,2] + 256
```

### missing trigger 1 (experiment 2)
See issue [#6](https://github.com/Neuroling/SPINCO_SINEEG/issues/6)

I found out that the trigger codes 1 are sometimes missing in experiment2[^2]. This happens if the trigger codes for the first word (100, 200, 300) are sent at exactly the same time as trigger 1 - which should not happen in the first place.  

In the past, we used trigger code 1 as the audio onset trigger, to which we aligned the clicks. However, if you look at the datacheck_eventCodes.py script, you can see that, even if trigger code 1 is present, the time between it and the trigger codes for the first word (100, 200, 300) is *highly* variable. If trigger code 1 were indeed the audio onset, it should always be exactly 0.16s before the first word trigger.

Trigger code 1 is sent by the psychopy component pp_start, which is set to be sent 0.08s after the audio-presentation routine starts. It is therefore tied not to the audio onset but to the psychopy routine (see github issue [#8](https://github.com/Neuroling/SPINCO_SINEEG/issues/8) ), and the audio onset is subject to variable lag from the start of the routine. There is no trigger sent to the EEG when the audio first starts, but that timing is logged in the .csv output under column "sound_1.started".

***Therefore: trigger code 1 is not related to the audio, and it is also shifted from the true audio onset by a variable delay.***

Furthermore, with the `datachecks_eventCodes.py` script [[link]](/datacheck_eventCodes.py) you can see that the trigger codes for the first word (100, 200, 300) are not reliable when trigger code 1 is missing. The time between them and the onset of the first stimulus word (callSign, named token_1_tmin in the csv file, codes 11*, 21*, 31*) is shifted only in trials where trigger 1 is missing. However: The time between the start of the callSign trigger and the other triggers (i.e. end of callSign, start of Colour, end of colour, etc.) remains within the range of +/- 30 samples (14ms) of what it should be - and that seems to  be the best we can do in terms of temporal accuracy. 

- For the second experiment, some of the triggers for the event of code 1 are missing. 
- Event 1 codes the start of the audio presentation screen in psychoPy (+0.08s). It is therefore always followed by the event codes for audio onset (100, 200 or 300)
- Event code 1 is missing in 8 trials in subj s201 and in 12 trials in subj s202. 
- In trials where event code 1 is missing, the event codes for audio onset (100, 200, 300) seem to be shifted backwards in time: When looking at the number of samples between the events coding audio onset (100, 200, 300) and the subsequent event (callSign onset), the difference is much smaller in those trials where event code 1 is missing.
- For some plots and datachecks surrounding this issue, see the script `datachecks_eventCodes.py`
