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


for i_call in call:
    # Parameters
    input_image_path = (thisDir + os.sep + i_call)  # Path to your existing image

    border_size = 5
    border_color = 'black'

        # Open the original image
    img = Image.open(input_image_path)

    # Add the border
    img_with_border = ImageOps.expand(img, border=border_size, fill=border_color)

    # Save the new image
    img_with_border.save((diroutput + os.sep + i_call))
    
    
    # # Create a new image with a transparent background
    # image_size = (300, 300)
    # image = Image.new('RGBA', image_size, (255, 255, 255, 0))
    
    # draw = ImageDraw.Draw(image)
    
    # # Define the properties of the square borders
    # square_size = 200
    # border_width = 5
    # top_left = ((image_size[0] - square_size) // 2, (image_size[1] - square_size) // 2)
    # bottom_right = (top_left[0] + square_size, top_left[1] + square_size)
    
    # # Draw the square with a border and transparent fill
    # draw.rectangle([top_left, bottom_right], fill=value, outline='black', width=border_width)
        

    # # Save the image
    # image.save((diroutput + os.sep + key + '.png'))
    
