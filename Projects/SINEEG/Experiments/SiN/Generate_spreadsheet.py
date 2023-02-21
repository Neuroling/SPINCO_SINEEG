# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:37:20 2023

@author: gfraga
"""
import os as os
import sys as sys
import glob as glob


if sys.platform=='linux':  basedir  = '/home/d.uzh.ch/gfraga/smbmount/'
else:  basedir ='V:/'

dirinput = basedir + 'spinco_data/AudioGens/text-to-speech-golang' # folder with .wav files
diroutput = basedir + 'spinco_data/AudioGens'

os.chdir(dirinput)
os.getcwd()



# finde files 
audifiles = glob.glob('*.wav')
textfiles = glob.glob('*.txt')


#validfiles= [files for files in glob.glob(dirinput + '/**/*.csv' ,recursive=True) if 
 #            'gathered/Concat' not in files and re.search(r'\d+\.csv', files)] # subject files here have a digit before extension 