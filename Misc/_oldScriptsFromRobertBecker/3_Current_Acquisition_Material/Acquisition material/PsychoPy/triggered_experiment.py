#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.2.3),
    on October 01, 2021, at 13:47
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

import psychopy
psychopy.useVersion('latest')


from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.2.3'
expName = 'eeg_contingent_digits'  # from the Builder filename that created this script
expInfo = {'participant': '1', 'session': '001'}
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
    originPath='C:\\Users\\admin\\Documents\\Neurofeedback\\4_Triggered Stimuli\\2_Measurements\\Measurement 9\\Acquisition material\\PsychoPy\\triggered_experiment.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1280, 1024], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Setup eyetracking
ioDevice = ioConfig = ioSession = ioServer = eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "Startup"
StartupClock = core.Clock()
# This routine prepares the needed elements for the functioning of the experiment.
# It also randomly generates the digit triplet for the experiment (see begin
# routine) and the randomized order of SiN vs NV speech presentation (see end 
# routine).
# if you want to change some experiment settings (such as nTrial, duration of the
# calibration etc.), you can do it here

# import packages---------------------------------------------------------------

import psychtoolbox as ptb
from pylsl import StreamInlet, resolve_stream
from psychopy import parallel, sound
import numpy as np
import scipy.stats as stats
import sys
import time
import random
import xlsxwriter
#import sounddevice as sd 
#import soundfile as sf
from itertools import groupby



# some init and debug parameters
use_debug = True
if use_debug:
    use_lpt = True
    use_real_EEG = False
    tresh_factor = 1.5
else:
    use_lpt = True
    use_real_EEG = True
    tresh_factor = []


# open output files-------------------------------------------------------------


dataCalibration_file = open("dataCalibration2.txt", "w") # alpha ratio during calibration
meanstd_file = open("meanStd2.txt", "w") # mean and std of the calibration
allTriggers_baseline = open("allTriggers_baseline2.txt", "w") # all found triggers for each tested factor during calibration
indiv_factor_file = open("indivFactor2.txt", "w") # individual factor estimated during calibration for the current subject
dataSignalCheck_file = open("dataSignalCheck2.txt", "w") # alpha ratio during signal check (experimental condition)
StimOrder_file = open("StimOrder2.txt", "w") # order of the trials (is currently SiN or NV speech?)
dataControl_file = open("dataControl2.txt", "w") # alpha ratio during signal check (control condition)


# get the EEG stream from OpenVibe----------------------------------------------


print("looking for streams...")
streams_EEG = resolve_stream('type', 'EEG_extracted')
inlet_EEG = StreamInlet(streams_EEG[0]) # create new inlets to read from the streams

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

Fz = 2 - 1
F8 = 31 - 1
FT10 = 27 - 1
O1 = 16 - 1
FC1 = 7 - 1
C3 = 8 - 1
CP1 = 12 - 1
CP5 = 11 - 1
P7 = 15 - 1
Pz = 13 - 1
P4 = 19 - 1


# Default settings for experiment-----------------------------------------------


nDigits = 3 # number presented digits in each trial
if use_debug:
    nTrials_1Block = 6 # number of trials in each block, normal is 70
else:
    nTrials_1Block = 70

nTrials = nTrials_1Block * 2 # number of trials in each condition (experimental vs control), represents 2 blocks.
refresh_rate = 60 # refreshing rate of the screen
min_ITI = 2 # duration of minimal ITI (time during which we don't check if the threshold is reached to trigger the digits)
srate_processed = 16 # sampling rate of the incoming signal

if use_debug:
    baseline_duration_sec = 5 # duration of baseline in seconds, normal is 100
else:
    baseline_duration_sec = 100 # duration of baseline in seconds, normal is 100

baseline_duration_frames = baseline_duration_sec * refresh_rate # duration of baseline in frames






# Default setting for individualized factor calculation-------------------------

min_factor = 2 # the minimal acceptable factor
max_factor = 3.5 # the maximal acceptable factor
step_factor = 0.1 # step size for testing the different factors
max_duration100Trials_min = 20 # how many minutes should each block last
max_duration100Trials_sec = max_duration100Trials_min * 60 # max minutes of each block converted in seconds
min_ITI_samples = min_ITI*srate_processed # mean ITI converted in number of samples
Interval = round(min_ITI * srate_processed) # how much sample points do we have to count to reach minimal ITI






# Since we have to play nTrials_1Block in maximum max_duration100Trials_sec,
# estimates the number of trigger we would have to find during the
# calibration (aka baseline).
interval_trigger_sec = max_duration100Trials_sec / nTrials_1Block # how many trigger should be found for each block
nTrigger_Baseline = round(baseline_duration_sec / interval_trigger_sec) # how many triggers should be found during calibration
#nTrigger_Baseline = 1


# Stimuli ----------------------------------------------------------------------


# Prepare file background noise
#ELSA's code: sound_noise, fs = sf.read('constantNoise_1minute_16kHz_filtered_mono_looped.wav', dtype='float32')  
#sound_noise, fs = sf.read('constantNoise_1minute_16kHz_filtered_mono_looped.wav', dtype='float32')  


#sound_noise = sound.Sound('constantNoise_1minute_16kHz_filtered_mono_looped.wav')  
sound_noise = sound.Sound('constantNoise_1minute_48kHz_filtered_mono_looped.wav',loops = -1, preBuffer= -1)  




# Initialize components for Routine "Welcome"
WelcomeClock = core.Clock()
Instructions_Noise = visual.TextStim(win=win, name='Instructions_Noise',
    text='Lieber Teilnehmer, willkommen zu unserem Experiment!\n\nVielen Dank für Deine Teilnahme. In diesem Experiment geht es darum, die Rolle neuronaler Oszillationen beim Sprachverstehen zu erforschen. Du wirst eine Reihe von Sprachstimuli – Ziffern – hören, die eingebettet sein werden in Rauschen, bzw. verzerrt dargestellt werden.\n\nBevor das eigentliche Experiment beginnt, wirst Du ein kontinuierliches Rauschen hören. Während des Abspielens des Geräuschs kannst du dem Versuchsleiter sagen, welche Lautstärke dir am besten passt.\n\nWenn du bereit bist, kannst du auf "Enter" drücken und das Geräusch wird starten.\n\n',
    font='Arial',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "Testing_Background_Noise"
Testing_Background_NoiseClock = core.Clock()
Fixation_cross_Test = visual.TextStim(win=win, name='Fixation_cross_Test',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "Instructions_practice"
Instructions_practiceClock = core.Clock()
Instructions_clear_Digits = visual.TextStim(win=win, name='Instructions_clear_Digits',
    text='In Kürze wirst Du mehrere Wörter hören, es werden immer 3 Ziffern nacheinander abgespielt werden, mehrmals hintereinander.\n\nNachdem Du eine solche Dreier-Reihe gehört hast, kannst du die entsprechenden 3 Ziffern mit der Tastatur einzeln eintippen, die Du gehört hast. Du musst jedes Mal auf "Enter" drücken, um eine Ziffer zu bestätigen.\n\nBeispiel: Du hast “1”,”2”,”3” gehört, dann tippe ein: “1”, gefolgt von “ENTER”, “2” --> ENTER, “3” --> ENTER.\n\nFalls du während des Tippens einen Tippfehler machst, kannst du einfach eine neue Ziffer eintippen. Nur die letzte Eingabe zählt!\n\nSobald du bereit bist, kannst du auf "Enter" drücken und die Trainingsphase wird anfangen.\n',
    font='Arial',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "clear_digits"
clear_digitsClock = core.Clock()
# This routine is playing 10 trials of clear digit triplets. This is meant
# for the subjects to learn how to type their response. The stimulus set is
# fixed (always the same triplets in the same order) and can be found in 
# the excel-file "practice_trials.xlsx"

#default variables
firstdigit = 0
seconddigit = 0
thirddigit = 0

speaker = [1,7,10,13,14,21,33,48,49,61]
digit1 = 'Speaker1_Digit0_48kHz_filtered_mono.wav'
digit2 = 'Speaker1_Digit0_48kHz_filtered_mono.wav'
digit3 = 'Speaker1_Digit0_48kHz_filtered_mono.wav'


Digit1_clear = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='Digit1_clear')
Digit1_clear.setVolume(1)
Digit2_clear = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='Digit2_clear')
Digit2_clear.setVolume(1)
Digit3_clear = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='Digit3_clear')
Digit3_clear.setVolume(1)

