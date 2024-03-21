#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 08:39:54 2024

@author: testuser
"""
from glob import glob
import os
import mne
import pickle
import Plotting_constants as const

#%%
class PlottingManager:
    
    def __init__(self):
        print("initialising PlottingManager")

#%%
    def get_evokeds(self, save = True):
        """
        This function returns a dict containing a lists for every condition, 
        which contain evoked arrays for every subject.
        
        In other words: Every subjects *_epo.fif is opened, then the evoked is
        created for every possible combination of degradation_level, noise_Type and
        accuracy. The evoked object is then appended to a list - there is a list
        for every combination of conditions, and each list stores the evoked-object
        of that condition of every subject. All lists are stored in a dict.

        Parameters
        ----------
        save : bool, default = True
            Whether the evoked dict should be saved as .pkl or only returned
            The default is True.

        Returns
        -------
        evokeds : dict of lists containing MNE evoked objects
            

        """
        
        print("creating evokeds...")
        # list of every possible combination of accuracy, noise & degradation, separated by /
        conditions = const.conditions
               
        # This will give us a dict containing a lists for every condition, which contain evoked arrays for every subject
        evokeds = {condition : [] for condition in conditions} # Create dict with empty lists for every condition
        
        for subjID in const.subjIDs: # for every subj, open *_epo.fif 
            epo_path = glob(os.path.join(const.dirinput, subjID, str("*" + const.fifFileEnd)), recursive=True)[0]
            epo = mne.read_epochs(epo_path)
            
            for event_type in conditions: # create the evoked-object for every condition and append to list inside the dict
                evo = epo[event_type]._compute_aggregate(picks=None)
                evo.comment = event_type
                evokeds[event_type].append(evo)
                
        filepath = os.path.join(const.dirinput,const.evokedsPickleFileEnd)
        if save:
            with open(filepath, 'wb') as f:
                pickle.dump(evokeds, f)
            print('evokeds saved to',filepath)
        return evokeds
    
#%% #TODO comment
    def grandaverage_evokeds(self, evokeds):
        evokeds_gAvg= {}       
        for condition in const.conditions:
            evokeds_gAvg[condition] = mne.grand_average(evokeds[condition], drop_bads = False, interpolate_bads = False)
            evokeds_gAvg[condition].comment = condition
        # evokeds_gAvg = list(evokeds_gAvg.values())
        return evokeds_gAvg
        
