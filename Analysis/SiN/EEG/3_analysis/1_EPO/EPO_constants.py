#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:47:21 2023

@author: samuemu

This script contains variables that do not change across scripts, such as subject IDs and event_id
"""

import os
from glob import glob

taskID = 'task-sin'
pipeID = 'pipeline-01'
setFileEnd = '_epoched_2.set'

thisDir = os.path.dirname(os.path.abspath(__file__))
subjIDs=[item for item in os.listdir(os.path.join(thisDir[:thisDir.find('Scripts')] + 'Data','SiN','rawdata')) if item[-1].isdigit()]


"""
These are the event labels:
    NoiseType / StimulusType / DegradationLevel / Accuracy / Voice
    
    X____ NoiseType: NV = 1, SSN = 2
    _X___ Stimulus Type: Call = 1, Colour = 2, Number = 3
    __X__ Degradation Level: Lv1 = 1, Lv2 = 2, Lv3 = 3
    ___X_ Accuracy: Incorrect = 0, Correct = 1
    ____X Voice: Feminine (Neural2-F) = 1, Masculine (Neural2-D) = 2
    
This allows you to filter the epochs using the event labels, i.e. by:
    epochs.__getitem__('NV') --------> will return all epochs with NV
    epochs.__getitem__('Lv1/call') --> will return all epochs with Lv1 degradation and CallSign
