# -*- coding: utf-8 -*-

""" Helper script for EPO_runner
=================================================================
@author: samuemu

This script contains all the functions needed to deal with MNE epoching.
It requires EPO_constants for things that don't change across files.
The functions are called by EPO_runner

""" 
import mne

import os
from glob import glob
import pandas as pd
import numpy as np
thisDir = os.path.dirname(os.path.abspath(__file__))
import EPO_constants as const

class EpochManager:
    """
    EpochManager is an object to handle reading & saving epochs and related things like metadata and event_ids.
    Calling this object requires a SubjID as an input, which will be used to determine file paths.
    It must therefore be called seperately for each subject.
    
    """
    
    def __init__(self, subjID):
        """
        initialising function for EpochManager, used to determine file paths

        Parameters
        ----------
        subjID : subject ID

        """
        self.subjID = subjID
        self.thisDir = const.thisDir
        self.dirinput = os.path.join(self.thisDir[:self.thisDir.find('Scripts')] + 'Data','SiN','derivatives', const.pipeID, const.taskID + '_preproc_epoched',subjID)
        self.set_fp = glob(os.path.join(self.dirinput, str("*"+ const.setFileEnd)), recursive=True)[0]
        self.epo_fp = self.set_fp[:self.set_fp.find(const.setFileEnd)]+'-epo.fif'
        self.events_fp = glob(os.path.join(self.thisDir[:self.thisDir.find('Scripts')] + 'Data','SiN','derivatives', const.pipeID, const.taskID, subjID,"*accu.tsv"), recursive=True)[0]
        self.beh_fp = glob(os.path.join(self.thisDir[:self.thisDir.find('Scripts')] + 'Data','SiN','rawdata', subjID, const.taskID, 'beh',"*.csv"), recursive=True)[0]
    
    def readEpo(self):
        """
        reads the epoched .fif file using the filepaths set by EpochManager
        """
        epo = mne.read_epochs(self.epo_fp)
        return epo
    
    def set2fif(self,fileinput=None,fileoutput=None,addMetadata=False,relabelEvents=False):
        """ takes the epoched .set file from EEGLAB and saves it as .fif file from MNE
        
        parameters: 
            fileinput : eeglab epoch file ending in .set (default is None, which will use the set_fp from EpochManager.__init__)
            fileoutput : where the mne file ending in .fif will be saved (default is None, which will use the epo_fp from EpochManager.__init__)
            addMetadata : if metadata should be constructed and added (default is false)
            relabelEvents: if events should be relabelled (default is false)
        
        returns:
            Nothing. To open the freshly saved epoch, call EpochManager.readEpo()
        """
        if relabelEvents==True and addMetadata==False:
            print('warning: metadata will be constructed to relabel events but will not be added')
        if fileinput is None:
            fileinput = self.set_fp
        if fileoutput is None:
            fileoutput = self.epo_fp
        epochs = mne.io.read_epochs_eeglab(fileinput)
        if addMetadata==True:
            epochs = self.addMetadata(epochs)
        if relabelEvents==True:
            epochs = self.relabelEvents(epochs)
        epochs.save(fileoutput, overwrite=True, fmt='double')

    
    def constructMetadata(self, epochs):
        """ constructs some metadata for the epochs. The metadata is taken from the
        accu.tsv file and the behavioural output .csv file
        
        This function is called by addMetadata
        
        """
        events_tsv = pd.read_csv(self.events_fp,sep='\t')
        beh_csv = pd.read_csv(self.beh_fp)
        
        ## Adding the info from the tsv to the metadat array
        tmp = len(events_tsv) - events_tsv['ACCURACY'].isnull().sum()
        metadat = np.zeros(shape=(tmp,3))
        idx = 0
        for i in range(1,len(events_tsv)):
            if np.isnan(events_tsv['ACCURACY'][i]):
                continue
            else:
                metadat[idx] = [(events_tsv['SAMPLES'][i]),(events_tsv['VALUE'][i]),(events_tsv['ACCURACY'][i])]
                idx=idx+1
        
        ## re-labelling the stim_codes to make them more legible        
        metadat=pd.DataFrame(metadat,columns=['tf','stim_code','accuracy'])
        metadat['accuracy'].replace(0,'inc', inplace=True)
        metadat['accuracy'].replace(1,'cor', inplace=True)
        metadat['block']=metadat['stim_code']
        metadat['block'].replace([111,112,113,114,121,122,123,124,131,132,133,134],'NV',inplace=True)
        metadat['block'].replace([211,212,213,214,221,222,223,224,231,232,233,234],'SSN',inplace=True)
        metadat['stim']=metadat['stim_code']
        metadat['stim'].replace([111,112,113,114,211,212,213,214],'CallSign',inplace=True)
        metadat['stim'].replace([121,122,123,124,221,222,223,224],'Colour',inplace=True)
        metadat['stim'].replace([131,132,133,134,231,232,233,234],'Number',inplace=True)
        
        ## reading the info from the csv to the metadat array
        beh_csv = beh_csv[['voice', 'levels', 'callSignCorrect','colourCorrect','numberCorrect']]
        beh_csv=beh_csv.replace(['-11db','0.2p'], 'Lv3')
        beh_csv=beh_csv.replace(['-9db','0.4p'], 'Lv2')
        beh_csv=beh_csv.replace(['-7db','0.6p'], 'Lv1')
        levels_metadat = list()
        voice_metadat = list()
        
        ## excluding trials with no response
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
        
        ## adding it to the metadata
        metadat['levels'] = levels_metadat
        metadat['voice'] = voice_metadat
        self.metadata = metadat
        
    def addMetadata(self,epochs):
        """
        adds metadata to the epochs
        metadata is constructed by calling constructMetadata

        """
        self.constructMetadata(epochs)
        epochs.metadata = self.metadata
        return epochs
    
    def relabelEvents(self,epochs,metadata=None):
        """
        relabels events and event_id using the metadata.
        event_id dict is taken from constants
        

        Parameters
        ----------
        epochs : epochs.EpochsFIF
            the epoched data
        metadata : metadata. Default is None, which will use the metadata from constructMetadata

        Returns
        -------
        epochs : epochs.EpochsFIF
            epoched data with relabelled events and event_id
        """
        if metadata != None:
            mtdat = metadata
        elif 'self.metadata' in locals():
            mtdat = self.metadata
            print('hey sam, it works (line 169) :D')
        else:
            self.constructMetadata(epochs)
            print('constructing metadata')
            mtdat = self.metadata
        
        mtdat['block'].replace('NV',1,inplace=True)
        mtdat['block'].replace('SSN',2,inplace=True)
        mtdat['stim'].replace('CallSign',1,inplace=True)
        mtdat['stim'].replace('Colour',2,inplace=True)
        mtdat['stim'].replace('Number',3,inplace=True)
        mtdat['levels'].replace('Lv1',1, inplace=True)
        mtdat['levels'].replace('Lv2',2, inplace=True)
        mtdat['levels'].replace('Lv3',3, inplace=True)
        mtdat['accuracy'].replace('inc',0, inplace=True)
        mtdat['accuracy'].replace('cor',1, inplace=True)
        mtdat['voice'].replace('Neural2-F',1,inplace=True)
        mtdat['voice'].replace('Neural2-D',2,inplace=True)
        
        for epIdx in range(len(epochs.events)):
            epochs.events[epIdx][2]=mtdat['block'][epIdx]*10000+ mtdat['stim'][epIdx]*1000+ mtdat['levels'][epIdx]*100+ mtdat['accuracy'][epIdx]*10+ mtdat['voice'][epIdx]
        epochs.event_id = const.event_id       
        return epochs
  
    