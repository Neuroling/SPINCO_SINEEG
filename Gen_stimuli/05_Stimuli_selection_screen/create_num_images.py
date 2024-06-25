#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:44:00 2024
@author: samuemu

Note: "Nul.png" is a bad filename and will lead to problems. Therefore, the image
of the number Zero ("Null" in german) is called "Zer.png"

Package: [Pillow](https://pypi.org/project/pillow/) - `python3 -m pip install --upgrade Pillow`
"""
from PIL import Image, ImageDraw, ImageFont

import os 

thisDir = os.getcwd()
diroutput = os.path.join(thisDir[:thisDir.find('Gen_stimuli')], 'Experiments','SiN','Experiment2','SiN_task','images')

num  = {'Ein':1, 'Zwe':2, 'Dre':3, 'Vie':4,'Fue':5, 'Sec':6, 'Neu':9, 'Zer':0}


for key, value in num.items():
    # Create a new image with a transparent background
    image_size = (310, 310)
    image = Image.new('RGBA', image_size, (255, 255, 255, 0))
    
    draw = ImageDraw.Draw(image)
    
    # Define the properties of the square borders
    square_size = 310
    border_width = 5
    top_left = (0,0)
    bottom_right = (top_left[0] + square_size, top_left[1] + square_size)
    
    # Draw the square with a border and transparent fill
    draw.rectangle([top_left, bottom_right], fill=None, outline='black', width=border_width)
        
    # Define the text properties
    text = str(value)
    font_size = square_size//2
    
    # Use DejaVu Sans font, commonly available on Linux
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, font_size)
    
    # Calculate text width and height using textbbox
    bbox = draw.textbbox((0, 0), text, font=font, align = 'mm')
    # returns [left, top, right, bottom] for the boundary box
    
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] #- bbox[1]
    # text_height = 70
    
    # Calculate the position to center the text
    text_position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)
    # text_position = (155,155)
    
    # Draw the text
    draw.text(text_position, text, fill='black', font=font, align = 'mm')
    

    # Save the image
    image.save((diroutput + os.sep + key + '.png'))
    