# Initialize components for Routine "Response_practice"
Response_practiceClock = core.Clock()
key_resp_3 = keyboard.Keyboard()
disp_answer_3 = visual.TextStim(win=win, name='disp_answer_3',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "repeat_practice"
repeat_practiceClock = core.Clock()
text_4 = visual.TextStim(win=win, name='text_4',
    text='Training wiederholen ? [j/n] Bei keiner Antwort geht das Experiment in 10 Sekunden weiter.',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_4 = keyboard.Keyboard()

# Initialize components for Routine "Instruction_start_Experiment"
Instruction_start_ExperimentClock = core.Clock()
Instructions_begin = visual.TextStim(win=win, name='Instructions_begin',
    text='Bevor das Experiment startet, wird Deine spontane Gehirnaktivität gemessen, während Du ein kontinuierliches Geräusch hören wirst.\n\nDu wirst ein Fixationskreuz sehen, das Du fixieren sollst. Bewege Dich bitte nicht, solange Du das Fixationskreuz siehst.\n\nWenn Du bereit bist, kannst Du auf "Enter" drücken.\n\n',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "Calibrating"
CalibratingClock = core.Clock()
Fixation_cross = visual.TextStim(win=win, name='Fixation_cross',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "repeat_calibration"
repeat_calibrationClock = core.Clock()
text_5 = visual.TextStim(win=win, name='text_5',
    text='Kalibrierung wiederholen [j/n]? Bei nein oder keiner Antwort geht das Experiment in 10 Sekunden weiter.',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_5 = keyboard.Keyboard()

# Initialize components for Routine "Break"
BreakClock = core.Clock()
Begin = visual.TextStim(win=win, name='Begin',
    text='Nun wird der erste Block starten. Insgesamt gibt es 4 Blöcke.\n\nWie bei der Trainingsübung wirst Du zuerst ein kontinuierliches Geräusch hören und gleichzeitig ein Fixationskreuz sehen. Bitte das Kreuz fixieren. Solange das Kreuz sichtbar ist, bewege Dich bitte auch nicht.\n\nNachher wirst du 3 Ziffern hören, die unterschiedlich verrauscht sind. Deine Aufgabe ist es, die Ziffern einzutippen, die du gehört hast.\n\nSobald du bereit bist, um den ersten Block zu starten, kannst du auf "Enter " drücken.\n',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "signal_check"
signal_checkClock = core.Clock()
# Default values for normalizing the signal
signal_trials = []
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

# Initialize components for Routine "digits_played"
digits_playedClock = core.Clock()
sound_digit1 = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='sound_digit1')
sound_digit1.setVolume(1.0)
sound_digit2 = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='sound_digit2')
sound_digit2.setVolume(1.0)
sound_digit3 = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='sound_digit3')
sound_digit3.setVolume(1.0)

# Initialize components for Routine "Response_subjects"
Response_subjectsClock = core.Clock()
key_resp = keyboard.Keyboard()
disp_answer = visual.TextStim(win=win, name='disp_answer',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "Next_Block"
Next_BlockClock = core.Clock()
Begin_3 = visual.TextStim(win=win, name='Begin_3',
    text='',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "signal_check_2"
signal_check_2Clock = core.Clock()
# Setting up the replay of ITI of the experimental condition.
# Once ITI is replayed, the digits are presented. Thus, we trigger without
# checking at the subject's alpha ratio

# block and trial counter
nCtrlBlock = 1
nCtrlTrials = 0
trial_nr_ctrl = []
Fixation_2 = visual.TextStim(win=win, name='Fixation_2',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "digits_played_2"
digits_played_2Clock = core.Clock()
#default variables
#firstdigit = 0
#seconddigit = 0
#thirddigit = 0
#noise = [100,60,50,60,30,45,25,20,85]
#speaker = [1,7,10,13,14,21,33,48,49,61]
#digit1 = 'NVS_Speaker_1_digit_0_100_envExtDepPt.wav_48kHz_filtered_mono.wav'
#digit2 = 'NVS_Speaker_1_digit_0_100_envExtDepPt.wav_48kHz_filtered_mono.wav'
#digit3 = 'NVS_Speaker_1_digit_0_100_envExtDepPt.wav_48kHz_filtered_mono.wav'
sound_digit1_2 = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='sound_digit1_2')
sound_digit1_2.setVolume(1.0)
sound_digit2_2 = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='sound_digit2_2')
sound_digit2_2.setVolume(1.0)
sound_digit3_2 = sound.Sound('A', secs=-1, stereo=False, hamming=True,
    name='sound_digit3_2')
sound_digit3_2.setVolume(1.0)

# Initialize components for Routine "Response_subjects_2"
Response_subjects_2Clock = core.Clock()
key_resp_2 = keyboard.Keyboard()
disp_answer_2 = visual.TextStim(win=win, name='disp_answer_2',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "Next_Block_2"
Next_Block_2Clock = core.Clock()
Begin_4 = visual.TextStim(win=win, name='Begin_4',
    text='',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "Startup"-------
continueRoutine = True
# update component parameters for each repeat
# This chunk of code is generating random digit triplets for each trial and
# each condition. The triplets are unique between trials
# meaning that there is no repeated triplets within 1 condition.
# Each triplet contains different digits: no repeated digits in one triplet.
# However, the digits are not counterbalanced for each condition (experimental_SiN,
# experimental_NV, control_SiN, control_NV)

# Preparing variables
nTrials_vector = np.arange(nTrials) # create the trial ID colomn: vector [0:nTrials]
out_matrix = np.zeros((nTrials, nDigits)) # create the array template of size: rows = nTrials , columns = 3 (nDigits)
labels_colomn = np.array(["TrialID","NFB_digit1","NFB_digit2","NFB_digit3"]) # define the labels of the columns for excel
possible_digit = 10 # number of possible digits (with 7)
exception_digit = 7 # digit to get rid off
stimuli_digits = np.arange(possible_digit) # get a vector from 0 to 9 which are the possible digits (with 7)
stimuli_digits = np.delete(stimuli_digits, exception_digit) # delete the digit 7 (not part of the stimuli)


# GENERATING DIGITS FOR EXPERIMENTAL CONDITION----------------------------------


# create the 3 digits randomly for each trial
for x in nTrials_vector:
    # randomly choose the 3 digits from the possible stimuli without 
    # remplacement (no identical digit in the same triplet)
    rand_digit = np.random.choice(stimuli_digits, size = nDigits, replace = False)
    out_matrix[x] = rand_digit

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
workbook = xlsxwriter.Workbook('Stimuli_exp_cond.xlsx')
worksheet = workbook.add_worksheet()
# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0
# Iterate over the data and write it out row by row.
for ID_trial, digit1, digit2, digit3 in (out_matrix_4xlsx):
    worksheet.write(row, col, ID_trial)
    worksheet.write(row, col + 1, digit1)
    worksheet.write(row, col + 2, digit2)
    worksheet.write(row, col + 3, digit3)
    row += 1

workbook.close()


# GENERATING DIGITS FOR CONTROL CONDITION---------------------------------------
# As stated above, there are the same contraints for the control condition.
# Chunk of code commented: add the condition that the triplets should be different
# across conditions (experimental vs control).
# We drop this condition since it is never met with increased number of trials.


# Preparing variables
out_matrix_control = np.zeros((nTrials, nDigits))  # create the array template of size: rows = nTrials , columns = 3 (nDigits)
elems_in_exp = [] # vector containing the information if current triplet is equal to one triplet in the experimental condition (logical)
inBothMat = True

# create the 3 digits randomly times the number of trials
for x in nTrials_vector:
    # randomly choose the 3 digits from the possible stimuli vector without 
    #remplacement (no identical digit in the same triplet)
    rand_digit = np.random.choice(stimuli_digits, size = nDigits, replace = False)
    out_matrix_control[x] = rand_digit

# get the unique triplets to identify which triplets are repeated between trials
unique_digits, index_uniques, count_rep_digits = np.unique(out_matrix_control, axis = 0, return_index=True, return_counts=True)

# check if there is at least one row which is repeated (containing the same digits as another row)
repeated_digits = np.where(count_rep_digits > 1) # a value > 1 means that the current row (triplet) is present more than once
repeated_digits = np.asarray(repeated_digits[0]) # convert as array (more convenient)
# get the index of the repeated digits in the original matrix
idx_repeated_digits = index_uniques[repeated_digits] 

# if at least 1 repeated digit...
while len(idx_repeated_digits) > 0:
    # choose random triplet again (without replacement)
    out_matrix_control[idx_repeated_digits[0]] = np.random.choice(stimuli_digits, size = nDigits, replace = False)
    # check again if there is repeated digits
    unique_digits, index_uniques, count_rep_digits = np.unique(out_matrix_control, axis = 0, return_index=True, return_counts=True)
    repeated_digits = np.where(count_rep_digits > 1)
    repeated_digits = np.asarray(repeated_digits[0])
    # get the index of the repeated digits in the original matrix
    idx_repeated_digits = index_uniques[repeated_digits]
    #continue the loop until no repeated digits anymore


# THE CONDITION WE DECIDED TO GET RID OFF:
# delete the TrialID column of the experimental condition matrix (easier for
# comparison)
#out_matrix = out_matrix[:,1:]

# Now that we have a matrix without repeating triplets, we have to check if the
# matrix of the condition contains same triplets as the control condition

#while inBothMat:
    
    # check if there is any row (triplet) in control condition matrix contained in
    # experimental condition matrix (output is logical)
    #elems_in_exp = (out_matrix_control[None,:] == out_matrix[:,None]).all(-1).any(0)
    # if any identical triplet found...
    #if any(elems_in_exp):
        # get the index of the duplicates
        #true_elems = np.where(elems_in_exp == True)
        #true_elems = np.asarray(true_elems[0])
        # reroll triplet for the current indices
        #out_matrix_control[true_elems[0]] = np.random.choice(stimuli_digits, size = nDigits, replace = False)
        # check if the previous reroll did not lead to identical triplets in the
        # current stimuli set (control condition)
        #unique_digits, index_uniques, count_rep_digits = np.unique(out_matrix_control, axis = 0, return_index=True, return_counts=True)
        #repeated_digits = np.where(count_rep_digits > 1)
        #repeated_digits = np.asarray(repeated_digits[0])
        # if at least 1 repeated digit, replace it and so on (see comments above)
        #while len(repeated_digits) > 0:
            #out_matrix_control[repeated_digits[0]] = np.random.choice(stimuli_digits, size = nDigits, replace = False)
            #unique_digits, index_uniques, count_rep_digits = np.unique(out_matrix_control, axis = 0, return_index=True, return_counts=True)
            #repeated_digits = np.where(count_rep_digits > 1)
            #repeated_digits = np.asarray(repeated_digits[0])
        # afterwards it will check again if the previous rerolls (if any) did not
        # lead to identical triplet across conditions (since inBothMath is
        # still True).
        
    # if no identical triplet across conditions, exit the loop
    #else:
            #inBothMat = False


# once the stimulus set is done, insert the trial ID next to the triplet
out_matrix_control = np.insert(out_matrix_control, 0, nTrials_vector, axis = 1)
# insert labels of columns for PsychoPy to read conditions
out_matrix_control_4xlsx = np.vstack((labels_colomn, out_matrix_control))

# after vstack, the format of the triplets is not the one we want. It is a
# 1 decimal string. We have to convert it in 0 decimal int.
col = np.arange(nDigits+1)
row = np.arange(nTrials+1)
row = row [1:] # get rid of the first row since there are char strings
for x in row:
    for i in col:
        out_matrix_control_4xlsx[x,i] = round(float(out_matrix_control_4xlsx[x,i]))

# Preparing Excel files
workbook = xlsxwriter.Workbook('Stimuli_ctrl_cond.xlsx')
worksheet = workbook.add_worksheet()
# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0
# Iterate over the data and write it out row by row.
for ID_trial, digit1, digit2, digit3 in (out_matrix_control_4xlsx):
    worksheet.write(row, col, ID_trial)
    worksheet.write(row, col + 1, digit1)
    worksheet.write(row, col + 2, digit2)
    worksheet.write(row, col + 3, digit3)
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
StartupClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Startup"-------
while continueRoutine:
    # get current time
    t = StartupClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=StartupClock)
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

# -------Ending Routine "Startup"-------
for thisComponent in StartupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# This chunk of code defines the order in which the tasks (NV speech vs SiN) will
# be presented. If the current trial is a NV or SiN is randomized. However,
# it should not have more than 3 identical tasks in consecutive order
# (NV, NV, NV, NV, SiN is not allowed: NV has to come max. 3 times in a row).
n_max_consecutive = 3 # Number of consecutive equal elements allowed
nTrials_half = round(nTrials / 2) # It is actually equal to the nTrials_1Block variable

# Create a nTrial long vector of 0 and 1 (half of the elements are 0, the other
# half 1) and shuffle the order of the elements to have a random order of presentation.
# 0: NV speech trial
# 1: SiN trial
tasks = np.ones(nTrials)
tasks[:nTrials_half] = 0
np.random.shuffle(tasks)

# Gather the elems present more than 3 times in a row in a separate vector and delete them
# from the initial vector.
tasks_grouped = [list(g) for k, g in groupby(tasks)] # group the elements together
consecutive = []
consecutive_vector = []
for i in tasks_grouped:
    if len(i) > n_max_consecutive:
        # select the consecutive elements which are above 3 times in a row
        consecutive = i[n_max_consecutive:]
        # gather the consecutive elements which are above 3 times in a row in a
        # separate vector
        consecutive_vector.append(consecutive)
        # delete them from the intial vector
        del i[n_max_consecutive:] 

# Take the initial vector and check where to put the removed elements back in order
# to respect the "max X times in a row" condition.
index = 0
for i in tasks_grouped:
    if not consecutive_vector: # this condition is necessary for the last iteration.
        break
    # The length of the current consecutive elems as well as the length of the
    # next group of consecutive elems should not be equal to 3. This is needed to know
    # where we are allowed to put the removed elems back.
    print(len(tasks_grouped))
    print([index+1])
    if len(i) < n_max_consecutive and len(tasks_grouped[index]) < n_max_consecutive: 
        # This condition is needed to put the 1 together and the 0 together to
        # keep the list grouped (e.g. [0,0,0], [1,1]...)
        if consecutive_vector[0][0] == tasks_grouped[index][0]:
            # place the elem back in the initial vector
            tasks_grouped[index].insert(0, consecutive_vector[0][0])
            # since the elem is back in the initial vector, delete it from the other vector
            del consecutive_vector[0][0] 
        elif consecutive_vector[0][0] == tasks_grouped[index+1][0]:
            tasks_grouped[index+1].insert(0, consecutive_vector[0][0])
            del consecutive_vector[0][0]
    
    # if no elems in the sublist anymore, delete the current sublist
    if len(consecutive_vector[0]) == 0:
        del consecutive_vector[0]
    index += 1

# get the list as a vector
tasks_grouped_list = [item for sublist in tasks_grouped for item in sublist] # listed list as a list
order_task_trial = np.asarray(tasks_grouped_list) # list as vector
sys.stdout = StimOrder_file # open file for saving order of stimulation
print(order_task_trial)
sys.stdout = sys.__stdout__ # close file


# the Routine "Startup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Welcome"-------
continueRoutine = True
# update component parameters for each repeat
# This is the text welcoming the subjects to the experiment.
# Once they read the text, they can press enter to continue.
begin_exp = []
# set EEG marker for displaying welcome text
if use_lpt:
    port.setData(109)
# keep track of which components have finished
WelcomeComponents = [Instructions_Noise]
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
WelcomeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Welcome"-------
while continueRoutine:
    # get current time
    t = WelcomeClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=WelcomeClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # Get the pressed key of the subject
    begin_exp = event.getKeys(keyList=['return'])
    
    # Begin experiment once the subject pressed enter
    if "return" in begin_exp:
        # if enter is pressed, the current routine stops and we move into the next one
        continueRoutine = False
    
    # *Instructions_Noise* updates
    if Instructions_Noise.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Instructions_Noise.frameNStart = frameN  # exact frame index
        Instructions_Noise.tStart = t  # local t and not account for scr refresh
        Instructions_Noise.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Instructions_Noise, 'tStartRefresh')  # time at next scr refresh
        Instructions_Noise.setAutoDraw(True)
    
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

# -------Ending Routine "Welcome"-------
for thisComponent in WelcomeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Welcome" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Testing_Background_Noise"-------
continueRoutine = True
routineTimer.add(5.000000)
# update component parameters for each repeat
# This routine is part of the practice trials and is meant to determine the
# volume of the background noise (ask the participant if too loud / too low)

# set EEG marker for testing the background noise
if use_lpt:
    port.setData(90)

# Start playing background noise
# ELSAS code: sd.play(sound_noise, fs, loop=True)

sound_noise.play()
# keep track of which components have finished
Testing_Background_NoiseComponents = [Fixation_cross_Test]
for thisComponent in Testing_Background_NoiseComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Testing_Background_NoiseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Testing_Background_Noise"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = Testing_Background_NoiseClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Testing_Background_NoiseClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
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
            win.timeOnFlip(Fixation_cross_Test, 'tStopRefresh')  # time at next scr refresh
            Fixation_cross_Test.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Testing_Background_NoiseComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Testing_Background_Noise"-------
for thisComponent in Testing_Background_NoiseComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Stop the background noise
sound_noise.stop()

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
    
    # ------Prepare to start Routine "Instructions_practice"-------
    continueRoutine = True
    # update component parameters for each repeat
    # This is the text welcoming the subjects to the experiment.
    # Once they read the text, they can press enter to continue.
    
    # set EEG marker for instruction practice block
    if use_lpt:
        port.setData(100)
    
    begin_exp = []
    
    # keep track of which components have finished
    Instructions_practiceComponents = [Instructions_clear_Digits]
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
    Instructions_practiceClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Instructions_practice"-------
    while continueRoutine:
        # get current time
        t = Instructions_practiceClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Instructions_practiceClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Get the pressed key of the subject
        begin_exp = event.getKeys(keyList=['return'])
        
        # Begin experiment once the subject pressed enter
        if "return" in begin_exp:
            # if enter is pressed, the current routine stops and we move into the next one
            continueRoutine = False
        
        # *Instructions_clear_Digits* updates
        if Instructions_clear_Digits.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Instructions_clear_Digits.frameNStart = frameN  # exact frame index
            Instructions_clear_Digits.tStart = t  # local t and not account for scr refresh
            Instructions_clear_Digits.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Instructions_clear_Digits, 'tStartRefresh')  # time at next scr refresh
            Instructions_clear_Digits.setAutoDraw(True)
        
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
    
    # -------Ending Routine "Instructions_practice"-------
    for thisComponent in Instructions_practiceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Instructions_practice" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    practice_trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('practice_trials.xlsx'),
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
        
        # ------Prepare to start Routine "clear_digits"-------
        continueRoutine = True
        # update component parameters for each repeat
        # Randomly choose one speaker for the current trial
        rand_speaker = (np.random.choice(speaker, size = 1))
        rand_speaker = int(rand_speaker[0])
        #print(rand_speaker)
        
        # Reading the current digits from xlsx file
        firstdigit = int(NFB_digit1)
        seconddigit = int(NFB_digit2)
        thirddigit = int(NFB_digit3)
        
        # Playing the first digit
        if firstdigit < 8:
            digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_48kHz_filtered_mono.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_48kHz_filtered_mono.wav'
        
        # Playing the second digit
        if seconddigit < 8:
            digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_48kHz_filtered_mono.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
            digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_48kHz_filtered_mono.wav'
        
        # Playing the third digit
        if thirddigit < 8:
            digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_48kHz_filtered_mono.wav'
        else: # here we have to change the index since there is no 7 in the stimuli
           digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_48kHz_filtered_mono.wav'
        Digit1_clear.setSound(digit1, hamming=True)
        Digit1_clear.setVolume(1, log=False)
        Digit2_clear.setSound(digit2, hamming=True)
        Digit2_clear.setVolume(1, log=False)
        Digit3_clear.setSound(digit3, hamming=True)
        Digit3_clear.setVolume(1, log=False)
        # keep track of which components have finished
        clear_digitsComponents = [Digit1_clear, Digit2_clear, Digit3_clear]
        for thisComponent in clear_digitsComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        clear_digitsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "clear_digits"-------
        while continueRoutine:
            # get current time
            t = clear_digitsClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=clear_digitsClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
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
                Digit1_clear.play()  # start the sound (it finishes automatically)
            # start/stop Digit2_clear
            if Digit2_clear.status == NOT_STARTED and Digit1_clear.status == FINISHED:
                # keep track of start time/frame for later
                Digit2_clear.frameNStart = frameN  # exact frame index
                Digit2_clear.tStart = t  # local t and not account for scr refresh
                Digit2_clear.tStartRefresh = tThisFlipGlobal  # on global time
                Digit2_clear.play()  # start the sound (it finishes automatically)
            # start/stop Digit3_clear
            if Digit3_clear.status == NOT_STARTED and Digit2_clear.status == FINISHED:
                # keep track of start time/frame for later
                Digit3_clear.frameNStart = frameN  # exact frame index
                Digit3_clear.tStart = t  # local t and not account for scr refresh
                Digit3_clear.tStartRefresh = tThisFlipGlobal  # on global time
                Digit3_clear.play()  # start the sound (it finishes automatically)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in clear_digitsComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "clear_digits"-------
        for thisComponent in clear_digitsComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        Digit1_clear.stop()  # ensure sound has stopped at end of routine
        practice_trials.addData('Digit1_clear.started', Digit1_clear.tStart)
        practice_trials.addData('Digit1_clear.stopped', Digit1_clear.tStop)
        Digit2_clear.stop()  # ensure sound has stopped at end of routine
        practice_trials.addData('Digit2_clear.started', Digit2_clear.tStart)
        practice_trials.addData('Digit2_clear.stopped', Digit2_clear.tStop)
        Digit3_clear.stop()  # ensure sound has stopped at end of routine
        practice_trials.addData('Digit3_clear.started', Digit3_clear.tStart)
        practice_trials.addData('Digit3_clear.stopped', Digit3_clear.tStop)
        # the Routine "clear_digits" was not non-slip safe, so reset the non-slip timer
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
            
            # ------Prepare to start Routine "Response_practice"-------
            continueRoutine = True
            # update component parameters for each repeat
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
            key_resp_3.keys = []
            key_resp_3.rt = []
            _key_resp_3_allKeys = []
            # keep track of which components have finished
            Response_practiceComponents = [key_resp_3, disp_answer_3]
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
            Response_practiceClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Response_practice"-------
            while continueRoutine:
                # get current time
                t = Response_practiceClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=Response_practiceClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # Collect every pressed key
                #keyPress = event.getKeys(keyList=['1','2','3','4','5','6','8','9','0', 'return'])
                keyPress = event.getKeys(keyList=['num_1','num_2','num_3','num_4','num_5','num_6', 'num_7', 'num_8','num_9','num_0', 'return'])
                
                # Gather the pressed key in a string vector
                response_string = "".join(key_resp_3.keys).replace('num_', '')
                #response_string = "".join(key_resp_test.keys)
                
                if response_string: # if response_string is not empty:
                    # only disp the last pressed key to enable the subjects to do corrections 
                    # (their final response is the last keypress before "enter")
                    response = response_string[-1] 
                
                response_text = "Gehörte Ziffer: {}".format(response)
                
                if "return" in keyPress: # if "enter" key pressed
                    continueRoutine = False # pass to the next iteration (digit)
                
                
                        
                
                
                # *key_resp_3* updates
                waitOnFlip = False
                if key_resp_3.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp_3.frameNStart = frameN  # exact frame index
                    key_resp_3.tStart = t  # local t and not account for scr refresh
                    key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
                    key_resp_3.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp_3.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp_3.getKeys(keyList=['num_0', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9', 'return'], waitRelease=False)
                    _key_resp_3_allKeys.extend(theseKeys)
                    if len(_key_resp_3_allKeys):
                        key_resp_3.keys = [key.name for key in _key_resp_3_allKeys]  # storing all keys
                        key_resp_3.rt = [key.rt for key in _key_resp_3_allKeys]
                
                # *disp_answer_3* updates
                if disp_answer_3.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    disp_answer_3.frameNStart = frameN  # exact frame index
                    disp_answer_3.tStart = t  # local t and not account for scr refresh
                    disp_answer_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(disp_answer_3, 'tStartRefresh')  # time at next scr refresh
                    disp_answer_3.setAutoDraw(True)
                if disp_answer_3.status == STARTED:  # only update if drawing
                    disp_answer_3.setText(response_text, log=False)
                
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
            
            # -------Ending Routine "Response_practice"-------
            for thisComponent in Response_practiceComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
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
            if key_resp_3.keys in ['', [], None]:  # No response was made
                key_resp_3.keys = None
            response_practice.addData('key_resp_3.keys',key_resp_3.keys)
            if key_resp_3.keys != None:  # we had a response
                response_practice.addData('key_resp_3.rt', key_resp_3.rt)
            response_practice.addData('key_resp_3.started', key_resp_3.tStartRefresh)
            response_practice.addData('key_resp_3.stopped', key_resp_3.tStopRefresh)
            # the Routine "Response_practice" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed nDigits repeats of 'response_practice'
        
        thisExp.nextEntry()
        
    # completed 1 repeats of 'practice_trials'
    
    
    # ------Prepare to start Routine "repeat_practice"-------
    continueRoutine = True
    routineTimer.add(10.000000)
    # update component parameters for each repeat
    key_resp_4.keys = []
    key_resp_4.rt = []
    _key_resp_4_allKeys = []
    # keep track of which components have finished
    repeat_practiceComponents = [text_4, key_resp_4]
    for thisComponent in repeat_practiceComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    repeat_practiceClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "repeat_practice"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = repeat_practiceClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=repeat_practiceClock)
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
            text_4.setAutoDraw(True)
        if text_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_4.tStartRefresh + 10-frameTolerance:
                # keep track of stop time/frame for later
                text_4.tStop = t  # not accounting for scr refresh
                text_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(text_4, 'tStopRefresh')  # time at next scr refresh
                text_4.setAutoDraw(False)
        
        # *key_resp_4* updates
        waitOnFlip = False
        if key_resp_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_4.frameNStart = frameN  # exact frame index
            key_resp_4.tStart = t  # local t and not account for scr refresh
            key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
            key_resp_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp_4.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                key_resp_4.tStop = t  # not accounting for scr refresh
                key_resp_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_resp_4, 'tStopRefresh')  # time at next scr refresh
                key_resp_4.status = FINISHED
        if key_resp_4.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_4.getKeys(keyList=['j', 'n'], waitRelease=False)
            _key_resp_4_allKeys.extend(theseKeys)
            if len(_key_resp_4_allKeys):
                key_resp_4.keys = _key_resp_4_allKeys[-1].name  # just the last key pressed
                key_resp_4.rt = _key_resp_4_allKeys[-1].rt
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in repeat_practiceComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "repeat_practice"-------
    for thisComponent in repeat_practiceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # It asks if we want to repeat the practice block. This is in case the subject
    # did not understand either the task or the way to provide his answer (or both).
    # ...Start the practice block again: press "y" (you have 20 seconds to press "y". If
    # you don't, the experiment will go on)
    # ...Don't retart it: just wait and the experiment will go on
    
    if key_resp_4.keys == 'j':
        practice_block.finished=0
        continueRoutine = True 
    elif key_resp_4.keys == 'n':
        practice_block.finished=1
        practice_trials.finished=1
        continueRoutine = False
    else:
        practice_block.finished=1
        practice_trials.finished=1
        continueRoutine = False
        
            
            
    practice_block.addData('text_4.started', text_4.tStartRefresh)
    practice_block.addData('text_4.stopped', text_4.tStopRefresh)
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
    
    # ------Prepare to start Routine "Instruction_start_Experiment"-------
    continueRoutine = True
    # update component parameters for each repeat
    # This is the instruction explaining that we will gather some neural data for a
    # period of time and that the person has the stay quiet. Subject press "enter
    # to continue.
    
    begin_exp = []
    
    # set EEG marker for instruction calibration
    if use_lpt:
        port.setData(101)
    # keep track of which components have finished
    Instruction_start_ExperimentComponents = [Instructions_begin]
    for thisComponent in Instruction_start_ExperimentComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Instruction_start_ExperimentClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Instruction_start_Experiment"-------
    while continueRoutine:
        # get current time
        t = Instruction_start_ExperimentClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Instruction_start_ExperimentClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Get the pressed key of the subject
        begin_exp = event.getKeys(keyList=['return'])
        
        # Begin experiment once the subject pressed enter
        if "return" in begin_exp:
            # if enter is pressed, the current routine stops and we move into the next one
            continueRoutine = False
        
        # *Instructions_begin* updates
        if Instructions_begin.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Instructions_begin.frameNStart = frameN  # exact frame index
            Instructions_begin.tStart = t  # local t and not account for scr refresh
            Instructions_begin.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Instructions_begin, 'tStartRefresh')  # time at next scr refresh
            Instructions_begin.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Instruction_start_ExperimentComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Instruction_start_Experiment"-------
    for thisComponent in Instruction_start_ExperimentComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Instruction_start_Experiment" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "Calibrating"-------
    continueRoutine = True
    # update component parameters for each repeat
    # In this routine, the alpha ratios of the subject will be recorded during the
    # so-called "calibration phase". Once collected, the mean and std will be calculated.
    # At the end of the routine, the individual factor for the threshold will be estimated:
    # Threshold = mean_ratio_calibration + estimated_indiv_factor * std_ratio_calibration
    
    # set EEG marker for calibration
    if use_lpt:
        port.setData(91)
    
    # Start playing background noise
    sound_noise.play()
    
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
    
    # keep track of which components have finished
    CalibratingComponents = [Fixation_cross]
    for thisComponent in CalibratingComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    CalibratingClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Calibrating"-------
    while continueRoutine:
        # get current time
        t = CalibratingClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=CalibratingClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # pull chunks from the EEG stream (see startup)
        chunk, timestamps = inlet_EEG.pull_chunk()
        chunks_frame = [i[0:32] for i in chunk] # select the 32 elecs of interest
        
        # calculate the alpha ratios of the incoming signal. Blue elecs and red elecs are
        # chosen from the topomap of TH's results.
        if chunks_frame:
            signal = chunks_frame
            # just select the elecs of interest and average them
            blue_elecs = np.average([signal[0][Fz], signal[0][F8], signal[0][FT10], signal[0][O1]])
            red_elecs = np.average([signal[0][C3], signal[0][CP1]])
            # build the ratio between these 2 clusters
            ratio_elecs = red_elecs - blue_elecs
            sys.stdout = dataCalibration_file # open file for saving ratios during calibration
            print(timestamps, ratio_elecs) # saving ratios during calibration
        
        # actualize count of frame
        count += 1
        
        # vector gathering ratios of each frame
        ratio_vec_rs = np.append(ratio_vec_rs, ratio_elecs) 
        
        # once calibration is over, calculates the mean and std of alpha ratio gathered
        # during the calibration
        if count == baseline_duration_frames: # once vector is 100 sec long, get the mean and std
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
            
            
            
            
        
                   
            
            
        
            
        
        
        # *Fixation_cross* updates
        if Fixation_cross.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            Fixation_cross.frameNStart = frameN  # exact frame index
            Fixation_cross.tStart = t  # local t and not account for scr refresh
            Fixation_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Fixation_cross, 'tStartRefresh')  # time at next scr refresh
            Fixation_cross.setAutoDraw(True)
        if Fixation_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Fixation_cross.tStartRefresh + baseline_duration_sec-frameTolerance:
                # keep track of stop time/frame for later
                Fixation_cross.tStop = t  # not accounting for scr refresh
                Fixation_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(Fixation_cross, 'tStopRefresh')  # time at next scr refresh
                Fixation_cross.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in CalibratingComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Calibrating"-------
    for thisComponent in CalibratingComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Stop the background noise
    sound_noise.stop()
    
    # find the individual factor of the current subject
    ratio_vec_rs = np.array(ratio_vec_rs) # convert baseline signal as array
    
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
    
    while nFound_triggers < nTrigger_Baseline and current_factor > 0:
        # find the indices of the calibration samples which are reaching the current threshold
        triggers = np.where(ratio_vec_rs > ratio_vec_mean + current_factor*ratio_vec_std)
        sys.stdout = allTriggers_baseline # open file for all found triggers during calibration
        print(current_factor, triggers[0])
        sys.stdout = sys.__stdout__ # close file for all found triggers during calibration
        
        # if there is only 1 trigger found, save it in the definitive trigger vector:
        if len(triggers[0]) == 1:
            def_triggers = triggers[0][0]
            
        # if there is more than 1 trigger found, do the later
        elif len(triggers[0]) > 1:
            # get the first trigger
            first_trigger = triggers[0][0]
            # the rest of the triggers are saved separately to check for the difference
            # between the first and the other triggers later.
            rest_triggers = triggers[0][1:]
            
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
            def_triggers = rest_triggers
            # prepend first trigger to result (because it was not there)
            def_triggers = np.insert(def_triggers, 0, triggers[0][0], axis=0)
            print(current_factor, "definitive triggers:", def_triggers)
            
        # get the number of definitive found triggers
        nFound_triggers = len(def_triggers)
        print(current_factor, "number of definitive triggers:", nFound_triggers)
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
    print('thresh =', ratio_vec_mean + int(indiv_factor) * ratio_vec_std)
    # the Routine "Calibrating" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "repeat_calibration"-------
    continueRoutine = True
    routineTimer.add(10.000000)
    # update component parameters for each repeat
    key_resp_5.keys = []
    key_resp_5.rt = []
    _key_resp_5_allKeys = []
    # keep track of which components have finished
    repeat_calibrationComponents = [text_5, key_resp_5]
    for thisComponent in repeat_calibrationComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    repeat_calibrationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "repeat_calibration"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = repeat_calibrationClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=repeat_calibrationClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_5* updates
        if text_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_5.frameNStart = frameN  # exact frame index
            text_5.tStart = t  # local t and not account for scr refresh
            text_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_5, 'tStartRefresh')  # time at next scr refresh
            text_5.setAutoDraw(True)
        if text_5.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_5.tStartRefresh + 10-frameTolerance:
                # keep track of stop time/frame for later
                text_5.tStop = t  # not accounting for scr refresh
                text_5.frameNStop = frameN  # exact frame index
                win.timeOnFlip(text_5, 'tStopRefresh')  # time at next scr refresh
                text_5.setAutoDraw(False)
        
        # *key_resp_5* updates
        waitOnFlip = False
        if key_resp_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_5.frameNStart = frameN  # exact frame index
            key_resp_5.tStart = t  # local t and not account for scr refresh
            key_resp_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_5, 'tStartRefresh')  # time at next scr refresh
            key_resp_5.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_5.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_5.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp_5.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                key_resp_5.tStop = t  # not accounting for scr refresh
                key_resp_5.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_resp_5, 'tStopRefresh')  # time at next scr refresh
                key_resp_5.status = FINISHED
        if key_resp_5.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_5.getKeys(keyList=['y'], waitRelease=False)
            _key_resp_5_allKeys.extend(theseKeys)
            if len(_key_resp_5_allKeys):
                key_resp_5.keys = _key_resp_5_allKeys[-1].name  # just the last key pressed
                key_resp_5.rt = _key_resp_5_allKeys[-1].rt
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in repeat_calibrationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "repeat_calibration"-------
    for thisComponent in repeat_calibrationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # It asks if we want to repeat the calibration. This is in case one of the
    # following criteria is not fulfilled (check the stdout of PsychoPy):
    #...Mean should NOT be around 0 (most of the values are around 2-4)
    #...Std should be acceptable compared to the mean (e.g. by a mean of 3.58, 3 is acceptable, 18 is not)
    #...The indiv factor should be at least 2
    # Here is what to do to restart the calibration:
    # ...Start thecalibration again: press "y" (you have 20 seconds to press "y". If
    # you don't, the experiment will go on)
    # ...Don't retart it: just wait and the experiment will go on
    
    if key_resp_5.keys:
        calibration_block.finished=0
        continueRoutine = True 
    else:
        calibration_block.finished=1
        #practice_trials.finished=1
        continueRoutine = False 
            
    calibration_block.addData('text_5.started', text_5.tStartRefresh)
    calibration_block.addData('text_5.stopped', text_5.tStopRefresh)
    thisExp.nextEntry()
    
