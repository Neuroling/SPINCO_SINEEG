# -*- coding: utf-8 -*-

""" 
Function script for EPO_runner
===============================================================================
@author: samuemu
Created November 2023

This script contains all the functions needed to deal with MNE epoching, such as 
importing from EEGLAB .set files, relabelling events, adding metadata, and creating
a frequency of occurrence table for the events.

These functions are called by EPO_runner, and require EPO_constants for variables 
that do not change across files.

"""
import EPO_constants as const
import mne

import os
from glob import glob
import pandas as pd
import numpy as np
thisDir = os.getcwd()


class EpochManager:
    """
    EpochManager is an object to handle reading & saving epochs and related things like metadata and event_ids.
    Initialising this object requires a SubjID as an input, which will be used to determine file paths.
    It must therefore be called seperately for each subject.
    
    Additionally, when initialising EpochManager, you can specify if the .set files from the pipeline used in
    S. Meier's MSc thesis shall be used (SM = True) or not. This is optional. Default is False. 
    See help(EpochManager.__init__) for more information

    """

    def __init__(self, subjID, SM=False):
        """
        initialising function for EpochManager, used to determine file paths
        

        Parameters
        ----------
        subjID : str
            subject ID
        
        SM : bool
            If true, will use the derivatives_SM data. Default is False.

        """
        self.subjID = subjID
        self.thisDir = const.thisDir
        
        if SM == False:
            self.dirinput = os.path.join(self.thisDir[:self.thisDir.find(
                'Scripts')] + 'Data', 'SiN', 'derivatives', const.pipeID, const.taskID + '_preproc_epoched', subjID)
            
            self.set_path = glob(os.path.join(self.dirinput, str(
                "*" + const.setFileEnd)), recursive=True)[0]
            
            self.epo_path = self.set_path[:self.set_path.find(
                const.setFileEnd)]+const.fifFileEnd
            
        else:
            self.dirinput = os.path.join(self.thisDir[:self.thisDir.find(
                'Scripts')] + 'Data', 'SiN', 'derivatives_SM', const.taskID, subjID)
            
            self.set_path = glob(os.path.join(self.dirinput, str(
                "*" + const.setFileEnd_SM)), recursive=True)[0]
            
            self.epo_path = self.set_path[:self.set_path.find(
                const.setFileEnd_SM)]+const.fifFileEnd_SM
                
        
        self.events_path = glob(os.path.join(self.thisDir[:self.thisDir.find(
            'Scripts')] + 'Data', 'SiN', 'derivatives', const.pipeID, const.taskID, subjID, "*accu.tsv"), recursive=True)[0]
        
        self.beh_path = glob(os.path.join(self.thisDir[:self.thisDir.find(
            'Scripts')] + 'Data', 'SiN', 'rawdata', subjID, const.taskID, 'beh', "*.csv"), recursive=True)[0]
        
        self.freqTable_path = os.path.join(
            self.dirinput[:self.dirinput.find(subjID)], const.freqTableEnd)

    def readEpo(self, fileinput=None):
        """
        READ EPOCHED MNE .fif FILE
        =======================================================================
        
        reads the epoched .fif file using the filepaths set by EpochManager
        Alternatively, filepaths can be provided manually with the fileinput parameter
        
        This obviously necessitates the existence of epoched .fif files.
        To create epoched .fif files from .set files, call EpochManager.set2fif()

        Parameters
        ----------
            fileinput : str | None
                Filepath to the epoched .fif file. If = None, will use the filepaths set by EpochManager

        returns
        -------
            epo : mne.Epochs instance
        """
        if fileinput is None:
            fileinput = self.epo_path

        print('¸.·´¯`·.¸><(((º>   reading epoched data of ' + self.subjID)
        epo = mne.read_epochs(fileinput)
        return epo

    def set2fif(self,
                fileinput=None,
                fileoutput=None,
                applyAverageReference=False,
                addMetadata=True,
                relabelEvents=True,
                ):
        """ 
        CONVERT .set FILE TO .fif FILE
        =======================================================================
        takes the epoched .set file from EEGLAB and saves it as .fif file from MNE

        Parameters
        ----------
            fileinput : str | None
                filepath for the eeglab epoch file ending in .set 
                default is None, which will use the set_path from EpochManager.__init__

            fileoutput : str | None
                where the mne file ending in .fif will be saved 
                default is None, which will use the epo_path from EpochManager.__init__

            applyAverageReference : bool | Default False
                if = True, will re-reference the data to average reference. 
                Default is False.

            addMetadata : bool | Default True
                if metadata should be constructed and added
                The metadata contains trial information
                It is added with the function EpochManager.addMetadata()

            relabelEvents: bool | Default True
                if events should be relabelled 
                Relabelled events will allow easier sorting and filtering of data.
                The function EpochManager.relabelEvents() will be used for this.
                For more information, see help(EpochManager.relabelEvents)
                
        returns
        -------
            Nothing. To open the freshly saved epoch, call EpochManager.readEpo()
        """

        if relabelEvents == True and addMetadata == False:
            print(
                '---> metadata will be constructed to relabel events but will not be added')

        if fileinput is None:
            fileinput = self.set_path

        if fileoutput is None:
            fileoutput = self.epo_path

        print('¸.·´¯`·.¸><(((º>   reading epoched data for ' + self.subjID)
        epochs = mne.io.read_epochs_eeglab(fileinput)

        if applyAverageReference:
            print('¸.·´¯`·.¸><(((º>   applying average reference')
            epochs = epochs.set_eeg_reference()

        if addMetadata == True:
            epochs = self.addMetadata(epochs)

        if relabelEvents == True:
            epochs = self.relabelEvents(epochs)
        
        epochs.comment = 'based on EEGlab file from '+fileinput

        print('¸.·´¯`·.¸><(((º>   saving epoched .fif file to '+fileoutput)
        epochs.save(fileoutput, overwrite=True, fmt='double')
        print('_.~"~._.~"~._.~"~._.~"~._ Done. _.~"~._.~"~._.~"~._.~"~._')

    def addMetadata(self, epochs):
        """
        ADDING METADATA TO EPOCHS
        =======================================================================
        
        Adds metadata to the epochs.
        Metadata stores trial information (like condition, accuracy, etc.) for each epoch.
        It is constructed with EpochManager.constructMetadata()
        For more information, see docsting of that function

        This function is called by EpochManager.set2fif (optional)
        
        Parameters
        ----------
        epochs : MNE.EpochsFIF object
            the epoched data
        """
        self.constructMetadata()
        epochs.metadata = self.metadata
        print('¸.·´¯`·.¸><(((º>   adding metadata')
        return epochs

    def constructMetadata(self):
        """ 
        CONSTRUCT METADATA 
        =======================================================================
        
        Using the accu.tsv file and the behavioural output .csv file, this function compiles
        metadata ( = trial information for each epoch).
        As part of this, stimulus triggers will be translated into human-readable labels
        
        Filepaths are handled by EpochManager.__init__

        This function is called by:
            addMetadata
            relabelEvents (optional)

        Returns:
            metadata
        """

        # Reading files
        events_tsv = pd.read_csv(self.events_path, sep='\t')
        beh_csv = pd.read_csv(self.beh_path)

        print('¸.·´¯`·.¸><(((º>   constructing metadata from ' +
              self.events_path +' and '+self.beh_path)

        # Adding the info from the tsv to the metadat array, skipping missed responses
        tmp = len(events_tsv) - events_tsv['ACCURACY'].isnull().sum()
        metadat = np.zeros(shape=(tmp, 3))
        idx = 0
        for i in range(1, len(events_tsv)):
            if np.isnan(events_tsv['ACCURACY'][i]):
                continue
            else:
                metadat[idx] = [(events_tsv['SAMPLES'][i]),
                                (events_tsv['VALUE'][i]), (events_tsv['ACCURACY'][i])]
                idx = idx+1

        # adding columns for block, stimulus type and accuracy and renaming everything to be more leigble
        metadat = pd.DataFrame(
            metadat, columns=['tf', 'stim_code', 'accuracy'])
        metadat['accuracy'].replace(0, 'inc', inplace=True)
        metadat['accuracy'].replace(1, 'cor', inplace=True)
        metadat['block'] = metadat['stim_code']
        metadat['block'].replace(
            [111, 112, 113, 114, 121, 122, 123, 124, 131, 132, 133, 134], 'NV', inplace=True)
        metadat['block'].replace(
            [211, 212, 213, 214, 221, 222, 223, 224, 231, 232, 233, 234], 'SSN', inplace=True)
        metadat['stimtype'] = metadat['stim_code']
        metadat['stimtype'].replace(
            [111, 112, 113, 114, 211, 212, 213, 214], 'CallSign', inplace=True)
        metadat['stimtype'].replace(
            [121, 122, 123, 124, 221, 222, 223, 224], 'Colour', inplace=True)
        metadat['stimtype'].replace(
            [131, 132, 133, 134, 231, 232, 233, 234], 'Number', inplace=True)
        metadat['stimulus'] = metadat['stim_code']
        metadat['stimulus'].replace(
            [111, 121, 131, 211, 221, 231], 'Stim1', inplace=True)
        metadat['stimulus'].replace(
            [112, 122, 132, 212, 222, 232], 'Stim2', inplace=True)
        metadat['stimulus'].replace(
            [113, 123, 133, 213, 223, 233], 'Stim3', inplace=True)
        metadat['stimulus'].replace(
            [114, 124, 134, 214, 224, 234], 'Stim4', inplace=True)

        # reading the info from the csv to the metadat array
        beh_csv = beh_csv[['voice', 'levels',
                           'callSignCorrect', 'colourCorrect', 'numberCorrect']]
        beh_csv = beh_csv.replace(['-11db', '0.2p'], 'Lv3')
        beh_csv = beh_csv.replace(['-9db', '0.4p'], 'Lv2')
        beh_csv = beh_csv.replace(['-7db', '0.6p'], 'Lv1')
        levels_metadat = list()
        voice_metadat = list()

        # exclude trials with no response
        for i in range(1, len(beh_csv)):
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

        # adding it to the metadat array
        metadat['levels'] = levels_metadat
        metadat['voice'] = voice_metadat
        self.metadata = metadat
        return metadat

    def relabelEvents(self, epochs, metadata=None):
        """
        relabels events and event_id using the metadata.
        event_id dict is taken from constants

        This function is called by set2fif (optional)
        This function calls constructMetadata (optional)
        
        -----------------------------------------------------------------------
        
        These are the event labels:
            NoiseType / StimulusType / DegradationLevel / Accuracy / Voice
            
            X_____ NoiseType: NV = 1, SSN = 2
            _X____ Stimulus Type: Call = 1, Colour = 2, Number = 3
            __X___ Stimulus: Adler/Gelb/Eins = 1, Drossel/Grün/Zwei = 2, Kröte/Rot/Drei = 3, Tiger/Weiss/Vier = 4
            ___X__ Degradation Level: Lv1 = 1, Lv2 = 2, Lv3 = 3
            ____X_ Accuracy: Incorrect = 0, Correct = 1
            _____X Voice: Feminine (Neural2-F) = 1, Masculine (Neural2-D) = 2
            
        This allows you to filter the epochs using the event labels, i.e. by:
            epochs.__getitem__('NV') --------> will return all epochs with NV
            epochs.__getitem__('Lv1/call') --> will return all epochs with Lv1 degradation and CallSign


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

        if metadata == None:  # use the specified metadata or construct new one
            try: # if there is already a metadata saved in the workspace, use that.
                mtdat= self.metadata
            except NameError: # if you get an error saying that self.metadata doesn't exist, construct new one
                self.constructMetadata()
                mtdat = self.metadata
        else:
            mtdat = metadata
        
        print('¸.·´¯`·.¸><(((º>   relabelling events')

        # recoding the metadata because epochs.events need to be numeric
        mtdat['levels'].replace('Lv1', 1, inplace=True)
        mtdat['levels'].replace('Lv2', 2, inplace=True)
        mtdat['levels'].replace('Lv3', 3, inplace=True)
        mtdat['accuracy'].replace('inc', 0, inplace=True)
        mtdat['accuracy'].replace('cor', 1, inplace=True)
        mtdat['voice'].replace('Neural2-F', 1, inplace=True)
        mtdat['voice'].replace('Neural2-D', 2, inplace=True)

        # put the recoded metadata together to create numeric codes
        for epIdx in range(len(epochs.events)):
            epochs.events[epIdx][2] = mtdat['stim_code'][epIdx]*1000 + \
                mtdat['levels'][epIdx]*100 + \
                mtdat['accuracy'][epIdx]*10 + mtdat['voice'][epIdx]
        epochs.event_id = const.event_id  # using the event_id dict from the constants
        return epochs

    def averageReference(self, epochs):
        """
        Apply average reference to the epochs

        Parameters
        ----------
        epochs : mne.Epochs object

        Returns
        -------
        epochs : mne.Epochs object
            Now re-referenced to average reference

        """
        epochs = epochs.set_eeg_reference()
        return epochs

    def countEventFrequency(self, epochs=None):
        """
        Creates a table listing all event_id codes, labels and their frequency of occurrence.

        Events must first be relabelled (using relabelEvents)

        This function only returns the frequency table but does not save it.
        
        This function calls createEmptyFrequencyDict (see more info on why in the documentation for that function)


        Parameters
        ----------
        epochs : epochs.EpochsFIF - Default is None, which will call readEpo

        Returns
        -------
        df : pandas dataframe

        """
        if epochs is None:  # if no epoch object is given, then first read the epoch file
            epochs = self.readEpo()

        # create empty dict (see docstring of createEmptyFrequencyDict() for more information)
        self.createEmptyFrequencyDict()
        freqCount = self.freqCountEmpty

        # making an array out of all recorded event ids
        events = epochs.events[:, 2]

        # Go through array elements and count frequencies
        # for each index in events, add +1 to the key of the corresponding event in freqCount
        for i in range(len(events)):
            freqCount[events[i]] += 1

        df = pd.DataFrame(freqCount.items(), columns=["event_id", "frequency"])
        df.insert(1, "events", const.all_event_labels)

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
