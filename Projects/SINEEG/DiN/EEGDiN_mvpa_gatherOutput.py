#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:03:40 2022

@author: gfraga
"""
from scipy.stats import sem
import matplotlib.pyplot as plt
import numpy as np
import mne.stats as mstats
from scipy.io import loadmat

# provide path to folder where results are stored
DataPath = "/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/25subj/Results/" 

# define the name of the output file
fname='Results_25subj_decode_within_SVM_11.07.2022_14.31.10.mat'

# Extract the decoding accuracy results     
data = loadmat(DataPath+fname)['results'][0,0]
DA = data['DA']


# %% Calculate average classification accuracy over the time series

# number of participants
numParts = np.shape(DA)[0]

# set time window in ms
times = [-2000, -5]

# set baseline length 
base = 0 

# get array indices
idx1 = int(np.where(data['times'] == times[0]+base)[1])
idx2 =  int(np.where(data['times'] == times[1]+base)[1])
timeInds = [idx1, idx2]


# calculate average classification accuracy for each participant over all conditions at each time point, flatten condition x condition matrix to look at pairwise accuracy
partAccuracies = np.array([[np.nanmean(np.ndarray.flatten(DA[part,point,:,:])) for point in range(timeInds[0],timeInds[1])] for part in range(np.shape(DA)[0])])

# calculate the group average classification accuracy over all conditions at each time point, flatten condition x condition matrix to look at pairwise accuracy
groupAccuracy = np.array([np.nanmean(np.ndarray.flatten(DA[:,point,:,:])) for point in range(timeInds[0],timeInds[1])])

# %% Significance of classification accuracy against chance
## Calculate significance of group average classification

b = np.full([numParts,399],50) # What are you testing against: in this case, theoretical chance of 50%

T_obs, clusters, cluster_p_values, H0 = mstats.permutation_cluster_test([partAccuracies,b], tail=1, out_type="mask")


# %% Plot 
plt.figure(figsize=(20,10))  
times2plot = np.linspace(times[0],times[1],num=399)

# Plot all participant accuracies  
for part in partAccuracies:
    #plt.plot(range(times[0],times[1]),part)
    plt.plot(times2plot,part)
    
    
# Calculate standard error 
#error = [sem(partAccuracies[:,i]) for i in range(timeInds[0],timeInds[1])]
error = [sem(partAccuracies[:,i]) for i in range(timeInds[0],timeInds[1])]

# % Plot standard error
#plt.fill_between(range(times[0],times[1]), groupAccuracy-error,groupAccuracy+error, alpha=0.3, color="teal")
plt.fill_between(times2plot, groupAccuracy-error,groupAccuracy+error, alpha=0.3, color="teal")

#  
# Plot group average accuracy
plt.plot(times2plot,groupAccuracy, linewidth=5,color="black", label="Group average accuracy")
 
# %%
# Plot significance bars
plt.subplot
for i_c, c in enumerate(clusters):
    c = c[0]
    if cluster_p_values[i_c] < 0.05:
        h = plt.axvspan(c.start-base, c.stop-base, 
                        color='black', alpha=0.5,ymin=0.17,ymax=0.19)
    
plt.hlines(0, -2000, 0)

plt.ylabel('Classification Accuracy %',fontsize=30)   
plt.xlabel('Time (ms)',fontsize=30)

plt.ylim(0, 90)
plt.xlim(times)

plt.tick_params(axis='x', labelsize=30)  
plt.tick_params(axis='y', labelsize=30)  

plt.legend(framealpha=1, frameon=True, fontsize=20,loc="upper right")

plt.show()