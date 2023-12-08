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
thisDir = os.getcwd()
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
        self.set_path = glob(os.path.join(self.dirinput, str("*"+ const.setFileEnd)), recursive=True)[0]
        self.epo_path = self.set_path[:self.set_path.find(const.setFileEnd)]+const.fifFileEnd
        self.events_path = glob(os.path.join(self.thisDir[:self.thisDir.find('Scripts')] + 'Data','SiN','derivatives', const.pipeID, const.taskID, subjID,"*accu.tsv"), recursive=True)[0]
        self.beh_path = glob(os.path.join(self.thisDir[:self.thisDir.find('Scripts')] + 'Data','SiN','rawdata', subjID, const.taskID, 'beh',"*.csv"), recursive=True)[0]
    
    
    def readEpo(self):
        """
        reads the epoched .fif file using the filepaths set by EpochManager
        """
        epo = mne.read_epochs(self.epo_path)
        return epo
    
    
    def set2fif(self,fileinput=None,fileoutput=None,addMetadata=False,relabelEvents=False):
        """ takes the epoched .set file from EEGLAB and saves it as .fif file from MNE
        
        parameters: 
            fileinput : eeglab epoch file ending in .set (default is None, which will use the set_path from EpochManager.__init__)
            fileoutput : where the mne file ending in .fif will be saved (default is None, which will use the epo_path from EpochManager.__init__)
            addMetadata : if metadata should be constructed and added (default is false)
            relabelEvents: if events should be relabelled (default is false)
        
        returns:
            Nothing. To open the freshly saved epoch, call EpochManager.readEpo()
        """
        if relabelEvents==True and addMetadata==False:
            print('warning: metadata will be constructed to relabel events but will not be added')
        if fileinput is None:
            fileinput = self.set_path
        if fileoutput is None:
            fileoutput = self.epo_path
        epochs = mne.io.read_epochs_eeglab(fileinput)
        if addMetadata==True:
            epochs = self.addMetadata(epochs)
        if relabelEvents==True:
            epochs = self.relabelEvents(epochs)
        epochs.save(fileoutput, overwrite=True, fmt='double')


    def addMetadata(self,epochs):
        """
        adds metadata to the epochs
        metadata is constructed by calling constructMetadata
        
        This function is called by set2fif (optional)

        """
        self.constructMetadata()
        epochs.metadata = self.metadata
        return epochs
    
    
    def constructMetadata(self):
        """ constructs some metadata for the epochs, using the accu.tsv file and the behavioural output .csv file. 
        Filepaths are handled by EpochManager.__init__
        
        This function is called by addMetadata and by relabelEvents (optional)
        
        Returns:
            metadata
        """
        # Reading files
        events_tsv = pd.read_csv(self.events_path,sep='\t')
        beh_csv = pd.read_csv(self.beh_path)
        
        ## Adding the info from the tsv to the metadat array, skipping missed responses
        tmp = len(events_tsv) - events_tsv['ACCURACY'].isnull().sum()
        metadat = np.zeros(shape=(tmp,3))
        idx = 0
        for i in range(1,len(events_tsv)):
            if np.isnan(events_tsv['ACCURACY'][i]):
                continue
            else:
                metadat[idx] = [(events_tsv['SAMPLES'][i]),(events_tsv['VALUE'][i]),(events_tsv['ACCURACY'][i])]
                idx=idx+1
        
        ## adding columns for block, stimulus type and accuracy and renaming everything to be more leigble    
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
        
        ## exclude trials with no response
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
        
        ## adding it to the metadat array
        metadat['levels'] = levels_metadat
        metadat['voice'] = voice_metadat
        self.metadata = metadat
        return metadat
        

    def relabelEvents(self,epochs,metadata=None):
        """
        relabels events and event_id using the metadata.
        event_id dict is taken from constants
        
        This function is called by set2fif (optional)
        This function calls constructMetadata (optional)
        

        Parameters
        ----------
        epochs : epochs.EpochsFIF
            the epoched data
        metadata : metadata. Default is None, which will call constructMetadata

        Returns
        -------
        epochs : epochs.EpochsFIF
            epoched data with relabelled events and event_id
        """
        
        
        if metadata == None: # use the specified metadata or construct new one
        
        ## This option below is a bit more efficient but prone to error (if metadata from 
        ## a previous subject is still saved, it might carry that over to the new subject)
        
            # try: # if there is already a metadata saved, use that. 
            #     mtdat= self.metadata
            # except NameError:
            #     self.constructMetadata()
            #     mtdat = self.metadata
            
        ## This method is a bit less efficient but does not risk that error    
            mtdat = self.constructMetadata()
            
        else:
            mtdat = metadata
        
        #recoding the metadata because epochs.events need to be numeric
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
        
        # put the recoded metadata together to create numeric codes
        for epIdx in range(len(epochs.events)):
            epochs.events[epIdx][2]=mtdat['stim_code'][epIdx]*1000+ mtdat['levels'][epIdx]*100+ mtdat['accuracy'][epIdx]*10+ mtdat['voice'][epIdx]
        epochs.event_id = const.event_id # using the   event_id dict from the constants
        return epochs
    
    def countEventFrequency(self,epoch=0):
        """
        Creates a table listing all event_id codes, labels and their frequency of occurrence.
        
        If the events are not first relabelled (using relabelEvents), it give an error
        
        Currently, this function only returns the frequency table but does not save it.
        This function is not called by any other function.
        This function calls createEmptyFrequencyDict (see more info on why in the documentation for that function)
        

        Parameters
        ----------
        epoch : epochs.EpochsFIF - Default is 0, which will call readEpo

        Returns
        -------
        df : pandas dataframe

        """
        if epoch == 0: # if no epoch structure is given, then first read the epoch file
            epoch = self.readEpo()
            
        # create empty dict (see documentation of createEmptyFrequencyDict() for more information)    
        self.createEmptyFrequencyDict()
        freqCount = self.freqCountEmpty 
        
        events = epoch.events[:,2] #making an array out of all recorded event ids
        
        # Go through array elements and count frequencies
        for i in range(len(events)): #for each index in events, add +1 to the key of the corresponding event in freqCount
            freqCount[events[i]] += 1
        
        df = pd.DataFrame(freqCount.items(),columns=["event_id","frequency"])
        df.insert(1,"events",const.all_event_labels)
        
        return df
    
    def createEmptyFrequencyDict(self):
        """
        This function creates a dict with all event_ids (from the constants) as keys 
        and assign the value 0 to every key (essentially creating an empty frequency count dict).
        
        self.freqCountEmpty is created every time countEventFrequency is called,
        and is then filled with the frequency counts in the same function.
        
        We cannot just create freqCountEmpty in the constants and then fill that,
        because of python's variable assignment system: if we do <freqCount = const.freqCountEmpty>
        and then fill freqCount, then const.freqCountEmpty would be updated as well.
        Which would mean that if the function countEventFrequency is called again, the
        const.freqCountEmpty would not be empty, and the new freqCount would be added 
        cumulatively to the old freqCount.
        
        Hence the creation of a new dict for freqCountEmpty with every time countEventFrequency is called.

        """
        self.freqCountEmpty = dict()
        for i in range(len(const.all_event_ids)):
            self.freqCountEmpty[const.all_event_ids[i]] = 0
        
        
        

  
    