# completed 100 repeats of 'calibration_block'


# ------Prepare to start Routine "Break"-------
continueRoutine = True
# update component parameters for each repeat
# Instructions of the experiment. Subject presses enter to continue

# set EEG marker for instructions experiment
if use_lpt:
    port.setData(102)

begin_expBlock = []
# keep track of which components have finished
BreakComponents = [Begin]
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
BreakClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Break"-------
while continueRoutine:
    # get current time
    t = BreakClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=BreakClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # Get the pressed key of the subject
    begin_expBlock = event.getKeys(keyList=['return'])
    
    # Begin experiment once the subject pressed enter
    if "return" in begin_expBlock:
        # if enter is pressed, the current routine stops and we move into the next one
        continueRoutine = False 
    
    # *Begin* updates
    if Begin.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Begin.frameNStart = frameN  # exact frame index
        Begin.tStart = t  # local t and not account for scr refresh
        Begin.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Begin, 'tStartRefresh')  # time at next scr refresh
        Begin.setAutoDraw(True)
    
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

# -------Ending Routine "Break"-------
for thisComponent in BreakComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Start playing background noise
# ELSAS code sound_noise, fs = sf.read('constantNoise_1minute_16kHz_filtered_mono_looped.wav', dtype='float32')  
#sound_noise.play()
thisExp.addData('Begin.started', Begin.tStartRefresh)
thisExp.addData('Begin.stopped', Begin.tStopRefresh)
# the Routine "Break" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
experimental_block = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='experimental_block')
thisExp.addLoop(experimental_block)  # add the loop to the experiment
thisExperimental_block = experimental_block.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisExperimental_block.rgb)
if thisExperimental_block != None:
    for paramName in thisExperimental_block:
        exec('{} = thisExperimental_block[paramName]'.format(paramName))