"""

event_id = {'NV/call/Lv1/inc/F':11101, 'NV/call/Lv1/inc/M':11102, 'NV/call/Lv1/cor/F':11111, 'NV/call/Lv1/cor/M':11112,
            'NV/call/Lv2/inc/F':11201, 'NV/call/Lv2/inc/M':11202, 'NV/call/Lv2/cor/F':11211, 'NV/call/Lv2/cor/M':11212,
            'NV/call/Lv3/inc/F':11301, 'NV/call/Lv3/inc/M':11302, 'NV/call/Lv3/cor/F':11311, 'NV/call/Lv3/cor/M':11312,
            'NV/col/Lv1/inc/F':12101, 'NV/col/Lv1/inc/M':12102, 'NV/col/Lv1/cor/F':12111, 'NV/col/Lv1/cor/M':12112,
            'NV/col/Lv2/inc/F':12201, 'NV/col/Lv2/inc/M':12202, 'NV/col/Lv2/cor/F':12211, 'NV/col/Lv2/cor/M':12212,
            'NV/col/Lv3/inc/F':12301, 'NV/col/Lv3/inc/M':12302, 'NV/col/Lv3/cor/F':12311, 'NV/col/Lv3/cor/M':12312,
            'NV/num/Lv1/inc/F':13101, 'NV/num/Lv1/inc/M':13102, 'NV/num/Lv1/cor/F':13111, 'NV/num/Lv1/cor/M':13112,
            'NV/num/Lv2/inc/F':13201, 'NV/num/Lv2/inc/M':13202, 'NV/num/Lv2/cor/F':13211, 'NV/num/Lv2/cor/M':13212,
            'NV/num/Lv3/inc/F':13301, 'NV/num/Lv3/inc/M':13302, 'NV/num/Lv3/cor/F':13311, 'NV/num/Lv3/cor/M':13312,
            'SSN/call/Lv1/inc/F':21101, 'SSN/call/Lv1/inc/M':21102, 'SSN/call/Lv1/cor/F':21111, 'SSN/call/Lv1/cor/M':21112,
            'SSN/call/Lv2/inc/F':21201, 'SSN/call/Lv2/inc/M':21202, 'SSN/call/Lv2/cor/F':21211, 'SSN/call/Lv2/cor/M':21212,
            'SSN/call/Lv3/inc/F':21301, 'SSN/call/Lv3/inc/M':21302, 'SSN/call/Lv3/cor/F':21311, 'SSN/call/Lv3/cor/M':21312,
            'SSN/col/Lv1/inc/F':22101, 'SSN/col/Lv1/inc/M':22102, 'SSN/col/Lv1/cor/F':22111, 'SSN/col/Lv1/cor/M':22112,
            'SSN/col/Lv2/inc/F':22201, 'SSN/col/Lv2/inc/M':22202, 'SSN/col/Lv2/cor/F':22211, 'SSN/col/Lv2/cor/M':22212,
            'SSN/col/Lv3/inc/F':22301, 'SSN/col/Lv3/inc/M':22302, 'SSN/col/Lv3/cor/F':22311, 'SSN/col/Lv3/cor/M':22312,
            'SSN/num/Lv1/inc/F':23101, 'SSN/num/Lv1/inc/M':23102, 'SSN/num/Lv1/cor/F':23111, 'SSN/num/Lv1/cor/M':23112,
            'SSN/num/Lv2/inc/F':23201, 'SSN/num/Lv2/inc/M':23202, 'SSN/num/Lv2/cor/F':23211, 'SSN/num/Lv2/cor/M':23212,
            'SSN/num/Lv3/inc/F':23301, 'SSN/num/Lv3/inc/M':23302, 'SSN/num/Lv3/cor/F':23311, 'SSN/num/Lv3/cor/M':23312,
            }

"""
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
"""
event_id2 = {'NV/call/Stim1/Lv1/inc/F':111101, 'NV/call/Stim1/Lv1/inc/M':111102, 'NV/call/Stim1/Lv1/cor/F':111111, 'NV/call/Stim1/Lv1/cor/M':111112,
            'NV/call/Stim1/Lv2/inc/F':111201, 'NV/call/Stim1/Lv2/inc/M':111202, 'NV/call/Stim1/Lv2/cor/F':111211, 'NV/call/Stim1/Lv2/cor/M':111212,
            'NV/call/Stim1/Lv3/inc/F':111301, 'NV/call/Stim1/Lv3/inc/M':111302, 'NV/call/Stim1/Lv3/cor/F':111311, 'NV/call/Stim1/Lv3/cor/M':111312,
            'NV/col/Stim1/Lv1/inc/F':121101, 'NV/col/Stim1/Lv1/inc/M':121102, 'NV/col/Stim1/Lv1/cor/F':121111, 'NV/col/Stim1/Lv1/cor/M':121112,
            'NV/col/Stim1/Lv2/inc/F':121201, 'NV/col/Stim1/Lv2/inc/M':121202, 'NV/col/Stim1/Lv2/cor/F':121211, 'NV/col/Stim1/Lv2/cor/M':121212,
            'NV/col/Stim1/Lv3/inc/F':121301, 'NV/col/Stim1/Lv3/inc/M':121302, 'NV/col/Stim1/Lv3/cor/F':121311, 'NV/col/Stim1/Lv3/cor/M':121312,
            'NV/num/Stim1/Lv1/inc/F':131101, 'NV/num/Stim1/Lv1/inc/M':131102, 'NV/num/Stim1/Lv1/cor/F':131111, 'NV/num/Stim1/Lv1/cor/M':131112,
            'NV/num/Stim1/Lv2/inc/F':131201, 'NV/num/Stim1/Lv2/inc/M':131202, 'NV/num/Stim1/Lv2/cor/F':131211, 'NV/num/Stim1/Lv2/cor/M':131212,
            'NV/num/Stim1/Lv3/inc/F':131301, 'NV/num/Stim1/Lv3/inc/M':131302, 'NV/num/Stim1/Lv3/cor/F':131311, 'NV/num/Stim1/Lv3/cor/M':131312,
            'SSN/call/Stim1/Lv1/inc/F':211101, 'SSN/call/Stim1/Lv1/inc/M':211102, 'SSN/call/Stim1/Lv1/cor/F':211111, 'SSN/call/Stim1/Lv1/cor/M':211112,
            'SSN/call/Stim1/Lv2/inc/F':211201, 'SSN/call/Stim1/Lv2/inc/M':211202, 'SSN/call/Stim1/Lv2/cor/F':211211, 'SSN/call/Stim1/Lv2/cor/M':211212,
            'SSN/call/Stim1/Lv3/inc/F':211301, 'SSN/call/Stim1/Lv3/inc/M':211302, 'SSN/call/Stim1/Lv3/cor/F':211311, 'SSN/call/Stim1/Lv3/cor/M':211312,
            'SSN/col/Stim1/Lv1/inc/F':221101, 'SSN/col/Stim1/Lv1/inc/M':221102, 'SSN/col/Stim1/Lv1/cor/F':221111, 'SSN/col/Stim1/Lv1/cor/M':221112,
            'SSN/col/Stim1/Lv2/inc/F':221201, 'SSN/col/Stim1/Lv2/inc/M':221202, 'SSN/col/Stim1/Lv2/cor/F':221211, 'SSN/col/Stim1/Lv2/cor/M':221212,
            'SSN/col/Stim1/Lv3/inc/F':221301, 'SSN/col/Stim1/Lv3/inc/M':221302, 'SSN/col/Stim1/Lv3/cor/F':221311, 'SSN/col/Stim1/Lv3/cor/M':221312,
            'SSN/num/Stim1/Lv1/inc/F':231101, 'SSN/num/Stim1/Lv1/inc/M':231102, 'SSN/num/Stim1/Lv1/cor/F':231111, 'SSN/num/Stim1/Lv1/cor/M':231112,
            'SSN/num/Stim1/Lv2/inc/F':231201, 'SSN/num/Stim1/Lv2/inc/M':231202, 'SSN/num/Stim1/Lv2/cor/F':231211, 'SSN/num/Stim1/Lv2/cor/M':231212,
            'SSN/num/Stim1/Lv3/inc/F':231301, 'SSN/num/Stim1/Lv3/inc/M':231302, 'SSN/num/Stim1/Lv3/cor/F':231311, 'SSN/num/Stim1/Lv3/cor/M':231312,
            
            'NV/call/Stim2/Lv1/inc/F':112101, 'NV/call/Stim2/Lv1/inc/M':112102, 'NV/call/Stim2/Lv1/cor/F':112111, 'NV/call/Stim2/Lv1/cor/M':112112,
            'NV/call/Stim2/Lv2/inc/F':112201, 'NV/call/Stim2/Lv2/inc/M':112202, 'NV/call/Stim2/Lv2/cor/F':112211, 'NV/call/Stim2/Lv2/cor/M':112212,
            'NV/call/Stim2/Lv3/inc/F':112301, 'NV/call/Stim2/Lv3/inc/M':112302, 'NV/call/Stim2/Lv3/cor/F':112311, 'NV/call/Stim2/Lv3/cor/M':112312,
            'NV/col/Stim2/Lv1/inc/F':122101, 'NV/col/Stim2/Lv1/inc/M':122102, 'NV/col/Stim2/Lv1/cor/F':122111, 'NV/col/Stim2/Lv1/cor/M':122112,
            'NV/col/Stim2/Lv2/inc/F':122201, 'NV/col/Stim2/Lv2/inc/M':122202, 'NV/col/Stim2/Lv2/cor/F':122211, 'NV/col/Stim2/Lv2/cor/M':122212,
            'NV/col/Stim2/Lv3/inc/F':122301, 'NV/col/Stim2/Lv3/inc/M':122302, 'NV/col/Stim2/Lv3/cor/F':122311, 'NV/col/Stim2/Lv3/cor/M':122312,
            'NV/num/Stim2/Lv1/inc/F':132101, 'NV/num/Stim2/Lv1/inc/M':132102, 'NV/num/Stim2/Lv1/cor/F':132111, 'NV/num/Stim2/Lv1/cor/M':132112,
            'NV/num/Stim2/Lv2/inc/F':132201, 'NV/num/Stim2/Lv2/inc/M':132202, 'NV/num/Stim2/Lv2/cor/F':132211, 'NV/num/Stim2/Lv2/cor/M':132212,
            'NV/num/Stim2/Lv3/inc/F':132301, 'NV/num/Stim2/Lv3/inc/M':132302, 'NV/num/Stim2/Lv3/cor/F':132311, 'NV/num/Stim2/Lv3/cor/M':132312,
            'SSN/call/Stim2/Lv1/inc/F':212101, 'SSN/call/Stim2/Lv1/inc/M':212102, 'SSN/call/Stim2/Lv1/cor/F':212111, 'SSN/call/Stim2/Lv1/cor/M':212112,
            'SSN/call/Stim2/Lv2/inc/F':212201, 'SSN/call/Stim2/Lv2/inc/M':212202, 'SSN/call/Stim2/Lv2/cor/F':212211, 'SSN/call/Stim2/Lv2/cor/M':212212,
            'SSN/call/Stim2/Lv3/inc/F':212301, 'SSN/call/Stim2/Lv3/inc/M':212302, 'SSN/call/Stim2/Lv3/cor/F':212311, 'SSN/call/Stim2/Lv3/cor/M':212312,
            'SSN/col/Stim2/Lv1/inc/F':222101, 'SSN/col/Stim2/Lv1/inc/M':222102, 'SSN/col/Stim2/Lv1/cor/F':222111, 'SSN/col/Stim2/Lv1/cor/M':222112,
            'SSN/col/Stim2/Lv2/inc/F':222201, 'SSN/col/Stim2/Lv2/inc/M':222202, 'SSN/col/Stim2/Lv2/cor/F':222211, 'SSN/col/Stim2/Lv2/cor/M':222212,
            'SSN/col/Stim2/Lv3/inc/F':222301, 'SSN/col/Stim2/Lv3/inc/M':222302, 'SSN/col/Stim2/Lv3/cor/F':222311, 'SSN/col/Stim2/Lv3/cor/M':222312,
            'SSN/num/Stim2/Lv1/inc/F':232101, 'SSN/num/Stim2/Lv1/inc/M':232102, 'SSN/num/Stim2/Lv1/cor/F':232111, 'SSN/num/Stim2/Lv1/cor/M':232112,
            'SSN/num/Stim2/Lv2/inc/F':232201, 'SSN/num/Stim2/Lv2/inc/M':232202, 'SSN/num/Stim2/Lv2/cor/F':232211, 'SSN/num/Stim2/Lv2/cor/M':232212,
            'SSN/num/Stim2/Lv3/inc/F':232301, 'SSN/num/Stim2/Lv3/inc/M':232302, 'SSN/num/Stim2/Lv3/cor/F':232311, 'SSN/num/Stim2/Lv3/cor/M':232312,
            
            'NV/call/Stim3/Lv1/inc/F':113101, 'NV/call/Stim3/Lv1/inc/M':113102, 'NV/call/Stim3/Lv1/cor/F':113111, 'NV/call/Stim3/Lv1/cor/M':113112,
            'NV/call/Stim3/Lv2/inc/F':113201, 'NV/call/Stim3/Lv2/inc/M':113202, 'NV/call/Stim3/Lv2/cor/F':113211, 'NV/call/Stim3/Lv2/cor/M':113212,
            'NV/call/Stim3/Lv3/inc/F':113301, 'NV/call/Stim3/Lv3/inc/M':113302, 'NV/call/Stim3/Lv3/cor/F':113311, 'NV/call/Stim3/Lv3/cor/M':113312,
            'NV/col/Stim3/Lv1/inc/F':123101, 'NV/col/Stim3/Lv1/inc/M':123102, 'NV/col/Stim3/Lv1/cor/F':123111, 'NV/col/Stim3/Lv1/cor/M':123112,
            'NV/col/Stim3/Lv2/inc/F':123201, 'NV/col/Stim3/Lv2/inc/M':123202, 'NV/col/Stim3/Lv2/cor/F':123211, 'NV/col/Stim3/Lv2/cor/M':123212,
            'NV/col/Stim3/Lv3/inc/F':123301, 'NV/col/Stim3/Lv3/inc/M':123302, 'NV/col/Stim3/Lv3/cor/F':123311, 'NV/col/Stim3/Lv3/cor/M':123312,
            'NV/num/Stim3/Lv1/inc/F':133101, 'NV/num/Stim3/Lv1/inc/M':133102, 'NV/num/Stim3/Lv1/cor/F':133111, 'NV/num/Stim3/Lv1/cor/M':133112,
            'NV/num/Stim3/Lv2/inc/F':133201, 'NV/num/Stim3/Lv2/inc/M':133202, 'NV/num/Stim3/Lv2/cor/F':133211, 'NV/num/Stim3/Lv2/cor/M':133212,
            'NV/num/Stim3/Lv3/inc/F':133301, 'NV/num/Stim3/Lv3/inc/M':133302, 'NV/num/Stim3/Lv3/cor/F':133311, 'NV/num/Stim3/Lv3/cor/M':133312,
            'SSN/call/Stim3/Lv1/inc/F':213101, 'SSN/call/Stim3/Lv1/inc/M':213102, 'SSN/call/Stim3/Lv1/cor/F':213111, 'SSN/call/Stim3/Lv1/cor/M':213112,
            'SSN/call/Stim3/Lv2/inc/F':213201, 'SSN/call/Stim3/Lv2/inc/M':213202, 'SSN/call/Stim3/Lv2/cor/F':213211, 'SSN/call/Stim3/Lv2/cor/M':213212,
            'SSN/call/Stim3/Lv3/inc/F':213301, 'SSN/call/Stim3/Lv3/inc/M':213302, 'SSN/call/Stim3/Lv3/cor/F':213311, 'SSN/call/Stim3/Lv3/cor/M':213312,
            'SSN/col/Stim3/Lv1/inc/F':223101, 'SSN/col/Stim3/Lv1/inc/M':223102, 'SSN/col/Stim3/Lv1/cor/F':223111, 'SSN/col/Stim3/Lv1/cor/M':223112,
            'SSN/col/Stim3/Lv2/inc/F':223201, 'SSN/col/Stim3/Lv2/inc/M':223202, 'SSN/col/Stim3/Lv2/cor/F':223211, 'SSN/col/Stim3/Lv2/cor/M':223212,
            'SSN/col/Stim3/Lv3/inc/F':223301, 'SSN/col/Stim3/Lv3/inc/M':223302, 'SSN/col/Stim3/Lv3/cor/F':223311, 'SSN/col/Stim3/Lv3/cor/M':223312,
            'SSN/num/Stim3/Lv1/inc/F':233101, 'SSN/num/Stim3/Lv1/inc/M':233102, 'SSN/num/Stim3/Lv1/cor/F':233111, 'SSN/num/Stim3/Lv1/cor/M':233112,
            'SSN/num/Stim3/Lv2/inc/F':233201, 'SSN/num/Stim3/Lv2/inc/M':233202, 'SSN/num/Stim3/Lv2/cor/F':233211, 'SSN/num/Stim3/Lv2/cor/M':233212,
            'SSN/num/Stim3/Lv3/inc/F':233301, 'SSN/num/Stim3/Lv3/inc/M':233302, 'SSN/num/Stim3/Lv3/cor/F':233311, 'SSN/num/Stim3/Lv3/cor/M':233312,
            }