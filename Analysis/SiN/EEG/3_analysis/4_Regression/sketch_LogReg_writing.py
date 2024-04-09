#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 07:42:19 2024

@author: testuser
"""


from pymer4.models import Lmer
import pandas as pd
import random

import LogReg_functions as functions
import LogReg_constants as const
LogRegManager = functions.LogRegManager()

data_dict, condition_dict = LogRegManager.get_data(output = True, condition = "NV")
ch_names = LogRegManager.metadata['ch_names']
#%%
idx = LogRegManager.random_subsample_accuracy(trial_info=condition_dict)

 
 #%%
## prepare the data
tmp_dict = {}
for subjID in const.subjIDs:    
    tmp_dict[subjID] = condition_dict[subjID]
    tmp_dict[subjID]['eeg_data'] = data_dict[subjID][:,0,0]
df = pd.concat(tmp_dict.values(), axis=0, ignore_index=True)
del tmp_dict

# TODO : treat every electrode as predictor
# TODO : do timepoints as bins of 64ms

# run the model
model = Lmer('accuracy ~ levels * eeg_data + wordPosition + (1|subjID)', data = df, family = 'binomial')
mdf = model.fit()
model.anova()


# tmp = Lmer('accuracy ~ levels * eeg_data + wordPosition + (1|subjID)', data = df, family = 'binomial').fit()
# tmp.shape
