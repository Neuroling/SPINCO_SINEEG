"""
Created on Tue Apr  2 14:48:30 2024

@author: sibme
"""

import pickle
import pandas as pd
import numpy as np
import random
import statsmodels.formula.api as smf
import mne
import matplotlib.pyplot as plt
import os

taskID = 'task-sin'
subjID = 's001'

thisDir = os.getcwd()
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data', 'SiN', 'derivatives_SM', taskID, subjID)


#noise = "NV"
noise = "SSN"

filepath = os.path.join(dirinput, subjID +"_Logit_Alpha_" + noise + "_FDR_allValues.pkl")
with open(filepath, 'rb') as f:
    logit_alpha = pickle.load(f)

keysList = list(logit_alpha.keys())
# print(keysList)

p_values = logit_alpha['p_values_uncorrected']
# print(p_values.shape)

# times = np.arange(-0.5, 0.5 + 1/26, 1/26) # Wofür brauchst du das? Unten definierst du "times" ja neu?

metad = logit_alpha['metadata']
# print(metad.keys())

fitting_method = metad['fitting_method']
# print(fitting_method)

times = list(metad['times'])
# print(times)
# print(metad['tmin'])
# print(metad['tmax'])

# print(metad['subsampling_iterations'])
# print(metad['subsampling_performed'])
# print(metad['degrees_of_freedom_Model'])

ch_names = metad['ch_names']
# print(ch_names)
# print(len(ch_names))
# print(ch_names[36])
ch_names[36] = 'AFz'
ch_types = ["eeg"]*64

n_channels = 64
sampling_freq = 1/(times[1]-times[0])
# print(sampling_freq)
info = mne.create_info(ch_names=ch_names, ch_types=ch_types, sfreq=sampling_freq)
print(info)
variable = metad['p_Values_index']

units = dict(eeg='p-values')
scalings = dict(eeg=1)

for ind in range(0,8):
    data = p_values[:,:,ind]
    titles = dict(eeg="Noise: " + noise + ", variable: " + variable[ind])
    evoked_array = mne.EvokedArray(data, info, tmin=times[0])
    evoked_array.set_montage("biosemi64")
    evoked_array.plot(units=units,scalings=scalings,titles=titles)
    plt.show()


