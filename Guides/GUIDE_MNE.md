# MNE toolbox for M/EEG analysis and visualization 
MNE is an open-source Python package for exploring, visualizing, and analyzing human neurophysiological data: MEG, EEG, sEEG, ECoG, NIRS, and more.

## Example from MVPA analysis 
In this **Example** we will use MNE to apply an **SVM** classifier for multivariate pattern analysis (**MVPA**) of EEG data. The data were collected as part of the Digit-in-noise (DIN) project by T. Houweling.
Here we use epoched .set files (EEGlab formated containing both header and data). 

The MVPA analysis is based on the code provided in: https://github.com/BayetLab/infant-EEG-MVPA-tutorial

### Importing EEG data in MNE 
- First consult this site: https://eeglab.org/others/EEGLAB_and_python.html,  https://mne.tools/0.17/manual/migrating.html
- Read epoched data: 
      `epochs = mne.io.read_epochs_eeglab('s9_DiN_epoched_ICrem.set')`
 
 - In our case , the info of interest, i.e., accuracy of each trial was encoded in EEG.epochs.accuracy in the eeglab data set. We were not able to directly access this in the output of mne.io.read_epochs_eeglab. However this info was preserved if we read the .set file  using loadmat so we did: 
  `# Retrieve trial accuracy
          mdat = sio.loadmat(fileinput,squeeze_me = True,simplify_cells = True,mat_dtype=True)['EEG']
          epochAccu = [epoch['accuracy'] for epoch in mdat['epoch']]
          
          # recode events 
          for epIdx in range(len(epochs.events)):
          epochs.events[epIdx][2]=epochAccu[epIdx]
          
          # add event information 
          event_dict = {'correct': 1, 'incorrect':0}
          epochs.event_id = event_dict
 `
 ## Visualizing 
