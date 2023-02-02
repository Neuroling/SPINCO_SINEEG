﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on January 17, 2023, at 13:15
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
filename = _thisDir + os.sep + 'data' + os.sep + u'psychopy_data_' + data.getDateStr()

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='V:\\gfraga\\scripts_neulin\\Projects\\SINEEG\\Experiments\\SiN\\AudioVisualIntegration-master\\PsychoPy\\gorkitests.py',
    savePickle=True, saveWideText=False,
    dataFileName=filename)
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

# --- Initialize components for Routine "instrExposure" ---
instrExposureText = visual.TextStim(win=win, name='instrExposureText',
    text='Jetzt hörst du gleich vier Sätze, die noch nicht computerbearbeitet sind. So bekommmst du eine Vorstellung, wie sich die Sätze in Normalsprache anhören.\n\nDu musst noch nichts tun, ausser zuhören. Die Übung beginnt danach.\n\nDrücke bitte die Leertaste, um zu beginnen.',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_4 = keyboard.Keyboard()

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
    image='images/drossel.png', mask=None, anchor='center',
    ori=0, pos=(-0.4, .10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-6.0)
call3 = visual.ImageStim(
    win=win,
    name='call3', 
    image='images/tiger.png', mask=None, anchor='center',
    ori=0, pos=(-0.4, -.10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-7.0)
call4 = visual.ImageStim(
    win=win,
    name='call4', 
    image='images/unke.png', mask=None, anchor='center',
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
    image='images/gruen.png', mask=None, anchor='center',
    ori=0, pos=(0.0, .10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-10.0)
colour3 = visual.ImageStim(
    win=win,
    name='colour3', 
    image='images/rot.png', mask=None, anchor='center',
    ori=0, pos=(0.0, -.10416666666666666665), size=(0.18, 0.18),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-11.0)
colour4 = visual.ImageStim(
    win=win,
    name='colour4', 
    image='images/weiss.png', mask=None, anchor='center',
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

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "instrExposure" ---
continueRoutine = True
# update component parameters for each repeat
key_resp_4.keys = []
key_resp_4.rt = []
_key_resp_4_allKeys = []
# Run 'Begin Routine' code from hideMouseOnBegin
win.mouseVisible = False 
# keep track of which components have finished
instrExposureComponents = [instrExposureText, key_resp_4]
for thisComponent in instrExposureComponents:
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

# --- Run Routine "instrExposure" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrExposureText* updates
    if instrExposureText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instrExposureText.frameNStart = frameN  # exact frame index
        instrExposureText.tStart = t  # local t and not account for scr refresh
        instrExposureText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instrExposureText, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'instrExposureText.started')
        instrExposureText.setAutoDraw(True)
    
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
        theseKeys = key_resp_4.getKeys(keyList=['space'], waitRelease=False)
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
    for thisComponent in instrExposureComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "instrExposure" ---
for thisComponent in instrExposureComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instrExposure" was not non-slip safe, so reset the non-slip timer
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
    if videoStimulus.status==FINISHED and participantResponseTime == None:
        participantResponseTime = trialClock.getTime()
    
    #switch to the next trial when the video is ended and response time (10 seconds) is over 
    if participantResponseTime and trialClock.getTime() - participantResponseTime > 10 and not blankScreenAfterResponse.status == STARTED:
        continueRoutine = False
    
    # *blankScreen* updates
    if blankScreen.status == NOT_STARTED and videoStimulus.status==FINISHED:
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
        if tThisFlipGlobal > blankScreen.tStartRefresh + 1.0-frameTolerance:
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
    if number1.status == NOT_STARTED and videoStimulus.status==FINISHED:
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
    if number3.status == NOT_STARTED and videoStimulus.status==FINISHED:
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
        if tThisFlipGlobal > blankScreenAfterResponse.tStartRefresh + 0.6-frameTolerance:
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
# store data for thisExp (ExperimentHandler)
thisExp.addData('mouseClickOnCall.x', mouseClickOnCall.x)
thisExp.addData('mouseClickOnCall.y', mouseClickOnCall.y)
thisExp.addData('mouseClickOnCall.leftButton', mouseClickOnCall.leftButton)
thisExp.addData('mouseClickOnCall.midButton', mouseClickOnCall.midButton)
thisExp.addData('mouseClickOnCall.rightButton', mouseClickOnCall.rightButton)
thisExp.addData('mouseClickOnCall.time', mouseClickOnCall.time)
thisExp.addData('mouseClickOnCall.clicked_name', mouseClickOnCall.clicked_name)
thisExp.nextEntry()
# store data for thisExp (ExperimentHandler)
thisExp.addData('mouseClickOnColour.x', mouseClickOnColour.x)
thisExp.addData('mouseClickOnColour.y', mouseClickOnColour.y)
thisExp.addData('mouseClickOnColour.leftButton', mouseClickOnColour.leftButton)
thisExp.addData('mouseClickOnColour.midButton', mouseClickOnColour.midButton)
thisExp.addData('mouseClickOnColour.rightButton', mouseClickOnColour.rightButton)
thisExp.addData('mouseClickOnColour.time', mouseClickOnColour.time)
thisExp.addData('mouseClickOnColour.clicked_name', mouseClickOnColour.clicked_name)
thisExp.nextEntry()
# store data for thisExp (ExperimentHandler)
thisExp.addData('mouseClickOnNumber.x', mouseClickOnNumber.x)
thisExp.addData('mouseClickOnNumber.y', mouseClickOnNumber.y)
thisExp.addData('mouseClickOnNumber.leftButton', mouseClickOnNumber.leftButton)
thisExp.addData('mouseClickOnNumber.midButton', mouseClickOnNumber.midButton)
thisExp.addData('mouseClickOnNumber.rightButton', mouseClickOnNumber.rightButton)
thisExp.addData('mouseClickOnNumber.time', mouseClickOnNumber.time)
thisExp.addData('mouseClickOnNumber.clicked_name', mouseClickOnNumber.clicked_name)
thisExp.nextEntry()
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

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsPickle(filename)
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()