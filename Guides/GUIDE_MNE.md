# MNE toolbox for M/EEG analysis and visualization 
MNE is an open-source Python package for exploring, visualizing, and analyzing human neurophysiological data: MEG, EEG, sEEG, ECoG, NIRS, and more.

## Example from MVPA analysis 
In this **Example** we will use MNE to apply an **SVM** classifier for multivariate pattern analysis (**MVPA**) of EEG data. The data were collected as part of the Digit-in-noise (DIN) project by T. Houweling.
Here we use epoched .set files (EEGlab formated containing both header and data). 

The MVPA analysis is based on the code provided in: https://github.com/BayetLab/infant-EEG-MVPA-tutorial

### Importing EEG data in MNE 
- First consult this site: https://eeglab.org/others/EEGLAB_and_python.html,  https://mne.tools/0.17/manual/migrating.html
- Read epoched data. 
          EEG = mne.io.read_epochs_eeglab('s9_DiN_epoched_ICrem.set')

          
          
