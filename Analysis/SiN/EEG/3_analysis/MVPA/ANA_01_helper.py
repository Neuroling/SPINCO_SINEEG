# -*- coding: utf-8 -*-

""" Helper script fro ANA_01
=================================================================
@author: samuemu

""" 
import mne

def eeglabEpo2mneEpo(fileinput):
    """ takes the epoched .set file from EEGLAB and returns an mne.Epochs object
    parameters: eeglab epoch file ending in .set
    """
    epochs = mne.io.read_epochs_eeglab(fileinput)
    epo_fn = fileinput[:fileinput.find('.set')]+'-epo.fif'
    epochs.save(epo_fn)