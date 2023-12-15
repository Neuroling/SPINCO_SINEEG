# -*- coding: utf-8 -*-
"""
CROSS-CHECKING DURATION & OUTPUT SUMMARY
===================================================
Created on Fri Oct  6 15:05:37 2023
This was done to check that source to raw data conversion was OK, and to record the durations of all files
This script is not part of preprocessing or analysis 

Create a .csv file with recording durations of all subjects

- Reads the duration and sampling rate from the json file of each subject
- Reads the number of samples from the .set file of each subject
- Reads the number of events/triggers and the number of samples (= time frame 
    of the last trigger, which is the end of block 4) 
    from the s0NN_task-sin_events_accu.tsv file of each subject
- Divides the number of samples (from the tsv/set file) by the sampling frequency (from the json file)
    to receive recording duration in seconds (allows comparison to json file)
- Saves to csv file (if save == True)

WARNING: looping over subjects will load the .set file of a subject and assign the variable "data_set" to it,
         then append the relevant info to the lists, then delete the object "data_set" to free up space,
         then move on to the next subject. However, data_set still seems to be loaded in the memory
         even after running <del data_set>, which requires a ton of RAM. [Need to fix abcde]
         
         --> If you don't have enough RAM, the kernel will force a restart and all progress will be lost.
         This happens when processing s002 with 16GB RAM, and when processing s004 with 32GB, meaning it 
         will likely require as much as 128GB RAM to process all 14 subjects.
         
         To make this reproducible even without having access to 128GB of RAM, I have added the 
         "MANUAL ENTRY" option below. For instructions on how to use it, go to the "MANUAL ENTRY" section.
         Be aware that this option is more prone to human-error, so if the output shows a different duration
         of the set file than the others, look here first.
         To disable it, set "manual" to False

@author: samuemu
"""

import os 
import pandas as pd 
import json
import mne

#%% User inputs
taskID = 'task-sin'
save = False # if True it will save csv file
manual = False # if False it will loop over all subj automatically (requires lots of RAM); 
# if True, see "MANUAL ENTRY" section below for instructions

#%% PATHS
thisDir = os.path.dirname(os.path.abspath(__file__))
diroutput= os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')
## below: Don't save subjIDs of the pilots or discarded subj (Only those ending with a digit)
subIDs= [item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]

#%% Create empty lists
filepaths_json = list()
durations_json = list()

filepaths_tsv  = list()
durations_tsv  = list()
samples_tsv   =  list()
n_events_tsv  =  list()

filepaths_set = list()
durations_set = list()
samples_set = list()

done = False # This is so it will only combine the lists into a datadframe if all necessary info is collected

#%% MANUAL ENTRY
if manual == True:
    
    """
    INSTRUCTIONS:
        Run the script, then copy+paste the number printed in the console ("s0** samples_set: [number]")
        as an entry to the dict samples_set (with the subjID as key). Then restart the kernel
        add +1 to the list_nr . Then re-run. Do this until the "done" message appears.
        
        Change the "max_processing" variable as needed. To see how many subjects your machine can handle,
        set manual to False, then wait and see how many were able to be processed before the kernel restarts.
    
    """
    
    ## ENTRIES
    samples_set={'s001':7633451, 's002':6968746, 's003':7494506, 's004':7379922, 's005':6920429, 
                 's006':7394664, 's007':6946771, 's008':8218416, 's009':7468062, 's010':7040777, 
                 's011':8208076, 's012':8175488, 's013':6862386, 's015':6880435}
    list_nr = 0 # which of the sublists to run (start with 0)
    max_processing = 3 # How many subj to process before requiring a restart of the kernel
    
    # This will create sublists of subIDs, each with a maximum number of entries specified in max_processing
    sublists = []
    for i in range(0, len(subIDs), max_processing):
        temp = subIDs[i:i+max_processing]
        sublists.append(temp)

    if len(samples_set) != len(subIDs):
        for subID in sublists[list_nr]:   
            dirinput=os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subID,taskID, 'eeg')
            rawdata = os.listdir(dirinput)
            print('_.~"(_.~"(_.~"(_.~"(_.~"(  now processing '+subID+'  _.~"(_.~"(_.~"(_.~"(_.~"(')
            ## open .set files, read duration, append it to list
            for file in rawdata:
                if file.endswith(".set") and file[3].isdigit():
                    # If the file is a ser file, get its filepath
                    fp = os.path.join(dirinput, file)
                    
                    # read number of samples
                    #filepaths_set.append(fp)
                    data_set = mne.io.read_raw_eeglab(fp)                 
                    print(subID + ' samples_set: '+str(len(data_set.times)))
                    
    else: # if the samples_set dict is complete, get the info from the json and tsv files
        print('finished processing set files. Now extracting durations from json and tsv files')
        for subID in subIDs:   
            dirinput=os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subID,taskID, 'eeg')
            rawdata = os.listdir(dirinput)
            
            # save filepaths to set files
            for file in rawdata:
                if file.endswith(".set") and file[3].isdigit():
                    # If the file is a ser file, get its filepath
                    fp = os.path.join(dirinput, file)
                    
                    # append filepaths, sample Nr, and duration
                    filepaths_set.append(fp)
                    
            ## open json files, read duration, append it to list
            for file in rawdata:
                if file.endswith("eeg.json") and file[3].isdigit():
                    # If the file is a json file, get its filepath
                    fp = os.path.join(dirinput, file)
                    filepaths_json.append(fp)
                    with open(fp, 'r') as f:
                        data_json = json.load(f)
                    durations_json.append(data_json['RecordingDurationSec'])
                    SamplingFrequencyHz= data_json['SamplingFrequencyHz']
                    
            ## open tsv files, read duration, divide duration by sampling frequency, append to list
            dirinput=os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives_SM',taskID,subID)
            rawdata = os.listdir(dirinput)
            for file in rawdata:
                if file.endswith("accu.tsv") and file[3].isdigit():
                    # If the file is a tsv file, get its filepath
                    fp = os.path.join(dirinput, file)
                    filepaths_tsv.append(fp)
                    data_tsv = pd.read_csv(fp,sep='\t')
                    temp = data_tsv.iloc[-1:]['SAMPLES'] # Read n of samples (last row)
                    samples = int(temp.iloc[0]) # Get value as int instead of pd series
                    samples_tsv.append(samples)
                    durations_tsv.append(samples/SamplingFrequencyHz)
                    n_events_tsv.append(len(data_tsv))
                    
        samples_set = list(samples_set.values()) # converting the dict to a list
        durations_set = [ i / SamplingFrequencyHz for i in samples_set]
        print('.-~-.-~-.-~.-~-.-~-.-~ done .-~-.-~-.-~.-~-.-~-.-~')
        done = True
