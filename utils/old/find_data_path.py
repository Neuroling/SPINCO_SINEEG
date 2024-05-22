# -*- coding: utf-8 -*-
""" Find my data path 
========================================================================
Created on Wed Jun  7 10:47:28 2023

- Gives the path to data based on the location of this function
- Assumes the following folder structure:
    
    ├──PROJECT/  
    .	├── scripts/
        │    
    	├── Data/
        └── ...    
- Call typing: data_path = find_data_path()

@author: gfraga
"""

# %%
import os
import inspect

def find_data_path(script_file=None):
    frame = inspect.currentframe()
    frame_info = inspect.getframeinfo(frame)
    script_file = frame_info.filename
    print('The function path is', script_file)
    
    # paths - Use script path as reference
    script_dir = os.path.dirname(os.path.abspath(script_file))
    # define data dir
    script_folder_index = script_dir.find(os.path.sep + 'scripts' + os.path.sep)
    data_path = os.path.join(script_dir[:script_folder_index] + 'Data')

    print('Your data path seems to be:', data_path)
    return data_path