for thisExperimental_block in experimental_block:
    currentLoop = experimental_block
    # abbreviate parameter names if possible (e.g. rgb = thisExperimental_block.rgb)
    if thisExperimental_block != None:
        for paramName in thisExperimental_block:
            exec('{} = thisExperimental_block[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    exp_trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('Stimuli_exp_cond.xlsx', selection=trial_nr),
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
        
        # ------Prepare to start Routine "signal_check"-------
        continueRoutine = True
        # update component parameters for each repeat
        # In this routine, we check the ongoing alpha ratio of the subject. If an alpha
        # ratio sample is greater than the threshold, the stimuli are triggered.
        # Threshold = mean_ratio_calibration + estimated_indiv_factor * std_ratio_calibration
        
        # set EEG marker for calibration
        if use_lpt:
            port.setData(92)
        
        ITI = 120 #set the iter trial interval at 2s (60 frames per second: 2 seconds = 120 frames)
        #continueRoutine = True
        count = 0
        disp = 0
        signal_current_trial = np.array([])
        
        #trigger1 = time.time() # get timestamp as seconds
        #trigger2 = 0
        
        # Define the subset of stimuli to play depending on block 1 or block 2:
        # block 1: Trials 1 to 70
        # block 2: Trials 71 to 140
        # The last entry of the slice is not being included, so the last included will be (nTrials_half - 1).
        # This is what we need because we want it to be (nTrials_half-1) because of the Python indexing starting from 0
        trial_nr = slice(0, nTrials_half) 
        if nExpBlock == 2:
            trial_nr = slice(nTrials_half, nTrials) 
        
        #print(nExpBlock, nExpTrials, trial_nr)
        
        # Define the current task to play: NV speech or SiN
        NV = []
        SiN = []
        if order_task_trial[nExpTrials] == 0:
            NV = 1
            SiN = 0
        else: 
            NV = 0
            SiN = 1
        
        # need to move parts from digits_played to here to start preparing things!
        # In this routine, the triplets are presented once the threshold
        # was reached in the previous routine. If NV speech or SiN is presented
        # depends on the random trial order defined in startup.
        # Maybe we could find a way to buffer the audio files in order to decrease the
        # delay.
        
        # Randomly choose one speaker for the current trial
        rand_speaker = np.random.choice(speaker, size = 1)
        rand_speaker = int(rand_speaker[0])
        #print(rand_speaker)
        
        # Defining the current digits
        firstdigit = int(NFB_digit1)
        seconddigit = int(NFB_digit2)
        thirddigit = int(NFB_digit3)
        
        if NV == 1 and SiN == 0:
            
            # Stop the background noise: For NV speech, we don't want any background noise
            # during stimulus presentation
            #sound_noise.stop()
            
            # Playing the first digit
            if firstdigit < 8:
                digit1 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(firstdigit)+'_'+str(noise[firstdigit])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit1 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(firstdigit)+'_'+str(noise[firstdigit-1])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
        
            # Playing the second digit
            if seconddigit < 8:
                digit2 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(seconddigit)+'_'+str(noise[seconddigit])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit2 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(seconddigit)+'_'+str(noise[seconddigit-1])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
        
            # Playing the third digit
            if thirddigit < 8:
                digit3 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(thirddigit)+'_'+str(noise[thirddigit])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit3 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(thirddigit)+'_'+str(noise[thirddigit-1])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
        
        
        elif NV == 0 and SiN == 1:
            
            # Playing the first digit
            if firstdigit < 8:
                digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_48kHz_filtered_mono.wav'
        
            # Playing the second digit
            if seconddigit < 8:
                digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_48kHz_filtered_mono.wav'
        
            # Playing the third digit
            if thirddigit < 8:
                digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_48kHz_filtered_mono.wav'
        
        
        
        
        
        
        # shall we try to prepare sounds here?
        
        sound_digit1 = sound.Sound(digit1, preBuffer= -1)
        sound_digit2 = sound.Sound(digit2, preBuffer= -1)
        sound_digit3 = sound.Sound(digit3, preBuffer= -1)
        
        # Start playing background noise
        sound_noise.play()
        
        
        
        # keep track of which components have finished
        signal_checkComponents = [Fixation]
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
        signal_checkClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "signal_check"-------
        while continueRoutine:
            # get current time
            t = signal_checkClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=signal_checkClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # actualize count of frame
            count += 1
            
            # pull chunks from the EEG stream
            chunk, timestamps = inlet_EEG.pull_chunk()
            chunks_frame = [i[0:32] for i in chunk] # select the 32 elecs of interest
                
            # calculate the alpha ratios of the incoming signal. Blue elecs and red elecs are
            # chosen from the topomap of TH's results.
            if chunks_frame:
                signal = chunks_frame
                # just select the elecs of interest and average them
                blue_elecs = np.average([signal[0][Fz], signal[0][F8], signal[0][FT10], signal[0][O1]])
                red_elecs = np.average([signal[0][C3], signal[0][CP1]])
                # build the ratio between these 2 clusters
                ratio_elecs = red_elecs - blue_elecs
                sys.stdout = dataSignalCheck_file # open Signal check file to save ratios during signal check
                #print("data_signalCheck")
                print(timestamps, ratio_elecs)
            
            # vector gathering signal for subsequent control condition
            signal_current_trial = np.append(signal_current_trial, ratio_elecs)
            
            if count > ITI: # wait for 2 seconds (ITI) before checking if the threshold is reached
                if ratio_elecs > ratio_vec_mean + int(indiv_factor) * ratio_vec_std: # if threshold is reached, current routine ends and stimuli are delivered
                #if ratio_elecs == ratio_elecs:
                    sys.stdout = sys.__stdout__ # close signal check file
                    #trigger2 = time.time()
                    continueRoutine = False # ends the current routine
                if use_debug: # if in debug mode, stimulate every 2 seconds
                    sys.stdout = sys.__stdout__ # close signal check file
                    continueRoutine = False # ends the current routine
            
                        
            
            
            # *Fixation* updates
            if Fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fixation.frameNStart = frameN  # exact frame index
                Fixation.tStart = t  # local t and not account for scr refresh
                Fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fixation, 'tStartRefresh')  # time at next scr refresh
                Fixation.setAutoDraw(True)
            
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
        
        # -------Ending Routine "signal_check"-------
        for thisComponent in signal_checkComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # save signal of the current trial in a list for control condition
        # it will then be used to determine the duration it took to trigger the stimuli
        # for each trial.
        signal_trials.append(signal_current_trial)
        
        #sys.stdout = MarkerExp
        #print(trigger1, trigger2)
        #sys.stdout = sys.__stdout__
        
        exp_trials.addData('Fixation.started', Fixation.tStartRefresh)
        exp_trials.addData('Fixation.stopped', Fixation.tStopRefresh)
        # the Routine "signal_check" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "digits_played"-------
        continueRoutine = True
        # update component parameters for each repeat
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
        digits_playedComponents = [sound_digit1, sound_digit2, sound_digit3]
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
        digits_playedClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "digits_played"-------
        while continueRoutine:
            # get current time
            t = digits_playedClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=digits_playedClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if use_lpt:
                if sound_digit1.status == STARTED:
                    port.setData(12)
                elif sound_digit2.status == STARTED:
                    port.setData(22)
                elif sound_digit3.status == STARTED:
                    port.setData(32)
            # start/stop sound_digit1
            if sound_digit1.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                sound_digit1.frameNStart = frameN  # exact frame index
                sound_digit1.tStart = t  # local t and not account for scr refresh
                sound_digit1.tStartRefresh = tThisFlipGlobal  # on global time
                sound_digit1.play()  # start the sound (it finishes automatically)
            # start/stop sound_digit2
            if sound_digit2.status == NOT_STARTED and sound_digit1.status == FINISHED:
                # keep track of start time/frame for later
                sound_digit2.frameNStart = frameN  # exact frame index
                sound_digit2.tStart = t  # local t and not account for scr refresh
                sound_digit2.tStartRefresh = tThisFlipGlobal  # on global time
                sound_digit2.play()  # start the sound (it finishes automatically)
            # start/stop sound_digit3
            if sound_digit3.status == NOT_STARTED and sound_digit2.status == FINISHED:
                # keep track of start time/frame for later
                sound_digit3.frameNStart = frameN  # exact frame index
                sound_digit3.tStart = t  # local t and not account for scr refresh
                sound_digit3.tStartRefresh = tThisFlipGlobal  # on global time
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
        
        # -------Ending Routine "digits_played"-------
        for thisComponent in digits_playedComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        if NV == 1 and SiN == 0:
            # Start replaying background noise because it was stopped in the NV speech task
            # Elsas code: sd.play(sound_noise, fs, loop=True)
            
            sound_noise.play()
        sound_digit1.stop()  # ensure sound has stopped at end of routine
        exp_trials.addData('sound_digit1.started', sound_digit1.tStart)
        exp_trials.addData('sound_digit1.stopped', sound_digit1.tStop)
        sound_digit2.stop()  # ensure sound has stopped at end of routine
        exp_trials.addData('sound_digit2.started', sound_digit2.tStart)
        exp_trials.addData('sound_digit2.stopped', sound_digit2.tStop)
        sound_digit3.stop()  # ensure sound has stopped at end of routine
        exp_trials.addData('sound_digit3.started', sound_digit3.tStart)
        exp_trials.addData('sound_digit3.stopped', sound_digit3.tStop)
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
            
            # ------Prepare to start Routine "Response_subjects"-------
            continueRoutine = True
            # update component parameters for each repeat
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
            Response_subjectsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Response_subjects"-------
            while continueRoutine:
                # get current time
                t = Response_subjectsClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=Response_subjectsClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # Collect every pressed key
                keyPress = event.getKeys(keyList=['num_1','num_2','num_3','num_4','num_5','num_6', 'num_7', 'num_8','num_9','num_0', 'return'])
                # Gather the pressed key in a string vector
                response_string = "".join(key_resp.keys).replace('num_', '') 
                
                if response_string: # if response_string is not empty:
                    # only disp the last pressed key to enable the subjects to do corrections 
                    # (their final response is the last keypress before "enter")
                    response = response_string[-1] 
                
                response_text_exp = "Gehörte Ziffer: {}".format(response)
                
                if "return" in keyPress: # if "enter" key pressed
                    continueRoutine = False # pass to the next iteration (digit)
                
                
                        
                
                
                # *key_resp* updates
                waitOnFlip = False
                if key_resp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp.frameNStart = frameN  # exact frame index
                    key_resp.tStart = t  # local t and not account for scr refresh
                    key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                    key_resp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp.getKeys(keyList=['num_0', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9', 'return'], waitRelease=False)
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
            
            # -------Ending Routine "Response_subjects"-------
            for thisComponent in Response_subjectsComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
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
            response_exp.addData('key_resp.started', key_resp.tStartRefresh)
            response_exp.addData('key_resp.stopped', key_resp.tStopRefresh)
            # the Routine "Response_subjects" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed nDigits repeats of 'response_exp'
        
        
        # ------Prepare to start Routine "Next_Block"-------
        continueRoutine = True
        # update component parameters for each repeat
        # At the end of the first block, there is a text saying that there is a break.
        # at the end of the second block, there is a text saying that there is a break
        # and that the experimentator will come to the room.
        # The subject can press "enter" whenever he is ready to go on
        
        begin_ExpBlock = []
        
        # changing / displaying the instruction depending on the current block finished
        instructions_next_block = ' '
        # if it is the last trial of the first block
        if nExpBlock == 1 and nExpTrials == (nTrials_half-1):
            sound_noise.stop() # Stop the background noise
            instructions_next_block = '''Du hast den ersten Block geschafft, Glückwunsch! Du kannst Dich kurz entspannen, wenn nötig.
            
            Sobald Du bereit bist, um den nächsten Block zu starten, kannst Du auf "Enter" drücken.
            
            Weiterhin gilt: Solange das Fixationskreuz sichtbar ist, bewege Dich bitte nicht.'''
        # if it is the last trial of the second block
        elif nExpBlock == 2 and nExpTrials == (nTrials-1):
            sound_noise.stop() # Stop the background noise
            instructions_next_block = '''Du hast den zweiten Block geschafft, Glückwunsch!
            
            Nun gibt es eine kleine Pause. Der/die VersuchsleiterIn wird in Kürze in den Raum kommen.'''
            #print(signal_trials)
        # if other trial
        else:
            continueRoutine = False
        Begin_3.setText(instructions_next_block)
        # keep track of which components have finished
        Next_BlockComponents = [Begin_3]
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
        Next_BlockClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Next_Block"-------
        while continueRoutine:
            # get current time
            t = Next_BlockClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=Next_BlockClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Get the pressed key of the subject
            begin_ExpBlock = event.getKeys(keyList=['return'])
            
            # Begin experiment once the subject pressed enter
            if "return" in begin_ExpBlock:
                continueRoutine = False # wait for the subject to press the key "enter"
            
            # *Begin_3* updates
            if Begin_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Begin_3.frameNStart = frameN  # exact frame index
                Begin_3.tStart = t  # local t and not account for scr refresh
                Begin_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Begin_3, 'tStartRefresh')  # time at next scr refresh
                Begin_3.setAutoDraw(True)
            
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
        
        # -------Ending Routine "Next_Block"-------
        for thisComponent in Next_BlockComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # set EEG marker for each instruction (after 1st and 2nd block are finished) 
        if use_lpt:
            if nExpTrials == (nTrials_half-1):
                port.setData(212)
            elif nExpTrials == (nTrials-1):
                port.setData(222)
            
        # Start playing background noise
        sound_noise.play()
        
        #print(signal_trials)
        
        # Update Trial counter
        nExpTrials += 1
        if nExpTrials == nTrials_half:
            nExpBlock += 1
        exp_trials.addData('Begin_3.started', Begin_3.tStartRefresh)
        exp_trials.addData('Begin_3.stopped', Begin_3.tStopRefresh)
        # the Routine "Next_Block" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'exp_trials'
    
    thisExp.nextEntry()
    
# completed 1 repeats of 'experimental_block'


# set up handler to look after randomisation of conditions etc
control_block = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='control_block')
thisExp.addLoop(control_block)  # add the loop to the experiment
thisControl_block = control_block.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisControl_block.rgb)
if thisControl_block != None:
    for paramName in thisControl_block:
        exec('{} = thisControl_block[paramName]'.format(paramName))

