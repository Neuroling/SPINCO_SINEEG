# -*- coding: utf-8 -*-
""" Take a electrode_locations file and save it in BIDS Compatible format
================================================================================
- Save a .tsv copy of electrode locations within each subject folder, e.g., s01_electrodes.tsv
- Save an additional .json file with chanCoordinate specifications
- Save 

Created on Thu May 25 11:35:12 2023

@author: gfraga
""" 
import re
import glob 
import os
import pandas as pd
import json
import mne
# find base directory 
baseDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# %% Read electrode locations 
chanLocsFile =  os.path.join(baseDir,'Data','Electrode_locations','Biosemi_73ch_EEGlab_xyx.tsv')
locs = pd.read_csv(chanLocsFile, delimiter = '\t', header = None)
locs = locs.rename(columns={0:'Electrode',1:'x',2:'y',3:'z'})

# %% Subject loop 
# find subject Raw eeg files

subjectDir = os.path.join(baseDir,'Data','SiN','raw')
files = [files for files in glob.glob(os.path.join(subjectDir,'**','*.bdf'), recursive = True) if re.search('p0.*', files)]
   
# %% 
for fi in files: 
    # Get folder, subject ID and task ID from fullfilename parts 
    diroutput = os.path.dirname(fi)
    subjID = os.path.basename(fi).replace('.bdf','').split('_')[0]
    taskID = os.path.basename(fi).replace('.bdf','').split('_')[1]
        
    # Read raw eeg data 
    raw = mne.io.read_raw_bdf(fi, preload=True,  infer_types=True)
    fileDuration = raw.n_times/ raw.info['sfreq']  
    fileSamplingRate = raw.info['sfreq']  
        
   # %% Get events for event .tsv file
    events = mne.find_events(raw)   
    events[:,0] = events[:,0] +1
    df_events = pd.DataFrame(events)
    df_events=    df_events.rename(columns= {0:"SAMPLES", 1:"TRIAL_TYPE", 2:"VALUE"})
    df_events['ONSET'] = df_events['SAMPLES'] /  raw.info['sfreq']
    df_events['DURATION'] = 'n/a'
    df_events['RESPONSE'] = 'n/a'
    
    # %% add copy of electrode coords in .tsv ( one per subject)
    tsv_file_path = os.path.join(diroutput,subjID + '_electrodes.tsv')
    if not os.path.exists(tsv_file_path):
        locs.to_csv(tsv_file_path, sep='\t', index=False)    
        print('---> added copy of electrode coords')        
    else:
        print("File already exists. Skipping saving the electrode locations .")            
    
    # %% Make electrode coordinates  json file  
    chanCoords = {
        "EEG_coordinate_System": "EEGlab",
        "EEGCoordinateUnits": "mm",
        "EEGCoordinateSystemDescription": "https://eeglab.org/tutorials/ConceptsGuide/coordinateSystem.html",
        "IntendedFor":  subjID + "_electrodes.tsv"
        }
    
    with open(os.path.join(diroutput,subjID + '_coordsystem.json'), 'w') as ff:
        json.dump(chanCoords, ff, indent=1)
        print('---> saved EEG json')


    # %% Make EEG json file at subject and task level with EEG recording details    
    metaData = {
            "ProjectName": "Speech in noise EEG", 
            "TaskName": "Sentence in noise - SIN",  # conditional, depending on label in filename. e.g., s001_task-SIN.bdf
            "TaskDescription": "A version of a speech intelligibility task using a coordinate response measure, based on Brungart et al.2001, DOI: 10.1121/1.1357812. German sentences are aurally presented either vocoded or with background noise, with 3 levels of difficulty. Each sentence has a fixed structure and 3 target items, which the subject must identify from 4 possible alternatives after each trial. Targets can be a call sign (Adler, Droessel, Kroete, Tiger), a color (gelb, gruen, rot, weiss) or a number (eins, zwei, drei, vier). A 3x4 grid is presented with images after each trial for the subject to click. The 64 possible combinations are presented in naturalistic synthesized speech with male and female voices.", 
            "Instructions":"Listen well and click on the images representing the words you heard after each trial (...)", 
            "InstitutionAddress": "LiRI Linguistic Research Infrastructure, University of Zurich, Andreasstrasse 15, 8050 Zurich, Switzerland", 
            "InstitutionName": "LiRI Linguistic Research Infrastructure, University of Zurich",
            "PowerLineFrequencyHz": 50, 
            "Manufacturer": "BIOSEMI", 
            "ManufacturersModelName": "ActiveTwo MK2HS", 
            "RecordingType": "continuous", 
            "RecordingDurationSec": fileDuration, 
            "EEGPlacementScheme":"International 1020 systen", 
            "EEGReference": "CMS/DRL", 
            "SamplingFrequencyHz": fileSamplingRate, 
            "EEGChannelCount": 64, 
            "MiscChannelCount": 2, 
            "TriggerChannelCount": 1, 
            "EOGChannelCount": 4, 
            "ECGChannelCount": 0, 
            "EMGChannelCount": 0, 
            "SoftwareFilters": "n/a", 
            "HardwareFilters": "n/a" 
        }
    
    with open(os.path.join(diroutput, subjID + '_' + taskID + '_eeg.json'), 'w') as ff:
        json.dump(metaData, ff, indent=2)
        print('---> saved EEG json')

# %%

 


 
