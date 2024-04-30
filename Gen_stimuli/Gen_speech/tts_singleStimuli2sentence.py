#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combining stimulus words into a sentence
------------------------------------------------------------------------------
Created on Fri Apr 26 12:26:24 2024
@author: samuemu

In natural speech, the coarticulation imposes a difference on the non-target
words. I.e. the non-target word "Vorsicht" will sound slightly different depending 
on the next word, meaning the "standardised" non-target words are not truly standardised.

Therefore, Alexis asked me to create the target words and non-target sentence parts
separately and then combine the audiofiles into a sentence.
"""

import wave

from pydub import AudioSegment
# https://github.com/jiaaro/pydub#installation

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
# Yes this could be done more elegant, more efficiently, and with less possibility for human error. 
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
    
    #%% Version 1: https://stackoverflow.com/a/2900266 - No error, but output corrupted
    # #%% Stitch the files in the current combination together
    # data = []
    # for input_file in combination:
    #     w = wave.open(input_file, 'rb')
    #     data.append( [w.getparams(), w.readframes(w.getnframes())] )
    #     w.close()
    
    # with wave.open('output_file', mode = 'wb') as output:
    #     # output = wave.open(output_file, 'wb')
    #     output.setparams(data[0][0])
    #     for params,frames in data:
    #         output.writeframes(frames)
    #     output.close()
         
    
    #%% Version 2: https://stackoverflow.com/a/13384198 - working, but inelegant
    s1 = AudioSegment.from_wav(combination[0])
    s2 = AudioSegment.from_wav(combination[1])
    s3 = AudioSegment.from_wav(combination[2])
    s4 = AudioSegment.from_wav(combination[3])
    s5 = AudioSegment.from_wav(combination[4])
    s6 = AudioSegment.from_wav(combination[5])
    
    combined = s1 + s2 + s3 + s4 + s5 + s6
    combined.export(output_file, format = 'wav')

    print(f"Combination {idx} created: {output_file}")            

            
     
