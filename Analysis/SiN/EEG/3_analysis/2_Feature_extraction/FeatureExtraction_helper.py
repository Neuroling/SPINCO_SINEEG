#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 07:57:06 2023

@author: samuemu
"""
import os
from glob import glob
thisDir = os.getcwd()

import mne
from mne.time_frequency import tfr_morlet
import matplotlib.pyplot as plt
import numpy as np

import FeatureExtraction_constants as const

class TFR_Manager:
    """
    """
    def __init__(self,epo):
        self.tmin = epo.times[0]
        self.tmax = epo.times[len(epo.times)-1]
    
    def