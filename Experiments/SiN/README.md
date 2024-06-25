# SiN Experiment Scripts
Sentence-in-noise EEG experiment 

Folders: 
- **Experiment1** is the experiment set up by G. Fraga and run in July 2023 - September 2023 (subjects s001 - s015)
- **Experiment2** is an adaptation of experiment1, set up by S. Mueller and run in June 2024 (subjects s201 - s204)

Within these folders you will find:
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
| ERP, post-stimuli | Multiclass decoding of 4 or 8 possible word choices  | Explore impact of noise/degradation levels on internal representation of words  ||

## Design

### Stimuli 

- Description: Simple sentences with a defined structure, in which certain words change and need to be chosen out of 4 or 8 words.
    - All sentences are of the structure "Vorsicht [callSign]! Gehe sofort zum [Colour] Feld der Spalte [Number]"
    - The callSign, Colour and Number change in each sentence. In experiment1, there are 4 options for each, in experiment2, there are 8 options for each.
    - The subject then needs to click the corresponding images on a 4x3 or 8x3 response grid
- Stimuli are presented as audio in different stages of degradation (see next section)
- The stimuli are generated using the pipeline described in `Flowchart_stimuliGeneration_Experiment1.png` and `Flowchart_stimuliGeneration_Experiment2.pdf` [^1]
    - The flowchart for experiment2 thoroughly documents which scripts are used in what order
    - It includes generation of stimuli, manipulation of the audio files (incl. degradation), generation of the spreadsheets in PsychoPy, as well as the creation of *SiN_practice* and *SiN_alphaVersion*
    
[^1]: Since I (samuelmull) joined this project after stimulus generation for experiment1, the `Flowchart_stimuliGeneration_Experiment1.png` I created might not be entirely accurate or complete. I re-created it from gfraga's amazing `SINEEG_report.html` and his documentation of the scripts. This is also what I then used as baseline to generate Stimuli for experiment2 - the pipeline of which I thoroughly documented in `Flowchart_stimuliGeneration_Experiment2.pdf` .  
You can find all of these files in `SINEEG/Docs/Procedures/` or `SINEEG/Docs/Reports/`. The stimuli generation flowcharts are, for the sake of convenience, redundantly saved in the respective `ExperimentN/SiN_task/docs` folder of the psychoPy experiment.    
    
### Stimulus degradation

In **Experiment1**, all stimuli are degraded using either noise vocoding (NV) or speech in speech-shaped noise (SiSSN). There are three levels of degradation for each.    

The stimuli are presented in 4 blocks (2 NV, 2 SiSSN), presented in alternating order. Each block contains all three levels of degradation.  

The degradation levels are:  
| Noise | degradation-levels |
|:------|:---------|
| SiSSN | -11dB, -9dB, -7dB |
| NV | 0.2p, 0.4p, 0.6p |

In **Experiment2**, 66% of stimuli are degraded using either noise vocoding (NV) or speech in speech-shaped noise (SiSSN). There is only one level of degradation for each.  

The stimuli are presented in 6 blocks (3 NV, 3 SiSSN), presented in alternating order. Each block contains 32 degraded stimuli, and 16 non-degraded stimuli ('clear trials').  

Since we realised that the stimuli were too difficult after running two subjects, different levels of degradation were used for the subsequent subjects:  
| Noise | degradation-levels |
|:------|:---------|
| SiSSN | -11dB / -9dB |
| NV | 0.2p / 0.4p |

### Response images

Original *CallSign* images from [MultiPic](https://doi.org/10.1080/17470218.2017.1310261) 

Experiment 1:
| CallSign | MultiPic number | MultiPic filename | Note |
|:---------|:----------------|:------------------|:-----|
| Tiger | Nr. 98 | PICTURE_98.png | - |
| Adler | Nr. 703 | PICTURE_703.png | - |
| Drossel | Nr. 430 | PICTURE_430.png | - |
| Kröte | Nr. 612 | PICTURE_612.png | Actually a frog. Nr. 584 would be a toad. |

Experiment 2:
| CallSign | MultiPic number | MultiPic filename | Note |
|:---------|:----------------|:------------------|:-----|
| Ratte | Nr. 137 | PICTURE_137.png | technically a mouse |
| Tiger | Nr. 98 | PICTURE_98.png | - |
| Adler | Nr. 703 | PICTURE_703.png | - |
| Eule | Nr. 323 | PICTURE_323.png | - |
| Velo | Nr. 23 | PICTURE_23.png | "Fahrrad" |
| Auto | Nr. 302 | PICTURE_23.png | other options: Nr. 358 / Nr. 364 |
