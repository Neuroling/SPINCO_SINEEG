#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on January 18, 2023, at 14:47
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
expName = 'MA_Theta_Exp'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'order': '',
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
    originPath='V:\\gfraga\\scripts_neulin\\Projects\\SINEEG\\Experiments\\SiN\\PsychoPy\\TESTEANDO.py',
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
    size=[2560, 1440], fullscr=True, screen=1, 
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

# --- Initialize components for Routine "instrTraining" ---
instrTrainText = visual.TextStim(win=win, name='instrTrainText',
    text='Jetzt hast du zuerst die Möglichkeit, die Aufgabe zu üben.\n\nSchau bitte in die Mitte des Bildschirms, wo ein Kreis zu sehen sein wird. \nBei einigen Sätzen wird der Kreis pulsieren.\n\nHöre bitte den Satz und versuche, zu verstehen, welche drei Wörter da vorkommen.\n\nJeder Satz hat dieselbe Struktur:\n\n        Vorsicht *Adler*, gang sofort zum *gäle* Fäld vo de Spalte *eis*. \n\nNach jedem Satz solltest du anklicken, welche drei Wörter du rausgehört hast. \nDafür klickst du auf die entsprechenden Bilder.\n\nDrücke bitte die Leertaste, um zu beginnen.',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=1.5, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_2 = keyboard.Keyboard()
# Run 'Begin Experiment' code from getOrder
firstHalf = "flow/orders/order%sA.csv" % expInfo['order']
secondHalf = "flow/orders/order%sB.csv" % expInfo['order']

# --- Initialize components for Routine "audioTrial" ---
sound_1 = sound.Sound('A', secs=-1, stereo=True, hamming=True,
    name='sound_1')
sound_1.setVolume(1.0)
screenAfterAudio = visual.ImageStim(
    win=win,
    name='screenAfterAudio', 
    image='images/gelb.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)

# --- Initialize components for Routine "trial" ---
# Run 'Begin Experiment' code from mapStimuliLabels
# Mappings for stimuli properties
mapCallSign = {
  "call1": "Ad",
  "call2": "Dr",
  "call3": "Ti",
  "call4": "Un"
  }
  
mapColour = {
  "colour1": "Ge",
  "colour2": "Gr",
  "colour3": "Ro",
  "colour4": "We"
  }
  
mapNumber = {
  "number1": 1,
  "number2": 2,
  "number3": 3,
  "number4": 4
  }
blankScreen = visual.ImageStim(
    win=win,
    name='blankScreen', 
    image='images/blankScreen.png', mask=None, anchor='center',
    ori=0, pos=(0, 0), size=[1920, 1080],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
call1 = visual.ImageStim(
    win=win,
    name='call1', 
    image='images/adler.png', mask=None, anchor='center',
    ori=0, pos=(-0.4, 0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
call2 = visual.ImageStim(
    win=win,
    name='call2', 
    image='images/unke.png', mask=None, anchor='center',
    ori=0, pos=(-0.4, .10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-6.0)
call3 = visual.ImageStim(
    win=win,
    name='call3', 
    image='images/drossel.png', mask=None, anchor='center',
    ori=0, pos=(-0.4, -.10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-7.0)
call4 = visual.ImageStim(
    win=win,
    name='call4', 
    image='sin', mask=None, anchor='center',
    ori=0, pos=(-0.4, -0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-8.0)
colour1 = visual.ImageStim(
    win=win,
    name='colour1', 
    image='images/gelb.png', mask=None, anchor='center',
    ori=0, pos=(0.0, 0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-9.0)
colour2 = visual.ImageStim(
    win=win,
    name='colour2', 
    image='images/rot.png', mask=None, anchor='center',
    ori=0, pos=(0.0, .10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-10.0)
colour3 = visual.ImageStim(
    win=win,
    name='colour3', 
    image='images/weiss.png', mask=None, anchor='center',
    ori=0, pos=(0.0, -.10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-11.0)
colour4 = visual.ImageStim(
    win=win,
    name='colour4', 
    image='images/gruen.png', mask=None, anchor='center',
    ori=0, pos=(0.0, -0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-12.0)
number1 = visual.ImageStim(
    win=win,
    name='number1', 
    image='images/1.png', mask=None, anchor='center',
    ori=0, pos=(0.4, 0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-13.0)
number2 = visual.ImageStim(
    win=win,
    name='number2', 
    image='images/2.png', mask=None, anchor='center',
    ori=0, pos=(0.4, .10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-14.0)
number3 = visual.ImageStim(
    win=win,
    name='number3', 
    image='images/3.png', mask=None, anchor='center',
    ori=0, pos=(0.4, -.10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-15.0)
number4 = visual.ImageStim(
    win=win,
    name='number4', 
    image='images/4.png', mask=None, anchor='center',
    ori=0, pos=(0.4, -0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-16.0)
mouseClickOnCall = event.Mouse(win=win)
x, y = [None, None]
mouseClickOnCall.mouseClock = core.Clock()
mouseClickOnColour = event.Mouse(win=win)
x, y = [None, None]
mouseClickOnColour.mouseClock = core.Clock()
mouseClickOnNumber = event.Mouse(win=win)
x, y = [None, None]
mouseClickOnNumber.mouseClock = core.Clock()
blankScreenAfterResponse = visual.ImageStim(
    win=win,
    name='blankScreenAfterResponse', 
    image='images/blankScreen.png', mask=None, anchor='center',
    ori=0, pos=(0, 0), size=[1920, 1080],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-25.0)

# --- Initialize components for Routine "instrExperiment" ---
instrExpText = visual.TextStim(win=win, name='instrExpText',
    text='Wir fangen nun mit dem Experiment an.\n\nSchau bitte in die Mitte des Bildschirms während du die Sätze anhörst.\n\nNach jedem Satz solltest du auf die entsprechenden Bilder klicken.\n\nDrücke bitte die Leertaste, um zu beginnen.',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_3 = keyboard.Keyboard()

# --- Initialize components for Routine "trial" ---
# Run 'Begin Experiment' code from mapStimuliLabels
# Mappings for stimuli properties
mapCallSign = {
  "call1": "Ad",
  "call2": "Dr",
  "call3": "Ti",
  "call4": "Un"
  }
  
mapColour = {
  "colour1": "Ge",
  "colour2": "Gr",
  "colour3": "Ro",
  "colour4": "We"
  }
  
mapNumber = {
  "number1": 1,
  "number2": 2,
  "number3": 3,
  "number4": 4
  }
blankScreen = visual.ImageStim(
    win=win,
    name='blankScreen', 
    image='images/blankScreen.png', mask=None, anchor='center',
    ori=0, pos=(0, 0), size=[1920, 1080],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
call1 = visual.ImageStim(
    win=win,
    name='call1', 
    image='images/adler.png', mask=None, anchor='center',
    ori=0, pos=(-0.4, 0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
call2 = visual.ImageStim(
    win=win,
    name='call2', 
    image='images/unke.png', mask=None, anchor='center',
    ori=0, pos=(-0.4, .10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-6.0)
call3 = visual.ImageStim(
    win=win,
    name='call3', 
    image='images/drossel.png', mask=None, anchor='center',
    ori=0, pos=(-0.4, -.10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-7.0)
call4 = visual.ImageStim(
    win=win,
    name='call4', 
    image='sin', mask=None, anchor='center',
    ori=0, pos=(-0.4, -0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-8.0)
colour1 = visual.ImageStim(
    win=win,
    name='colour1', 
    image='images/gelb.png', mask=None, anchor='center',
    ori=0, pos=(0.0, 0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-9.0)
colour2 = visual.ImageStim(
    win=win,
    name='colour2', 
    image='images/rot.png', mask=None, anchor='center',
    ori=0, pos=(0.0, .10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-10.0)
colour3 = visual.ImageStim(
    win=win,
    name='colour3', 
    image='images/weiss.png', mask=None, anchor='center',
    ori=0, pos=(0.0, -.10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-11.0)
colour4 = visual.ImageStim(
    win=win,
    name='colour4', 
    image='images/gruen.png', mask=None, anchor='center',
    ori=0, pos=(0.0, -0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-12.0)
number1 = visual.ImageStim(
    win=win,
    name='number1', 
    image='images/1.png', mask=None, anchor='center',
    ori=0, pos=(0.4, 0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-13.0)
number2 = visual.ImageStim(
    win=win,
    name='number2', 
    image='images/2.png', mask=None, anchor='center',
    ori=0, pos=(0.4, .10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-14.0)
number3 = visual.ImageStim(
    win=win,
    name='number3', 
    image='images/3.png', mask=None, anchor='center',
    ori=0, pos=(0.4, -.10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-15.0)
number4 = visual.ImageStim(
    win=win,
    name='number4', 
    image='images/4.png', mask=None, anchor='center',
    ori=0, pos=(0.4, -0.3125), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-16.0)
mouseClickOnCall = event.Mouse(win=win)
x, y = [None, None]
mouseClickOnCall.mouseClock = core.Clock()
mouseClickOnColour = event.Mouse(win=win)
x, y = [None, None]
mouseClickOnColour.mouseClock = core.Clock()
mouseClickOnNumber = event.Mouse(win=win)
x, y = [None, None]
mouseClickOnNumber.mouseClock = core.Clock()
blankScreenAfterResponse = visual.ImageStim(
    win=win,
    name='blankScreenAfterResponse', 
    image='images/blankScreen.png', mask=None, anchor='center',
    ori=0, pos=(0, 0), size=[1920, 1080],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-25.0)

# --- Initialize components for Routine "thanks" ---
thanksText = visual.TextStim(win=win, name='thanksText',
    text="That's all folks!\n\nVielen Dank für deine Teilnahme an unserer Studie und deinen wichtigen Beitrag zu Sprachverarbeitung.\n",
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_5 = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "instrTraining" ---
continueRoutine = True
# update component parameters for each repeat
key_resp_2.keys = []
key_resp_2.rt = []
_key_resp_2_allKeys = []
# Run 'Begin Routine' code from hideMouse
win.mouseVisible = False 
# keep track of which components have finished
instrTrainingComponents = [instrTrainText, key_resp_2]
for thisComponent in instrTrainingComponents:
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

# --- Run Routine "instrTraining" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrTrainText* updates
    if instrTrainText.status == NOT_STARTED and frameN >= 0:
        # keep track of start time/frame for later
        instrTrainText.frameNStart = frameN  # exact frame index
        instrTrainText.tStart = t  # local t and not account for scr refresh
        instrTrainText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instrTrainText, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'instrTrainText.started')
        instrTrainText.setAutoDraw(True)
    
    # *key_resp_2* updates
    waitOnFlip = False
    if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.tStart = t  # local t and not account for scr refresh
        key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp_2.started')
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_2.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_2.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_2_allKeys.extend(theseKeys)
        if len(_key_resp_2_allKeys):
            key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
            key_resp_2.rt = _key_resp_2_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrTrainingComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "instrTraining" ---
for thisComponent in instrTrainingComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instrTraining" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
training = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('stimList.xlsx'),
    seed=None, name='training')
thisExp.addLoop(training)  # add the loop to the experiment
thisTraining = training.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTraining.rgb)
if thisTraining != None:
    for paramName in thisTraining:
        exec('{} = thisTraining[paramName]'.format(paramName))

for thisTraining in training:
    currentLoop = training
    # abbreviate parameter names if possible (e.g. rgb = thisTraining.rgb)
    if thisTraining != None:
        for paramName in thisTraining:
            exec('{} = thisTraining[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "audioTrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    sound_1.setSound(audioFile, hamming=True)
    sound_1.setVolume(1.0, log=False)
    # keep track of which components have finished
    audioTrialComponents = [sound_1, screenAfterAudio]
    for thisComponent in audioTrialComponents:
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
    
    # --- Run Routine "audioTrial" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # start/stop sound_1
        if sound_1.status == NOT_STARTED and frameN >= 0.0:
            # keep track of start time/frame for later
            sound_1.frameNStart = frameN  # exact frame index
            sound_1.tStart = t  # local t and not account for scr refresh
            sound_1.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('sound_1.started', tThisFlipGlobal)
            sound_1.play(when=win)  # sync with win flip
        
        # *screenAfterAudio* updates
        if screenAfterAudio.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            screenAfterAudio.frameNStart = frameN  # exact frame index
            screenAfterAudio.tStart = t  # local t and not account for scr refresh
            screenAfterAudio.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(screenAfterAudio, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'screenAfterAudio.started')
            screenAfterAudio.setAutoDraw(True)
        if screenAfterAudio.status == STARTED:
            if bool(sound_1.status==FINISHED):
                # keep track of stop time/frame for later
                screenAfterAudio.tStop = t  # not accounting for scr refresh
                screenAfterAudio.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'screenAfterAudio.stopped')
                screenAfterAudio.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in audioTrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "audioTrial" ---
    for thisComponent in audioTrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    sound_1.stop()  # ensure sound has stopped at end of routine
    # the Routine "audioTrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "trial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from setOpacityAndHideMouse
    #set opacity of response buttons to 1 (fully visible)
    call1.opacity = 1
    call2.opacity = 1
    call3.opacity = 1
    call4.opacity = 1
    
    colour1.opacity = 1
    colour2.opacity = 1
    colour3.opacity = 1
    colour4.opacity = 1
    
    number1.opacity = 1
    number2.opacity = 1
    number3.opacity = 1
    number4.opacity = 1
    # Run 'Begin Routine' code from switchToNextTrialAfterResponseTimeOver
    participantResponseTime = None
    # Run 'Begin Routine' code from printoutCorrectAnswersForDebugging
    print("%s, %s, %s" % (callSign,colour,number))
    call4.setImage(call4)
    # setup some python lists for storing info about the mouseClickOnCall
    mouseClickOnCall.x = []
    mouseClickOnCall.y = []
    mouseClickOnCall.leftButton = []
    mouseClickOnCall.midButton = []
    mouseClickOnCall.rightButton = []
    mouseClickOnCall.time = []
    mouseClickOnCall.clicked_name = []
    gotValidClick = False  # until a click is received
    mouseClickOnCall.mouseClock.reset()
    # setup some python lists for storing info about the mouseClickOnColour
    mouseClickOnColour.x = []
    mouseClickOnColour.y = []
    mouseClickOnColour.leftButton = []
    mouseClickOnColour.midButton = []
    mouseClickOnColour.rightButton = []
    mouseClickOnColour.time = []
    mouseClickOnColour.clicked_name = []
    gotValidClick = False  # until a click is received
    mouseClickOnColour.mouseClock.reset()
    # setup some python lists for storing info about the mouseClickOnNumber
    mouseClickOnNumber.x = []
    mouseClickOnNumber.y = []
    mouseClickOnNumber.leftButton = []
    mouseClickOnNumber.midButton = []
    mouseClickOnNumber.rightButton = []
    mouseClickOnNumber.time = []
    mouseClickOnNumber.clicked_name = []
    gotValidClick = False  # until a click is received
    mouseClickOnNumber.mouseClock.reset()
    # keep track of which components have finished
    trialComponents = [blankScreen, call1, call2, call3, call4, colour1, colour2, colour3, colour4, number1, number2, number3, number4, mouseClickOnCall, mouseClickOnColour, mouseClickOnNumber, blankScreenAfterResponse]
    for thisComponent in trialComponents:
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
    
    # --- Run Routine "trial" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from setOpacityAndHideMouse
        
        #show mouse cursor only at the response screen
        win.mouseVisible = False 
        if call1.status == STARTED:
            win.mouseVisible = True
        
        # Run 'Each Frame' code from switchToNextTrialAfterResponseTimeOver
        if participantResponseTime == None and screenAfterAudio.status == FINISHED:
            participantResponseTime = trialClock.getTime()
            
        #switch to the next trial when the video is ended and response time (10 seconds) is over 
        #if participantResponseTime and trialClock.getTime() - participantResponseTime > 10 and not blankScreenAfterResponse.status == STARTED:
        #    continueRoutine = False
        
        # *blankScreen* updates
        if blankScreen.status == NOT_STARTED and screenAfterAudio.status==FINISHED:
            # keep track of start time/frame for later
            blankScreen.frameNStart = frameN  # exact frame index
            blankScreen.tStart = t  # local t and not account for scr refresh
            blankScreen.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(blankScreen, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'blankScreen.started')
            blankScreen.setAutoDraw(True)
        if blankScreen.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > blankScreen.tStartRefresh + 4.0-frameTolerance:
                # keep track of stop time/frame for later
                blankScreen.tStop = t  # not accounting for scr refresh
                blankScreen.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blankScreen.stopped')
                blankScreen.setAutoDraw(False)
        
        # *call1* updates
        if call1.status == NOT_STARTED and blankScreen.status==FINISHED:
            # keep track of start time/frame for later
            call1.frameNStart = frameN  # exact frame index
            call1.tStart = t  # local t and not account for scr refresh
            call1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(call1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'call1.started')
            call1.setAutoDraw(True)
        if call1.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                call1.tStop = t  # not accounting for scr refresh
                call1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'call1.stopped')
                call1.setAutoDraw(False)
        
        # *call2* updates
        if call2.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            call2.frameNStart = frameN  # exact frame index
            call2.tStart = t  # local t and not account for scr refresh
            call2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(call2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'call2.started')
            call2.setAutoDraw(True)
        if call2.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                call2.tStop = t  # not accounting for scr refresh
                call2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'call2.stopped')
                call2.setAutoDraw(False)
        
        # *call3* updates
        if call3.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            call3.frameNStart = frameN  # exact frame index
            call3.tStart = t  # local t and not account for scr refresh
            call3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(call3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'call3.started')
            call3.setAutoDraw(True)
        if call3.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                call3.tStop = t  # not accounting for scr refresh
                call3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'call3.stopped')
                call3.setAutoDraw(False)
        
        # *call4* updates
        if call4.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            call4.frameNStart = frameN  # exact frame index
            call4.tStart = t  # local t and not account for scr refresh
            call4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(call4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'call4.started')
            call4.setAutoDraw(True)
        if call4.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                call4.tStop = t  # not accounting for scr refresh
                call4.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'call4.stopped')
                call4.setAutoDraw(False)
        
        # *colour1* updates
        if colour1.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            colour1.frameNStart = frameN  # exact frame index
            colour1.tStart = t  # local t and not account for scr refresh
            colour1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(colour1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'colour1.started')
            colour1.setAutoDraw(True)
        if colour1.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                colour1.tStop = t  # not accounting for scr refresh
                colour1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colour1.stopped')
                colour1.setAutoDraw(False)
        
        # *colour2* updates
        if colour2.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            colour2.frameNStart = frameN  # exact frame index
            colour2.tStart = t  # local t and not account for scr refresh
            colour2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(colour2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'colour2.started')
            colour2.setAutoDraw(True)
        if colour2.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                colour2.tStop = t  # not accounting for scr refresh
                colour2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colour2.stopped')
                colour2.setAutoDraw(False)
        
        # *colour3* updates
        if colour3.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            colour3.frameNStart = frameN  # exact frame index
            colour3.tStart = t  # local t and not account for scr refresh
            colour3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(colour3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'colour3.started')
            colour3.setAutoDraw(True)
        if colour3.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                colour3.tStop = t  # not accounting for scr refresh
                colour3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colour3.stopped')
                colour3.setAutoDraw(False)
        
        # *colour4* updates
        if colour4.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            colour4.frameNStart = frameN  # exact frame index
            colour4.tStart = t  # local t and not account for scr refresh
            colour4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(colour4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'colour4.started')
            colour4.setAutoDraw(True)
        if colour4.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                colour4.tStop = t  # not accounting for scr refresh
                colour4.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colour4.stopped')
                colour4.setAutoDraw(False)
        
        # *number1* updates
        if number1.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            number1.frameNStart = frameN  # exact frame index
            number1.tStart = t  # local t and not account for scr refresh
            number1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(number1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'number1.started')
            number1.setAutoDraw(True)
        if number1.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                number1.tStop = t  # not accounting for scr refresh
                number1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'number1.stopped')
                number1.setAutoDraw(False)
        
        # *number2* updates
        if number2.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            number2.frameNStart = frameN  # exact frame index
            number2.tStart = t  # local t and not account for scr refresh
            number2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(number2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'number2.started')
            number2.setAutoDraw(True)
        if number2.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                number2.tStop = t  # not accounting for scr refresh
                number2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'number2.stopped')
                number2.setAutoDraw(False)
        
        # *number3* updates
        if number3.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            number3.frameNStart = frameN  # exact frame index
            number3.tStart = t  # local t and not account for scr refresh
            number3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(number3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'number3.started')
            number3.setAutoDraw(True)
        if number3.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                number3.tStop = t  # not accounting for scr refresh
                number3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'number3.stopped')
                number3.setAutoDraw(False)
        
        # *number4* updates
        if number4.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            number4.frameNStart = frameN  # exact frame index
            number4.tStart = t  # local t and not account for scr refresh
            number4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(number4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'number4.started')
            number4.setAutoDraw(True)
        if number4.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                number4.tStop = t  # not accounting for scr refresh
                number4.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'number4.stopped')
                number4.setAutoDraw(False)
        # *mouseClickOnCall* updates
        if mouseClickOnCall.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            mouseClickOnCall.frameNStart = frameN  # exact frame index
            mouseClickOnCall.tStart = t  # local t and not account for scr refresh
            mouseClickOnCall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouseClickOnCall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouseClickOnCall.started', t)
            mouseClickOnCall.status = STARTED
            prevButtonState = mouseClickOnCall.getPressed()  # if button is down already this ISN'T a new click
        if mouseClickOnCall.status == STARTED:  # only update if started and not finished!
            buttons = mouseClickOnCall.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    try:
                        iter([call1, call2, call3, call4])
                        clickableList = [call1, call2, call3, call4]
                    except:
                        clickableList = [[call1, call2, call3, call4]]
                    for obj in clickableList:
                        if obj.contains(mouseClickOnCall):
                            gotValidClick = True
                            mouseClickOnCall.clicked_name.append(obj.name)
                    x, y = mouseClickOnCall.getPos()
                    mouseClickOnCall.x.append(x)
                    mouseClickOnCall.y.append(y)
                    buttons = mouseClickOnCall.getPressed()
                    mouseClickOnCall.leftButton.append(buttons[0])
                    mouseClickOnCall.midButton.append(buttons[1])
                    mouseClickOnCall.rightButton.append(buttons[2])
                    mouseClickOnCall.time.append(mouseClickOnCall.mouseClock.getTime())
                    if gotValidClick:
                        continueRoutine = False  # abort routine on response
        # Run 'Each Frame' code from disableCallButtons
                    if gotValidClick:
                        mouseClickOnCall.status = FINISHED
                        if call1.name != mouseClickOnCall.clicked_name[-1]: call1.opacity = 0.2
                        if call2.name != mouseClickOnCall.clicked_name[-1]: call2.opacity = 0.2
                        if call3.name != mouseClickOnCall.clicked_name[-1]: call3.opacity = 0.2
                        if call4.name != mouseClickOnCall.clicked_name[-1]: call4.opacity = 0.2
                        continueRoutine = True
        # *mouseClickOnColour* updates
        if mouseClickOnColour.status == NOT_STARTED and mouseClickOnCall.status==FINISHED:
            # keep track of start time/frame for later
            mouseClickOnColour.frameNStart = frameN  # exact frame index
            mouseClickOnColour.tStart = t  # local t and not account for scr refresh
            mouseClickOnColour.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouseClickOnColour, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouseClickOnColour.started', t)
            mouseClickOnColour.status = STARTED
            prevButtonState = mouseClickOnColour.getPressed()  # if button is down already this ISN'T a new click
        if mouseClickOnColour.status == STARTED:  # only update if started and not finished!
            buttons = mouseClickOnColour.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    try:
                        iter([colour1, colour2, colour3, colour4])
                        clickableList = [colour1, colour2, colour3, colour4]
                    except:
                        clickableList = [[colour1, colour2, colour3, colour4]]
                    for obj in clickableList:
                        if obj.contains(mouseClickOnColour):
                            gotValidClick = True
                            mouseClickOnColour.clicked_name.append(obj.name)
                    x, y = mouseClickOnColour.getPos()
                    mouseClickOnColour.x.append(x)
                    mouseClickOnColour.y.append(y)
                    buttons = mouseClickOnColour.getPressed()
                    mouseClickOnColour.leftButton.append(buttons[0])
                    mouseClickOnColour.midButton.append(buttons[1])
                    mouseClickOnColour.rightButton.append(buttons[2])
                    mouseClickOnColour.time.append(mouseClickOnColour.mouseClock.getTime())
                    if gotValidClick:
                        continueRoutine = False  # abort routine on response
        # Run 'Each Frame' code from disableColourButtons
                    if gotValidClick:
                        mouseClickOnColour.status = FINISHED
                        if colour1.name != mouseClickOnColour.clicked_name[-1]: colour1.opacity = 0.2
                        if colour2.name != mouseClickOnColour.clicked_name[-1]: colour2.opacity = 0.2
                        if colour3.name != mouseClickOnColour.clicked_name[-1]: colour3.opacity = 0.2
                        if colour4.name != mouseClickOnColour.clicked_name[-1]: colour4.opacity = 0.2
                        continueRoutine = True
        # *mouseClickOnNumber* updates
        if mouseClickOnNumber.status == NOT_STARTED and mouseClickOnColour.status ==FINISHED:
            # keep track of start time/frame for later
            mouseClickOnNumber.frameNStart = frameN  # exact frame index
            mouseClickOnNumber.tStart = t  # local t and not account for scr refresh
            mouseClickOnNumber.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouseClickOnNumber, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouseClickOnNumber.started', t)
            mouseClickOnNumber.status = STARTED
            prevButtonState = mouseClickOnNumber.getPressed()  # if button is down already this ISN'T a new click
        if mouseClickOnNumber.status == STARTED:  # only update if started and not finished!
            buttons = mouseClickOnNumber.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    try:
                        iter([number1, number2, number3, number4])
                        clickableList = [number1, number2, number3, number4]
                    except:
                        clickableList = [[number1, number2, number3, number4]]
                    for obj in clickableList:
                        if obj.contains(mouseClickOnNumber):
                            gotValidClick = True
                            mouseClickOnNumber.clicked_name.append(obj.name)
                    x, y = mouseClickOnNumber.getPos()
                    mouseClickOnNumber.x.append(x)
                    mouseClickOnNumber.y.append(y)
                    buttons = mouseClickOnNumber.getPressed()
                    mouseClickOnNumber.leftButton.append(buttons[0])
                    mouseClickOnNumber.midButton.append(buttons[1])
                    mouseClickOnNumber.rightButton.append(buttons[2])
                    mouseClickOnNumber.time.append(mouseClickOnNumber.mouseClock.getTime())
                    if gotValidClick:
                        continueRoutine = False  # abort routine on response
        # Run 'Each Frame' code from disableNumberButtons
                    if gotValidClick:
                        mouseClickOnNumber.status = FINISHED
                        if number1.name != mouseClickOnNumber.clicked_name[-1]: number1.opacity = 0.2
                        if number2.name != mouseClickOnNumber.clicked_name[-1]: number2.opacity = 0.2
                        if number3.name != mouseClickOnNumber.clicked_name[-1]: number3.opacity = 0.2
                        if number4.name != mouseClickOnNumber.clicked_name[-1]: number4.opacity = 0.2
                        #continueRoutine = True
        
        # *blankScreenAfterResponse* updates
        if blankScreenAfterResponse.status == NOT_STARTED and mouseClickOnNumber.status==FINISHED:
            # keep track of start time/frame for later
            blankScreenAfterResponse.frameNStart = frameN  # exact frame index
            blankScreenAfterResponse.tStart = t  # local t and not account for scr refresh
            blankScreenAfterResponse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(blankScreenAfterResponse, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'blankScreenAfterResponse.started')
            blankScreenAfterResponse.setAutoDraw(True)
        if blankScreenAfterResponse.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > blankScreenAfterResponse.tStartRefresh + 0.6 -frameTolerance:
                # keep track of stop time/frame for later
                blankScreenAfterResponse.tStop = t  # not accounting for scr refresh
                blankScreenAfterResponse.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blankScreenAfterResponse.stopped')
                blankScreenAfterResponse.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "trial" ---
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for training (TrialHandler)
    training.addData('mouseClickOnCall.x', mouseClickOnCall.x)
    training.addData('mouseClickOnCall.y', mouseClickOnCall.y)
    training.addData('mouseClickOnCall.leftButton', mouseClickOnCall.leftButton)
    training.addData('mouseClickOnCall.midButton', mouseClickOnCall.midButton)
    training.addData('mouseClickOnCall.rightButton', mouseClickOnCall.rightButton)
    training.addData('mouseClickOnCall.time', mouseClickOnCall.time)
    training.addData('mouseClickOnCall.clicked_name', mouseClickOnCall.clicked_name)
    # store data for training (TrialHandler)
    training.addData('mouseClickOnColour.x', mouseClickOnColour.x)
    training.addData('mouseClickOnColour.y', mouseClickOnColour.y)
    training.addData('mouseClickOnColour.leftButton', mouseClickOnColour.leftButton)
    training.addData('mouseClickOnColour.midButton', mouseClickOnColour.midButton)
    training.addData('mouseClickOnColour.rightButton', mouseClickOnColour.rightButton)
    training.addData('mouseClickOnColour.time', mouseClickOnColour.time)
    training.addData('mouseClickOnColour.clicked_name', mouseClickOnColour.clicked_name)
    # store data for training (TrialHandler)
    training.addData('mouseClickOnNumber.x', mouseClickOnNumber.x)
    training.addData('mouseClickOnNumber.y', mouseClickOnNumber.y)
    training.addData('mouseClickOnNumber.leftButton', mouseClickOnNumber.leftButton)
    training.addData('mouseClickOnNumber.midButton', mouseClickOnNumber.midButton)
    training.addData('mouseClickOnNumber.rightButton', mouseClickOnNumber.rightButton)
    training.addData('mouseClickOnNumber.time', mouseClickOnNumber.time)
    training.addData('mouseClickOnNumber.clicked_name', mouseClickOnNumber.clicked_name)
    # Run 'End Routine' code from evaluateResponses
    #evaluate correctness of response and write into a new column TRUE, FALSE, or NO_ANSW  
    if len(mouseClickOnCall.clicked_name) > 0:
        currentLoop.addData('callSignCorrect', mapCallSign[mouseClickOnCall.clicked_name[0]] == callSign) 
        print(mapCallSign[mouseClickOnCall.clicked_name[0]])
    else:
        currentLoop.addData('callSignCorrect', "NO_ANSW") 
    if len(mouseClickOnColour.clicked_name) > 0:
        currentLoop.addData('colourCorrect', mapColour[mouseClickOnColour.clicked_name[0]] == colour) 
        print(mapColour[mouseClickOnColour.clicked_name[0]])
    else:
        currentLoop.addData('colourCorrect', "NO_ANSW") 
    if len(mouseClickOnNumber.clicked_name) > 0:
        currentLoop.addData('numberCorrect', mapNumber[mouseClickOnNumber.clicked_name[0]] == number) 
        print(mapNumber[mouseClickOnNumber.clicked_name[0]])
    else:
        currentLoop.addData('numberCorrect', "NO_ANSW") 
    # Run 'End Routine' code from saveAfterEachTrial
    #sicherIstSicher
    #thisExp.saveAsWideText(filename+'.csv')
    #logging.flush()
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'training'

# get names of stimulus parameters
if training.trialList in ([], [None], None):
    params = []
else:
    params = training.trialList[0].keys()
# save data for this loop
training.saveAsExcel(filename + '.xlsx', sheetName='training',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

# --- Prepare to start Routine "instrExperiment" ---
continueRoutine = True
# update component parameters for each repeat
key_resp_3.keys = []
key_resp_3.rt = []
_key_resp_3_allKeys = []
# keep track of which components have finished
instrExperimentComponents = [instrExpText, key_resp_3]
for thisComponent in instrExperimentComponents:
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

# --- Run Routine "instrExperiment" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrExpText* updates
    if instrExpText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instrExpText.frameNStart = frameN  # exact frame index
        instrExpText.tStart = t  # local t and not account for scr refresh
        instrExpText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instrExpText, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'instrExpText.started')
        instrExpText.setAutoDraw(True)
    
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
        theseKeys = key_resp_3.getKeys(keyList=['space'], waitRelease=False)
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
    for thisComponent in instrExperimentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "instrExperiment" ---
for thisComponent in instrExperimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instrExperiment" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
blockA = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(block),
    seed=None, name='blockA')
thisExp.addLoop(blockA)  # add the loop to the experiment
thisBlockA = blockA.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlockA.rgb)
if thisBlockA != None:
    for paramName in thisBlockA:
        exec('{} = thisBlockA[paramName]'.format(paramName))

for thisBlockA in blockA:
    currentLoop = blockA
    # abbreviate parameter names if possible (e.g. rgb = thisBlockA.rgb)
    if thisBlockA != None:
        for paramName in thisBlockA:
            exec('{} = thisBlockA[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "trial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from setOpacityAndHideMouse
    #set opacity of response buttons to 1 (fully visible)
    call1.opacity = 1
    call2.opacity = 1
    call3.opacity = 1
    call4.opacity = 1
    
    colour1.opacity = 1
    colour2.opacity = 1
    colour3.opacity = 1
    colour4.opacity = 1
    
    number1.opacity = 1
    number2.opacity = 1
    number3.opacity = 1
    number4.opacity = 1
    # Run 'Begin Routine' code from switchToNextTrialAfterResponseTimeOver
    participantResponseTime = None
    # Run 'Begin Routine' code from printoutCorrectAnswersForDebugging
    print("%s, %s, %s" % (callSign,colour,number))
    call4.setImage(call4)
    # setup some python lists for storing info about the mouseClickOnCall
    mouseClickOnCall.x = []
    mouseClickOnCall.y = []
    mouseClickOnCall.leftButton = []
    mouseClickOnCall.midButton = []
    mouseClickOnCall.rightButton = []
    mouseClickOnCall.time = []
    mouseClickOnCall.clicked_name = []
    gotValidClick = False  # until a click is received
    mouseClickOnCall.mouseClock.reset()
    # setup some python lists for storing info about the mouseClickOnColour
    mouseClickOnColour.x = []
    mouseClickOnColour.y = []
    mouseClickOnColour.leftButton = []
    mouseClickOnColour.midButton = []
    mouseClickOnColour.rightButton = []
    mouseClickOnColour.time = []
    mouseClickOnColour.clicked_name = []
    gotValidClick = False  # until a click is received
    mouseClickOnColour.mouseClock.reset()
    # setup some python lists for storing info about the mouseClickOnNumber
    mouseClickOnNumber.x = []
    mouseClickOnNumber.y = []
    mouseClickOnNumber.leftButton = []
    mouseClickOnNumber.midButton = []
    mouseClickOnNumber.rightButton = []
    mouseClickOnNumber.time = []
    mouseClickOnNumber.clicked_name = []
    gotValidClick = False  # until a click is received
    mouseClickOnNumber.mouseClock.reset()
    # keep track of which components have finished
    trialComponents = [blankScreen, call1, call2, call3, call4, colour1, colour2, colour3, colour4, number1, number2, number3, number4, mouseClickOnCall, mouseClickOnColour, mouseClickOnNumber, blankScreenAfterResponse]
    for thisComponent in trialComponents:
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
    
    # --- Run Routine "trial" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from setOpacityAndHideMouse
        
        #show mouse cursor only at the response screen
        win.mouseVisible = False 
        if call1.status == STARTED:
            win.mouseVisible = True
        
        # Run 'Each Frame' code from switchToNextTrialAfterResponseTimeOver
        if participantResponseTime == None and screenAfterAudio.status == FINISHED:
            participantResponseTime = trialClock.getTime()
            
        #switch to the next trial when the video is ended and response time (10 seconds) is over 
        #if participantResponseTime and trialClock.getTime() - participantResponseTime > 10 and not blankScreenAfterResponse.status == STARTED:
        #    continueRoutine = False
        
        # *blankScreen* updates
        if blankScreen.status == NOT_STARTED and screenAfterAudio.status==FINISHED:
            # keep track of start time/frame for later
            blankScreen.frameNStart = frameN  # exact frame index
            blankScreen.tStart = t  # local t and not account for scr refresh
            blankScreen.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(blankScreen, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'blankScreen.started')
            blankScreen.setAutoDraw(True)
        if blankScreen.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > blankScreen.tStartRefresh + 4.0-frameTolerance:
                # keep track of stop time/frame for later
                blankScreen.tStop = t  # not accounting for scr refresh
                blankScreen.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blankScreen.stopped')
                blankScreen.setAutoDraw(False)
        
        # *call1* updates
        if call1.status == NOT_STARTED and blankScreen.status==FINISHED:
            # keep track of start time/frame for later
            call1.frameNStart = frameN  # exact frame index
            call1.tStart = t  # local t and not account for scr refresh
            call1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(call1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'call1.started')
            call1.setAutoDraw(True)
        if call1.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                call1.tStop = t  # not accounting for scr refresh
                call1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'call1.stopped')
                call1.setAutoDraw(False)
        
        # *call2* updates
        if call2.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            call2.frameNStart = frameN  # exact frame index
            call2.tStart = t  # local t and not account for scr refresh
            call2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(call2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'call2.started')
            call2.setAutoDraw(True)
        if call2.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                call2.tStop = t  # not accounting for scr refresh
                call2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'call2.stopped')
                call2.setAutoDraw(False)
        
        # *call3* updates
        if call3.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            call3.frameNStart = frameN  # exact frame index
            call3.tStart = t  # local t and not account for scr refresh
            call3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(call3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'call3.started')
            call3.setAutoDraw(True)
        if call3.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                call3.tStop = t  # not accounting for scr refresh
                call3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'call3.stopped')
                call3.setAutoDraw(False)
        
        # *call4* updates
        if call4.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            call4.frameNStart = frameN  # exact frame index
            call4.tStart = t  # local t and not account for scr refresh
            call4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(call4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'call4.started')
            call4.setAutoDraw(True)
        if call4.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                call4.tStop = t  # not accounting for scr refresh
                call4.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'call4.stopped')
                call4.setAutoDraw(False)
        
        # *colour1* updates
        if colour1.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            colour1.frameNStart = frameN  # exact frame index
            colour1.tStart = t  # local t and not account for scr refresh
            colour1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(colour1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'colour1.started')
            colour1.setAutoDraw(True)
        if colour1.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                colour1.tStop = t  # not accounting for scr refresh
                colour1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colour1.stopped')
                colour1.setAutoDraw(False)
        
        # *colour2* updates
        if colour2.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            colour2.frameNStart = frameN  # exact frame index
            colour2.tStart = t  # local t and not account for scr refresh
            colour2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(colour2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'colour2.started')
            colour2.setAutoDraw(True)
        if colour2.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                colour2.tStop = t  # not accounting for scr refresh
                colour2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colour2.stopped')
                colour2.setAutoDraw(False)
        
        # *colour3* updates
        if colour3.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            colour3.frameNStart = frameN  # exact frame index
            colour3.tStart = t  # local t and not account for scr refresh
            colour3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(colour3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'colour3.started')
            colour3.setAutoDraw(True)
        if colour3.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                colour3.tStop = t  # not accounting for scr refresh
                colour3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colour3.stopped')
                colour3.setAutoDraw(False)
        
        # *colour4* updates
        if colour4.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            colour4.frameNStart = frameN  # exact frame index
            colour4.tStart = t  # local t and not account for scr refresh
            colour4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(colour4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'colour4.started')
            colour4.setAutoDraw(True)
        if colour4.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                colour4.tStop = t  # not accounting for scr refresh
                colour4.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colour4.stopped')
                colour4.setAutoDraw(False)
        
        # *number1* updates
        if number1.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            number1.frameNStart = frameN  # exact frame index
            number1.tStart = t  # local t and not account for scr refresh
            number1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(number1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'number1.started')
            number1.setAutoDraw(True)
        if number1.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                number1.tStop = t  # not accounting for scr refresh
                number1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'number1.stopped')
                number1.setAutoDraw(False)
        
        # *number2* updates
        if number2.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            number2.frameNStart = frameN  # exact frame index
            number2.tStart = t  # local t and not account for scr refresh
            number2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(number2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'number2.started')
            number2.setAutoDraw(True)
        if number2.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                number2.tStop = t  # not accounting for scr refresh
                number2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'number2.stopped')
                number2.setAutoDraw(False)
        
        # *number3* updates
        if number3.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            number3.frameNStart = frameN  # exact frame index
            number3.tStart = t  # local t and not account for scr refresh
            number3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(number3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'number3.started')
            number3.setAutoDraw(True)
        if number3.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                number3.tStop = t  # not accounting for scr refresh
                number3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'number3.stopped')
                number3.setAutoDraw(False)
        
        # *number4* updates
        if number4.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            number4.frameNStart = frameN  # exact frame index
            number4.tStart = t  # local t and not account for scr refresh
            number4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(number4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'number4.started')
            number4.setAutoDraw(True)
        if number4.status == STARTED:
            if bool(blankScreenAfterResponse.status == STARTED):
                # keep track of stop time/frame for later
                number4.tStop = t  # not accounting for scr refresh
                number4.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'number4.stopped')
                number4.setAutoDraw(False)
        # *mouseClickOnCall* updates
        if mouseClickOnCall.status == NOT_STARTED and blankScreen.status ==FINISHED:
            # keep track of start time/frame for later
            mouseClickOnCall.frameNStart = frameN  # exact frame index
            mouseClickOnCall.tStart = t  # local t and not account for scr refresh
            mouseClickOnCall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouseClickOnCall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouseClickOnCall.started', t)
            mouseClickOnCall.status = STARTED
            prevButtonState = mouseClickOnCall.getPressed()  # if button is down already this ISN'T a new click
        if mouseClickOnCall.status == STARTED:  # only update if started and not finished!
            buttons = mouseClickOnCall.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    try:
                        iter([call1, call2, call3, call4])
                        clickableList = [call1, call2, call3, call4]
                    except:
                        clickableList = [[call1, call2, call3, call4]]
                    for obj in clickableList:
                        if obj.contains(mouseClickOnCall):
                            gotValidClick = True
                            mouseClickOnCall.clicked_name.append(obj.name)
                    x, y = mouseClickOnCall.getPos()
                    mouseClickOnCall.x.append(x)
                    mouseClickOnCall.y.append(y)
                    buttons = mouseClickOnCall.getPressed()
                    mouseClickOnCall.leftButton.append(buttons[0])
                    mouseClickOnCall.midButton.append(buttons[1])
                    mouseClickOnCall.rightButton.append(buttons[2])
                    mouseClickOnCall.time.append(mouseClickOnCall.mouseClock.getTime())
                    if gotValidClick:
                        continueRoutine = False  # abort routine on response
        # Run 'Each Frame' code from disableCallButtons
                    if gotValidClick:
                        mouseClickOnCall.status = FINISHED
                        if call1.name != mouseClickOnCall.clicked_name[-1]: call1.opacity = 0.2
                        if call2.name != mouseClickOnCall.clicked_name[-1]: call2.opacity = 0.2
                        if call3.name != mouseClickOnCall.clicked_name[-1]: call3.opacity = 0.2
                        if call4.name != mouseClickOnCall.clicked_name[-1]: call4.opacity = 0.2
                        continueRoutine = True
        # *mouseClickOnColour* updates
        if mouseClickOnColour.status == NOT_STARTED and mouseClickOnCall.status==FINISHED:
            # keep track of start time/frame for later
            mouseClickOnColour.frameNStart = frameN  # exact frame index
            mouseClickOnColour.tStart = t  # local t and not account for scr refresh
            mouseClickOnColour.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouseClickOnColour, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouseClickOnColour.started', t)
            mouseClickOnColour.status = STARTED
            prevButtonState = mouseClickOnColour.getPressed()  # if button is down already this ISN'T a new click
        if mouseClickOnColour.status == STARTED:  # only update if started and not finished!
            buttons = mouseClickOnColour.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    try:
                        iter([colour1, colour2, colour3, colour4])
                        clickableList = [colour1, colour2, colour3, colour4]
                    except:
                        clickableList = [[colour1, colour2, colour3, colour4]]
                    for obj in clickableList:
                        if obj.contains(mouseClickOnColour):
                            gotValidClick = True
                            mouseClickOnColour.clicked_name.append(obj.name)
                    x, y = mouseClickOnColour.getPos()
                    mouseClickOnColour.x.append(x)
                    mouseClickOnColour.y.append(y)
                    buttons = mouseClickOnColour.getPressed()
                    mouseClickOnColour.leftButton.append(buttons[0])
                    mouseClickOnColour.midButton.append(buttons[1])
                    mouseClickOnColour.rightButton.append(buttons[2])
                    mouseClickOnColour.time.append(mouseClickOnColour.mouseClock.getTime())
                    if gotValidClick:
                        continueRoutine = False  # abort routine on response
        # Run 'Each Frame' code from disableColourButtons
                    if gotValidClick:
                        mouseClickOnColour.status = FINISHED
                        if colour1.name != mouseClickOnColour.clicked_name[-1]: colour1.opacity = 0.2
                        if colour2.name != mouseClickOnColour.clicked_name[-1]: colour2.opacity = 0.2
                        if colour3.name != mouseClickOnColour.clicked_name[-1]: colour3.opacity = 0.2
                        if colour4.name != mouseClickOnColour.clicked_name[-1]: colour4.opacity = 0.2
                        continueRoutine = True
        # *mouseClickOnNumber* updates
        if mouseClickOnNumber.status == NOT_STARTED and mouseClickOnColour.status ==FINISHED:
            # keep track of start time/frame for later
            mouseClickOnNumber.frameNStart = frameN  # exact frame index
            mouseClickOnNumber.tStart = t  # local t and not account for scr refresh
            mouseClickOnNumber.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouseClickOnNumber, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouseClickOnNumber.started', t)
            mouseClickOnNumber.status = STARTED
            prevButtonState = mouseClickOnNumber.getPressed()  # if button is down already this ISN'T a new click
        if mouseClickOnNumber.status == STARTED:  # only update if started and not finished!
            buttons = mouseClickOnNumber.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    try:
                        iter([number1, number2, number3, number4])
                        clickableList = [number1, number2, number3, number4]
                    except:
                        clickableList = [[number1, number2, number3, number4]]
                    for obj in clickableList:
                        if obj.contains(mouseClickOnNumber):
                            gotValidClick = True
                            mouseClickOnNumber.clicked_name.append(obj.name)
                    x, y = mouseClickOnNumber.getPos()
                    mouseClickOnNumber.x.append(x)
                    mouseClickOnNumber.y.append(y)
                    buttons = mouseClickOnNumber.getPressed()
                    mouseClickOnNumber.leftButton.append(buttons[0])
                    mouseClickOnNumber.midButton.append(buttons[1])
                    mouseClickOnNumber.rightButton.append(buttons[2])
                    mouseClickOnNumber.time.append(mouseClickOnNumber.mouseClock.getTime())
                    if gotValidClick:
                        continueRoutine = False  # abort routine on response
        # Run 'Each Frame' code from disableNumberButtons
                    if gotValidClick:
                        mouseClickOnNumber.status = FINISHED
                        if number1.name != mouseClickOnNumber.clicked_name[-1]: number1.opacity = 0.2
                        if number2.name != mouseClickOnNumber.clicked_name[-1]: number2.opacity = 0.2
                        if number3.name != mouseClickOnNumber.clicked_name[-1]: number3.opacity = 0.2
                        if number4.name != mouseClickOnNumber.clicked_name[-1]: number4.opacity = 0.2
                        #continueRoutine = True
        
        # *blankScreenAfterResponse* updates
        if blankScreenAfterResponse.status == NOT_STARTED and mouseClickOnNumber.status==FINISHED:
            # keep track of start time/frame for later
            blankScreenAfterResponse.frameNStart = frameN  # exact frame index
            blankScreenAfterResponse.tStart = t  # local t and not account for scr refresh
            blankScreenAfterResponse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(blankScreenAfterResponse, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'blankScreenAfterResponse.started')
            blankScreenAfterResponse.setAutoDraw(True)
        if blankScreenAfterResponse.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > blankScreenAfterResponse.tStartRefresh + 0.6 -frameTolerance:
                # keep track of stop time/frame for later
                blankScreenAfterResponse.tStop = t  # not accounting for scr refresh
                blankScreenAfterResponse.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blankScreenAfterResponse.stopped')
                blankScreenAfterResponse.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "trial" ---
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for blockA (TrialHandler)
    blockA.addData('mouseClickOnCall.x', mouseClickOnCall.x)
    blockA.addData('mouseClickOnCall.y', mouseClickOnCall.y)
    blockA.addData('mouseClickOnCall.leftButton', mouseClickOnCall.leftButton)
    blockA.addData('mouseClickOnCall.midButton', mouseClickOnCall.midButton)
    blockA.addData('mouseClickOnCall.rightButton', mouseClickOnCall.rightButton)
    blockA.addData('mouseClickOnCall.time', mouseClickOnCall.time)
    blockA.addData('mouseClickOnCall.clicked_name', mouseClickOnCall.clicked_name)
    # store data for blockA (TrialHandler)
    blockA.addData('mouseClickOnColour.x', mouseClickOnColour.x)
    blockA.addData('mouseClickOnColour.y', mouseClickOnColour.y)
    blockA.addData('mouseClickOnColour.leftButton', mouseClickOnColour.leftButton)
    blockA.addData('mouseClickOnColour.midButton', mouseClickOnColour.midButton)
    blockA.addData('mouseClickOnColour.rightButton', mouseClickOnColour.rightButton)
    blockA.addData('mouseClickOnColour.time', mouseClickOnColour.time)
    blockA.addData('mouseClickOnColour.clicked_name', mouseClickOnColour.clicked_name)
    # store data for blockA (TrialHandler)
    blockA.addData('mouseClickOnNumber.x', mouseClickOnNumber.x)
    blockA.addData('mouseClickOnNumber.y', mouseClickOnNumber.y)
    blockA.addData('mouseClickOnNumber.leftButton', mouseClickOnNumber.leftButton)
    blockA.addData('mouseClickOnNumber.midButton', mouseClickOnNumber.midButton)
    blockA.addData('mouseClickOnNumber.rightButton', mouseClickOnNumber.rightButton)
    blockA.addData('mouseClickOnNumber.time', mouseClickOnNumber.time)
    blockA.addData('mouseClickOnNumber.clicked_name', mouseClickOnNumber.clicked_name)
    # Run 'End Routine' code from evaluateResponses
    #evaluate correctness of response and write into a new column TRUE, FALSE, or NO_ANSW  
    if len(mouseClickOnCall.clicked_name) > 0:
        currentLoop.addData('callSignCorrect', mapCallSign[mouseClickOnCall.clicked_name[0]] == callSign) 
        print(mapCallSign[mouseClickOnCall.clicked_name[0]])
    else:
        currentLoop.addData('callSignCorrect', "NO_ANSW") 
    if len(mouseClickOnColour.clicked_name) > 0:
        currentLoop.addData('colourCorrect', mapColour[mouseClickOnColour.clicked_name[0]] == colour) 
        print(mapColour[mouseClickOnColour.clicked_name[0]])
    else:
        currentLoop.addData('colourCorrect', "NO_ANSW") 
    if len(mouseClickOnNumber.clicked_name) > 0:
        currentLoop.addData('numberCorrect', mapNumber[mouseClickOnNumber.clicked_name[0]] == number) 
        print(mapNumber[mouseClickOnNumber.clicked_name[0]])
    else:
        currentLoop.addData('numberCorrect', "NO_ANSW") 
    # Run 'End Routine' code from saveAfterEachTrial
    #sicherIstSicher
    #thisExp.saveAsWideText(filename+'.csv')
    #logging.flush()
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'blockA'

# get names of stimulus parameters
if blockA.trialList in ([], [None], None):
    params = []
else:
    params = blockA.trialList[0].keys()
# save data for this loop
blockA.saveAsExcel(filename + '.xlsx', sheetName='blockA',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

# --- Prepare to start Routine "thanks" ---
continueRoutine = True
# update component parameters for each repeat
key_resp_5.keys = []
key_resp_5.rt = []
_key_resp_5_allKeys = []
# keep track of which components have finished
thanksComponents = [thanksText, key_resp_5]
for thisComponent in thanksComponents:
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

# --- Run Routine "thanks" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *thanksText* updates
    if thanksText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        thanksText.frameNStart = frameN  # exact frame index
        thanksText.tStart = t  # local t and not account for scr refresh
        thanksText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(thanksText, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'thanksText.started')
        thanksText.setAutoDraw(True)
    
    # *key_resp_5* updates
    waitOnFlip = False
    if key_resp_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_5.frameNStart = frameN  # exact frame index
        key_resp_5.tStart = t  # local t and not account for scr refresh
        key_resp_5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_5, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp_5.started')
        key_resp_5.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_5.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_5.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_5.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_5_allKeys.extend(theseKeys)
        if len(_key_resp_5_allKeys):
            key_resp_5.keys = _key_resp_5_allKeys[-1].name  # just the last key pressed
            key_resp_5.rt = _key_resp_5_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "thanks" ---
for thisComponent in thanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "thanks" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

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
