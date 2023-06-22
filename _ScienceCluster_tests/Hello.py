# -*- coding: utf-8 -*-
""" Testing science Cluster
=================================

Lets just try to read some data
""" 
import re
import glob 
import os


# paths 
baseDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
chanLocsFile =  os.path.join(baseDir,'_ScienceClusters_tests','SiN','Biosemi_73ch_EEGlab_xyx.tsv')

# User inputs  
subjPattern = 'p003' 

# %% Subject loop 
# find subject Raw eeg files

subjectDir = os.path.join(baseDir,'Data','SiN','raw')
files = [files for files in glob.glob(os.path.join(subjectDir,'**','*.bdf'), recursive = True) if re.search(subjPattern + '.*', files)]
   
# %% 
 print(files)