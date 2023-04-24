#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 10:18:34 2022

@author: gfraga
"""
basedirinput  = '/mnt/nfs/din_v1/experimentData/' 
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN' 
# find target files
files = glob(basedirinput + "*/EEG_DATA/DOWNSAMPLED/DiN/*ICrem.set", recursive=True)
# Retrieve list of subjects name from folder structure
subjects =  [[item for item in currpart if 'SUBJECT' in item] 
             for currpart in [fullpath.split('/')
                              for fullpath in files]] 
 