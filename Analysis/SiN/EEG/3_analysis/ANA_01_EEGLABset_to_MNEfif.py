
""" READ EEGLAB EPOCHS in MNE 
=================================================================
@author: samuemull

reading epoched eeglab .set files and saves mne .fif files
Adds Metadata

 
""" 

import os
from glob import glob
import scipy.io as sio
import numpy as np
import mne 
import pandas as pd
#import MVPA.ANA_01_helper as hp

#%% inputs and paths
