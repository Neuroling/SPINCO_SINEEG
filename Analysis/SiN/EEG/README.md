
## General info 

### Naming Conventions
Expect a numbered folder for each part of the analysis (1_source_to_raw, 2_preproc, etc) indicating their sequence. Then within each folder, scripts have a prefix indicating `category + '-' +  order in which they are run + descriptive Name` (e.g., `Prep-01_xxx`, `Prep-02_xxx`). In some cases, the name is followed by `exp2` to indicate that this script is specific to experiment2 (which means subjects s201-s204). [^1] 

If there is a number in the middle of the filename, like for pipeline, the number indicates the version of the pipeline, and not the order in which they are run (e.g., `Prep-01_pipe01_xx`, `Prep-01_pipe02_xxx` )

[^1]: For a run down on what 'experiment1' and 'experiment2' means, check the [project report](https://github.com/Neuroling/SPINCO_SINEEG/wiki/Project-Report-June-2024) or this [README](https://github.com/Neuroling/SPINCO_SINEEG/tree/main/Experiments/SiN) file

## 1_source_to_raw 

The Biosemi EEG data is recorded in a single **.bdf** file (24-bit) for the entire session, which consists on a main task and two resting state recordings (before and after task). 
The file has an `Erg1` channel with the audio output signal to help correcting for audio delay. Unfortunately, this channel is missing in subjects s201 and s202, and it is wrong in s203.


## 2_preprocessing 

Multiple pipelines for task and resting state data
Generated data considered as *derivatives* 

## 3_analysis

Multiple analyses 
