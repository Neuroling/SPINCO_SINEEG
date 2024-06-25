# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 11:57:29 2023

@author: gfraga
"""

import speech_recognition as sr
import os 

os.chdir('V:\spinco_data\AudioGens')


# Load the audio file
r = sr.Recognizer()
with sr.AudioFile("myaudio.mp3") as source:
    audio = r.record(source)

# Transcribe the audio into text
transcription = r.recognize_google(audio, show_all=True)

# Get the word-level timing information
word_timings = [(word.word, word.start_time, word.end_time) for word in transcription.words]

# Print the word-level timing information
for word, start_time, end_time in word_timings:
    print(f"Word: {word}, Start Time: {start_time}, End Time: {end_time}")