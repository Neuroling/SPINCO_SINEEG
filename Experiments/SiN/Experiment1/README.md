# SiN Experiment 1 Scripts
Sentence-in-noise EEG experiment 

Folders: 
- **SiN_task** folders contain the actual experiment. Contains output participant performance data
- **SiN_practice**: has some practice trials to show to the participants offline (e.g., before electrode placement). No output logs 
- **PsychoPy_LevelTests**: some test run outside the eeg lab to test different noise manipulations 

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


### Manipulations Experiment 1

 | Condition | Levels | Description | 
|:-----|:-----------|:-------|
| Type | 2 | SiSSN or VC || 
| Level | 3 |  SNR/vocoding chan mixing || 

### Task 
Grid Response screen with 4 x 3 choices

| call1 | colour1 | number1 |
| call2 | colour2 | number2 |
| call3 | colour3 | number3 |
| call4 | colour4 | number4 |

### Response images
CallSign images from [MultiPic](https://doi.org/10.1080/17470218.2017.1310261)

CallSign and MultiPic Number:
- Tiger - Nr. 98
- Adler - Nr. 703
- Drossel - Nr. 430
- Kröte - Nr. 612 (For future reference, Nr. 584 would be better)

- Ratte - Nr. 137
- Eule - Nr. 323
- Flugzeug - Nr. 297
- Auto - Nr. 302 / Nr. 358 / Nr. 364
