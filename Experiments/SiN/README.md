# SiN Experiment Scripts
Sentence-in-noise EEG experiment 


Folders: 
- **Experiment1** is the experiment run by G. Fraga and S. Mueller in July - September 2023 (subjects s001 - s015)
- **Experiment2** is the experiment run by S. Mueller in June 2024 (subjects s201 - s204)

within these folders you will find:
- **SiN_task**: contain the actual experiment. Contains output participant performance data
- **SiN_practice**: has some practice trials to show to the participants offline (e.g., before electrode placement). No output logs.
- **PsychoPy_LevelTests**: some test run outside the eeg lab to test different noise manipulations (only for experiment1)
- **SiN_alphaVersion**: Minimal example of SiN_task, with shorter blocks and only one block order, resulting in less stimuli (which can therefore be pushed to github and shared that way) (only for experiment2)
    - If you update anything in SiN_task, make sure to run the script located at `Scripts/Gen_stimuli/Gen_speech_noise_sequences/Create_AlphaVersion.py` [link](https://github.com/Neuroling/SPINCO_SINEEG/blob/main/Gen_stimuli/Gen_speech_noise_sequences/Create_AlphaVersion.py) to create a new alpha version from SiN_task.

## Overal Goal

Analysis aims
| Data | Decoding-classes | Goal | 
|:-----|:-----------|:-------|
| Pre-stimuli | 2-class correct vs incorrect  | Finding EEG features associated with better speech-in-noise comprehension. Find targets for neurofeedback | 
| ERP, post-stimuli | Multiclass decoding of 4 possible word choices  |Explore impact of noise/degradation levels on internal representation of words  ||

## Design
### Stimuli 
- Description: Simple sentences with a defined structured of which the last word is to be filled in with 1 out of 4 possible words 
- Source: 
- n_sentences, n_ words, etc (...) 