for thisControl_block in control_block:
    currentLoop = control_block
    # abbreviate parameter names if possible (e.g. rgb = thisControl_block.rgb)
    if thisControl_block != None:
        for paramName in thisControl_block:
            exec('{} = thisControl_block[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    ctrl_trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('Stimuli_ctrl_cond.xlsx', selection=trial_nr_ctrl),
        seed=None, name='ctrl_trials')
    thisExp.addLoop(ctrl_trials)  # add the loop to the experiment
    thisCtrl_trial = ctrl_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisCtrl_trial.rgb)
    if thisCtrl_trial != None:
        for paramName in thisCtrl_trial:
            exec('{} = thisCtrl_trial[paramName]'.format(paramName))
    
    for thisCtrl_trial in ctrl_trials:
        currentLoop = ctrl_trials
        # abbreviate parameter names if possible (e.g. rgb = thisCtrl_trial.rgb)
        if thisCtrl_trial != None:
            for paramName in thisCtrl_trial:
                exec('{} = thisCtrl_trial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "signal_check_2"-------
        continueRoutine = True
        # update component parameters for each repeat
        # set EEG marker for calibration
        if use_lpt:
            port.setData(93)
        
        # Set default values
        count_frames = 0
        disp = 0
        
        #trigger1 = time.time() # get timestamp as seconds
        #trigger2 = 0
        
        
        # Define the subset of stimuli to play depending on block 1 or block 2:
        # block 1: Trials 1 to 70
        # block 2: Trials 71 to 140
        # The last entry of the slice is not being included, so the last included will be (nTrials_half - 1).
        # This is what we need because we want it to be (nTrials_half-1) because of the Python indexing starting from 0
        trial_nr_ctrl = slice(0, nTrials_half) 
        if nCtrlBlock == 2:
            trial_nr_ctrl = slice(nTrials_half, nTrials) 
        
        #print(nCtrlBlock, nCtrlTrials, trial_nr_ctrl)
        
        # Define the current task to play: NV speech or SiN
        NV = []
        SiN = []
        if order_task_trial[nCtrlTrials] == 0:
            NV = 1
            SiN = 0
        else: 
            NV = 0
            SiN = 1
            
            
            
        # need to move parts from digits_played to here to start preparing things!
        # In this routine, the triplets are presented once the threshold
        # was reached in the previous routine. If NV speech or SiN is presented
        # depends on the random trial order defined in startup.
        # Maybe we could find a way to buffer the audio files in order to decrease the
        # delay.
        
        # Randomly choose one speaker for the current trial
        rand_speaker = np.random.choice(speaker, size = 1)
        rand_speaker = int(rand_speaker[0])
        #print(rand_speaker)
        
        # Defining the current digits
        firstdigit = int(NFB_digit1)
        seconddigit = int(NFB_digit2)
        thirddigit = int(NFB_digit3)
        
        if NV == 1 and SiN == 0:
            
            # Stop the background noise: For NV speech, we don't want any background noise
            # during stimulus presentation
            #sound_noise.stop()
            
            # Playing the first digit
            if firstdigit < 8:
                digit1 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(firstdigit)+'_'+str(noise[firstdigit])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit1 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(firstdigit)+'_'+str(noise[firstdigit-1])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
        
            # Playing the second digit
            if seconddigit < 8:
                digit2 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(seconddigit)+'_'+str(noise[seconddigit])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit2 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(seconddigit)+'_'+str(noise[seconddigit-1])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
        
            # Playing the third digit
            if thirddigit < 8:
                digit3 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(thirddigit)+'_'+str(noise[thirddigit])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit3 = 'NVS_Speaker_'+str(rand_speaker)+'_digit_'+str(thirddigit)+'_'+str(noise[thirddigit-1])+'_envExtDepPt.wav_48kHz_filtered_mono.wav'
        
        
        elif NV == 0 and SiN == 1:
            
            # Playing the first digit
            if firstdigit < 8:
                digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit1 = 'Speaker'+str(rand_speaker)+'_Digit'+str(firstdigit)+'_48kHz_filtered_mono.wav'
        
            # Playing the second digit
            if seconddigit < 8:
                digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit2 = 'Speaker'+str(rand_speaker)+'_Digit'+str(seconddigit)+'_48kHz_filtered_mono.wav'
        
            # Playing the third digit
            if thirddigit < 8:
                digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_48kHz_filtered_mono.wav'
            else: # here we have to change the index since there is no 7 in the stimuli
                digit3 = 'Speaker'+str(rand_speaker)+'_Digit'+str(thirddigit)+'_48kHz_filtered_mono.wav'
        
        
        
        
        
        
        # shall we try to prepare sounds here?
        sound_digit1_2 = sound.Sound(digit1, preBuffer= -1)
        sound_digit2_2 = sound.Sound(digit2, preBuffer= -1)
        sound_digit3_2 = sound.Sound(digit3, preBuffer= -1)
        
        # Start playing background noise
        sound_noise.play()
        # keep track of which components have finished
        signal_check_2Components = [Fixation_2]
        for thisComponent in signal_check_2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        signal_check_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "signal_check_2"-------
        while continueRoutine:
            # get current time
            t = signal_check_2Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=signal_check_2Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # actualize count of frame
            count_frames += 1
            
            # pull chunks from the previously resolved EEG stream (see startup)
            chunk, timestamps = inlet_EEG.pull_chunk()
            chunks_frame = [i[0:32] for i in chunk] # select the 32 elecs of interest
                
            # processing the incoming signal to build the ratio
            if chunks_frame:
                signal = chunks_frame
                # just select the elecs of interest and average them
                blue_elecs = np.average([signal[0][Fz], signal[0][F8], signal[0][FT10], signal[0][O1]])
                red_elecs = np.average([signal[0][C3], signal[0][CP1]])
                ratio_elecs = red_elecs - blue_elecs
                sys.stdout = dataControl_file # open file for saving ratios during control triggering
                #print("SignalCheck2")
                print(timestamps, ratio_elecs)
            
            # dont use the current ratios and just stop the current routine when the replay of ITI is over
            if count_frames > len(signal_trials[nCtrlTrials]):
                sys.stdout = sys.__stdout__ # close control triggering file
                #trigger2 = time.time()
                continueRoutine = False
            
            
            
            # *Fixation_2* updates
            if Fixation_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fixation_2.frameNStart = frameN  # exact frame index
                Fixation_2.tStart = t  # local t and not account for scr refresh
                Fixation_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fixation_2, 'tStartRefresh')  # time at next scr refresh
                Fixation_2.setAutoDraw(True)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in signal_check_2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "signal_check_2"-------
        for thisComponent in signal_check_2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        #sys.stdout = MarkerControl
        #print(trigger1, trigger2)
        #sys.stdout = sys.__stdout__
        
        
        ctrl_trials.addData('Fixation_2.started', Fixation_2.tStartRefresh)
        ctrl_trials.addData('Fixation_2.stopped', Fixation_2.tStopRefresh)
        # the Routine "signal_check_2" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "digits_played_2"-------
        continueRoutine = True
        # update component parameters for each repeat
        # In this routine, the triplets are presented once the threshold
        # was reached in the previous routine. If NV speech or SiN is presented
        # depends on the random trial order defined in startup.
        # Maybe we could find a way to buffer the audio files in order to decrease the
        # delay.
        
        # now we only play stimuli here, nothing else
        # first we send triggers with lpt, should not take long,
        # then play digits, should be more precise
        
        if NV == 1 and SiN == 0:
            
            # Stop the background noise: For NV speech, we don't want any background noise
            # during stimulus presentation
            sound_noise.stop()
        sound_digit1_2.setSound(digit1, hamming=True)
        sound_digit1_2.setVolume(1.0, log=False)
        sound_digit2_2.setSound(digit2, hamming=True)
        sound_digit2_2.setVolume(1.0, log=False)
        sound_digit3_2.setSound(digit3, hamming=True)
        sound_digit3_2.setVolume(1.0, log=False)
        # keep track of which components have finished
        digits_played_2Components = [sound_digit1_2, sound_digit2_2, sound_digit3_2]
        for thisComponent in digits_played_2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        digits_played_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "digits_played_2"-------
        while continueRoutine:
            # get current time
            t = digits_played_2Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=digits_played_2Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if use_lpt:
                if sound_digit1_2.status == STARTED:
                    ported.setData(13)
                elif sound_digit2_2.status == STARTED:
                    ported.setData(23)
                elif sound_digit3_2.status == STARTED:
                    ported.setData(33)
            # start/stop sound_digit1_2
            if sound_digit1_2.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                sound_digit1_2.frameNStart = frameN  # exact frame index
                sound_digit1_2.tStart = t  # local t and not account for scr refresh
                sound_digit1_2.tStartRefresh = tThisFlipGlobal  # on global time
                sound_digit1_2.play()  # start the sound (it finishes automatically)
            # start/stop sound_digit2_2
            if sound_digit2_2.status == NOT_STARTED and sound_digit1_2.status == FINISHED:
                # keep track of start time/frame for later
                sound_digit2_2.frameNStart = frameN  # exact frame index
                sound_digit2_2.tStart = t  # local t and not account for scr refresh
                sound_digit2_2.tStartRefresh = tThisFlipGlobal  # on global time
                sound_digit2_2.play()  # start the sound (it finishes automatically)
            # start/stop sound_digit3_2
            if sound_digit3_2.status == NOT_STARTED and sound_digit2_2.status == FINISHED:
                # keep track of start time/frame for later
                sound_digit3_2.frameNStart = frameN  # exact frame index
                sound_digit3_2.tStart = t  # local t and not account for scr refresh
                sound_digit3_2.tStartRefresh = tThisFlipGlobal  # on global time
                sound_digit3_2.play()  # start the sound (it finishes automatically)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in digits_played_2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "digits_played_2"-------
        for thisComponent in digits_played_2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        #if NV == 1 and SiN == 0:
        #    # Start replaying background noise because it was stopped in the NV speech task
        #    sound_noise.play()
        sound_digit1_2.stop()  # ensure sound has stopped at end of routine
        ctrl_trials.addData('sound_digit1_2.started', sound_digit1_2.tStart)
        ctrl_trials.addData('sound_digit1_2.stopped', sound_digit1_2.tStop)
        sound_digit2_2.stop()  # ensure sound has stopped at end of routine
        ctrl_trials.addData('sound_digit2_2.started', sound_digit2_2.tStart)
        ctrl_trials.addData('sound_digit2_2.stopped', sound_digit2_2.tStop)
        sound_digit3_2.stop()  # ensure sound has stopped at end of routine
        ctrl_trials.addData('sound_digit3_2.started', sound_digit3_2.tStart)
        ctrl_trials.addData('sound_digit3_2.stopped', sound_digit3_2.tStop)
        # the Routine "digits_played_2" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        response_ctrl = data.TrialHandler(nReps=nDigits, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='response_ctrl')
        thisExp.addLoop(response_ctrl)  # add the loop to the experiment
        thisResponse_ctrl = response_ctrl.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisResponse_ctrl.rgb)
        if thisResponse_ctrl != None:
            for paramName in thisResponse_ctrl:
                exec('{} = thisResponse_ctrl[paramName]'.format(paramName))
        
        for thisResponse_ctrl in response_ctrl:
            currentLoop = response_ctrl
            # abbreviate parameter names if possible (e.g. rgb = thisResponse_ctrl.rgb)
            if thisResponse_ctrl != None:
                for paramName in thisResponse_ctrl:
                    exec('{} = thisResponse_ctrl[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "Response_subjects_2"-------
            continueRoutine = True
            # update component parameters for each repeat
            count = 0
            response2 = ''
            keyPress2 = []
            response_string2 = []
            key_resp_2.keys = []
            key_resp_2.rt = []
            _key_resp_2_allKeys = []
            # keep track of which components have finished
            Response_subjects_2Components = [key_resp_2, disp_answer_2]
            for thisComponent in Response_subjects_2Components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            Response_subjects_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Response_subjects_2"-------
            while continueRoutine:
                # get current time
                t = Response_subjects_2Clock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=Response_subjects_2Clock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # Collect every pressed key
                keyPress2 = event.getKeys(keyList=['num_1','num_2','num_3','num_4','num_5','num_6', 'num_7', 'num_8','num_9','num_0', 'return'])
                # Gather the pressed key in a string vector
                response_string2 = "".join(key_resp_2.keys).replace('num_', '') 
                
                if response_string2: # if response_string is not empty:
                    response2 = response_string2[-1] # disp the last pressed key
                
                response_text_ctrl = "Gehörte Ziffer {}".format(response2)
                
                if "return" in keyPress2: # if "enter" key pressed
                    continueRoutine = False # pass to the next iteration
                
                        
                
                
                # *key_resp_2* updates
                waitOnFlip = False
                if key_resp_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp_2.frameNStart = frameN  # exact frame index
                    key_resp_2.tStart = t  # local t and not account for scr refresh
                    key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
                    key_resp_2.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp_2.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp_2.getKeys(keyList=['num_0', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9', 'return'], waitRelease=False)
                    _key_resp_2_allKeys.extend(theseKeys)
                    if len(_key_resp_2_allKeys):
                        key_resp_2.keys = [key.name for key in _key_resp_2_allKeys]  # storing all keys
                        key_resp_2.rt = [key.rt for key in _key_resp_2_allKeys]
                
                # *disp_answer_2* updates
                if disp_answer_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    disp_answer_2.frameNStart = frameN  # exact frame index
                    disp_answer_2.tStart = t  # local t and not account for scr refresh
                    disp_answer_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(disp_answer_2, 'tStartRefresh')  # time at next scr refresh
                    disp_answer_2.setAutoDraw(True)
                if disp_answer_2.status == STARTED:  # only update if drawing
                    disp_answer_2.setText(response_text_ctrl, log=False)
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Response_subjects_2Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Response_subjects_2"-------
            for thisComponent in Response_subjects_2Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # set EEG marker after each digit response 
            if use_lpt:
                if response_ctrl.thisN == 0:
                    port.setData(43)
                elif response_ctrl.thisN == 1:
                    port.setData(53)
                elif response_ctrl.thisN == 2:
                    port.setData(63)
            # check responses
            if key_resp_2.keys in ['', [], None]:  # No response was made
                key_resp_2.keys = None
            response_ctrl.addData('key_resp_2.keys',key_resp_2.keys)
            if key_resp_2.keys != None:  # we had a response
                response_ctrl.addData('key_resp_2.rt', key_resp_2.rt)
            response_ctrl.addData('key_resp_2.started', key_resp_2.tStartRefresh)
            response_ctrl.addData('key_resp_2.stopped', key_resp_2.tStopRefresh)
            # the Routine "Response_subjects_2" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed nDigits repeats of 'response_ctrl'
        
        
        # ------Prepare to start Routine "Next_Block_2"-------
        continueRoutine = True
        # update component parameters for each repeat
        # At the end of the third block, there is a text saying that there is a break.
        # at the end of the fourth block, there is a text saying that the experiment is finished
        # The subject can press "enter" whenever he is ready to go on
        
        begin_Controlblock = []
        
        # changing / displaying the instruction depending on the current block finishe
        instructions_next_block = ' '
        # if it is the last trial of the first block
        if nCtrlBlock == 1 and nCtrlTrials == (nTrials_half-1):
            sound_noise.stop() # Stop the background noise
            instructions_next_block = '''Du hast den dritten Block geschafft, Glückwunsch! 
            
            Sobald Du bereit bist, um den nächsten Block zu starten, kannst Du auf "Enter" drücken.
            
            Weiterhin gilt: Während das Fixationskreuz sichtbar ist, bewege Dich bitte nicht.'''
            
        # if it is the last trial of the second block
        elif nCtrlBlock == 2 and nCtrlTrials == (nTrials-1):
            sound_noise.stop() # Stop the background noise
            instructions_next_block = '''Das Experiment ist nun zu Ende. Vielen Dank für Deine Teilnahme!'''
            #print(signal_trials)
        # if other trial
        else:
            continueRoutine = False
        Begin_4.setText(instructions_next_block)
        # keep track of which components have finished
        Next_Block_2Components = [Begin_4]
        for thisComponent in Next_Block_2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        Next_Block_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Next_Block_2"-------
        while continueRoutine:
            # get current time
            t = Next_Block_2Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=Next_Block_2Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Get the pressed key of the subject
            begin_Controlblock = event.getKeys(keyList=['return'])
            
            # Begin experiment once the subject pressed enter
            if "return" in begin_Controlblock:
                continueRoutine = False # wait for the subject to press the key "enter"
            
            # *Begin_4* updates
            if Begin_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Begin_4.frameNStart = frameN  # exact frame index
                Begin_4.tStart = t  # local t and not account for scr refresh
                Begin_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Begin_4, 'tStartRefresh')  # time at next scr refresh
                Begin_4.setAutoDraw(True)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Next_Block_2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Next_Block_2"-------
        for thisComponent in Next_Block_2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # set EEG marker for each instruction (after 1st and 2nd block are finished) 
        if use_lpt:
            if nCtrlTrials == (nTrials_half-1):
                port.setData(233)
            elif nCtrlTrials == (nTrials-1):
                port.setData(243)
        
        # Start playing background noise
        sound_noise.play()
        
        #print(signal_trials)
        
        # Update Trial counter
        nCtrlTrials += 1
        if nCtrlTrials == nTrials_half:
            nCtrlBlock += 1
        ctrl_trials.addData('Begin_4.started', Begin_4.tStartRefresh)
        ctrl_trials.addData('Begin_4.stopped', Begin_4.tStopRefresh)
        # the Routine "Next_Block_2" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'ctrl_trials'
    
    thisExp.nextEntry()
    
# completed 1 repeats of 'control_block'


# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
