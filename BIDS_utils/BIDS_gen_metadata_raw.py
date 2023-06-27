# -*- coding: utf-8 -*-
""" Reorganize in BIDs structure
================================================================================
For each raw .bdf file save meta data: 
- .tsv file with electrode locations within each subject folder, e.g., s01_electrodes.tsv
- .json with chanCoordinate specifying the coordinate system
- .json EEG metadata:
    - Duration and sampling rate logged (read .bdf with MNE toolbox)
    - Description of task depending on task coded in the filename
    
Created on Thu May 25 11:35:12 2023
@author: gfraga
""" 
import re
import glob 
import os
import pandas as pd
import json
import mne

# paths 
baseDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
chanLocsFile =  os.path.join(baseDir,'Data','Electrode_locations','Biosemi_73ch_EEGlab_xyx.tsv')

# User inputs  
subjPattern = 'p002'
save_event_file = False 


# %% Subject loop 
# find subject Raw eeg files

subjectDir = os.path.join(baseDir,'Data','SiN','raw')
files = [files for files in glob.glob(os.path.join(subjectDir,'**','*.bdf'), recursive = True) if re.search(subjPattern + '.*', files)]
   
# %% 
for fileinput in files: 
    
    # Get folder, subject ID and task ID from fullfilename parts 
    subjID = os.path.basename(fileinput).replace('.bdf','').split('_')[0]
    taskID = os.path.basename(fileinput).replace('.bdf','').split('_')[1]
    diroutput = os.path.dirname(fileinput)
           
    # Read raw eeg data 
    raw = mne.io.read_raw_bdf(fileinput, preload=True,  infer_types=True)
    fileDuration = raw.n_times/ raw.info['sfreq']  
    fileSamplingRate = raw.info['sfreq']  
        
    # % Get events for event .tsv file
    # ------------------------------------------------------------------
    if save_event_file:      
        # find events 
        events = mne.find_events(raw,min_duration=0.002)
        events[:,0] = events[:,0] +1
        df_events = pd.DataFrame(events)
        df_events = df_events.rename(columns= {0:"SAMPLES", 1:"TRIAL_TYPE", 2:"VALUE"})
        df_events['ONSET'] = df_events['SAMPLES'] /  raw.info['sfreq']
        df_events['DURATION'] = 'n/a'
        df_events['RESPONSE'] = 'n/a'
                
        tsv_file_path = os.path.join(diroutput,subjID +  '_' + taskID + '_events.tsv')
        if not os.path.exists(tsv_file_path):
            df_events.to_csv(tsv_file_path, sep='\t', index=False)    
            print('---> added tsv file of events')        
        else:
            print("File already exists. Skipping saving the event .")            
         
        
    
    # %% Add copy of electrode coords in .tsv ( one per subject)
    # -----------------------------------------------------------------------------
    # % Read electrode locations 
    locs = pd.read_csv(chanLocsFile, delimiter = '\t', header = None)
    locs = locs.rename(columns={0:'Electrode',1:'x',2:'y',3:'z'})
       
    
    tsv_file_path = os.path.join(diroutput,subjID + '_electrodes.tsv')
    if not os.path.exists(tsv_file_path):
        locs.to_csv(tsv_file_path, sep='\t', index=False)    
        print('---> added copy of electrode coords')        
    else:
        print("File already exists. Skipping saving the electrode locations .")            
    
    # add json file to describe coordinate system
    chanCoords = {
        "EEG_coordinate_System": "EEGlab",
        "EEGCoordinateUnits": "mm",
        "EEGCoordinateSystemDescription": "https://eeglab.org/tutorials/ConceptsGuide/coordinateSystem.html",
        "IntendedFor":  subjID + "_electrodes.tsv"
        }
    
    with open(os.path.join(diroutput,subjID + '_coordsystem.json'), 'w') as ff:
        json.dump(chanCoords, ff, indent=1)
        print('---> saved coord system json')

    # %% Task information 
    # -----------------------------------------------------------------------------
      
    if "task_sin" in taskID:     
        task_descript = "A version of a speech intelligibility task using a coordinate response measure, based on Brungart et al.2001, DOI: 10.1121/1.1357812. German sentences are aurally presented either vocoded or with background noise, with 3 levels of difficulty. Each sentence has a fixed structure and 3 target items, which the subject must identify from 4 possible alternatives after each trial. Targets can be a call sign (Adler, Droessel, Kroete, Tiger), a color (gelb, gruen, rot, weiss) or a number (eins, zwei, drei, vier). A 3x4 grid is presented with images after each trial for the subject to click. The 64 possible combinations are presented in naturalistic synthesized speech with male and female voices." 
        task_instructions =  "Listen well and click on the images representing the words you heard after each trial (...)"
    
    elif 'task-rest'  in taskID:
        task_descript = "4 minutes eyes-closed resting state. A beep is used to indicate beginning and end of the four minutes."      
        task_instructions =  "Close your eyes and try to remain still as possible. After hearing the second beep you can open them again"
        
    
    
    # %% Make EEG json file at subject and task level with EEG recording details    
    metaData = {
            "ProjectName": "Speech in noise EEG", 
            "TaskName": taskID,  # extract from label in filename. e.g., s001_task-SIN.bdf
            "TaskDescription": task_descript,
            "Instructions": task_instructions, 
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

 


 