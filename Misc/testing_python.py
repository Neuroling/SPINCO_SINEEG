# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
from scipy.stats import sem
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
from scipy.io import loadmat


# provide path to folder where results are stored
DataPath = 'V:/spinco_data/SINEEG/analysis/mvpa/'
    
    # define the name of the output file
fname='Results_Infants_included_decode_within_SVM_22-Sep-2022_44205.mat'
    
   # Extract the decoding accuracy results     
data = loadmat(DataPath+fname)['results'][0,0]
DA = data['DA']
    
    

# number of participants
numParts = np.shape(DA)[0]

# set time window
times = [-50, 500]
# set baseline length 
base = 50 
# get array indices
timeInds = [times[0] + base, times[1] + base]

# calculate average classification accuracy for each participant over all conditions at each time point, flatten condition x condition matrix to look at pairwise accuracy
partAccuracies = np.array([[np.nanmean(np.ndarray.flatten(DA[part,point,:,:])) for point in range(timeInds[0],timeInds[1])] for part in range(np.shape(DA)[0])])

# calculate the group average classification accuracy over all conditions at each time point, flatten condition x condition matrix to look at pairwise accuracy
groupAccuracy = np.array([np.nanmean(np.ndarray.flatten(DA[:,point,:,:])) for point in range(timeInds[0],timeInds[1])])


#################

## Calculate significance of group average classification

b = np.full([numParts,550],50) # What are you testing against: in this case, theoretical chance of 50%

T_obs, clusters, cluster_p_values, H0 = mstats.permutation_cluster_test([partAccuracies,b], tail=1, out_type="mask")

#########################
#[GFG]
# PLOTLY!
# Using plotly.express
import plotly.express as px

df =  pd.DataFrame(partAccuracies)
df.append(np.array(range(-50,500)))
df = pd.DataFrame(df)
 
df = px.data.stocks()
fig = px.line(df, x='date', y="GOOG")
fig.show()


timeseq = list(range(-50,500))
fig = px.line(partAccuracies, x=timeseq)


df.index.name = 'subj'
df.reset_index(inplace=True)
df.subj = ['s' + str(x) for x in df.subj]





######################################################################
## Plot group accuracy, participant accuracies over time series, and bars indicating where accuracy was significantly above chance

plt.figure(figsize=(20,10))  

# Plot all participant accuracies  
for part in partAccuracies:
    plt.plot(range(times[0],times[1]),part)
    
# Calculate standard error 
error = [sem(partAccuracies[:,i]) for i in range(timeInds[0],timeInds[1])]
    
# Plot standard error
plt.fill_between(range(times[0],times[1]), groupAccuracy-error,groupAccuracy+error, alpha=0.3, color="teal")
    
# Plot group average accuracy
plt.plot(range(times[0],times[1]),groupAccuracy, linewidth=5,color="black", label="Group average accuracy")
    
# Plot significance bars
plt.subplot
for i_c, c in enumerate(clusters):
    c = c[0]
    if cluster_p_values[i_c] < 0.05:
        h = plt.axvspan(c.start-base, c.stop-base, 
                        color='black', alpha=0.5,ymin=0.17,ymax=0.19)
            
plt.hlines(50, -50, 500)

plt.ylabel('Classification Accuracy %',fontsize=30)   
plt.xlabel('Time (ms)',fontsize=30)

plt.ylim(35, 90)
plt.xlim(times)

plt.tick_params(axis='x', labelsize=30)  
plt.tick_params(axis='y', labelsize=30)  

plt.legend(framealpha=1, frameon=True, fontsize=20,loc="upper right")

plt.show()
