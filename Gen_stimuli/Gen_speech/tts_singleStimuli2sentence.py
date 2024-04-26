#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 12:26:24 2024

@author: testuser
"""
import wave
from itertools import product
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
filename = os.path.join(dirinput, (lang_voice_speaker+'_'+'*'+'.wav'))
os.path.exists(dirinput)
audiofiles = glob(filename, recursive= True)
# TODO

def stitch_wav_files(input_files, output_file):
    # Open the output file in write mode
    output_wav = wave.open(output_file, 'wb')

    # Initialize variables for the output file parameters
    num_channels = 0
    sample_width = 0
    frame_rate = 0
    num_frames = 0

    for input_file in input_files:
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

    # Update the output file parameters
    output_wav.setnchannels(num_channels)
    output_wav.setsampwidth(sample_width)
    output_wav.setframerate(frame_rate)
    output_wav.setnframes(num_frames)

    # Close the output file
    output_wav.close()

def combine_wav_combinations(files_list1, files_list2, files_list3, output_dir):
    # Generate all combinations of files from the three lists
    combinations = product(files_list1, files_list2, files_list3)

    for idx, combination in enumerate(combinations, start=1):
        # Create a unique filename for each combination
        output_file = f"{output_dir}/combined_{idx}.wav"
        # Stitch the files in the current combination together
        stitch_wav_files(combination, output_file)
        print(f"Combination {idx} created: {output_file}")

# # Example usage
# files_list1 = ["file1a.wav", "file1b.wav"]
# files_list2 = ["file2a.wav", "file2b.wav"]
# files_list3 = ["file3a.wav", "file3b.wav"]
# output_dir = "output_folder"
# combine_wav_combinations(files_list1, files_list2, files_list3, output_dir)
