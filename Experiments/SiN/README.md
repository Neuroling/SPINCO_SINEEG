# SiN Experiment Scripts
Sentence-in-noise EEG experiment 

Folders: 
- **PsychoPy** folders contain the actual experiment 

## Goal

Analysis aims
| Data | Decoding-classes | Goal | 
|:-----|:-----------|:-------|
| Pre-stimuli | 2-class correct vs incorrect  | Finding EEG features associated with better speech-in-noise comprehension. Find targets for neurofeedback | 
| ERP, post-stimuli | Multiclass decoding of 4 possible word choices  |Explore impact of noise/degradation levels on internal representation of words  ||

## Design
### Stimuli 
- Description: Simple sentences with a defined structured of which the last word is to be filled in with 1 out of 4 possible words 
- Source: (paper ref or extend description here 
- n_sentences, n_ words, etc (...) 

### TO DO
#### EEG triggers
- Audio timing: take direct line of the audio and record it into an Aux chan on the EEG to ensure we have exact stimulus onsets
- Extract times of the key words in the sentences for EEG analysis

### Manipulations

 | Condition | Levels | Description | 
|:-----|:-----------|:-------|
| Type | 2 | SiSSN or VC || 
| Level | 3 |  SNR/vocoding chan mixing || 

### Task 
Response screen with 4 choices


