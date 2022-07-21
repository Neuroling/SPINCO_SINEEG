#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on July 19, 2022, at 15:37
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
    originPath='D:\\Gorka\\PsychoPy\\triggered_experiment_revDesign_lastrun.py',
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
    size=[1280, 720], fullscr=True, screen=0, 
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

# some init and debug parameters
use_debug = True #True

if use_debug:
    use_lpt = True
    use_real_EEG = True
    #debug_color = 'white'
    debug_color = 'white'
    #SIN_stim_only = True

else:
    use_lpt = True
    use_real_EEG = True
    debug_color = 'gray'
    
# if NV blocks should come first, then set to 1
# current rule: EVEN --> NV_first (set to 1), ODD --> SIN first
NV_first = 1



# open output files-------------------------------------------------------------
dataCalibration_file = open("./data/dataCalibration.txt", "w") # alpha ratio during calibration
meanstd_file = open("./data/meanStd.txt", "w") # mean and std of the calibration
allTriggers_baseline = open("./data/allTriggers_baseline.txt", "w") # all found triggers for each tested factor during calibration
indiv_factor_file = open("./data/indivFactor.txt", "w") # individual factor estimated during calibration for the current subject
dataTresholdCheck_file = open("./data/dataTresholdCheck.txt", "w") # alpha ratio during signal check (experimental condition)

#StimOrder_file = open("./data/StimOrder.txt", "w") # order of the trials (is currently SiN or NV speech?)
dataControl_file = open("./data/dataControl.txt", "w") # alpha ratio during signal check (control condition)


# get the EEG stream from OpenVibe----------------------------------------------


print("looking for streams...")
streams_EEG = resolve_stream('type', 'EEG_extracted')
inlet_EEG = StreamInlet(streams_EEG[0], max_buflen = 1, max_chunklen =1, processing_flags =  1 | 2 | 4 | 8) # create new inlets to read from the streams

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


# Default settings for experiment-----------------------------------------------

# the MAP configuration, which elecs are important 



nDigits = 3 # number presented digits in each trial

# these are the other remaining params to insert into stim file (4 = speaker, nv_stim, trigger_stim, jitter_stim)
nRestElems = 4

if use_debug:
    nTrials_1Block = 8 # number of trials in each block, normal is 70
    # do you want to estimate a real threshold on EEG data or take some artificial values?
    use_real_thresh = 1
    #n_runs_practice = 2
    min_ITI_secs = 0.5 # duration of minimal ITI (time during which we don't check if the threshold is reached to trigger the digits)
else:
    nTrials_1Block = 70
    # do you want to estimate a real threshold on EEG data or take some artificial values?
    use_real_thresh = 1
    #n_runs_practice = 100
    min_ITI_secs = 2 # duration of minimal ITI (time during which we don't check if the threshold is reached to trigger the digits)

    
nBlocks = 4    
nTrials = nTrials_1Block * nBlocks # number of trials in each condition (experimental vs control), represents 2 blocks.



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
    mean_interval_triggers_sec = 12

## also not needed anymore?
#baseline_duration_frames = baseline_duration_sec * srate_processed # duration of baseline in frames


# Default setting for individualized factor calculation-------------------------

max_factor = 3.5 # the maximal acceptable factor
step_factor = 0.1 # step size for testing the different factors

#max_duration100Trials_min = 20 # how many minutes should each block last
#max_duration100Trials_sec = max_duration100Trials_min * 60 # max minutes of each block converted in seconds

min_ITI_samples = min_ITI_secs*srate_processed # mean ITI converted in number of samples
#Interval = round(min_ITI_secs * srate_processed) # how much sample points do we have to count to reach minimal ITI

#ITI = 2 * srate_processed #set the iter trial interval at 2s (60 frames per second: 2 seconds = 120 frames)

ITI_secs = 2

