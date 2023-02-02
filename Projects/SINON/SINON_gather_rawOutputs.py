"""
Created on Mon Jan 30 13:31:37 2023
@author: gfraga

"""
import os  # Commands to remember: os.getcwd(), os.listdir() 
import pandas as pd
import glob
import sys as sys

# paths
if sys.platform=='linux':  basedir  = '/home/d.uzh.ch/gfraga/smbmount/'
else:  basedir ='V:/'

dirinput =  basedir + 'spinco_data/SINON/outputs/data_exp_116083-v1/'
diroutput = basedir + '/spinco_data/SINON/outputs/data_exp_116083-v1/gathered'

# % find relevant files
files = glob.glob(dirinput + "data_exp*task*.csv", recursive=True)

# Decode identifiers of each task
filetags = { 'PM': ['krnm','ay71'], 
              '2FC':['uiag'],
              'LD': ['q399','7qgr']}

#%  for each task: find files, merge and add task tag to filename with merged tables
# ---------------------------------------
os.chdir(diroutput)

for taskname in filetags.keys():
    # find files for current 
    matching_files = [file for file in files if any(tag in file for tag in filetags[taskname])]

    #Read files of this taks and concatenate
    dfs = [pd.read_csv(taskfile) for taskfile in matching_files]
    concatenated_df = pd.concat(dfs, axis=0)
    
    # write to file 
    concatenated_df.to_csv('Concat_' + taskname + '.csv')

    #Split subjecs of each concatenated table (one table per task)
    concatenated_df['Participant Private ID'] = concatenated_df['Participant Private ID'].astype(str).str.replace('.0','')
    
    
    grouped =  concatenated_df.groupby('Participant Private ID')
        
    for name, group in grouped:
        os.mkdir(taskname + '_' + name)            
        group.to_csv(f'{taskname}_{name}/{taskname}_{name}.csv', index=False)
        