#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:44:00 2024

@author: samuemu

Package: [Pillow](https://pypi.org/project/pillow/) - `python3 -m pip install --upgrade Pillow`
"""
from PIL import Image, ImageOps

import os 

thisDir = os.getcwd()
diroutput = os.path.join(thisDir[:thisDir.find('Gen_stimuli')], 'Experiments','SiN','Experiment2','SiN_task','images')

call = ['Adl', 'Eul', 'Rat', 'Tig', 'Vel', 'Aut', 'Mes', 'Gab']
call = [i + '.png' for i in call]

# border parameters
border_size = 5
border_color = 'black'

for i_call in call:
    
    # open the original image
    input_image_path = (thisDir + os.sep + i_call)  # Path to the existing image
    img = Image.open(input_image_path)
    
    # Add the border - Note: The new image will be of size <size original image> + (border_size * 2)
    img_with_border = ImageOps.expand(img, border=border_size, fill=border_color)

    # Save the new image
    img_with_border.save((diroutput + os.sep + i_call))
    
    
