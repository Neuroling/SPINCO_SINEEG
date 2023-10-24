# -*- coding: utf-8 -*-

""" Helper script fro ANA_01
=================================================================
@author: samuemu

""" 
import mne

def eeglabEpo2mneEpo(fileinput):
    """ takes the epoched .set file from EEGLAB and returns an mne.Epochs object
    
    parameters: 
        fileinput : eeglab epoch file ending in .set
    """
    epochs = mne.io.read_epochs_eeglab(fileinput)
    epo_fn = fileinput[:fileinput.find('.set')]+'-epo.fif'
    epochs.save(epo_fn, overwrite=True, fmt='double')
    del epochs
    epo = mne.read_epochs(epo_fn)
    return epo