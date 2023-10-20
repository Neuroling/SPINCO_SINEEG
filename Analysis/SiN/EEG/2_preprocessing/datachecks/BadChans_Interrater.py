"""
- Reads the quality assessment .csv for the EEG channels
- compares the ratings
- NOT WORKING YET

Created on Fri Oct 25 2023

"""

import os 
import pandas as pd 

# User inputs
copyraw = 0
taskID = 'task-sin'

#%% PATHS
thisDir = os.path.dirname(os.path.abspath(__file__))
dirinput= os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives_SM')
filename='QualityAssessment.csv'

df = pd.read_csv(os.path.join(dirinput, filename))
df=df.rename(columns={'BadChans':'BadChansSib','BadChans.1':'BadChansSam'})
df=df[['SUBJ','BadChansSib','BadChansSam','autoBadChans']]


def find_common_elements(row):
    sets = [set(item.split(',')) for item in row]
    common_elements = set.intersection(*sets)
    return common_elements

 

# Apply the function row-wise
df['Common_Elements'] = df.apply(find_common_elements, axis=1)

 

# Filter out rows with no common elements
df_filtered = df[df['Common_Elements'].apply(len) > 0]

 

print(df_filtered)
