# -*- coding: utf-8 -*-

""" Helper script fro ANA_01
=================================================================
@author: samuemu

""" 
import mne
import MVPA.ANA_01_constants as const
import os
from glob import glob
import pandas as pd
import numpy as np

class EpochManager:
    def __init__(self, subjID):
        self.subjID = subjID
        self.thisDir = const.thisDir
        self.dirinput = os.path.join(self.thisDir[:self.thisDir.find('Scripts')] + 'Data','SiN','derivatives', const.pipeID, const.taskID + '_preproc_epoched',subjID)
        self.set_fp = glob(os.path.join(self.dirinput, str("*"+ const.setFileEnd)), recursive=True)[0]
        self.epo_fp = self.set_fp[:self.set_fp.find(const.setFileEnd)]+'-epo.fif'
        self.events_fp = glob(os.path.join(self.thisDir[:self.thisDir.find('Scripts')] + 'Data','SiN','derivatives', const.pipeID, const.taskID, subjID,"*accu.tsv"), recursive=True)[0]
        self.beh_fp = glob(os.path.join(self.thisDir[:self.thisDir.find('Scripts')] + 'Data','SiN','rawdata', subjID, const.taskID, 'beh',"*.csv"), recursive=True)[0]
    
    def readEpo(self):
        epo = mne.read_epochs(self.epo_fp)
        return epo
    
    def set2fif(self,fileinput=None,fileoutput=None,metadata=False):
        """ takes the epoched .set file from EEGLAB and returns an mne.Epochs object
        
        parameters: 
            fileinput : eeglab epoch file ending in .set (default is set_fp)
            fileoutput : where the mne file ending in .fif will be saved (default is epo_fp)
            metadata : if metadata should be constructed and added (default is false)
        """
        if fileinput is None:
            fileinput = self.set_fp
        if fileoutput is None:
            fileoutput = self.epo_fp
        epochs = mne.io.read_epochs_eeglab(fileinput)
        if metadata==True:
            epochs = self.AddMetadata(epochs)
        epochs.save(fileoutput, overwrite=True, fmt='double')
        epo = mne.read_epochs(fileoutput)
        return epo
    
    def AddMetadata(self, epochs):
        """ adds some metadata to the epochs. The metadata is taken from the
        accu.tsv file and the behavioural output .csv file
        
        """
        events_tsv = pd.read_csv(self.events_fp,sep='\t')
        beh_csv = pd.read_csv(self.beh_fp)
        
        # Adding the info from the tsv to the metadat array
        tmp = len(events_tsv) - events_tsv['ACCURACY'].isnull().sum()
        metadat = np.zeros(shape=(tmp,3))
        idx = 0
        for i in range(1,len(events_tsv)):
            if np.isnan(events_tsv['ACCURACY'][i]):
                continue
            else:
                metadat[idx] = [(events_tsv['SAMPLES'][i]),(events_tsv['VALUE'][i]),(events_tsv['ACCURACY'][i])]
                idx=idx+1
        
        # re-labelling the stim_codes to make them more legible        
        metadat=pd.DataFrame(metadat,columns=['tf','stim_code','accuracy'])
        metadat['accuracy'].replace(0,'inc', inplace=True)
        metadat['accuracy'].replace(1,'cor', inplace=True)
        metadat['block']=metadat['stim_code']
        metadat['block'].replace([111,112,113,114,121,122,123,124,131,132,133,134],'NV',inplace=True)
        metadat['block'].replace([211,212,213,214,221,222,223,224,231,232,233,234],'NV',inplace=True)
        metadat['stim']=metadat['stim_code']
        metadat['stim'].replace([111,112,113,114,211,212,213,214],'CallSign',inplace=True)
        metadat['stim'].replace([121,122,123,124,221,222,223,224],'Colour',inplace=True)
        metadat['stim'].replace([131,132,133,134,231,232,233,234],'Number',inplace=True)
        
        #adding the info from the csv to the metadat array
        beh_csv = beh_csv[['voice', 'levels', 'callSignCorrect','colourCorrect','numberCorrect']]
        beh_csv=beh_csv.replace(['-11db','0.2p'], 'Lv3')
        beh_csv=beh_csv.replace(['-9db','0.4p'], 'Lv2')
        beh_csv=beh_csv.replace(['-7db','0.6p'], 'Lv1')
        levels_metadat = list()
        voice_metadat = list()
        for i in range(1,len(beh_csv)):
            if str(beh_csv['levels'][i]).startswith('L'):
                if beh_csv['callSignCorrect'][i] != "NO_ANSW":
                    levels_metadat.append(beh_csv['levels'][i])
                    voice_metadat.append(beh_csv['voice'][i])
                if beh_csv['colourCorrect'][i] != "NO_ANSW":
                    levels_metadat.append(beh_csv['levels'][i])
                    voice_metadat.append(beh_csv['voice'][i])
                if beh_csv['numberCorrect'][i] != "NO_ANSW":
                    levels_metadat.append(beh_csv['levels'][i])
                    voice_metadat.append(beh_csv['voice'][i])
                    
        metadat['levels'] = levels_metadat
        metadat['voice'] = voice_metadat
        
        epochs.metadata = metadat
        return epochs
    