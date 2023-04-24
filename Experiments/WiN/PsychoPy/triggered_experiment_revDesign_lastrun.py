#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on January 16, 2023, at 14:01
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.1'
expName = 'eeg_contingent_digits'  # from the Builder filename that created this script
expInfo = {
    'participant': '1',
    'session': '001',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='V:\\gfraga\\scripts_neulin\\Projects\\SINEEG\\Experiments\\WiN\\PsychoPy\\triggered_experiment_revDesign_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[2560, 1440], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "Startup" ---
# Run 'Begin Experiment' code from code_startup
# This routine prepares the needed elements for the functioning of the experiment.
# It also randomly generates the digit triplet for the experiment (see begin
# routine) and the randomized order of SiN vs NV speech presentation (see end 
# routine).
# if you want to change some experiment settings (such as nTrial, duration of the
# calibration etc.), you can do it here

# import packages---------------------------------------------------------------

import psychtoolbox as ptb
from pylsl import StreamInlet, resolve_stream
from psychopy import prefs

from psychopy import parallel
import numpy as np
import scipy.stats as stats
import math
import os
import sys
import time
import random
import xlsxwriter
#import sounddevice as sd 
#import soundfile as sf
from itertools import groupby

#explicit loading of PTB sound library no matter what
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound
from river import stream, compose, linear_model, optim, preprocessing, metrics
from collections import OrderedDict
import pandas as pd

# some init and debug parameters
use_debug = True #True

if use_debug:
    use_lpt = False
    use_real_EEG = True
    #debug_color = 'white'
    debug_color = 'white'
    # what is an acceptable level of ROC AUC?
    threshold_performance = 0.45

else:
    use_lpt = True
    use_real_EEG = True
    debug_color = 'gray'
    # what is an acceptable level of ROC AUC?
    threshold_performance = 0.6

# let's do even subject numbers = NV first, odd SIN first    
NV_first = 0
SIN_only = 1


# setting up monitors
SCREEN_SIZE = (320,200)                 # screen res, my screens are identical 
#win0 = visual.Window(SCREEN_SIZE, screen=0, fullscr=True)
win_info = visual.Window(SCREEN_SIZE, screen=1, fullscr=False)

cwd = os.getcwd()
experimentdir = os.getcwd()
os.chdir('..')
openvibedir = os.getcwd() + str('/OpenVibe/')
os.chdir(cwd)

openvibetoolboxdir = 'C:\\Program Files\\openvibe-2.2.0-64bit\\bin'

# open output files-------------------------------------------------------------
dataCalibration_file = open("./data/dataCalibration.txt", "w") # alpha ratio during calibration
meanstd_file = open("./data/meanStd.txt", "w") # mean and std of the calibration
allTriggers_baseline = open("./data/allTriggers_baseline.txt", "w") # all found triggers for each tested factor during calibration
indiv_factor_file = open("./data/indivFactor.txt", "w") # individual factor estimated during calibration for the current subject
dataLogRegWeights = open("./data/logRegWeights.txt", "w") # all weights of all runs of online classification
dataLogRegWeightsFinal = open("./data/logRegWeightsFinal.txt", "w") # all weights of all runs of online classification
#dataSignalCheck_file = open("./data/dataSignalCheck.txt", "w") # alpha ratio during signal check (experimental condition)
#StimOrder_file = open("./data/StimOrder.txt", "w") # order of the trials (is currently SiN or NV speech?)
dataControl_file = open("./data/dataControl.txt", "w") # alpha ratio during signal check (control condition)


# get the EEG stream from OpenVibe----------------------------------------------

print("looking for alpha 32 stream...")
#streams_ALPHA_32 = resolve_stream('type', 'EEG_32_extracted','source_id','OpenViBEAlphaStream32')
streams_ALPHA_32 = resolve_stream('type', 'EEG_32_extracted')

inlet_EEG_32 = StreamInlet(streams_ALPHA_32[0], max_buflen = 1, max_chunklen =1, processing_flags =  1 | 2 | 4 | 8) # create new inlets to read from the streams

if use_lpt:
    port = parallel.ParallelPort(address=0xDFF8) # open the parallel port for EEG markers
    port.setData(0) # 0 as marker for begin exp


# set triggers------------------------------------------------------------------


# The logic of the EEG markers is the following:
# The last number always indicate the current condition: 
# ..... 9: start experiment
# ..... 0: practice trials
# ..... 1: calibration phase
# ..... 2: experimental condition
# ..... 3: control condition
# The first number always indicate the type of event
# ..... 10: instructions
# ..... 9: signal check (the time needed to trigger)
# ..... 1,2 or 3: for 1st, 2nd or 3rd presented digit (stimulus presentation)
# ..... 4,5 or 6: for 1st, 2nd or 3rd typed digit (response of the subjects)

#Examples: 
# ..... 101: marker of the instructions before the calibration phase
# ..... 12: marker of the first presented digit during the experimental condition

# The markers of the break between each block are as follow:
# 1st number = 2
# 2nd number = current block number
# 3rd numner = current condition (see above)

# Example:
# ..... 212: marker of the first block in the experimental condition


#index of electrodes------------------------------------------------------------
# define the index of the elecs of interest for the current experiment 
#(actual index -1 because of 0 being the first elem in Python)
# at the moment, this is just for double checking, not used here 
# (bc openvibe already computes the weighted ratio!)

FP1 = 1 -1
Fz = 2 - 1
F3 = 3 - 1
F7 = 4 - 1
FT9 = 5 -1
FC5 = 6 - 1
FC1 = 7 - 1
C3 = 8 - 1
T7 = 9 -1
TP9 = 10 -1
CP5 = 11 - 1
CP1 = 12 - 1
Pz = 13 - 1
P3 = 14 -1
P7 = 15 - 1
O1 = 16 - 1
Oz = 17 - 1
O2 = 18 - 1
P4 = 19 -1
P8 = 20 -1
TP10 = 21 -1
CP6 = 22 -1
CP2 = 23 -1 
Cz = 24 -1
C4 = 25 -1
T8 = 26 -1
FT10 = 27 -1
FC6 = 28 -1
FC2 = 29 -1
F4 = 30 -1
F8 = 31 -1
FP2 = 32 -1 


elecs_def = ['FP1','Fz','F3','F7','FT9','FC5','FC1','C3','T7','TP9','CP5','CP1','Pz','P3','P7',
'O1','Oz','O2','P4','P8','TP10','CP6','CP2','Cz','C4','T8','FT10','FC6','FC2','F4','F8','FP2']


# trigger name for ME condition block start
trigger_me = '152' 


# Default settings for experiment-----------------------------------------------

# the MAP configuration, which elecs are important 



nDigits = 3 # number presented digits in each trial

nDigits_practice = 1 # number presented digits in each trial
nDigits_ME = 1 # number presented digits in each trial
nDigits_trigger = 1 # number presented digits in each trial

max_ntrials_ME = 100

# these are the other remaining params to insert into stim file (4 = speaker, nv_stim, trigger_stim, jitter_stim)
nRestElems = 4

if use_debug:
    nTrials_1Block = 8 # number of trials in each block, normal is 70
    nTrials_1Block_ME = 4

    # do you want to estimate a real threshold on EEG data or take some artificial values?
    use_real_thresh = 1
    #n_runs_practice = 2
    min_ITI_secs = 0.5 # duration of minimal ITI (time during which we don't check if the threshold is reached to trigger the digits)
else:
    nTrials_1Block = 70
    nTrials_1Block_ME = 30

    # do you want to estimate a real threshold on EEG data or take some artificial values?
    use_real_thresh = 1
    #n_runs_practice = 100
    min_ITI_secs = 2 # duration of minimal ITI (time during which we don't check if the threshold is reached to trigger the digits)

    
nBlocks = 4    
nTrials = nTrials_1Block * nBlocks # number of trials in each condition (experimental vs control), represents 2 blocks.

nTrials_ME = nTrials_1Block_ME * nBlocks # number of trials in each condition (experimental vs control), represents 2 blocks.


## these two variables below should not be needed anymore, so I will comment them out for now
#refresh_rate = 60 # refreshing rate of the screen
srate_processed = 16 # sampling rate of the incoming signal


# adapt calibration duration
if use_debug:
    baseline_duration_sec = 20 # duration of baseline in seconds, normal is 100
    min_factor = 1 # the minimal acceptable factor
    # on average we want triggers every 2 seconds in debug
    mean_interval_triggers_sec = 5

else:
    baseline_duration_sec = 100 # duration of baseline in seconds, normal is 100
    min_factor = 2 # the minimal acceptable factor
    # on average we want triggers every 12 seconds in real mode (gives us a good clear 
    # pattern that is triggered)
    mean_interval_triggers_sec = 10

## also not needed anymore?
#baseline_duration_frames = baseline_duration_sec * srate_processed # duration of baseline in frames


# Default setting for individualized factor calculation-------------------------

max_factor = 3.5 # the maximal acceptable factor
step_factor = 0.1 # step size for testing the different factors

# default individual factor
if not(use_debug):
    indiv_factor_def = 2
else:
    indiv_factor_def = 1.5

#max_duration100Trials_min = 20 # how many minutes should each block last
#max_duration100Trials_sec = max_duration100Trials_min * 60 # max minutes of each block converted in seconds

min_ITI_samples = min_ITI_secs*srate_processed # mean ITI converted in number of samples
#Interval = round(min_ITI_secs * srate_processed) # how much sample points do we have to count to reach minimal ITI

#ITI = 2 * srate_processed #set the iter trial interval at 2s (60 frames per second: 2 seconds = 120 frames)

ITI_secs = 2
ITI_secs_ME = 2

# default ITI
ctrl_ITI_secs = ITI_secs
ctrl_ITI_secs_ME = ITI_secs_ME




# Default values for normalizing the signal
signal_trials = []
trial_nr = []

# Default color values
ratio_vec = 0
current_mean_ratio = 0

# block and trial counter
nExpBlock = 1
nExpTrials = 0

# speaker IDs and how many speaker per triplet ?
speaker = [1,7,10,13,14,21,33,48,49,61]
nSpeakers = 1




#mean_interval_triggers_frames = mean_interval_triggers_sec * srate_processed




# Since we have to play nTrials_1Block in maximum max_duration100Trials_sec,
# estimates the number of trigger we would have to find during the
# calibration (aka baseline).

#interval_trigger_sec = max_duration100Trials_sec / nTrials_1Block # how many trigger should be found for each block

nTrigger_Baseline = round(baseline_duration_sec / mean_interval_triggers_sec) # how many triggers should be found during calibration



# Stimuli ----------------------------------------------------------------------


# Prepare file background noise
noise_duration_sec = 55
sound_noise = sound.Sound('constantNoise_1minute_48kHz_filtered_mono_looped.wav',loops = -1, preBuffer= -1)  


# ML part: (using river incr learning package)
#model = compose.Pipeline(
#    preprocessing.StandardScaler(),
#    linear_model.LogisticRegression( optim.SGD(lr=0.01) )
#    )
#metric = metrics.ROCAUC()


# ML definition part:
# ATM we are NOT using the pipeline approach,
# easier to access the weights of the logreg model!
init_model_with_GA = True

scaler = preprocessing.StandardScaler()
optimizer = optim.SGD(lr=0.25)
log_reg = linear_model.LogisticRegression(optimizer)

y_true = []
y_pred = []

metric = metrics.ROCAUC()



# TODO: need to read this in!
logreg_GA_weights = np.array([-0.65366,-0.8439,-0.34247,0.26497,-0.96761,0.17281,-0.76015,
                              -0.05704,1.2634,2.2554,1.5669,-0.23876,-0.65028,1.3928,1.5245,-0.56074,-0.8411,-0.38715,-0.20447,0.36553,
                              2.2554,0.38178,-1.7044,-1.0085,-1.0204,1.0637,-0.24061,-0.19489,-0.49427,-0.6571,0.19257,-0.87227])

logreg_GA_weights = stats.zscore(logreg_GA_weights)
logreg_GA_weights_dict = OrderedDict(zip(elecs_def, logreg_GA_weights))
logreg_GA_weights_dict = dict(logreg_GA_weights_dict)




# --- Initialize components for Routine "Welcome" ---
Instructions_Background_Noise = visual.TextStim(win=win, name='Instructions_Background_Noise',
    text='Lieber Teilnehmer, willkommen zu unserem Experiment!\n\nVielen Dank für Deine Teilnahme. In diesem Experiment geht es darum, die Rolle neuronaler Oszillationen beim Sprachverstehen zu erforschen. Du wirst eine Reihe von Sprachstimuli – Ziffern – hören, die eingebettet sein werden in Rauschen, bzw. verzerrt dargestellt werden.\n\nBevor das eigentliche Experiment beginnt, wirst Du ein kontinuierliches Rauschen hören. Während des Abspielens des Geräuschs kannst du dem Versuchsleiter sagen, welche Lautstärke dir am besten passt.\n\nWenn du bereit bist, kannst du auf "Enter" drücken und das Geräusch wird starten.\n\n',
    font='Arial',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "Test_Background_Noise" ---
Fixation_cross_Test = visual.TextStim(win=win, name='Fixation_cross_Test',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "Instructions_practice" ---
text_practice = visual.TextStim(win=win, name='text_practice',
    text='In Kürze wirst Du Ziffern hören, es wird immer eine einzelne Ziffer abgespielt werden, und das ganze mehrmals hintereinander.\n\nNachdem Du eine solche Ziffer gehört hast, kannst du die entsprechenden Ziffer mit der Tastatur eintippen. Du musst jedes Mal auf "Enter" drücken, um eine Ziffer zu bestätigen.\n\nBeispiel: Du hast “1” gehört, dann tippe ein: “1”, gefolgt von “ENTER”.\n\nFalls du während des Tippens einen Tippfehler machst, kannst du einfach eine neue Ziffer eintippen. Nur die letzte Eingabe zählt!\n\nSobald du bereit bist, kannst du auf "Enter" drücken und die Trainingsphase wird anfangen.\n',
    font='Arial',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_4 = keyboard.Keyboard()

# --- Initialize components for Routine "Present_practice" ---
# Run 'Begin Experiment' code from code_practice_pres
# This routine is playing 10 trials of clear digit triplets. This is meant
# for the subjects to learn how to type their response. The stimulus set is
# fixed (always the same triplets in the same order) and can be found in 
# the excel-file "practice_trials.xlsx"

#default variables
firstdigit = 0
seconddigit = 0
thirddigit = 0

speaker = [1,7,10,13,14,21,33,48,49,61]
digit1 = 'Speaker1_Digit0_adjusted.wav'
digit2 = 'Speaker1_Digit0_adjusted.wav'
digit3 = 'Speaker1_Digit0_adjusted.wav'


Digit1_clear = sound.Sound('A', secs=-1, stereo=False, hamming=False,
    name='Digit1_clear')
Digit1_clear.setVolume(1)

# --- Initialize components for Routine "Response_practice" ---
response_practice_resp = keyboard.Keyboard()
text_practice_resp = visual.TextStim(win=win, name='text_practice_resp',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);

# --- Initialize components for Routine "Repeat_practice" ---
text_practice_repeat = visual.TextStim(win=win, name='text_practice_repeat',
    text='Training wiederholen ? Bei Antwort "0" wird wiederholt, bei "Enter" gehts es weiter.',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
response_practice_repeat = keyboard.Keyboard()

# --- Initialize components for Routine "Instructions_ME" ---
text_4 = visual.TextStim(win=win, name='text_4',
    text='In Kürze wirst Du wieder Ziffern hoeren, immer eine jeweils, das ganze wiederholt.\n\nWie vorher, nach einem solchen Reiz bitte die entsprechenden Ziffer mit der Tastatur einzeln eintippen. Du musst jedes Mal auf "Enter" drücken, um zu bestätigen.\n\nBeispiel: Du hast “1” gehört, dann tippe ein: “1”, gefolgt von “ENTER”.\n\nSobald du bereit bist, kannst du auf "Enter" drücken und dieser Teil des Experimentes wird beginnen.\n',
    font='Arial',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_7 = keyboard.Keyboard()

# --- Initialize components for Routine "Prestim_ME" ---
# Run 'Begin Experiment' code from code_ME
# This is the first part of the map extraction loop
# This is for getting trials to classifify understood/non understood,
# buid a map and then use the map for triggering
# Default values for normalizing the signal
#signal_trials = []
# trial_nr = []

# Default color values
ratio_vec = 0

# initivalize matrix for all trial averages of alpha map
ratio_mat_all_avgs_ME = np.empty((200,32))
ratio_mat_all_avgs_ME[:] = np.NaN



current_mean_ratio = 0

# block and trial counter
#nBlock_ME = 1
#nTrials_ME = 0


#default variables for digit playback
firstdigit_ME = 0
seconddigit_ME = 0
thirddigit_ME = 0
noise_ME = [100,60,50,60,30,45,25,20,85]
speaker_ME = [1,7,10,13,14,21,33,48,49,61]
digit1_ME = 'NVS_Speaker_1_digit_0_100_envExtDepPt.wav_48kHz_filtered_mono'
digit2_ME = 'NVS_Speaker_1_digit_0_100_envExtDepPt.wav_48kHz_filtered_mono'
digit3_ME = 'NVS_Speaker_1_digit_0_100_envExtDepPt.wav_48kHz_filtered_mono'

# init matrix of alpha envelopes value (for one trial, 32chs, up to 100 samples)
ratio_mat_trial_ME_old = np.empty((100,32))
ratio_mat_trial_ME_old[:] = np.NaN


Fixation_ME = visual.TextStim(win=win, name='Fixation_ME',
    text='+',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "Playing_Digits_ME" ---
sound_digit_1_ME = sound.Sound('A', secs=-1, stereo=False, hamming=False,
    name='sound_digit_1_ME')
sound_digit_1_ME.setVolume(1.0)
text_2 = visual.TextStim(win=win, name='text_2',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-2.0);

# --- Initialize components for Routine "Response_subjects_ME" ---
# Run 'Begin Experiment' code from code_resp_ME
count_rme = 0

key_resp_ME = keyboard.Keyboard()
disp_answer_ME = visual.TextStim(win=win, name='disp_answer_ME',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-2.0);
text_7 = visual.TextStim(win=win, name='text_7',
    text='',
    font='Open Sans',
    pos=(0, -0.1), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# --- Initialize components for Routine "Classify_ME" ---
# Run 'Begin Experiment' code from code_5
iscorrect_trial = np.zeros((200,1))
iscorrect_trial[:] =np.nan




# --- Initialize components for Routine "Next_Block_ME" ---

# --- Initialize components for Routine "Show_Instructions_ME" ---
text_next_block_ME = visual.TextStim(win=win, name='text_next_block_ME',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
response_nextblock_ME = keyboard.Keyboard()

# --- Initialize components for Routine "Break" ---
text_break = visual.TextStim(win=win, name='text_break',
    text='Nun wird der erste Hauptblock starten. Insgesamt gibt es 4 Blöcke.\n\nWie schon vorher wirst Du zuerst ein kontinuierliches Geräusch hören und gleichzeitig ein Fixationskreuz sehen. Bitte das Kreuz fixieren. Solange das Kreuz sichtbar ist, bewege Dich bitte auch nicht.\n\nNachher wirst du 1 Ziffer hören, die verrauscht sein wird. Deine Aufgabe ist es, die Ziffer einzutippen, die du gehört hast.\n\nSobald du bereit bist, um den ersten Block zu starten, kannst du auf "Enter " drücken.\n',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
response_break = keyboard.Keyboard()

# --- Initialize components for Routine "signal_check" ---
# Run 'Begin Experiment' code from code_2
# Default values for normalizing the signal
#signal_trials = []
trial_nr = []

# Default color values
ratio_vec = 0
current_mean_ratio = 0

# block and trial counter
nExpBlock = 1
nExpTrials = 0


#default variables for digit playback
firstdigit = 0
seconddigit = 0
thirddigit = 0
noise = [100,60,50,60,30,45,25,20,85]
speaker = [1,7,10,13,14,21,33,48,49,61]
digit1 = 'NVS_Speaker_1_digit_0_100_envExtDepPt.wav_48kHz_filtered_mono'
digit2 = 'NVS_Speaker_1_digit_0_100_envExtDepPt.wav_48kHz_filtered_mono'
digit3 = 'NVS_Speaker_1_digit_0_100_envExtDepPt.wav_48kHz_filtered_mono'



Fixation = visual.TextStim(win=win, name='Fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
text_6 = visual.TextStim(win=win, name='text_6',
    text='',
    font='Open Sans',
    pos=(0, -0.1), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
text_5 = visual.TextStim(win=win, name='text_5',
    text='',
    font='Open Sans',
    pos=(0, -0.3), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# --- Initialize components for Routine "digits_played" ---
Fixation_Play = visual.TextStim(win=win, name='Fixation_Play',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-1.0);
sound_digit1 = sound.Sound('A', secs=-1, stereo=False, hamming=False,
    name='sound_digit1')
sound_digit1.setVolume(1.0)

# --- Initialize components for Routine "Response_subjects" ---
key_resp = keyboard.Keyboard()
disp_answer = visual.TextStim(win=win, name='disp_answer',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);

# --- Initialize components for Routine "Next_Block" ---

# --- Initialize components for Routine "Show_instructions" ---
text_nextblock = visual.TextStim(win=win, name='text_nextblock',
    text='',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-1.0);
response_nextblock = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "Startup" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from code_startup
# This chunk of code is generating random digit triplets for each trial and
# each condition. The triplets are unique between trials
# meaning that there is no repeated triplets within 1 condition.
# Each triplet contains different digits: no repeated digits in one triplet.
# However, the digits are not counterbalanced for each condition (experimental_SiN,
# experimental_NV, control_SiN, control_NV)

# Preparing variables
nTrials_vector = np.arange(nTrials) # create the trial ID colomn: vector [0:nTrials]
out_matrix = np.zeros((nTrials, nDigits)) # create the array template of size: rows = nTrials , columns = 3 (nDigits)
out_matrix_rest = np.zeros((nTrials, nRestElems)) # create the array template of size: rows = nTrials , columns = 3 (nDigits)

labels_colomn = np.array(["TrialID","NFB_digit1","NFB_digit2","NFB_digit3","Speaker_trial","NV_trial","Triggered_trial","Jitter_trial"]) # define the labels of the columns for excel
possible_digit = 10 # number of possible digits (with 7)
exception_digit = 7 # digit to get rid off
stimuli_digits = np.arange(possible_digit) # get a vector from 0 to 9 which are the possible digits (with 7)
stimuli_digits = np.delete(stimuli_digits, exception_digit) # delete the digit 7 (not part of the stimuli)




# GENERATING DIGITS AND PARAMS FOR EXPERIMENTAL CONDITION-
# we have: digits 1,2,3, speaker, NV vs sin, trigger vs control, jitter (for control condition)


# create the 3 digits randomly for each trial
for x in nTrials_vector:
    # randomly choose the 3 digits from the possible stimuli without 
    # remplacement (no identical digit in the same triplet)
    rand_digit = np.random.choice(stimuli_digits, size = nDigits, replace = False)

    out_matrix[x] = rand_digit

# create the info for the rest:
# speaker, nv_stim, trigger_stim, jitter_stim
trigger_vec = np.empty((len(nTrials_vector),))
trigger_vec[::2] = 1
trigger_vec[1::2] = 0

# degradation types, 1 = NV, 0 = SiN
# this implements a 2 block-wise alternative between SIN and NV
#degtype = np.random.choice([0,1],2,replace = False)

if NV_first:
    degtype = [1,0]
else:
    degtype = [0,1]        

degrad = [*np.zeros(nTrials_1Block*2)+degtype[0], *np.zeros(nTrials_1Block*2)+degtype[1]]
#print(degrad)

if SIN_only:
    degtype = [0,0]

degrad = [*np.zeros(nTrials_1Block*2)+degtype[0], *np.zeros(nTrials_1Block*2)+degtype[1]]
#print(degrad)





#degrad_trig = np.random.choice(degrad,nTrials_1Block*2,replace = False)
#degrad_ctrl = np.random.choice(degrad,nTrials_1Block*2,replace = False)

count_ctrl = count_trig = 0
for x in nTrials_vector:
    # randomly choose speaker, degradation type, alternate trigger vs control, add random jitter 
    # remplacement (no identical digit in the same triplet)
    rand_speaker = np.random.choice(speaker, size = nSpeakers, replace = False)
    #rand_degrad = np.random.choice(degradation, size = 1, replace = True)
    
    rand_trigger = trigger_vec[x]
    # for trigger trials, no extra jitter
    if  (x % 2) == 0:
        rand_jitter = 0
        count_trig+=1
    # but for control, yes
    else:
        rand_jitter= np.round(np.random.uniform(-2,2,1))
        #rand_degrad = degrad_ctrl[count_ctrl]    
        count_ctrl+=1
    
    rand_degrad = int(degrad[x])

    out_matrix_rest[x] = rand_speaker,rand_degrad,rand_trigger,rand_jitter



# get the unique triplets to identify which triplets are repeated between trials
unique_triplets, index_uniques, count_rep_triplets = np.unique(out_matrix, axis = 0, return_index=True, return_counts=True)

# check if there is at least one row which is repeated (containing the same digits as another row)
repeated_triplets = np.where(count_rep_triplets > 1) # a value > 1 means that the current row (triplet) is present more than once
repeated_triplets = np.asarray(repeated_triplets[0]) # convert as array (more convenient)
# get the index of the repeated triplets in the original matrix
idx_repeated_triplets = index_uniques[repeated_triplets]

# if at least 1 triplet repeated ...
while len(idx_repeated_triplets) > 0:
    # choose random triplet again (without replacement to avoid identical digits in the triplet)
    out_matrix[idx_repeated_triplets[0]] = np.random.choice(stimuli_digits, size = nDigits, replace = False)
    # check again if there are some repeated triplets
    unique_triplets, index_uniques, count_rep_triplets = np.unique(out_matrix, axis = 0, return_index=True, return_counts=True)
    repeated_triplets = np.where(count_rep_triplets > 1)
    repeated_triplets = np.asarray(repeated_triplets[0])
    # get the index of the repeated triplets in the original matrix
    idx_repeated_triplets = index_uniques[repeated_triplets]
    #continue the loop until no repeated triplets anymore

# once the stimulus set is done, insert the trial ID next to the triplet
out_matrix = np.insert(out_matrix, 0, nTrials_vector, axis = 1)
out_matrix = np.append(out_matrix, out_matrix_rest, axis = 1)

nv_trl_idxs = np.where(out_matrix[:,5]==1)
trig_trl_idxs = np.where(out_matrix[:,6]==1)
sin_trl_idxs = np.where(out_matrix[:,5]==0)
ctrl_trl_idxs = np.where(out_matrix[:,6]==0)

nv_trig_trl_idx = np.intersect1d(nv_trl_idxs,trig_trl_idxs)
nv_ctrl_trl_idx = np.intersect1d(nv_trl_idxs,ctrl_trl_idxs)
sin_trig_trl_idx = np.intersect1d(sin_trl_idxs,trig_trl_idxs)
sin_ctrl_trl_idx = np.intersect1d(sin_trl_idxs,ctrl_trl_idxs)

#digits_1_ori = 

# get "original" digits from trigger NV and scramble for the other three conditions!
nfb_digit1_ori = out_matrix[sin_trig_trl_idx,1]
nfb_digit2_ori = out_matrix[sin_trig_trl_idx,2]
nfb_digit3_ori = out_matrix[sin_trig_trl_idx,3]

# scramble for control NV
nfb_digit1_scr = np.random.choice(nfb_digit1_ori,len(nfb_digit1_ori),replace = False)
nfb_digit2_scr = np.random.choice(nfb_digit2_ori,len(nfb_digit2_ori),replace = False)
nfb_digit3_scr = np.random.choice(nfb_digit3_ori,len(nfb_digit3_ori),replace = False)

if not(SIN_only):
    out_matrix[nv_ctrl_trl_idx,1] = nfb_digit1_scr
    out_matrix[nv_ctrl_trl_idx,2] = nfb_digit2_scr
    out_matrix[nv_ctrl_trl_idx,3] = nfb_digit3_scr

# scramble for trigger NV
nfb_digit1_scr = np.random.choice(nfb_digit1_ori,len(nfb_digit1_ori),replace = False)
nfb_digit2_scr = np.random.choice(nfb_digit2_ori,len(nfb_digit2_ori),replace = False)
nfb_digit3_scr = np.random.choice(nfb_digit3_ori,len(nfb_digit3_ori),replace = False)
if not(SIN_only):
    out_matrix[nv_trig_trl_idx,1] = nfb_digit1_scr
    out_matrix[nv_trig_trl_idx,2] = nfb_digit2_scr
    out_matrix[nv_trig_trl_idx,3] = nfb_digit3_scr

# scramble for ctrl sin
nfb_digit1_scr = np.random.choice(nfb_digit1_ori,len(nfb_digit1_ori),replace = False)
nfb_digit2_scr = np.random.choice(nfb_digit2_ori,len(nfb_digit2_ori),replace = False)
nfb_digit3_scr = np.random.choice(nfb_digit3_ori,len(nfb_digit3_ori),replace = False)

out_matrix[sin_ctrl_trl_idx,1] = nfb_digit1_scr
out_matrix[sin_ctrl_trl_idx,2] = nfb_digit2_scr
out_matrix[sin_ctrl_trl_idx,3] = nfb_digit3_scr




# insert labels of columns for PsychoPy to read conditions
out_matrix_4xlsx = np.vstack((labels_colomn, out_matrix))

# after vstack, the format of the triplets is not the one we want. It is a
col = np.arange(nDigits+1)
# 1 decimal string. We have to convert it in 0 decimal int.
row = np.arange(nTrials+1)
row = row [1:] # get rid of the first row since there are char strings
for x in row:
    for i in col:
        out_matrix_4xlsx[x,i] = round(float(out_matrix_4xlsx[x,i]))

# Preparing Excel files
workbook = xlsxwriter.Workbook('./data/Stimuli_exp_cond.xlsx')
worksheet = workbook.add_worksheet()
# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0
# Iterate over the data and write it out row by row.
for ID_trial, digit1, digit2, digit3,speaker,deg_type,trigger_cond,jitter in (out_matrix_4xlsx):
    worksheet.write(row, col, ID_trial)
    worksheet.write(row, col + 1, digit1)
    worksheet.write(row, col + 2, digit2)
    worksheet.write(row, col + 3, digit3)

    worksheet.write(row, col + 4, speaker)
    worksheet.write(row, col + 5, deg_type)
    worksheet.write(row, col + 6, trigger_cond)
    worksheet.write(row, col + 7, jitter)


    row += 1

workbook.close()


# keep track of which components have finished
StartupComponents = []
for thisComponent in StartupComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Startup" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in StartupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Startup" ---
for thisComponent in StartupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Startup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "Welcome" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from code_welcome
# This is the text welcoming the subjects to the experiment.
# Once they read the text, they can press enter to continue.
begin_exp = []
# set EEG marker for displaying welcome text
if use_lpt:
    port.setData(109)
# keep track of which components have finished
WelcomeComponents = [Instructions_Background_Noise]
for thisComponent in WelcomeComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Welcome" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # Run 'Each Frame' code from code_welcome
    # Get the pressed key of the subject
    begin_exp = event.getKeys(keyList=['return'])
    
    # Begin experiment once the subject pressed enter
    if "return" in begin_exp:
        # if enter is pressed, the current routine stops and we move into the next one
        continueRoutine = False
    
    # *Instructions_Background_Noise* updates
    if Instructions_Background_Noise.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Instructions_Background_Noise.frameNStart = frameN  # exact frame index
        Instructions_Background_Noise.tStart = t  # local t and not account for scr refresh
        Instructions_Background_Noise.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Instructions_Background_Noise, 'tStartRefresh')  # time at next scr refresh
        Instructions_Background_Noise.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in WelcomeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Welcome" ---
for thisComponent in WelcomeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Welcome" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "Test_Background_Noise" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from code_bg_noise
# This routine is part of the practice trials and is meant to determine the
# volume of the background noise (ask the participant if too loud / too low)

# set EEG marker for testing the background noise
if use_lpt:
    port.setData(90)

# Start playing background noise
# ELSAS code: sd.play(sound_noise, fs, loop=True)

sound_noise.play()

#frame_count = 0
# keep track of which components have finished
Test_Background_NoiseComponents = [Fixation_cross_Test]
for thisComponent in Test_Background_NoiseComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Test_Background_Noise" ---
while continueRoutine and routineTimer.getTime() < 5.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # Run 'Each Frame' code from code_bg_noise
    #frame_count += 1
    
    # *Fixation_cross_Test* updates
    if Fixation_cross_Test.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        Fixation_cross_Test.frameNStart = frameN  # exact frame index
        Fixation_cross_Test.tStart = t  # local t and not account for scr refresh
        Fixation_cross_Test.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Fixation_cross_Test, 'tStartRefresh')  # time at next scr refresh
        Fixation_cross_Test.setAutoDraw(True)
    if Fixation_cross_Test.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > Fixation_cross_Test.tStartRefresh + 5-frameTolerance:
            # keep track of stop time/frame for later
            Fixation_cross_Test.tStop = t  # not accounting for scr refresh
            Fixation_cross_Test.frameNStop = frameN  # exact frame index
            Fixation_cross_Test.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Test_Background_NoiseComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Test_Background_Noise" ---
for thisComponent in Test_Background_NoiseComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from code_bg_noise
# Stop the background noise
sound_noise.stop()
# using non-slip timing so subtract the expected duration of this Routine
routineTimer.addTime(-5.000000)

# set up handler to look after randomisation of conditions etc
practice_block = data.TrialHandler(nReps=100, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='practice_block')
thisExp.addLoop(practice_block)  # add the loop to the experiment
thisPractice_block = practice_block.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPractice_block.rgb)
if thisPractice_block != None:
    for paramName in thisPractice_block:
        exec('{} = thisPractice_block[paramName]'.format(paramName))

for thisPractice_block in practice_block:
    currentLoop = practice_block
    # abbreviate parameter names if possible (e.g. rgb = thisPractice_block.rgb)
    if thisPractice_block != None:
        for paramName in thisPractice_block:
            exec('{} = thisPractice_block[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "Instructions_practice" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_practice_inst
    # This is the text welcoming the subjects to the experiment.
    # Once they read the text, they can press enter to continue.
    
    # set EEG marker for instruction practice block
    if use_lpt:
        port.setData(100)
    
    begin_exp = []
    
    key_resp_4.keys = []
    key_resp_4.rt = []
    _key_resp_4_allKeys = []
    # keep track of which components have finished
    Instructions_practiceComponents = [text_practice, key_resp_4]
    for thisComponent in Instructions_practiceComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Instructions_practice" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_practice* updates
        if text_practice.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_practice.frameNStart = frameN  # exact frame index
            text_practice.tStart = t  # local t and not account for scr refresh
            text_practice.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_practice, 'tStartRefresh')  # time at next scr refresh
            text_practice.setAutoDraw(True)
        
        # *key_resp_4* updates
        waitOnFlip = False
        if key_resp_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_4.frameNStart = frameN  # exact frame index
            key_resp_4.tStart = t  # local t and not account for scr refresh
            key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_4.started')
            key_resp_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_4.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_4.getKeys(keyList=['return'], waitRelease=False)
            _key_resp_4_allKeys.extend(theseKeys)
            if len(_key_resp_4_allKeys):
                key_resp_4.keys = _key_resp_4_allKeys[-1].name  # just the last key pressed
                key_resp_4.rt = _key_resp_4_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Instructions_practiceComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Instructions_practice" ---
    for thisComponent in Instructions_practiceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Instructions_practice" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    practice_trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('data/practice_trials.xlsx'),
        seed=None, name='practice_trials')
    thisExp.addLoop(practice_trials)  # add the loop to the experiment
    thisPractice_trial = practice_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPractice_trial.rgb)
    if thisPractice_trial != None:
        for paramName in thisPractice_trial:
            exec('{} = thisPractice_trial[paramName]'.format(paramName))
    
    for thisPractice_trial in practice_trials:
        currentLoop = practice_trials
        # abbreviate parameter names if possible (e.g. rgb = thisPractice_trial.rgb)
        if thisPractice_trial != None:
            for paramName in thisPractice_trial:
                exec('{} = thisPractice_trial[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "Present_practice" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_practice_pres
        # Randomly choose one speaker for the current trial
        #rand_speaker = (np.random.choice(speaker, size = 1))
        #rand_speaker = int(rand_speaker[0])
        
        rand_speaker = int(Speaker_trial)
        
        #print(rand_speaker)
        
        # Reading the current digits from xlsx file
        firstdigit = int(NFB_digit1)
        seconddigit = int(NFB_digit2)
        thirddigit = int(NFB_digit3)
        
        # Playing the first digit
        if firstdigit < 8:
            digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_adjusted.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_adjusted.wav'
        
        # Playing the second digit
        if seconddigit < 8:
            digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_adjusted.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_adjusted.wav'
        
        # Playing the third digit
        if thirddigit < 8:
            digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_adjusted.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
           digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_adjusted.wav'
        Digit1_clear.setSound(digit1, hamming=False)
        Digit1_clear.setVolume(1, log=False)
        # keep track of which components have finished
        Present_practiceComponents = [Digit1_clear]
        for thisComponent in Present_practiceComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Present_practice" ---
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from code_practice_pres
            # set EEG marker bei each digit onset
            if use_lpt:
                if Digit1_clear.status == STARTED:
                    port.setData(10)
                elif Digit2_clear.status == STARTED:
                    port.setData(20)
                elif Digit3_clear.status == STARTED:
                    port.setData(30)
            # start/stop Digit1_clear
            if Digit1_clear.status == NOT_STARTED and t >= 0-frameTolerance:
                # keep track of start time/frame for later
                Digit1_clear.frameNStart = frameN  # exact frame index
                Digit1_clear.tStart = t  # local t and not account for scr refresh
                Digit1_clear.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('Digit1_clear.started', t)
                Digit1_clear.play()  # start the sound (it finishes automatically)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Present_practiceComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Present_practice" ---
        for thisComponent in Present_practiceComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        Digit1_clear.stop()  # ensure sound has stopped at end of routine
        # the Routine "Present_practice" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        response_practice = data.TrialHandler(nReps=nDigits_practice, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='response_practice')
        thisExp.addLoop(response_practice)  # add the loop to the experiment
        thisResponse_practice = response_practice.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisResponse_practice.rgb)
        if thisResponse_practice != None:
            for paramName in thisResponse_practice:
                exec('{} = thisResponse_practice[paramName]'.format(paramName))
        
        for thisResponse_practice in response_practice:
            currentLoop = response_practice
            # abbreviate parameter names if possible (e.g. rgb = thisResponse_practice.rgb)
            if thisResponse_practice != None:
                for paramName in thisResponse_practice:
                    exec('{} = thisResponse_practice[paramName]'.format(paramName))
            
            # --- Prepare to start Routine "Response_practice" ---
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_practice_resp
            # In this routine, the reponse of the subject are saved.
            # The subjects have to type the 3 digits separately (one per screen) and confirm
            # their end choice by pressing enter: digit 1 - ENTER - digit 2 - ENTER - digit 3 - ENTER
            # Output: Excel file in the data folder of PsychoPy. Note that every key pressed
            # are saved in this output file. The actual response of the subject is the reponse
            # just before the "enter" keypress
            
            response = ''
            theseKeys3 = []
            keyPress = []
            response_string = []
            
            
            left_text = visual.TextStim(win_info, text='Practice trials going on', flipHoriz=False)
            left_text.setAutoDraw(True)
            win_info.flip()
            
            response_practice_resp.keys = []
            response_practice_resp.rt = []
            _response_practice_resp_allKeys = []
            # keep track of which components have finished
            Response_practiceComponents = [response_practice_resp, text_practice_resp]
            for thisComponent in Response_practiceComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Response_practice" ---
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # Run 'Each Frame' code from code_practice_resp
                # Collect every pressed key
                #keyPress = event.getKeys(keyList=['1','2','3','4','5','6','8','9','0', 'return'])
                #keyPress = event.getKeys(keyList=['num_1','num_2','num_3','num_4','num_5','num_6', 'num_7', 'num_8','num_9','num_0', 'return'])
                
                # Gather the pressed key in a string vector
                response_string = "".join(response_practice_resp.keys).replace('num_', '')
                #response_string = "".join(key_resp_test.keys)
                
                if response_string: # if response_string is not empty:
                    # only disp the last pressed key to enable the subjects to do corrections 
                    # (their final response is the last keypress before "enter")
                    response = response_string[-1] 
                
                response_text = "Gehörte Ziffer: {}".format(response)
                
                #if "return" in keyPress: # if "enter" key pressed
                #    continueRoutine = False # pass to the next iteration (digit)
                
                if "return" in response_practice_resp.keys: # if "enter" key pressed
                    continueRoutine = False # pass to the next iteration (digit)
                
                
                # *response_practice_resp* updates
                waitOnFlip = False
                if response_practice_resp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    response_practice_resp.frameNStart = frameN  # exact frame index
                    response_practice_resp.tStart = t  # local t and not account for scr refresh
                    response_practice_resp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(response_practice_resp, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'response_practice_resp.started')
                    response_practice_resp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(response_practice_resp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(response_practice_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if response_practice_resp.status == STARTED and not waitOnFlip:
                    theseKeys = response_practice_resp.getKeys(keyList=['num_0','num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9', 'return'], waitRelease=False)
                    _response_practice_resp_allKeys.extend(theseKeys)
                    if len(_response_practice_resp_allKeys):
                        response_practice_resp.keys = [key.name for key in _response_practice_resp_allKeys]  # storing all keys
                        response_practice_resp.rt = [key.rt for key in _response_practice_resp_allKeys]
                
                # *text_practice_resp* updates
                if text_practice_resp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    text_practice_resp.frameNStart = frameN  # exact frame index
                    text_practice_resp.tStart = t  # local t and not account for scr refresh
                    text_practice_resp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_practice_resp, 'tStartRefresh')  # time at next scr refresh
                    text_practice_resp.setAutoDraw(True)
                if text_practice_resp.status == STARTED:  # only update if drawing
                    text_practice_resp.setText(response_text, log=False)
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Response_practiceComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Response_practice" ---
            for thisComponent in Response_practiceComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # Run 'End Routine' code from code_practice_resp
            # set EEG marker after each digit response 
            if use_lpt:
                if response_practice.thisN == 0:
                    port.setData(40)
                elif response_practice.thisN == 1:
                    port.setData(50)
                elif response_practice.thisN == 2:
                    port.setData(60)
            
            left_text.setAutoDraw(False)
            win_info.flip()
            
            #print(response_practice.thisN)
            # check responses
            if response_practice_resp.keys in ['', [], None]:  # No response was made
                response_practice_resp.keys = None
            response_practice.addData('response_practice_resp.keys',response_practice_resp.keys)
            if response_practice_resp.keys != None:  # we had a response
                response_practice.addData('response_practice_resp.rt', response_practice_resp.rt)
            # the Routine "Response_practice" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed nDigits_practice repeats of 'response_practice'
        
        thisExp.nextEntry()
        
    # completed 1 repeats of 'practice_trials'
    
    
    # --- Prepare to start Routine "Repeat_practice" ---
    continueRoutine = True
    # update component parameters for each repeat
    response_practice_repeat.keys = []
    response_practice_repeat.rt = []
    _response_practice_repeat_allKeys = []
    # keep track of which components have finished
    Repeat_practiceComponents = [text_practice_repeat, response_practice_repeat]
    for thisComponent in Repeat_practiceComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Repeat_practice" ---
    while continueRoutine and routineTimer.getTime() < 5.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_practice_repeat
        if response_practice_repeat.keys == 'return':
            practice_block.finished=1
            practice_trials.finished=1
            continueRoutine = False
        
        # *text_practice_repeat* updates
        if text_practice_repeat.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_practice_repeat.frameNStart = frameN  # exact frame index
            text_practice_repeat.tStart = t  # local t and not account for scr refresh
            text_practice_repeat.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_practice_repeat, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_practice_repeat.started')
            text_practice_repeat.setAutoDraw(True)
        if text_practice_repeat.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_practice_repeat.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                text_practice_repeat.tStop = t  # not accounting for scr refresh
                text_practice_repeat.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_practice_repeat.stopped')
                text_practice_repeat.setAutoDraw(False)
        
        # *response_practice_repeat* updates
        waitOnFlip = False
        if response_practice_repeat.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            response_practice_repeat.frameNStart = frameN  # exact frame index
            response_practice_repeat.tStart = t  # local t and not account for scr refresh
            response_practice_repeat.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(response_practice_repeat, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'response_practice_repeat.started')
            response_practice_repeat.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(response_practice_repeat.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(response_practice_repeat.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if response_practice_repeat.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > response_practice_repeat.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                response_practice_repeat.tStop = t  # not accounting for scr refresh
                response_practice_repeat.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'response_practice_repeat.stopped')
                response_practice_repeat.status = FINISHED
        if response_practice_repeat.status == STARTED and not waitOnFlip:
            theseKeys = response_practice_repeat.getKeys(keyList=['num_0','return'], waitRelease=False)
            _response_practice_repeat_allKeys.extend(theseKeys)
            if len(_response_practice_repeat_allKeys):
                response_practice_repeat.keys = _response_practice_repeat_allKeys[-1].name  # just the last key pressed
                response_practice_repeat.rt = _response_practice_repeat_allKeys[-1].rt
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Repeat_practiceComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Repeat_practice" ---
    for thisComponent in Repeat_practiceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_practice_repeat
    # It asks if we want to repeat the practice block. This is in case the subject
    # did not understand either the task or the way to provide his answer (or both).
    # ...Start the practice block again: press "y" (you have 20 seconds to press "y". If
    # you don't, the experiment will go on)
    # ...Don't retart it: just wait and the experiment will go on
    
    if response_practice_repeat.keys == 'num_0':
        practice_block.finished=0
        continueRoutine = True 
    elif response_practice_repeat.keys == 'return':
        practice_block.finished=1
        practice_trials.finished=1
        continueRoutine = False
    else:
        practice_block.finished=1
        practice_trials.finished=1
        continueRoutine = False
        
            
            
    # using non-slip timing so subtract the expected duration of this Routine
    routineTimer.addTime(-5.000000)
    thisExp.nextEntry()
    
# completed 100 repeats of 'practice_block'


# --- Prepare to start Routine "Instructions_ME" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from code_11
# Instructions of the experiment. Subject presses enter to continue

# set EEG marker for instructions experiment
if use_lpt:
    port.setData(102)

#begin_expBlock = []
key_resp_7.keys = []
key_resp_7.rt = []
_key_resp_7_allKeys = []
# keep track of which components have finished
Instructions_MEComponents = [text_4, key_resp_7]
for thisComponent in Instructions_MEComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Instructions_ME" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_4* updates
    if text_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_4.frameNStart = frameN  # exact frame index
        text_4.tStart = t  # local t and not account for scr refresh
        text_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_4, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_4.started')
        text_4.setAutoDraw(True)
    
    # *key_resp_7* updates
    waitOnFlip = False
    if key_resp_7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_7.frameNStart = frameN  # exact frame index
        key_resp_7.tStart = t  # local t and not account for scr refresh
        key_resp_7.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_7, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp_7.started')
        key_resp_7.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_7.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_7.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_7.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_7.getKeys(keyList=['return'], waitRelease=False)
        _key_resp_7_allKeys.extend(theseKeys)
        if len(_key_resp_7_allKeys):
            key_resp_7.keys = _key_resp_7_allKeys[-1].name  # just the last key pressed
            key_resp_7.rt = _key_resp_7_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Instructions_MEComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Instructions_ME" ---
for thisComponent in Instructions_MEComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Instructions_ME" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
ME_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('V:/gfraga/scripts_neulin/Projects/SINEEG/Experiments/WiN/PsychoPy/data/Stimuli_ME_cond.xlsx'),
    seed=None, name='ME_trials')
thisExp.addLoop(ME_trials)  # add the loop to the experiment
thisME_trial = ME_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisME_trial.rgb)
if thisME_trial != None:
    for paramName in thisME_trial:
        exec('{} = thisME_trial[paramName]'.format(paramName))

for thisME_trial in ME_trials:
    currentLoop = ME_trials
    # abbreviate parameter names if possible (e.g. rgb = thisME_trial.rgb)
    if thisME_trial != None:
        for paramName in thisME_trial:
            exec('{} = thisME_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "Prestim_ME" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_ME
    # In this routine, we check the ongoing alpha ratio of the subject. If an alpha
    # ratio sample is greater than the threshold, the stimuli are triggered.
    # Threshold = mean_ratio_calibration + estimated_indiv_factor * std_ratio_calibration
    
    # set EEG marker for calibration
    if use_lpt:
        port.setData(trigger_me)
    
    
    
    #continueRoutine = True
    count = 0
    disp = 0
    #signal_current_trial = np.array([])
    
    #ratio_mat_rs_ME = []
    
    ratio_mat_trial_ME = np.empty((100,32))
    ratio_mat_trial_ME[:] = np.NaN
    
    
    #trigger1 = time.time() # get timestamp as seconds
    #trigger2 = 0
    t_trial_start_ME = time.time()
    #if order_task_trial[nExpTrials] == 0:
    #    NV = 1
    #    SiN = 0
    #else: 
    #    NV = 0
    #    SiN = 1
    
    # query speaker for trial
    #rand_speaker = np.random.choice(speaker, size = 1)
    rand_speaker_ME = int(Speaker_trial_ME)
    
    # query jiiter for trial
    jitter_secs_ME = int(round(Jitter_trial_ME))
    
    
    # set upper bound for control condition ITI to be 5 seconds +/- 1
    if ctrl_ITI_secs_ME > 10:
        ctrl_ITI_secs_ME = 5
    
    #print(rand_speaker)
    
    # Defining the current digits (loaded frin xls file)
    firstdigit_ME = int(NFB_digit1_ME)
    seconddigit_ME = int(NFB_digit2_ME)
    thirddigit_ME = int(NFB_digit3_ME)
    
    # query degradation type for trial
    SiN = 1
    
    
    
    if SiN == 1:
        
        # Playing the first digit
        if firstdigit_ME < 8:
            digit1_ME = 'Speaker'+str(rand_speaker_ME)+'_Digit'+str(firstdigit_ME)+'_adjusted.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit1_ME = 'Speaker'+str(rand_speaker_ME)+'_Digit'+str(firstdigit_ME)+'_adjusted.wav'
    
        # Playing the second digit
        if seconddigit_ME < 8:
            digit2_ME = 'Speaker'+str(rand_speaker_ME)+'_Digit'+str(seconddigit_ME)+'_adjusted.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit2_ME = 'Speaker'+str(rand_speaker_ME)+'_Digit'+str(seconddigit_ME)+'_adjusted.wav'
    
        # Playing the third digit
        if thirddigit_ME < 8:
            digit3_ME = 'Speaker'+str(rand_speaker_ME)+'_Digit'+str(thirddigit_ME)+'_adjusted.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit3_ME = 'Speaker'+str(rand_speaker_ME)+'_Digit'+str(thirddigit_ME)+'_adjusted.wav'
    
    
    
    
    
    
    # shall we try to prepare sounds here?
    
    sound_digit1_ME = sound.Sound(digit1_ME, preBuffer= -1)
    sound_digit2_ME = sound.Sound(digit2_ME, preBuffer= -1)
    sound_digit3_ME = sound.Sound(digit3_ME, preBuffer= -1)
     
    # query stim condition fro trial
    
    trial_trig_ME = False
    
    # Start playing background noise
    sound_noise.play(loops = 2)
    
    
    
    # keep track of which components have finished
    Prestim_MEComponents = [Fixation_ME]
    for thisComponent in Prestim_MEComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Prestim_ME" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_ME
        # actualize count of frame
        
        current_time_ME = time.time()
        passed_time_ME = current_time_ME - t_trial_start_ME
        
        # pull chunks from the EEG stream
        chunk_ME, timestamps_ME = inlet_EEG_32.pull_sample()
        
        # get all you can get, throw away the last value (usually a zero)
        ratio_elecs_ME = chunk_ME[0:-1]
            
        # if we want to run adaptive:    
        # add more onto the previous baseline measurements to allow updateing
        #ratio_mat_rs_ME = np.append(ratio_mat_rs_ME, ratio_elecs_ME) 
        
        ratio_mat_trial_ME[count,:] = np.array(ratio_elecs_ME)
        
         #+ jitter_secs_ME: # wait for 2 seconds (ITI) before checking if the threshold is reached
        if passed_time_ME > ITI_secs_ME:
            continueRoutine = False # ends the current routine                
        
        count += 1
        
        
        
        # *Fixation_ME* updates
        if Fixation_ME.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Fixation_ME.frameNStart = frameN  # exact frame index
            Fixation_ME.tStart = t  # local t and not account for scr refresh
            Fixation_ME.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Fixation_ME, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Fixation_ME.started')
            Fixation_ME.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Prestim_MEComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Prestim_ME" ---
    for thisComponent in Prestim_MEComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_ME
    ratio_mat_rs_ME_sh = str(ratio_mat_trial_ME.shape)
    # the Routine "Prestim_ME" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Playing_Digits_ME" ---
    continueRoutine = True
    # update component parameters for each repeat
    sound_digit_1_ME.setSound(digit1_ME, hamming=False)
    sound_digit_1_ME.setVolume(1.0, log=False)
    text_2.setText(ME_trials.thisTrialN)
    # keep track of which components have finished
    Playing_Digits_MEComponents = [sound_digit_1_ME, text_2]
    for thisComponent in Playing_Digits_MEComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Playing_Digits_ME" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_pd_ME
        if use_lpt:
            # trigger condition, set the right triggers
            if sound_digit1_ME.status == STARTED:
                port.setData(14)
            elif sound_digit2_ME.status == STARTED:
                port.setData(24)
            elif sound_digit3_ME.status == STARTED:
                port.setData(34)
        # start/stop sound_digit_1_ME
        if sound_digit_1_ME.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sound_digit_1_ME.frameNStart = frameN  # exact frame index
            sound_digit_1_ME.tStart = t  # local t and not account for scr refresh
            sound_digit_1_ME.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('sound_digit_1_ME.started', t)
            sound_digit_1_ME.play()  # start the sound (it finishes automatically)
        
        # *text_2* updates
        if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_2.frameNStart = frameN  # exact frame index
            text_2.tStart = t  # local t and not account for scr refresh
            text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_2.started')
            text_2.setAutoDraw(True)
        if text_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_2.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                text_2.tStop = t  # not accounting for scr refresh
                text_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_2.stopped')
                text_2.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Playing_Digits_MEComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Playing_Digits_ME" ---
    for thisComponent in Playing_Digits_MEComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_pd_ME
    count_rme = 0
    sound_digit_1_ME.stop()  # ensure sound has stopped at end of routine
    # the Routine "Playing_Digits_ME" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    response_ME = data.TrialHandler(nReps=nDigits_ME, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='response_ME')
    thisExp.addLoop(response_ME)  # add the loop to the experiment
    thisResponse_ME = response_ME.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisResponse_ME.rgb)
    if thisResponse_ME != None:
        for paramName in thisResponse_ME:
            exec('{} = thisResponse_ME[paramName]'.format(paramName))
    
    for thisResponse_ME in response_ME:
        currentLoop = response_ME
        # abbreviate parameter names if possible (e.g. rgb = thisResponse_ME.rgb)
        if thisResponse_ME != None:
            for paramName in thisResponse_ME:
                exec('{} = thisResponse_ME[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "Response_subjects_ME" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_resp_ME
        # In this routine, the reponse of the subject are saved.
        # The subjects have to type the 3 digits separately (one per screen) and confirm
        # their end choice by pressing enter: digit 1 - ENTER - digit 2 - ENTER - digit 3 - ENTER
        # Output: Excel file in the data folder of PsychoPy. Note that every key pressed
        # are saved in this output file. The actual response of the subject is the reponse
        # just before the "enter" keypress
        
        
        response = ''
        theseKeys3 = []
        keyPress = []
        response_string = []
        
        
        # just in case, restart noise sound, loop it twice 
        # workaround for problem with automatic looping
        # enough for any proper triggering ATM (lasts more than 110secs)
        sound_noise.play(loops = 2)
        key_resp_ME.keys = []
        key_resp_ME.rt = []
        _key_resp_ME_allKeys = []
        text_7.setText(count_rme)
        # keep track of which components have finished
        Response_subjects_MEComponents = [key_resp_ME, disp_answer_ME, text_7]
        for thisComponent in Response_subjects_MEComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Response_subjects_ME" ---
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from code_resp_ME
            # Collect every pressed key
            #keyPress = event.getKeys(keyList=['num_1','num_2','num_3','num_4','num_5','num_6', 'num_7', 'num_8','num_9','num_0', 'return'])
            # Gather the pressed key in a string vector
            response_string = "".join(key_resp_ME.keys).replace('num_', '') 
            
            if response_string: # if response_string is not empty:
                # only disp the last pressed key to enable the subjects to do corrections 
                # (their final response is the last keypress before "enter")
                response = response_string[-1] 
            
            response_text = "Gehörte Ziffer: {}".format(response)
            if count_rme == 0:
                # we keep this for later classification
                response_fd_all_keys = key_resp_ME.keys
                response_fd_string = "".join(response_fd_all_keys).replace('num_', '') 
                response_firstdigit = response_fd_string 
            
            
            
            if "return" in key_resp_ME.keys: # if "enter" key pressed
                response = response_string[-1] 
                continueRoutine = False # pass to the next iteration (digit)
            
            
                    
            
            
            # *key_resp_ME* updates
            waitOnFlip = False
            if key_resp_ME.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp_ME.frameNStart = frameN  # exact frame index
                key_resp_ME.tStart = t  # local t and not account for scr refresh
                key_resp_ME.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_ME, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_ME.started')
                key_resp_ME.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_ME.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_ME.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_ME.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_ME.getKeys(keyList=['num_0','num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9', 'return','1','2','3','4','5','6','7','8','9','0'], waitRelease=False)
                _key_resp_ME_allKeys.extend(theseKeys)
                if len(_key_resp_ME_allKeys):
                    key_resp_ME.keys = [key.name for key in _key_resp_ME_allKeys]  # storing all keys
                    key_resp_ME.rt = [key.rt for key in _key_resp_ME_allKeys]
            
            # *disp_answer_ME* updates
            if disp_answer_ME.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                disp_answer_ME.frameNStart = frameN  # exact frame index
                disp_answer_ME.tStart = t  # local t and not account for scr refresh
                disp_answer_ME.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(disp_answer_ME, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'disp_answer_ME.started')
                disp_answer_ME.setAutoDraw(True)
            if disp_answer_ME.status == STARTED:  # only update if drawing
                disp_answer_ME.setText(response_text, log=False)
            
            # *text_7* updates
            if text_7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_7.frameNStart = frameN  # exact frame index
                text_7.tStart = t  # local t and not account for scr refresh
                text_7.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_7, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_7.started')
                text_7.setAutoDraw(True)
            if text_7.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text_7.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    text_7.tStop = t  # not accounting for scr refresh
                    text_7.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_7.stopped')
                    text_7.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Response_subjects_MEComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Response_subjects_ME" ---
        for thisComponent in Response_subjects_MEComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from code_resp_ME
        # set EEG marker after each digit response 
        if use_lpt:
            if response_ME.thisN == 0:
                port.setData(42)
            elif response_ME.thisN == 1:
                port.setData(52)
            elif response_ME.thisN == 2:
                port.setData(62)
                
        count_rme+=1
        # check responses
        if key_resp_ME.keys in ['', [], None]:  # No response was made
            key_resp_ME.keys = None
        response_ME.addData('key_resp_ME.keys',key_resp_ME.keys)
        if key_resp_ME.keys != None:  # we had a response
            response_ME.addData('key_resp_ME.rt', key_resp_ME.rt)
        # the Routine "Response_subjects_ME" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed nDigits_ME repeats of 'response_ME'
    
    
    # --- Prepare to start Routine "Classify_ME" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_5
    # here we preproc single trial data
    #and prep them for classification
    #trial_count_ME +=1  
    
    # use official trial counter from ME_trials
    
    # preproccing the envelope data:
    nan_tpoints = np.where(np.isnan(ratio_mat_trial_ME).any(axis=1))
    endp = nan_tpoints[0][0]-1
    ratio_mat_trial_ME = ratio_mat_trial_ME[:endp-1,:]
    
    
    ratio_vec_mat = np.concatenate((ratio_mat_trial_ME_old,ratio_mat_trial_ME))
    ratio_mat_trial_ME_old = ratio_vec_mat
    
    # always get like ~300ms prestim data for alpha, average
    prestim_vals = ratio_mat_trial_ME[-6:,:]
    prestim_trial_avg_ME = np.average(prestim_vals,axis=0)
    
    
    # add to overall matrix to keep
    #ratio_mat_all_avgs_ME[trial_count_ME,:] = prestim_trial_avg_ME
    ratio_mat_all_avgs_ME[ME_trials.thisTrialN,:] = prestim_trial_avg_ME
    
    
    # getting the current response, correct / incorrect (yi)
    
    
    
    if str(firstdigit_ME) == response_firstdigit[0]:
        iscorrect_trial[ME_trials.thisTrialN] = 1
    else:
        iscorrect_trial[ME_trials.thisTrialN] = 0
        
    currentTrlCorrect = iscorrect_trial[ME_trials.thisTrialN]
    
    # input: current 32 channel avg alpha power before stim (xi)
    xi = OrderedDict(zip(elecs_def, prestim_trial_avg_ME))
    
    yi = int(iscorrect_trial[ME_trials.thisTrialN])
    
    #yi_pred = model.predict_proba_one(xi)
    # Update the running metric with the prediction and ground truth value
    #metric.update(yi, yi_pred)
    # Train the model with the new sample
    #model.learn_one(xi, yi)
    #current_perf = float(t.replace('ROCAUC: ',''))
    #print(f'ROC AUC: {metric}')
    
    xi_scaled = scaler.learn_one(xi).transform_one(xi)
    yi_pred = log_reg.predict_proba_one(xi_scaled)
    log_reg.learn_one(xi_scaled, yi)
    
    # if set, do initializing with group average weights
    if init_model_with_GA:
        if ME_trials.thisTrialN == 1:
            for elecs in elecs_def:
                log_reg._weights[elecs] = logreg_GA_weights_dict[elecs]
    
    y_true.append(yi)
    y_pred.append(yi_pred[True])
    metric = metric.update(yi, yi_pred)
    
    logreg_perf = float(str(metric).replace('ROCAUC: ',''))
    
    
    
    # convert dict to array for later processing
    logdict = log_reg.weights
    log_reg_vec = np.array(list(logdict.items()))
    log_reg_vec = log_reg_vec[:,1]
    
    # save the updated weights from the logistic regression 
    sys.stdout = dataLogRegWeights # open Signal check file to save ratios during signal check
    print(log_reg_vec)
    sys.stdout = sys.__stdout__ # close signal check file
    
    
    # show info on experimentator screen
    left_text2 = visual.TextStim(win_info, pos=(0.0, -0.1),text='Current trial correct?:' + str(currentTrlCorrect))
    left_text2.setAutoDraw(True)
    win_info.flip()
    left_text = visual.TextStim(win_info, text='Current ROC AUC:' + str(logreg_perf))
    left_text.setAutoDraw(True)
    win_info.flip()
    
    # keep track of which components have finished
    Classify_MEComponents = []
    for thisComponent in Classify_MEComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Classify_ME" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Classify_MEComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Classify_ME" ---
    for thisComponent in Classify_MEComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_5
    left_text.setAutoDraw(False)
    win_info.flip()
    
    # the Routine "Classify_ME" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Next_Block_ME" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_nb_ME
    # At the end of the first block, there is a text saying that there is a break.
    # at the end of the second block, there is a text saying that there is a break
    # and that the experimentator will come to the room.
    # The subject can press "enter" whenever he is ready to go on
    
    # changing / displaying the instruction depending on the current block finished
    instructions_next_block_ME = ''
    # if it is the last trial of the first block
    if nTrials_ME == (nTrials_1Block_ME - 1):
        sound_noise.stop() # Stop the background noise
        instructions_next_block_ME = '''Du hast den ersten Block geschafft, Glückwunsch! Du kannst Dich kurz entspannen, wenn nötig.
        
        Sobald Du bereit bist, um den nächsten Block zu starten, kannst Du auf "Enter" drücken.
        
        Weiterhin gilt: Solange das Fixationskreuz sichtbar ist, bewege Dich bitte nicht.'''
    # if it is the last trial of the second block
    elif nTrials_ME == (nTrials_1Block_ME*2 - 1):
        sound_noise.stop() # Stop the background noise
        instructions_next_block_ME = '''Du hast den zweiten Block geschafft, Glückwunsch!
        
        Zeit für eine kurze Pause. Der/die VersuchsleiterIn wird in Kürze in den Raum kommen.
        Sobald Du danach bereit bist, um den nächsten Block zu starten, kannst Du auf "Enter" drücken.'''
        
    elif nTrials_ME == (nTrials_1Block_ME*3 - 1):
        sound_noise.stop() # Stop the background noise
        instructions_next_block_ME = '''Du hast den dritten Block geschafft, Glückwunsch!
        
         Sobald Du bereit bist, um den nächsten Block zu starten, kannst Du auf "Enter" drücken.'''
    
    elif nTrials_ME == (nTrials_1Block_ME*4 - 1):
        sound_noise.stop() # Stop the background noise
        instructions_next_block_ME = '''Du hast den letzten Block geschafft, Glückwunsch!
        
        Vielen Dank für Deine Teilnahme! Der/die VersuchsleiterIn wird in Kürze in den Raum kommen.'''
    
    elif logreg_perf > threshold_performance or count > max_ntrials_ME:
        sound_noise.stop() # Stop the background noise
        instructions_next_block_ME = '''Die Kalibrierungphase ist zu Ende, gut gemacht!
        
        Der/die VersuchsleiterIn wird in Kürze in den Raum kommen.'''
        
        # need to prepare data for trigger condition:
        # instead of long calibration we just apply the newly acquired weights and run them 
        # (multiply data by weights) on the already acquired prestim data and get summary stats
        # like mean and std. then use trigger criterion (how many triggers per minute) to establish 
        # the individual factor
        
        ratio_vec_rs  = ratio_vec_mat.astype(float) * log_reg_vec.astype(float)
        ratio_vec_mean = np.nanmean(ratio_vec_rs)
        ratio_vec_std = np.nanstd(ratio_vec_rs)
        indiv_factor = indiv_factor_def
    
        print(ratio_vec_mean)
        print(ratio_vec_std)
        print(indiv_factor)
        
        
        # save the updated weights from the logistic regression 
        # if we end up with ROC AUC > 0.6:
        if count < max_ntrials_ME:
            final_weights = log_reg_vec
            
        # if we end up with ROC AUC < 0.6:
        # use group average weights 
        else:
            final_weights = logreg_GA_weights
        
        #final_weights = np.round(final_weights,5)
        
        sys.stdout = dataLogRegWeightsFinal # open Signal check file to save ratios during signal check
        print(final_weights)
        sys.stdout = sys.__stdout__ # close signal check file
        
        template_string_weights = str(list(final_weights)).replace(',',';').replace('[','').replace(']','')
        template_string_weights = template_string_weights.replace("'","").replace(' ','')
        template_string_begin = '<OpenViBE-SettingsOverride>\n<SettingValue>'
        template_string_end = '</SettingValue>\n<SettingValue>1</SettingValue>\n<SettingValue>32</SettingValue>\n<SettingValue></SettingValue>\n</OpenViBE-SettingsOverride>'
    
        file1 = open("../OpenVibe/Alpha_triggered_map_spatial_filters_individual.cfg","w+")
        file1.writelines(template_string_begin)
        file1.writelines(template_string_weights)
        file1.writelines(template_string_end)
        file1.close()    
        
        # also - close 32 channel stream!
        # inlet_EEG_32.flush()
        # inlet_EEG_32 = inlet_EEG_32.close_stream()
        
        #inlet_EEG_32 = inlet_EEG_32.__del__()
        
    # if other trial
    else:
        continueRoutine = False
    # keep track of which components have finished
    Next_Block_MEComponents = []
    for thisComponent in Next_Block_MEComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Next_Block_ME" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_nb_ME
        # Get the pressed key of the subject
        begin_Block_ME = event.getKeys(keyList=['return'])
        
        # Begin experiment once the subject pressed enter
        if "return" in begin_Block_ME:
            continueRoutine = False # wait for the subject to press the key "enter"
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Next_Block_MEComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Next_Block_ME" ---
    for thisComponent in Next_Block_MEComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_nb_ME
    # set EEG marker for each instruction (after 1st and 2nd block are finished) 
    if use_lpt:
            port.setData(212)
        
    # Start playing background noise
    sound_noise.play()
    
    #print(signal_trials)
    
    # Update Trial counter
    #nExpTrials += 1
    # the Routine "Next_Block_ME" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Show_Instructions_ME" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_nextblock_ME
    #just go on with next trial, if there is no pause ...
    if not instructions_next_block_ME:
        continueRoutine = False
    text_next_block_ME.setText(instructions_next_block_ME)
    response_nextblock_ME.keys = []
    response_nextblock_ME.rt = []
    _response_nextblock_ME_allKeys = []
    # keep track of which components have finished
    Show_Instructions_MEComponents = [text_next_block_ME, response_nextblock_ME]
    for thisComponent in Show_Instructions_MEComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Show_Instructions_ME" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_next_block_ME* updates
        if text_next_block_ME.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_next_block_ME.frameNStart = frameN  # exact frame index
            text_next_block_ME.tStart = t  # local t and not account for scr refresh
            text_next_block_ME.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_next_block_ME, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_next_block_ME.started')
            text_next_block_ME.setAutoDraw(True)
        
        # *response_nextblock_ME* updates
        waitOnFlip = False
        if response_nextblock_ME.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            response_nextblock_ME.frameNStart = frameN  # exact frame index
            response_nextblock_ME.tStart = t  # local t and not account for scr refresh
            response_nextblock_ME.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(response_nextblock_ME, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'response_nextblock_ME.started')
            response_nextblock_ME.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(response_nextblock_ME.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(response_nextblock_ME.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if response_nextblock_ME.status == STARTED and not waitOnFlip:
            theseKeys = response_nextblock_ME.getKeys(keyList=['return'], waitRelease=False)
            _response_nextblock_ME_allKeys.extend(theseKeys)
            if len(_response_nextblock_ME_allKeys):
                response_nextblock_ME.keys = _response_nextblock_ME_allKeys[-1].name  # just the last key pressed
                response_nextblock_ME.rt = _response_nextblock_ME_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Show_Instructions_MEComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Show_Instructions_ME" ---
    for thisComponent in Show_Instructions_MEComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_nextblock_ME
    if logreg_perf > threshold_performance:
        ME_trials.finished=1
        continueRoutine = False
    # check responses
    if response_nextblock_ME.keys in ['', [], None]:  # No response was made
        response_nextblock_ME.keys = None
    ME_trials.addData('response_nextblock_ME.keys',response_nextblock_ME.keys)
    if response_nextblock_ME.keys != None:  # we had a response
        ME_trials.addData('response_nextblock_ME.rt', response_nextblock_ME.rt)
    # the Routine "Show_Instructions_ME" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'ME_trials'


# --- Prepare to start Routine "Break" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from code_6
# Instructions of the experiment. Subject presses enter to continue

# set EEG marker for instructions experiment
if use_lpt:
    port.setData(102)

#begin_expBlock = []



# show info on experimentator screen
left_text = visual.TextStim(win_info, text='Final ROC AUC:' + str(logreg_perf))
left_text.setAutoDraw(True)
win_info.flip()

#olddir = os.getcwd()
#os.chdir(openvibetoolboxdir)
#os.system("taskkill /f /im  openvibe-designer.exe")
#os.system("taskkill /f /im  openvibe-designer.exe")
#os.system("taskkill /f /im  openvibe-designer.exe")
#os.system("taskkill /f /im  openvibe-designer.exe")



#if not(use_debug):
#    os.system('openvibe-designer.exe --play ' + '"' + openvibedir +  '/Alpha_triggered_post_ME.xml' + '"')
#else:
#    os.system('openvibe-designer.exe --play ' + '"' + openvibedir +  '/Alpha_triggered_post_ME_debug.xml' + '"')
        
#os.chdir(olddir)

#time.sleep(3)
        
        
        
#print("looking for logreg weighted alpha stream...")
#streams_EEG = resolve_stream('type', 'EEG_extracted')
#inlet_EEG = StreamInlet(streams_EEG[0], max_buflen = 1, max_chunklen =1, processing_flags =  1 | 2 | 4 | 8) # create new inlets to read from the streams

response_break.keys = []
response_break.rt = []
_response_break_allKeys = []
# keep track of which components have finished
BreakComponents = [text_break, response_break]
for thisComponent in BreakComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Break" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_break* updates
    if text_break.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_break.frameNStart = frameN  # exact frame index
        text_break.tStart = t  # local t and not account for scr refresh
        text_break.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_break, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_break.started')
        text_break.setAutoDraw(True)
    
    # *response_break* updates
    waitOnFlip = False
    if response_break.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        response_break.frameNStart = frameN  # exact frame index
        response_break.tStart = t  # local t and not account for scr refresh
        response_break.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(response_break, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'response_break.started')
        response_break.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(response_break.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(response_break.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if response_break.status == STARTED and not waitOnFlip:
        theseKeys = response_break.getKeys(keyList=['return'], waitRelease=False)
        _response_break_allKeys.extend(theseKeys)
        if len(_response_break_allKeys):
            response_break.keys = _response_break_allKeys[-1].name  # just the last key pressed
            response_break.rt = _response_break_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in BreakComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Break" ---
for thisComponent in BreakComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Break" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
exp_trials = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('data/Stimuli_exp_cond.xlsx'),
    seed=None, name='exp_trials')
thisExp.addLoop(exp_trials)  # add the loop to the experiment
thisExp_trial = exp_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisExp_trial.rgb)
if thisExp_trial != None:
    for paramName in thisExp_trial:
        exec('{} = thisExp_trial[paramName]'.format(paramName))

for thisExp_trial in exp_trials:
    currentLoop = exp_trials
    # abbreviate parameter names if possible (e.g. rgb = thisExp_trial.rgb)
    if thisExp_trial != None:
        for paramName in thisExp_trial:
            exec('{} = thisExp_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "signal_check" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_2
    # In this routine, we check the ongoing alpha ratio of the subject. If an alpha
    # ratio sample is greater than the threshold, the stimuli are triggered.
    # Threshold = mean_ratio_calibration + estimated_indiv_factor * std_ratio_calibration
    
    # set EEG marker for calibration
    if use_lpt:
        port.setData(92)
    
    
    
    #continueRoutine = True
    count = 0
    disp = 0
    
    # wait for weighted alpha stream:
    
    
    
    
    
    
    
    #signal_current_trial = np.array([])
    
    #trigger1 = time.time() # get timestamp as seconds
    #trigger2 = 0
    
    # Define the subset of stimuli to play depending on block 1 or block 2:
    # block 1: Trials 1 to 70
    # block 2: Trials 71 to 140
    # The last entry of the slice is not being included, so the last included will be (nTrials_half - 1).
    # This is what we need because we want it to be (nTrials_half-1) because of the Python indexing starting from 0
    #trial_nr = slice(0, nTrials_half) 
    
    #if nExpBlock == 2:
    #    trial_nr = slice(nTrials_half, nTrials) 
    
    #print(nExpBlock, nExpTrials, trial_nr)
    
    # Define the current task to play: NV speech or SiN
    #t_trial_start = time.time()
    t_trial_start = time.time()
    #if order_task_trial[nExpTrials] == 0:
    #    NV = 1
    #    SiN = 0
    #else: 
    #    NV = 0
    #    SiN = 1
    
    # need to move parts from digits_played to here to start preparing things!
    # In this routine, the triplets are presented once the threshold
    # was reached in the previous routine. If NV speech or SiN is presented
    # depends on the random trial order defined in startup.
    # Maybe we could find a way to buffer the audio files in order to decrease the
    # delay.
    
    # query speaker for trial
    #rand_speaker = np.random.choice(speaker, size = 1)
    rand_speaker = int(Speaker_trial)
    
    # query jiiter for trial
    jitter_secs = int(round(Jitter_trial))
    
    
    # set upper bound for control condition ITI to be 5 seconds +/- 1
    if ctrl_ITI_secs > 10:
        ctrl_ITI_secs = 5
    
    #print(rand_speaker)
    
    # Defining the current digits (loaded frin xls file)
    firstdigit = int(NFB_digit1)
    seconddigit = int(NFB_digit2)
    thirddigit = int(NFB_digit3)
    
    # query degradation type for trial
    if NV_trial == 1:
        NV = 1
        SiN = 0
    else:
        NV = 0
        SiN = 1
    
    
    
    if NV == 1 and SiN == 0:
        
        # Stop the background noise: For NV speech, we don't want any background noise
        # during stimulus presentation
        #sound_noise.stop()
        
        # Playing the first digit
        if firstdigit < 8:
            digit1 = 'NVS_4CHS_Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_'+str(noise[firstdigit])+'ptEnv_48kHz_filtered_mono.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit1 = 'NVS_4CHS_Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_'+str(noise[firstdigit-1])+'ptEnv_48kHz_filtered_mono.wav'
    
        # Playing the second digit
        if seconddigit < 8:
            digit2 = 'NVS_4CHS_Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_'+str(noise[seconddigit])+'ptEnv_48kHz_filtered_mono.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit2 = 'NVS_4CHS_Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_'+str(noise[seconddigit-1])+'ptEnv_48kHz_filtered_mono.wav'
    
        # Playing the third digit
        if thirddigit < 8:
            digit3 = 'NVS_4CHS_Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_'+str(noise[thirddigit])+'ptEnv_48kHz_filtered_mono.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit3 = 'NVS_4CHS_Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_'+str(noise[thirddigit-1])+'ptEnv_48kHz_filtered_mono.wav'
    
    
    elif NV == 0 and SiN == 1:
        
        # Playing the first digit
        if firstdigit < 8:
            digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_adjusted.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_adjusted.wav'
    
        # Playing the second digit
        if seconddigit < 8:
            digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_adjusted.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_adjusted.wav'
    
        # Playing the third digit
        if thirddigit < 8:
            digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_adjusted.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_adjusted.wav'
    
    
    
    
    
    
    # shall we try to prepare sounds here?
    
    sound_digit1 = sound.Sound(digit1, preBuffer= -1)
    sound_digit2 = sound.Sound(digit2, preBuffer= -1)
    sound_digit3 = sound.Sound(digit3, preBuffer= -1)
     
    # query stim condition fro trial
    
    if Triggered_trial:
        trial_trig = True
    else:
        trial_trig = False
    
    # overwrite individual factor, set to 1 SD
    if not(use_real_thresh):
        indiv_factor = 1
        ratio_vec_mean = 0
        ratio_vec_std = 0.5
    
    # define threshold from last calibration
    print(ratio_vec_mean)
    print(ratio_vec_std)
    print(indiv_factor)
    threshold = float(ratio_vec_mean) + float(indiv_factor) * float(ratio_vec_std)
    
    # Start playing background noise
    sound_noise.play(loops = 2)
    
    
    
    text_6.setColor('white', colorSpace='rgb')
    # keep track of which components have finished
    signal_checkComponents = [Fixation, text_6, text_5]
    for thisComponent in signal_checkComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "signal_check" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_2
        # actualize count of frame
        # count += 1
        
        current_time = time.time()
        passed_time = current_time - t_trial_start
        
        # pull chunks from the EEG stream
        #chunk, timestamps = inlet_EEG.pull_sample()
        #ratio_elecs = chunk[0]
        
        # pull chunks from the EEG stream
        chunk, timestamps = inlet_EEG_32.pull_sample()
        
        # get all you can get, throw away the last value (usually a zero)
        ratio_elecs = chunk[0:-1]
        
        ratio_elecs  = np.matmul(np.array(ratio_elecs).astype(float),np.array(final_weights).astype(float))
        
        # if we want to run adaptive:    
        # add more onto the previous baseline measurements to allow updateing
        ratio_vec_rs = np.append(ratio_vec_rs, ratio_elecs) 
        ratio_vec_mean = np.nanmean(ratio_vec_rs) # mean of the 100 seconds calibration
        ratio_vec_std = np.nanstd(ratio_vec_rs) # std of the 100 seconds calibration    
        threshold = ratio_vec_mean + indiv_factor * ratio_vec_std    
            
        # calculate the alpha ratios of the incoming signal. Blue elecs and red elecs are
        # chosen from the topomap of TH's results.
        #if ratio_elecs:
        #       
        #    sys.stdout = dataSignalCheck_file # open Signal check file to save ratios during signal check
        #    print(timestamps, ratio_elecs)
        
            
        
        if passed_time > ITI_secs: # wait for 2 seconds (ITI) before checking if the threshold is reached
            #if use_debug: # if in debug mode, stimulate every 2 seconds
            #    sys.stdout = sys.__stdout__ # close signal check file
            #    continueRoutine = False # ends the current routine
            # in trigger condition: check whether ratio larger than threshold
            if trial_trig:
                if ratio_elecs > threshold: # if threshold is reached, current routine ends and stimuli are delivered
                #if ratio_elecs == ratio_elecs:
                #    sys.stdout = sys.__stdout__ # close signal check file
                    # at which time have we triggered?
                    # we need count variable + ITI
                    #trigger2 = time.time()
                    t_trial_trig = time.time()
                    
                    # should be in seconds - this is for the next untriggered stimulation
                    ctrl_ITI_secs = (t_trial_trig - t_trial_start)
                    # toggle trial condition
                    #trial_trig = False
                    continueRoutine = False # ends the current routine
                else:
                    continueRoutine = True # ends the current routine
            # in control condition: check when enough time has passed
            else:
                if passed_time > ctrl_ITI_secs + jitter_secs: # if threshold is reached, current routine ends and stimuli are delivered
                    #if ratio_elecs == ratio_elecs:
                    # sys.stdout = sys.__stdout__ # close signal check file
                    #trigger2 = time.time()
                    # toggle trial condition
                    #trial_trig = True
                    continueRoutine = False # ends the current routine                
        
                    
        
        
        # *Fixation* updates
        if Fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Fixation.frameNStart = frameN  # exact frame index
            Fixation.tStart = t  # local t and not account for scr refresh
            Fixation.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Fixation, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Fixation.started')
            Fixation.setAutoDraw(True)
        
        # *text_6* updates
        if text_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_6.frameNStart = frameN  # exact frame index
            text_6.tStart = t  # local t and not account for scr refresh
            text_6.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_6, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_6.started')
            text_6.setAutoDraw(True)
        if text_6.status == STARTED:  # only update if drawing
            text_6.setText(threshold, log=False)
        
        # *text_5* updates
        if text_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_5.frameNStart = frameN  # exact frame index
            text_5.tStart = t  # local t and not account for scr refresh
            text_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_5, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_5.started')
            text_5.setAutoDraw(True)
        if text_5.status == STARTED:  # only update if drawing
            text_5.setText(ratio_elecs, log=False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in signal_checkComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "signal_check" ---
    for thisComponent in signal_checkComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_2
    # save signal of the current trial in a list for control condition
    # it will then be used to determine the duration it took to trigger the stimuli
    # for each trial.
    
    #signal_trials.append(signal_current_trial)
    
    #sys.stdout = MarkerExp
    #print(trigger1, trigger2)
    #sys.stdout = sys.__stdout__
    
    # the Routine "signal_check" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "digits_played" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code
    if NV == 1 and SiN == 0:
        # Start replaying background noise because it was stopped in the NV speech task
        # Elsas code: sd.play(sound_noise, fs, loop=True)
        
        sound_noise.stop()
    sound_digit1.setSound(digit1, hamming=False)
    sound_digit1.setVolume(1.0, log=False)
    # keep track of which components have finished
    digits_playedComponents = [Fixation_Play, sound_digit1]
    for thisComponent in digits_playedComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "digits_played" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code
        if use_lpt:
            # trigger condition, set the right triggers
            if trial_trig:
                if sound_digit1.status == STARTED:
                    port.setData(12)
                elif sound_digit2.status == STARTED:
                    port.setData(22)
                elif sound_digit3.status == STARTED:
                    port.setData(32)
            # control condition
            else:
                if sound_digit1.status == STARTED:
                    port.setData(13)
                elif sound_digit2.status == STARTED:
                    port.setData(23)
                elif sound_digit3.status == STARTED:
                    port.setData(33)
        
        # *Fixation_Play* updates
        if Fixation_Play.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Fixation_Play.frameNStart = frameN  # exact frame index
            Fixation_Play.tStart = t  # local t and not account for scr refresh
            Fixation_Play.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Fixation_Play, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Fixation_Play.started')
            Fixation_Play.setAutoDraw(True)
        if Fixation_Play.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Fixation_Play.tStartRefresh + 1.4-frameTolerance:
                # keep track of stop time/frame for later
                Fixation_Play.tStop = t  # not accounting for scr refresh
                Fixation_Play.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fixation_Play.stopped')
                Fixation_Play.setAutoDraw(False)
        # start/stop sound_digit1
        if sound_digit1.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sound_digit1.frameNStart = frameN  # exact frame index
            sound_digit1.tStart = t  # local t and not account for scr refresh
            sound_digit1.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('sound_digit1.started', t)
            sound_digit1.play()  # start the sound (it finishes automatically)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in digits_playedComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "digits_played" ---
    for thisComponent in digits_playedComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code
    if NV == 1 and SiN == 0:
        # Start replaying background noise because it was stopped in the NV speech task
        # Elsas code: sd.play(sound_noise, fs, loop=True)
        
        sound_noise.play()
    sound_digit1.stop()  # ensure sound has stopped at end of routine
    # the Routine "digits_played" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    response_exp = data.TrialHandler(nReps=nDigits_trigger, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='response_exp')
    thisExp.addLoop(response_exp)  # add the loop to the experiment
    thisResponse_exp = response_exp.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisResponse_exp.rgb)
    if thisResponse_exp != None:
        for paramName in thisResponse_exp:
            exec('{} = thisResponse_exp[paramName]'.format(paramName))
    
    for thisResponse_exp in response_exp:
        currentLoop = response_exp
        # abbreviate parameter names if possible (e.g. rgb = thisResponse_exp.rgb)
        if thisResponse_exp != None:
            for paramName in thisResponse_exp:
                exec('{} = thisResponse_exp[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "Response_subjects" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_resp_keys
        # In this routine, the reponse of the subject are saved.
        # The subjects have to type the 3 digits separately (one per screen) and confirm
        # their end choice by pressing enter: digit 1 - ENTER - digit 2 - ENTER - digit 3 - ENTER
        # Output: Excel file in the data folder of PsychoPy. Note that every key pressed
        # are saved in this output file. The actual response of the subject is the reponse
        # just before the "enter" keypress
        
        count = 0
        response = ''
        theseKeys3 = []
        keyPress = []
        response_string = []
        
        
        # just in case, restart noise sound, loop it twice 
        # workaround for problem with automatic looping
        # enough for any proper triggering ATM (lasts more than 110secs)
        sound_noise.play(loops = 2)
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # keep track of which components have finished
        Response_subjectsComponents = [key_resp, disp_answer]
        for thisComponent in Response_subjectsComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Response_subjects" ---
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from code_resp_keys
            # Collect every pressed key
            #keyPress = event.getKeys(keyList=['num_1','num_2','num_3','num_4','num_5','num_6', 'num_7', 'num_8','num_9','num_0', 'return'])
            # Gather the pressed key in a string vector
            response_string = "".join(key_resp.keys).replace('num_', '') 
            
            if response_string: # if response_string is not empty:
                # only disp the last pressed key to enable the subjects to do corrections 
                # (their final response is the last keypress before "enter")
                response = response_string[-1] 
            
            response_text_exp = "Gehörte Ziffer: {}".format(response)
            
            if "return" in key_resp.keys: # if "enter" key pressed
                continueRoutine = False # pass to the next iteration (digit)
            
            
                    
            
            
            # *key_resp* updates
            waitOnFlip = False
            if key_resp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['num_0','num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9', 'return'], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = [key.name for key in _key_resp_allKeys]  # storing all keys
                    key_resp.rt = [key.rt for key in _key_resp_allKeys]
            
            # *disp_answer* updates
            if disp_answer.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                disp_answer.frameNStart = frameN  # exact frame index
                disp_answer.tStart = t  # local t and not account for scr refresh
                disp_answer.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(disp_answer, 'tStartRefresh')  # time at next scr refresh
                disp_answer.setAutoDraw(True)
            if disp_answer.status == STARTED:  # only update if drawing
                disp_answer.setText(response_text_exp, log=False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Response_subjectsComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Response_subjects" ---
        for thisComponent in Response_subjectsComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from code_resp_keys
        # set EEG marker after each digit response 
        if use_lpt:
            if response_exp.thisN == 0:
                port.setData(42)
            elif response_exp.thisN == 1:
                port.setData(52)
            elif response_exp.thisN == 2:
                port.setData(62)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        response_exp.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            response_exp.addData('key_resp.rt', key_resp.rt)
        # the Routine "Response_subjects" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed nDigits_trigger repeats of 'response_exp'
    
    
    # --- Prepare to start Routine "Next_Block" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_13
    # At the end of the first block, there is a text saying that there is a break.
    # at the end of the second block, there is a text saying that there is a break
    # and that the experimentator will come to the room.
    # The subject can press "enter" whenever he is ready to go on
    
    # changing / displaying the instruction depending on the current block finished
    # if it is the last trial of the first block
    instructions_next_block = ''
    
    
    if nExpTrials == (nTrials_1Block - 1):
        sound_noise.stop() # Stop the background noise
        instructions_next_block = '''Du hast den ersten Block geschafft, Glückwunsch! Du kannst Dich kurz entspannen, wenn nötig.
        
        Sobald Du bereit bist, um den nächsten Block zu starten, kannst Du auf "Enter" drücken.
        
        Weiterhin gilt: Solange das Fixationskreuz sichtbar ist, bewege Dich bitte nicht.'''
    # if it is the last trial of the second block
    elif nExpTrials == (nTrials_1Block*2 - 1):
        sound_noise.stop() # Stop the background noise
        instructions_next_block = '''Du hast den zweiten Block geschafft, Glückwunsch!
        
        Zeit für eine kurze Pause. Der/die VersuchsleiterIn wird in Kürze in den Raum kommen.
        Sobald Du danach bereit bist, um den nächsten Block zu starten, kannst Du auf "Enter" drücken.'''
        
    elif nExpTrials == (nTrials_1Block*3 - 1):
        sound_noise.stop() # Stop the background noise
        instructions_next_block = '''Du hast den dritten Block geschafft, Glückwunsch!
        
         Sobald Du bereit bist, um den nächsten Block zu starten, kannst Du auf "Enter" drücken.'''
    
    elif nExpTrials == (nTrials_1Block*4 - 1):
        sound_noise.stop() # Stop the background noise
        instructions_next_block = '''Du hast den letzten Block geschafft, Glückwunsch!
        
        Vielen Dank für Deine Teilnahme! Der/die VersuchsleiterIn wird in Kürze in den Raum kommen.'''
    
    
    # if other trial
    else:
        continueRoutine = False
    # keep track of which components have finished
    Next_BlockComponents = []
    for thisComponent in Next_BlockComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Next_Block" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_13
        # Get the pressed key of the subject
        begin_ExpBlock = event.getKeys(keyList=['return'])
        
        # Begin experiment once the subject pressed enter
        if "return" in begin_ExpBlock:
            continueRoutine = False # wait for the subject to press the key "enter"
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Next_BlockComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Next_Block" ---
    for thisComponent in Next_BlockComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_13
    # set EEG marker for each instruction (after 1st and 2nd block are finished) 
    if use_lpt:
            port.setData(212)
        
    # Start playing background noise
    sound_noise.play()
    
    #print(signal_trials)
    
    # Update Trial counter
    nExpTrials += 1
    # the Routine "Next_Block" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Show_instructions" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_nextblock
    #just go on with next trial, if there is no pause ...
    if not instructions_next_block:
        continueRoutine = False
    text_nextblock.setText(instructions_next_block)
    response_nextblock.keys = []
    response_nextblock.rt = []
    _response_nextblock_allKeys = []
    # keep track of which components have finished
    Show_instructionsComponents = [text_nextblock, response_nextblock]
    for thisComponent in Show_instructionsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Show_instructions" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_nextblock* updates
        if text_nextblock.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_nextblock.frameNStart = frameN  # exact frame index
            text_nextblock.tStart = t  # local t and not account for scr refresh
            text_nextblock.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_nextblock, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_nextblock.started')
            text_nextblock.setAutoDraw(True)
        
        # *response_nextblock* updates
        waitOnFlip = False
        if response_nextblock.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            response_nextblock.frameNStart = frameN  # exact frame index
            response_nextblock.tStart = t  # local t and not account for scr refresh
            response_nextblock.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(response_nextblock, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'response_nextblock.started')
            response_nextblock.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(response_nextblock.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(response_nextblock.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if response_nextblock.status == STARTED and not waitOnFlip:
            theseKeys = response_nextblock.getKeys(keyList=['return'], waitRelease=False)
            _response_nextblock_allKeys.extend(theseKeys)
            if len(_response_nextblock_allKeys):
                response_nextblock.keys = _response_nextblock_allKeys[-1].name  # just the last key pressed
                response_nextblock.rt = _response_nextblock_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Show_instructionsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Show_instructions" ---
    for thisComponent in Show_instructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if response_nextblock.keys in ['', [], None]:  # No response was made
        response_nextblock.keys = None
    exp_trials.addData('response_nextblock.keys',response_nextblock.keys)
    if response_nextblock.keys != None:  # we had a response
        exp_trials.addData('response_nextblock.rt', response_nextblock.rt)
    # the Routine "Show_instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'exp_trials'

# Run 'End Experiment' code from code_13
sound_noise.stop()


# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
