#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 09:01:21 2024

@author: samuemu
"""
import PreStim_constants as const
import os
import pickle

class ERPManager:
    
    def long_df(self):
        tmp = {}
        for subjID in const.subjIDs:
            pickle_path_in = os.path.join(const.thisDir[:const.thisDir.find(
                'Scripts')] + 'Data', 'SiN','analysis', 'eeg', const.taskID,'features',subjID,subjID + const.inputPickleFileEnd)
            
            print('opening dict:',pickle_path_in)
            with open(pickle_path_in, 'rb') as f:
                tfr_bands = pickle.load(f)
                
            df = tfr_bands['epoch_metadata']
            df['data'] = tfr_bands['Alpha_data'][:,0,0]
            df['subjID'] = [subjID for i in range(1152)]
            del tfr_bands
            tmp[subjID]=df
            del df
            
                
            