# default ITI
ctrl_ITI_secs = ITI_secs



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
    text='In Kürze wirst Du mehrere Wörter hören, es werden immer 3 Ziffern nacheinander abgespielt werden, mehrmals hintereinander.\n\nNachdem Du eine solche Dreier-Reihe gehört hast, kannst du die entsprechenden 3 Ziffern mit der Tastatur einzeln eintippen, die Du gehört hast. Du musst jedes Mal auf "Enter" drücken, um eine Ziffer zu bestätigen.\n\nBeispiel: Du hast “1”,”2”,”3” gehört, dann tippe ein: “1”, gefolgt von “ENTER”, “2” --> ENTER, “3” --> ENTER.\n\nFalls du während des Tippens einen Tippfehler machst, kannst du einfach eine neue Ziffer eintippen. Nur die letzte Eingabe zählt!\n\nSobald du bereit bist, kannst du auf "Enter" drücken und die Trainingsphase wird anfangen.\n',
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


Digit1_clear = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='Digit1_clear')
Digit1_clear.setVolume(1)
Digit2_clear = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='Digit2_clear')
Digit2_clear.setVolume(1)
Digit3_clear = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='Digit3_clear')
Digit3_clear.setVolume(1)

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

# --- Initialize components for Routine "Instruction_Calibration" ---
text_calibration = visual.TextStim(win=win, name='text_calibration',
    text='Bevor das Experiment startet, wird Deine spontane Gehirnaktivität gemessen, während Du ein kontinuierliches Geräusch hören wirst.\n\nDu wirst ein Fixationskreuz sehen, das Du fixieren sollst. Bewege Dich bitte nicht, solange Du das Fixationskreuz siehst.\n\nWenn Du bereit bist, kannst Du auf "Enter" drücken.\n\n',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_3 = keyboard.Keyboard()

# --- Initialize components for Routine "Calibration" ---
# Run 'Begin Experiment' code from Code_calibration
ratio_vec_rs = 0
ratio_vec_mean = 0
ratio_vec_std = 0

time_diff = 0
Fix_cross_calibration = visual.TextStim(win=win, name='Fix_cross_calibration',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
text = visual.TextStim(win=win, name='text',
    text='',
    font='Open Sans',
    pos=(0, -0.1), height=0.1, wrapWidth=None, ori=0.0, 
    color=debug_color, colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# --- Initialize components for Routine "Repeat_calibration" ---
text_calibration_repeat = visual.TextStim(win=win, name='text_calibration_repeat',
    text='Kalibrierung wiederholen ? Bei "0" wird wiederholt, bei "Enter" geht das Experiment weiter.',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
response_calibration_repeat = keyboard.Keyboard()

# --- Initialize components for Routine "Break" ---
text_break = visual.TextStim(win=win, name='text_break',
    text='Nun wird der erste Block starten. Insgesamt gibt es 4 Blöcke.\n\nWie bei der Trainingsübung wirst Du zuerst ein kontinuierliches Geräusch hören und gleichzeitig ein Fixationskreuz sehen. Bitte das Kreuz fixieren. Solange das Kreuz sichtbar ist, bewege Dich bitte auch nicht.\n\nNachher wirst du 3 Ziffern hören, die unterschiedlich verrauscht sind. Deine Aufgabe ist es, die Ziffern einzutippen, die du gehört hast.\n\nSobald du bereit bist, um den ersten Block zu starten, kannst du auf "Enter " drücken.\n',
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

# --- Initialize components for Routine "digits_played" ---
Fixation_Play = visual.TextStim(win=win, name='Fixation_Play',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-1.0);
sound_digit1 = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='sound_digit1')
sound_digit1.setVolume(1.0)
sound_digit2 = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='sound_digit2')
sound_digit2.setVolume(1.0)
sound_digit3 = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='sound_digit3')
sound_digit3.setVolume(1.0)

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
print(degrad)


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
        rand_jitter= np.round(np.random.uniform(-4,4,1))
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
nfb_digit1_ori = out_matrix[nv_trig_trl_idx,1]
nfb_digit2_ori = out_matrix[nv_trig_trl_idx,2]
nfb_digit3_ori = out_matrix[nv_trig_trl_idx,3]

# scramble for control NV
nfb_digit1_scr = np.random.choice(nfb_digit1_ori,len(nfb_digit1_ori),replace = False)
nfb_digit2_scr = np.random.choice(nfb_digit2_ori,len(nfb_digit2_ori),replace = False)
nfb_digit3_scr = np.random.choice(nfb_digit3_ori,len(nfb_digit3_ori),replace = False)

out_matrix[nv_ctrl_trl_idx,1] = nfb_digit1_scr
out_matrix[nv_ctrl_trl_idx,2] = nfb_digit2_scr
out_matrix[nv_ctrl_trl_idx,3] = nfb_digit3_scr

# scramble for trigger sin
nfb_digit1_scr = np.random.choice(nfb_digit1_ori,len(nfb_digit1_ori),replace = False)
nfb_digit2_scr = np.random.choice(nfb_digit2_ori,len(nfb_digit2_ori),replace = False)
nfb_digit3_scr = np.random.choice(nfb_digit3_ori,len(nfb_digit3_ori),replace = False)

out_matrix[sin_trig_trl_idx,1] = nfb_digit1_scr
out_matrix[sin_trig_trl_idx,2] = nfb_digit2_scr
out_matrix[sin_trig_trl_idx,3] = nfb_digit3_scr

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
# 1 decimal string. We have to convert it in 0 decimal int.
col = np.arange(nDigits+1)
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
        Digit1_clear.setSound(digit1, hamming=True)
        Digit1_clear.setVolume(1, log=False)
        Digit2_clear.setSound(digit2, hamming=True)
        Digit2_clear.setVolume(1, log=False)
        Digit3_clear.setSound(digit3, hamming=True)
        Digit3_clear.setVolume(1, log=False)
        # keep track of which components have finished
        Present_practiceComponents = [Digit1_clear, Digit2_clear, Digit3_clear]
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
            # start/stop Digit2_clear
            if Digit2_clear.status == NOT_STARTED and Digit1_clear.status == FINISHED:
                # keep track of start time/frame for later
                Digit2_clear.frameNStart = frameN  # exact frame index
                Digit2_clear.tStart = t  # local t and not account for scr refresh
                Digit2_clear.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('Digit2_clear.started', t)
                Digit2_clear.play()  # start the sound (it finishes automatically)
            # start/stop Digit3_clear
            if Digit3_clear.status == NOT_STARTED and Digit2_clear.status == FINISHED:
                # keep track of start time/frame for later
                Digit3_clear.frameNStart = frameN  # exact frame index
                Digit3_clear.tStart = t  # local t and not account for scr refresh
                Digit3_clear.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('Digit3_clear.started', t)
                Digit3_clear.play()  # start the sound (it finishes automatically)
            
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
        Digit2_clear.stop()  # ensure sound has stopped at end of routine
        Digit3_clear.stop()  # ensure sound has stopped at end of routine
        # the Routine "Present_practice" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        response_practice = data.TrialHandler(nReps=nDigits, method='sequential', 
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
            
        # completed nDigits repeats of 'response_practice'
        
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


# set up handler to look after randomisation of conditions etc
calibration_block = data.TrialHandler(nReps=100, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='calibration_block')
thisExp.addLoop(calibration_block)  # add the loop to the experiment
thisCalibration_block = calibration_block.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisCalibration_block.rgb)
if thisCalibration_block != None:
    for paramName in thisCalibration_block:
        exec('{} = thisCalibration_block[paramName]'.format(paramName))

for thisCalibration_block in calibration_block:
    currentLoop = calibration_block
    # abbreviate parameter names if possible (e.g. rgb = thisCalibration_block.rgb)
    if thisCalibration_block != None:
        for paramName in thisCalibration_block:
            exec('{} = thisCalibration_block[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "Instruction_Calibration" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_calibration
    # This is the instruction explaining that we will gather some neural data for a
    # period of time and that the person has the stay quiet. Subject press "enter
    # to continue.
    
    #begin_exp = []
    
    # set EEG marker for instruction calibration
    if use_lpt:
        port.setData(101)
    key_resp_3.keys = []
    key_resp_3.rt = []
    _key_resp_3_allKeys = []
    # keep track of which components have finished
    Instruction_CalibrationComponents = [text_calibration, key_resp_3]
    for thisComponent in Instruction_CalibrationComponents:
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
    
    # --- Run Routine "Instruction_Calibration" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_calibration
        # Get the pressed key of the subject
        #begin_exp = event.getKeys(keyList=['return'])
        
        # Begin experiment once the subject pressed enter
        #if "return" in begin_exp:
        #    # if enter is pressed, the current routine stops and we move into the next one
        #    continueRoutine = False
        
        # *text_calibration* updates
        if text_calibration.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_calibration.frameNStart = frameN  # exact frame index
            text_calibration.tStart = t  # local t and not account for scr refresh
            text_calibration.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_calibration, 'tStartRefresh')  # time at next scr refresh
            text_calibration.setAutoDraw(True)
        
        # *key_resp_3* updates
        waitOnFlip = False
        if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.tStart = t  # local t and not account for scr refresh
            key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_3.started')
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_3.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_3.getKeys(keyList=['return'], waitRelease=False)
            _key_resp_3_allKeys.extend(theseKeys)
            if len(_key_resp_3_allKeys):
                key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
                key_resp_3.rt = _key_resp_3_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Instruction_CalibrationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Instruction_Calibration" ---
    for thisComponent in Instruction_CalibrationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Instruction_Calibration" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Calibration" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from Code_calibration
    # In this routine, the alpha ratios of the subject will be recorded during the
    # so-called "calibration phase". Once collected, the mean and std will be calculated.
    # At the end of the routine, the individual factor for the threshold will be estimated:
    # Threshold = mean_ratio_calibration + estimated_indiv_factor * std_ratio_calibration
    
    # set EEG marker for calibration
    if use_lpt:
        port.setData(91)
    
    # Start playing background noise
    
    nloops = math.ceil(baseline_duration_sec / noise_duration_sec)
    sound_noise.play(loops = nloops)
    
    # Default values for signal processing and mean and std calculation 
    signal = 0
    blue_elecs = 0
    red_elecs = 0
    ratio_elecs = 0
    count = 0
    ratio_vec_rs = 0
    ratio_vec_mean = 0
    ratio_vec_std = 0
    
    # Default values for calculating individualized threshold
    nFound_triggers = 0
    current_factor = max_factor
    diff_vector = []
    triggers = []
    first_trigger = []
    rest_triggers = []
    def_triggers = []
    indiv_factor = 0
    counter = 0
    
    #time_start = time.time()
    time_start_calibration = time.time()
    # keep track of which components have finished
    CalibrationComponents = [Fix_cross_calibration, text]
    for thisComponent in CalibrationComponents:
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
    
    # --- Run Routine "Calibration" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from Code_calibration
        # pull chunks from the EEG stream (see startup)
        signal, timestamps = inlet_EEG.pull_sample()
        #signal = [i[0] for i in chunk] # select the 32 elecs of interest
        
        current_time = time.time()
        passed_time = current_time - time_start_calibration
        
        
        # calculate the alpha ratios of the incoming signal. Blue elecs and red elecs are
        # chosen from the topomap of TH's results.
        if signal:
            
            # just select the elecs of interest and average them
            
            
            # ratio between elecs is already done in openvibe, just read it in
            ratio_elecs = signal[0]
            sys.stdout = dataCalibration_file # open file for saving ratios during calibration
            print(timestamps, ratio_elecs) # saving ratios during calibration
            # vector gathering ratios of each frame
            ratio_vec_rs = np.append(ratio_vec_rs, ratio_elecs) 
        
        
        
        
        # once calibration is over, calculates the mean and std of alpha ratio gathered
        # during the calibration
        if passed_time > baseline_duration_sec: # once vector is 100 sec long, get the mean and std
            sys.stdout = sys.__stdout__ # close the data calibration file
            ratio_vec_mean = np.average(ratio_vec_rs) # mean of the 100 seconds calibration
            ratio_vec_std = np.std(ratio_vec_rs) # std of the 100 seconds calibration
            sys.stdout = meanstd_file # open file for saving std and mean
            print(ratio_vec_mean) # saving mean
            print(ratio_vec_std) # saving std
            
            sys.stdout = sys.__stdout__ # close std and mean file
            # print mean and std in the console to check the values
            print('mean = ', ratio_vec_mean)
            print('std = ', ratio_vec_std)
            time_end = time.time()
            #time_diff = time_end - time_start_calibration
            time.sleep(1)
            continueRoutine = False
            
        else:
            continueRoutine = True
        
                
            
            
        # actualize count of frame
        # count += 1
            
            
            
        
                   
            
            
        
            
        
        
        # *Fix_cross_calibration* updates
        if Fix_cross_calibration.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            Fix_cross_calibration.frameNStart = frameN  # exact frame index
            Fix_cross_calibration.tStart = t  # local t and not account for scr refresh
            Fix_cross_calibration.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Fix_cross_calibration, 'tStartRefresh')  # time at next scr refresh
            Fix_cross_calibration.setAutoDraw(True)
        if Fix_cross_calibration.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Fix_cross_calibration.tStartRefresh + baseline_duration_sec-frameTolerance:
                # keep track of stop time/frame for later
                Fix_cross_calibration.tStop = t  # not accounting for scr refresh
                Fix_cross_calibration.frameNStop = frameN  # exact frame index
                Fix_cross_calibration.setAutoDraw(False)
        
        # *text* updates
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            text.setAutoDraw(True)
        if text.status == STARTED:  # only update if drawing
            text.setText(passed_time, log=False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in CalibrationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Calibration" ---
    for thisComponent in CalibrationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from Code_calibration
    # Stop the background noise
    sound_noise.stop()
    
    # find the individual factor of the current subject
    ratio_vec_rs = np.array(ratio_vec_rs) # convert baseline signal to array
    
    sys.stdout = sys.__stdout__ # close file for all found triggers during calibration
    print('Length of alpha vec =' + str(len(ratio_vec_rs)))
    #print('Time diff =' + str(time_diff))
    
    
    # to find the individual factor, we start from the greatest acceptable factor
    # and check how many triggers we find for each factor. Once the number of
    # found triggers is greater or equal than the number estimated in "startup", 
    # we get the previous factor in the while loop,
    # which is greater than the current one (if found_trigger == 10 for a current_factor == 2.5,
    # we will take the factor of the preceding iteration, that is, 2.6).
    # If the current_factor is smaller than the lowest acceptable factor, we have to
    # exclude the current subject.
    # Properties: We do not save consecutive triggers lasting as long as the ITI (2 sec). If 
    # the length of consecutive triggers is greater than the ITI (in sample count), we 
    # save 2 triggers out of this vector: the first one and the nth sample exceeding the ITI.
    
    # as long as there are less triggers than expected do this:
    while nFound_triggers < nTrigger_Baseline and current_factor > 0:
        # find the indices of the calibration samples which are reaching the current threshold
        triggers = np.where(ratio_vec_rs > ratio_vec_mean + current_factor*ratio_vec_std)
        sys.stdout = allTriggers_baseline # open file for all found triggers during calibration
        print(current_factor, triggers[0])
        sys.stdout = sys.__stdout__ # close file for all found triggers during calibration
        
        # if there is only 1 trigger found, save it in the definitive trigger vector:
        if len(triggers[0]) == 1:
            def_triggers = int(triggers[0][0])
            
        # if there is more than 1 trigger found, do the later
        elif len(triggers[0]) > 1:
            # get the first trigger
            first_trigger = int(triggers[0][0])
            # the rest of the triggers are saved separately to check for the difference
            # between the first and the other triggers later.
            rest_triggers = [int(x) for x in triggers[0][1:]]
            
            # check for consecutive samples
            counter = 0
            for x in rest_triggers:
                # check distance between first trigger and next
                # if not sufficiently large ...
                if not (np.diff([first_trigger,x]) > min_ITI_samples):
                    # ... then delete second trigger, go on
                    rest_triggers= np.delete(rest_triggers, counter)
                else: # if distance ok:
                    # move on with checking distance from next trigger and keep the
                    # value in the vector
                    first_trigger = rest_triggers[counter]
                    # increase counter
                    counter +=1  
                    
            # once the loop is done, write a definitive trigger vector with all triggers
            # there:
            def_triggers = np.array(rest_triggers)
            # prepend first trigger to result (because it was not there)
            def_triggers = np.insert(def_triggers, 0, triggers[0][0], axis=0)
            print(current_factor, "definitive triggers:", def_triggers)
            
        # get the number of definitive found triggers
        if isinstance(def_triggers, int):
            nFound_triggers = 1
        else:
            nFound_triggers = len(def_triggers)
        print(current_factor, "number of definitive triggers:", nFound_triggers)
        
        # decrease current factor by step factor (e.g. 0.1)
        current_factor -= step_factor
        current_factor = round(current_factor,1)
    
    if current_factor > 0:
        # get the factor of the preceding iteration
        indiv_factor = round(current_factor+step_factor, 1)
        #indiv_factor = current_factor
        sys.stdout = indiv_factor_file # open file for saving individualized factor
        print(indiv_factor)
        sys.stdout = sys.__stdout__ # close individualized factor file
    
        # Once the loop is over, check the reason why this loop stops:
        # 1) the current factor is smaller than the minimum acceptable factor or
        # 2) if the number or found triggers is greater than the number estimated in "startup".
    
        if indiv_factor < min_factor: # check for 1)
            print("The individualized factor of this subject is equal to", indiv_factor, "which is smaller than the smallest acceptable factor", min_factor) # exclude the subject
        else: # check for 2)
            print("indiv factor = ", indiv_factor)
    
    else: # if current_factor =< 0
        print("No positive trigger could be found for this person: too much triggers needed in short time")
    
    # print current thresh of subject:
    print('thresh =', ratio_vec_mean + (indiv_factor * ratio_vec_std))
    # the Routine "Calibration" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Repeat_calibration" ---
    continueRoutine = True
    # update component parameters for each repeat
    response_calibration_repeat.keys = []
    response_calibration_repeat.rt = []
    _response_calibration_repeat_allKeys = []
    # keep track of which components have finished
    Repeat_calibrationComponents = [text_calibration_repeat, response_calibration_repeat]
    for thisComponent in Repeat_calibrationComponents:
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
    
    # --- Run Routine "Repeat_calibration" ---
    while continueRoutine and routineTimer.getTime() < 10.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_calibration_repeat
        if response_calibration_repeat.keys == 'return':
            calibration_block.finished=1
            continueRoutine = False
        
        # *text_calibration_repeat* updates
        if text_calibration_repeat.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_calibration_repeat.frameNStart = frameN  # exact frame index
            text_calibration_repeat.tStart = t  # local t and not account for scr refresh
            text_calibration_repeat.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_calibration_repeat, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_calibration_repeat.started')
            text_calibration_repeat.setAutoDraw(True)
        if text_calibration_repeat.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_calibration_repeat.tStartRefresh + 10-frameTolerance:
                # keep track of stop time/frame for later
                text_calibration_repeat.tStop = t  # not accounting for scr refresh
                text_calibration_repeat.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_calibration_repeat.stopped')
                text_calibration_repeat.setAutoDraw(False)
        
        # *response_calibration_repeat* updates
        waitOnFlip = False
        if response_calibration_repeat.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            response_calibration_repeat.frameNStart = frameN  # exact frame index
            response_calibration_repeat.tStart = t  # local t and not account for scr refresh
            response_calibration_repeat.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(response_calibration_repeat, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'response_calibration_repeat.started')
            response_calibration_repeat.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(response_calibration_repeat.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(response_calibration_repeat.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if response_calibration_repeat.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > response_calibration_repeat.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                response_calibration_repeat.tStop = t  # not accounting for scr refresh
                response_calibration_repeat.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'response_calibration_repeat.stopped')
                response_calibration_repeat.status = FINISHED
        if response_calibration_repeat.status == STARTED and not waitOnFlip:
            theseKeys = response_calibration_repeat.getKeys(keyList=['num_0','return'], waitRelease=False)
            _response_calibration_repeat_allKeys.extend(theseKeys)
            if len(_response_calibration_repeat_allKeys):
                response_calibration_repeat.keys = _response_calibration_repeat_allKeys[-1].name  # just the last key pressed
                response_calibration_repeat.rt = _response_calibration_repeat_allKeys[-1].rt
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Repeat_calibrationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Repeat_calibration" ---
    for thisComponent in Repeat_calibrationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_calibration_repeat
    # It asks if we want to repeat the calibration. This is in case the subject
    # did not understand either the task or the way to provide his answer (or both).
    # ...Start the practice block again: press "y" (you have 20 seconds to press "y". If
    # you don't, the experiment will go on)
    # ...Don't retart it: just wait and the experiment will go on
    
    if response_calibration_repeat.keys == 'num_0':
        calibration_block.finished=0
        continueRoutine = True 
    elif response_calibration_repeat.keys == 'return':
        calibration_block.finished=1
        continueRoutine = False
    else:
        calibration_block.finished=1
        continueRoutine = False
            
    # using non-slip timing so subtract the expected duration of this Routine
    routineTimer.addTime(-10.000000)
    thisExp.nextEntry()
    
# completed 100 repeats of 'calibration_block'


# --- Prepare to start Routine "Break" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from code_6
# Instructions of the experiment. Subject presses enter to continue

# set EEG marker for instructions experiment
if use_lpt:
    port.setData(102)

#begin_expBlock = []
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
    threshold = ratio_vec_mean + indiv_factor * ratio_vec_std    
    
    
    # Start playing background noise
    sound_noise.play(loops = 2)
    
    
    
    text_6.setColor(debug_color, colorSpace='rgb')
    # keep track of which components have finished
    signal_checkComponents = [Fixation, text_6]
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
        chunk, timestamps = inlet_EEG.pull_sample()
        ratio_elecs = chunk[0]
            
        # if we want to run adaptive:    
        # add more onto the previous baseline measurements to allow updateing
        ratio_vec_rs = np.append(ratio_vec_rs, ratio_elecs) 
        ratio_vec_mean = np.average(ratio_vec_rs) # mean of the 100 seconds calibration
        ratio_vec_std = np.std(ratio_vec_rs) # std of the 100 seconds calibration    
        threshold = ratio_vec_mean + indiv_factor * ratio_vec_std    
            
        # calculate the alpha ratios of the incoming signal. Blue elecs and red elecs are
        # chosen from the topomap of TH's results.
        #if ratio_elecs:
        #       
        sys.stdout = dataTresholdCheck_file # open Signal check file to save ratios during signal check
        print(timestamps, threshold)
        
            
        
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
    sys.stdout = sys.__stdout__
    
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
    sound_digit1.setSound(digit1, hamming=True)
    sound_digit1.setVolume(1.0, log=False)
    sound_digit2.setSound(digit2, hamming=True)
    sound_digit2.setVolume(1.0, log=False)
    sound_digit3.setSound(digit3, hamming=True)
    sound_digit3.setVolume(1.0, log=False)
    # keep track of which components have finished
    digits_playedComponents = [Fixation_Play, sound_digit1, sound_digit2, sound_digit3]
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
        # start/stop sound_digit2
        if sound_digit2.status == NOT_STARTED and sound_digit1.status == FINISHED:
            # keep track of start time/frame for later
            sound_digit2.frameNStart = frameN  # exact frame index
            sound_digit2.tStart = t  # local t and not account for scr refresh
            sound_digit2.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('sound_digit2.started', t)
            sound_digit2.play()  # start the sound (it finishes automatically)
        # start/stop sound_digit3
        if sound_digit3.status == NOT_STARTED and sound_digit2.status == FINISHED:
            # keep track of start time/frame for later
            sound_digit3.frameNStart = frameN  # exact frame index
            sound_digit3.tStart = t  # local t and not account for scr refresh
            sound_digit3.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('sound_digit3.started', t)
            sound_digit3.play()  # start the sound (it finishes automatically)
        
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
    sound_digit2.stop()  # ensure sound has stopped at end of routine
    sound_digit3.stop()  # ensure sound has stopped at end of routine
    # the Routine "digits_played" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    response_exp = data.TrialHandler(nReps=nDigits, method='sequential', 
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
        
    # completed nDigits repeats of 'response_exp'
    
    
    # --- Prepare to start Routine "Next_Block" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_13
    # At the end of the first block, there is a text saying that there is a break.
    # at the end of the second block, there is a text saying that there is a break
    # and that the experimentator will come to the room.
    # The subject can press "enter" whenever he is ready to go on
    
    # changing / displaying the instruction depending on the current block finished
    instructions_next_block = ''
    # if it is the last trial of the first block
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
