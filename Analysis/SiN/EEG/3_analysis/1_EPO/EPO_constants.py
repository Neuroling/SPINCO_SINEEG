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