#%%
else:  # if manual is disabled      
       
    #%% loop over all subj: first read json files and append duration to list, then do the same for tsv files
    for subID in subIDs:   
        dirinput=os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata', subID,taskID, 'eeg')
        rawdata = os.listdir(dirinput)
        print('_.~"(_.~"(_.~"(_.~"(_.~"(  now processing '+subID+'  _.~"(_.~"(_.~"(_.~"(_.~"(')
        
        ## open json files, read duration, append it to list
        for file in rawdata:
            if file.endswith("eeg.json") and file[3].isdigit():
                # If the file is a json file, get its filepath
                fp = os.path.join(dirinput, file)
                filepaths_json.append(fp)
                with open(fp, 'r') as f:
                    data_json = json.load(f)
                durations_json.append(data_json['RecordingDurationSec'])
                SamplingFrequencyHz= data_json['SamplingFrequencyHz']
                  
            ## open .set files, read duration, append it to list
            for file in rawdata:
                if file.endswith(".set") and file[3].isdigit():
                    # If the file is a ser file, get its filepath
                    fp = os.path.join(dirinput, file)
                    
                    # append filepaths, sample Nr, and duration
                    filepaths_set.append(fp)
                    data_set = mne.io.read_raw_eeglab(fp)
                    samples_set.append(len(data_set.times))
                    durations_set.append(len(data_set.times)/SamplingFrequencyHz)
                    
                    print('samples_set: '+str(len(data_set.times)))
                    print('durations_set: ' +str(len(data_set.times)/SamplingFrequencyHz))
                    
                    # delete to free up space, because data is a huge object
                    for name in dir():
                        if name=='data_set':
                            del globals()[name] 
                
        ## open tsv files, read duration, divide duration by sampling frequency, append to list
        dirinput=os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','derivatives_SM',taskID,subID)
        rawdata = os.listdir(dirinput)
        for file in rawdata:
            if file.endswith("accu.tsv") and file[3].isdigit():
                # If the file is a tsv file, get its filepath
                fp = os.path.join(dirinput, file)
                filepaths_tsv.append(fp)
                data_tsv = pd.read_csv(fp,sep='\t')
                temp = data_tsv.iloc[-1:]['SAMPLES'] # Read n of samples (last row)
                samples = int(temp.iloc[0]) # Get value as int instead of pd series
                samples_tsv.append(samples)
                durations_tsv.append(samples/SamplingFrequencyHz)
                n_events_tsv.append(len(data_tsv))
                
                print('samples_tsv: '+str(samples))
                print('durations_tsv: '+str(samples/SamplingFrequencyHz))
        done = True

#%%
if done == True:
    #%% Create dataframe from the lists
    df = pd.DataFrame(list(zip(subIDs, durations_json, filepaths_json, 
                               durations_set, samples_set, filepaths_set,
                               durations_tsv, samples_tsv, n_events_tsv, filepaths_tsv)), 
                      columns =['subjID', 'duration_json', 'filepath_json', 
                                'duration_set', 'n_samples_set', 'filepath_set',
                                'duration_tsv', 'n_samples_tsv', 'n_events_tsv',
                                'filepath_tsv'])
    
    #%% save dataframe
    if save == True:
        df.to_csv(os.path.join(diroutput,'recording_durations.csv'))
        print('saved to '+os.path.join(diroutput,'recording_durations.csv'))
