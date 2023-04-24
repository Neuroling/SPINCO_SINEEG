#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.1.3),
    on April 12, 2023, at 12:10
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from psychopy import locale_setup
from psychopy import prefs
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, parallel
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

#import psychtoolbox as ptb
from psychopy import sound
import psychopy.visual
import psychopy.event
import psychopy.core

clock = psychopy.core.Clock()
print('TIME O_o')
print(clock.getTime())


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.1.3'
expName = 'SentenceInNoise'  # from the Builder filename that created this script
expInfo = {'participant': 's00', 'order': '1'}
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
    originPath='Z:\\gfraga\\scripts_neulin\\Projects\\SINEEG\\Experiments\\Timing_test\\Timing_test_ptb\\Timing_test.py',
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
# Setup ioHub
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

# Initialize components for Routine "instrTraining"
instrTrainingClock = core.Clock()
#if (SubjectNumber % 2 == 0):
#    Order=ABCD
#else:
#    Order=CDBA
    

        
instrTrainText = visual.TextStim(win=win, name='instrTrainText',
    text='Quick and dirty timing test',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=1, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_2 = keyboard.Keyboard()

# Initialize components for Routine "startBlock"
startBlockClock = core.Clock()
blockStart = visual.TextStim(win=win, name='blockStart',
    text='Begin  block ',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp = keyboard.Keyboard()

# Initialize components for Routine "audioTrial"
audioTrialClock = core.Clock()
sound_1 = sound.Sound('A', secs=-1, stereo=True, hamming=True,
    name='sound_1')
sound_1.setVolume(1.0)
fixation = visual.ShapeStim(
    win=win, name='fixation', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.5,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=0.75, depth=-2.0, interpolate=True)
screenAfterAudio = visual.ImageStim(
    win=win,
    name='screenAfterAudio', 
    image='images/grayScreen.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
pp_start = parallel.ParallelPort(address='0x3FE8')
pp_start_2 = parallel.ParallelPort(address='0x3FE8')

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "instrTraining"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_2.keys = []
key_resp_2.rt = []
_key_resp_2_allKeys = []
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
instrTrainingClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "instrTraining"-------
while continueRoutine:
    # get current time
    t = instrTrainingClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=instrTrainingClock)
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
        instrTrainText.setAutoDraw(True)
    
    # *key_resp_2* updates
    waitOnFlip = False
    if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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

# -------Ending Routine "instrTraining"-------
for thisComponent in instrTrainingComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('instrTrainText.started', instrTrainText.tStartRefresh)
thisExp.addData('instrTrainText.stopped', instrTrainText.tStopRefresh)
# the Routine "instrTraining" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "startBlock"-------
continueRoutine = True
# update component parameters for each repeat
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []
# keep track of which components have finished
startBlockComponents = [blockStart, key_resp]
for thisComponent in startBlockComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
startBlockClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "startBlock"-------
while continueRoutine:
    # get current time
    t = startBlockClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=startBlockClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *blockStart* updates
    if blockStart.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        blockStart.frameNStart = frameN  # exact frame index
        blockStart.tStart = t  # local t and not account for scr refresh
        blockStart.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(blockStart, 'tStartRefresh')  # time at next scr refresh
        blockStart.setAutoDraw(True)
    
    # *key_resp* updates
    waitOnFlip = False
    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
        theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(_key_resp_allKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in startBlockComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "startBlock"-------
for thisComponent in startBlockComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('blockStart.started', blockStart.tStartRefresh)
thisExp.addData('blockStart.stopped', blockStart.tStopRefresh)
# the Routine "startBlock" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Sequence.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "audioTrial"-------
    continueRoutine = True
    # update component parameters for each repeat
    sound_1.setSound(audiofile, hamming=True)
    sound_1.setVolume(1.0, log=False)
    # Trigger 
    myClock = core.Clock()
    now = myClock.getTime()
    
    # Trigger times 
    
    
    # Some runner prints for testing
    print('<<<< now')
    print(now)
    
     # 
    
    win.mouseVisible = False 
    
    # keep track of which components have finished
    audioTrialComponents = [sound_1, fixation, screenAfterAudio, pp_start, pp_start_2]
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
    audioTrialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "audioTrial"-------
    while continueRoutine:
        # get current time
        t = audioTrialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=audioTrialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # start/stop sound_1
        if sound_1.status == NOT_STARTED and frameN >= 0.0:
            # keep track of start time/frame for later
            sound_1.frameNStart = frameN  # exact frame index
            sound_1.tStart = t  # local t and not account for scr refresh
            sound_1.tStartRefresh = tThisFlipGlobal  # on global time
            sound_1.play(when=win)  # sync with win flip
        
        # *fixation* updates
        if fixation.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            fixation.frameNStart = frameN  # exact frame index
            fixation.tStart = t  # local t and not account for scr refresh
            fixation.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
            fixation.setAutoDraw(True)
        if fixation.status == STARTED:
            if bool(sound_1.status==FINISHED):
                # keep track of stop time/frame for later
                fixation.tStop = t  # not accounting for scr refresh
                fixation.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fixation, 'tStopRefresh')  # time at next scr refresh
                fixation.setAutoDraw(False)
        
        # *screenAfterAudio* updates
        if screenAfterAudio.status == NOT_STARTED and frameN >= fixation.status==FINISHED  :
            # keep track of start time/frame for later
            screenAfterAudio.frameNStart = frameN  # exact frame index
            screenAfterAudio.tStart = t  # local t and not account for scr refresh
            screenAfterAudio.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(screenAfterAudio, 'tStartRefresh')  # time at next scr refresh
            screenAfterAudio.setAutoDraw(True)
        if screenAfterAudio.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > 2 -frameTolerance:
                # keep track of stop time/frame for later
                screenAfterAudio.tStop = t  # not accounting for scr refresh
                screenAfterAudio.frameNStop = frameN  # exact frame index
                win.timeOnFlip(screenAfterAudio, 'tStopRefresh')  # time at next scr refresh
                screenAfterAudio.setAutoDraw(False)
        # *pp_start* updates
        if pp_start.status == NOT_STARTED and tThisFlip >= 0.065-frameTolerance:
            # keep track of start time/frame for later
            pp_start.frameNStart = frameN  # exact frame index
            pp_start.tStart = t  # local t and not account for scr refresh
            pp_start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pp_start, 'tStartRefresh')  # time at next scr refresh
            pp_start.status = STARTED
            win.callOnFlip(pp_start.setData, int(1))
        if pp_start.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pp_start.tStartRefresh + 0.01-frameTolerance:
                # keep track of stop time/frame for later
                pp_start.tStop = t  # not accounting for scr refresh
                pp_start.frameNStop = frameN  # exact frame index
                win.timeOnFlip(pp_start, 'tStopRefresh')  # time at next scr refresh
                pp_start.status = FINISHED
                win.callOnFlip(pp_start.setData, int(0))
        # *pp_start_2* updates
        if pp_start_2.status == NOT_STARTED and tThisFlip >= 0.05 +0.05-frameTolerance:
            # keep track of start time/frame for later
            pp_start_2.frameNStart = frameN  # exact frame index
            pp_start_2.tStart = t  # local t and not account for scr refresh
            pp_start_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pp_start_2, 'tStartRefresh')  # time at next scr refresh
            pp_start_2.status = STARTED
            win.callOnFlip(pp_start_2.setData, int(108))
        if pp_start_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pp_start_2.tStartRefresh + 0.01-frameTolerance:
                # keep track of stop time/frame for later
                pp_start_2.tStop = t  # not accounting for scr refresh
                pp_start_2.frameNStop = frameN  # exact frame index
                win.timeOnFlip(pp_start_2, 'tStopRefresh')  # time at next scr refresh
                pp_start_2.status = FINISHED
                win.callOnFlip(pp_start_2.setData, int(0))
        
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
    
    # -------Ending Routine "audioTrial"-------
    for thisComponent in audioTrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    sound_1.stop()  # ensure sound has stopped at end of routine
    trials.addData('sound_1.started', sound_1.tStartRefresh)
    trials.addData('sound_1.stopped', sound_1.tStopRefresh)
    trials.addData('fixation.started', fixation.tStartRefresh)
    trials.addData('fixation.stopped', fixation.tStopRefresh)
    trials.addData('screenAfterAudio.started', screenAfterAudio.tStartRefresh)
    trials.addData('screenAfterAudio.stopped', screenAfterAudio.tStopRefresh)
    if pp_start.status == STARTED:
        win.callOnFlip(pp_start.setData, int(0))
    trials.addData('pp_start.started', pp_start.tStartRefresh)
    trials.addData('pp_start.stopped', pp_start.tStopRefresh)
    if pp_start_2.status == STARTED:
        win.callOnFlip(pp_start_2.setData, int(0))
    trials.addData('pp_start_2.started', pp_start_2.tStartRefresh)
    trials.addData('pp_start_2.stopped', pp_start_2.tStopRefresh)
    # the Routine "audioTrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'trials'

# get names of stimulus parameters
if trials.trialList in ([], [None], None):
    params = []
else:
    params = trials.trialList[0].keys()
# save data for this loop
trials.saveAsExcel(filename + '.xlsx', sheetName='trials',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])
trials.saveAsText(filename + 'trials.csv', delim=',',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

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
