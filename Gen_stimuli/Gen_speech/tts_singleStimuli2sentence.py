#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 12:26:24 2024

@author: testuser
"""
import wave

import os
from glob import glob

thisDir = os.getcwd()
dirinput = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz','tts-golang')
diroutput = os.path.join(thisDir[:thisDir.find('Scripts')], 'Stimuli','AudioGens','Experiment2', 'tts-golang-44100hz','tts-golang_sentences')

# Get list of callSign, Colour and Number stimuli
callSign = ['Adler','Eule', 'Tiger','Ratte', 
         'Hammer',  'Schraube', 'Flugzeug', 'Auto']

colour = ['gelben','gruenen','roten','weissen', 'blauen', 
         'schwarzen', 'pinken', 'braunen', 'grauen']

number = ['Eins','Zwei','Drei','Vier', 'Fuenf', 'Sechs', 'Acht', 'Neun']

commonWords = ['Vorsicht', 'gehe sofort zum', 'Feld der Spalte']

lang_voice_speaker = 'DE_Neural2-F'

# use those to create lists of filepaths
# Yes this could be done easier, more efficiently, and with less possibility for human error. 
# (i.e. with itertools.product)
# But I have not had lunch, it is 16.30 on a Friday, and this works, so we're going with this :)
combinations = []
combination_name = []
for i in callSign:

    for ii in colour:

        for iii in number: 
            thisCallSign = i[:4]
            thisColour   = ii[:4]
            thisNumber   = iii[:4]
            
            combination_name.append(thisCallSign + '-' + thisColour + '-' + thisNumber)
            files = []
            files.append(glob(os.path.join(dirinput, (lang_voice_speaker+'_'+commonWords[0][:4]+'.wav')))[0])
            files.append(glob(os.path.join(dirinput, (lang_voice_speaker+'_'+thisCallSign+'.wav')))[0])
            
            files.append(glob(os.path.join(dirinput, (lang_voice_speaker+'_'+commonWords[1][:4]+'.wav')))[0])
            files.append(glob(os.path.join(dirinput, (lang_voice_speaker+'_'+thisColour+'.wav')))[0])
            
            files.append(glob(os.path.join(dirinput, (lang_voice_speaker+'_'+commonWords[2][:4]+'.wav')))[0])
            files.append(glob(os.path.join(dirinput, (lang_voice_speaker+'_'+thisNumber+'.wav')))[0])
            combinations.append(files)

   


for idx, combination in enumerate(combinations):
    # Create a unique filename for each combination
    output_file = os.path.join(diroutput, lang_voice_speaker + '_' +  combination_name[idx] + '.wav')
    
    # Stitch the files in the current combination together
    # Open the output file in write mode
    with wave.open('output_file', mode = 'wb') as output_wav:
        print('1')
        # Initialize variables for the output file parameters
        num_channels = 0
        sample_width = 0
        frame_rate = 0
        num_frames = 0
        
    
        for input_file in combination:
            # Open each input file
            
            with wave.open(input_file, 'rb') as input_wav:
                # If this is the first file, set the output parameters
                if num_channels == 0:
                    num_channels = input_wav.getnchannels()
                    sample_width = input_wav.getsampwidth()
                    frame_rate = input_wav.getframerate()
    
                # Read frames from input file and write to output file
                frames = input_wav.readframes(input_wav.getnframes())
                output_wav.writeframes(frames)
                num_frames += input_wav.getnframes()
        print('2')
        # Update the output file parameters
        output_wav.setnchannels(num_channels)
        output_wav.setsampwidth(sample_width)
        output_wav.setframerate(frame_rate)
        output_wav.setnframes(num_frames)
        print('3')
        # Close the output file
        output_wav.close()


    print(f"Combination {idx} created: {output_file}")            
            
     
