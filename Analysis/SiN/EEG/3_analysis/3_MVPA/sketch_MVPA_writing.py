#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test/writing Script for the MVPA
===============================================================================
author: samuemu
Created on Fri Jan 12 13:24:52 2024



"""
import os
import pickle
thisDir = os.path.dirname(__file__)

import MVPA_constants as const
import MVPA_functions as functions

# with open(pickle_path, 'rb') as f:
#     tfr_bands = pickle.load(f)
    

# #%% Get crossvalidation scores
# y = epo.metadata['accuracy'] # What variable we want to predict

# for thisBand in const.freqbands:
#     all_scores_full, scores, std_scores = TFRManager.get_crossval_scores(X=tfr_bands[thisBand], y = y)
#     tfr_bands[thisBand+'_crossval_FullEpoch'] = all_scores_full
#     tfr_bands[thisBand+'_crossval_timewise_mean'] = scores
#     tfr_bands[thisBand+'_crossval_timewise_std'] = std_scores
# # TODO - Hm. all [band]_timewise_mean and all [band]_timewise_std are the same value. Check if there's an error somewhere
