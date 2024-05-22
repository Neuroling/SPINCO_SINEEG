#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:44:00 2024

@author: samuemu

Package: [Pillow](https://pypi.org/project/pillow/) - `python3 -m pip install --upgrade Pillow`
"""
from PIL import Image, ImageDraw

import os 

thisDir = os.getcwd()
diroutput = os.path.join(thisDir[:thisDir.find('Gen_stimuli')], 'Experiments','SiN','Experiment2','SiN_task','images')

col  = {'gel':'yellow', 'gru':'green', 'rot':'red', 'wei':'white',
                    'bla':'blue', 'bra':'#a05a2cff', 'pin':'#f107b1ff', 'sch':'black'}


for key, value in col.items():
    # Create a new image with a transparent background
    image_size = (310, 310)
    image = Image.new('RGBA', image_size, (255, 255, 255, 0))
    
    draw = ImageDraw.Draw(image)
    
    # Define the properties of the square borders
    square_size = 310
    border_width = 5
    top_left = ((image_size[0] - square_size) // 2, (image_size[1] - square_size) // 2)
    bottom_right = (top_left[0] + square_size, top_left[1] + square_size)
    
    # Draw the square with a border and transparent fill
    draw.rectangle([top_left, bottom_right], fill=value, outline='black', width=border_width)
        

    # Save the image
    image.save((diroutput + os.sep + key + '.png'))
