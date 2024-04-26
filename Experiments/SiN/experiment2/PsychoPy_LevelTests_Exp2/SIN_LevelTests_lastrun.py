#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.1.1),
    on April 25, 2024, at 08:39
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'pyo'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from preparations
#import psychtoolbox as ptb
from psychopy import sound
import psychopy.visual
import psychopy.event
import psychopy.core

clock = psychopy.core.Clock()
print('TIME O_o')
print(clock.getTime())
# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.1.1'
expName = 'SentenceInNoise'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': 's00',
    'order': '1',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_loggingLevel = logging.getLevel('exp')
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
    # override logging level
    _loggingLevel = logging.getLevel(
        prefs.piloting['pilotLoggingLevel']
    )

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='Y:\\Projects\\Spinco\\SINEEG\\Scripts\\Experiments\\SiN\\experiment2\\PsychoPy_LevelTests_Exp2\\SIN_LevelTests_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # this outputs to the screen, not a file
    logging.console.setLevel(_loggingLevel)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=_loggingLevel)
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=[1280, 720], fullscr=_fullScr, screen=0,
            winType='pyglet', allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height', 
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.mouseVisible = False
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    ioServer = io.launchHubServer(window=win, **ioConfig)
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('key_resp_2') is None:
        # initialise key_resp_2
        key_resp_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_2',
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    # create speaker 'sound_1'
    deviceManager.addDevice(
        deviceName='sound_1',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=-1
    )
    if deviceManager.getDevice('key_resp_5') is None:
        # initialise key_resp_5
        key_resp_5 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_5',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "instrTraining" ---
    # Run 'Begin Experiment' code from preparations
    #if (SubjectNumber % 2 == 0):
    #    Order=ABCD
    #else:
    #    Order=CDBA
        
    
            
    instrTrainText = visual.TextStim(win=win, name='instrTrainText',
        text='In diesem Versuch hören Sie gleich strukturierte Sätze mit jeweils drei wechselnden Wörtern (*...*)\n\nBeispiel: Vorsicht *Adler* , geh sofort zum *gelben* Feld von der Spalte *drei*. \n\nSie sollen sich die Sätze anhören und jeweils versuchen die drei darin vorkommenden Wörter zu verstehen. \n\nIhre Aufgab ist es, nach jedem Satz die zu dren drei Wörtern passenden Bilder der Reihenfolge nach mit der Maus auf dem Bildschirm anzuklicken\n\nDrücke bitte die Leertaste, um zu beginnen.',
        font='Arial',
        pos=(0, 0), height=0.04, wrapWidth=1, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp_2 = keyboard.Keyboard(deviceName='key_resp_2')
    # Run 'Begin Experiment' code from getOrder
    orderFile = "order" + expInfo['order']+ ".csv"
    prefs.hardware['audioLib'] = 'pyo'
    
    # --- Initialize components for Routine "startBlock" ---
    blockStart = visual.TextStim(win=win, name='blockStart',
        text='Begin  block ',
        font='Arial',
        pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # --- Initialize components for Routine "audioTrial" ---
    sound_1 = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='sound_1',    name='sound_1'
    )
    sound_1.setVolume(1.0)
    fixation = visual.ShapeStim(
        win=win, name='fixation', vertices='cross',
        size=(0.05, 0.05),
        ori=0.0, pos=(0, 0), anchor='center',
        lineWidth=0.5,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=0.75, depth=-1.0, interpolate=True)
    screenAfterAudio = visual.ImageStim(
        win=win,
        name='screenAfterAudio', 
        image='images/grayScreen.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    
    # --- Initialize components for Routine "trial" ---
    # Run 'Begin Experiment' code from mapStimuliLabels
    # Mappings for stimuli properties
    mapCallSign = {
      "call1": "Ad",
      "call2": "Dr",
      "call3": "Kr",
      "call4": "Ti"
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
        image='images/grayScreen.png', mask=None, anchor='center',
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
        image='images/kroete.png', mask=None, anchor='center',
        ori=0, pos=(-0.4, -.10416666666666666665), size=(0.18, 0.18),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-7.0)
    call4 = visual.ImageStim(
        win=win,
        name='call4', 
        image='images/tiger.png', mask=None, anchor='center',
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
    
    # --- Initialize components for Routine "thanks" ---
    thanksText = visual.TextStim(win=win, name='thanksText',
        text="That's all folks!\n\nVielen Dank für deine Teilnahme an unserer Studie und deinen wichtigen Beitrag zu Sprachverarbeitung.\n",
        font='Arial',
        pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_5 = keyboard.Keyboard(deviceName='key_resp_5')
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "instrTraining" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('instrTraining.started', globalClock.getTime(format='float'))
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
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instrTrainText* updates
        
        # if instrTrainText is starting this frame...
        if instrTrainText.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            instrTrainText.frameNStart = frameN  # exact frame index
            instrTrainText.tStart = t  # local t and not account for scr refresh
            instrTrainText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instrTrainText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instrTrainText.started')
            # update status
            instrTrainText.status = STARTED
            instrTrainText.setAutoDraw(True)
        
        # if instrTrainText is active this frame...
        if instrTrainText.status == STARTED:
            # update params
            pass
        
        # *key_resp_2* updates
        waitOnFlip = False
        
        # if key_resp_2 is starting this frame...
        if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.tStart = t  # local t and not account for scr refresh
            key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_2.started')
            # update status
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_2.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_2_allKeys.extend(theseKeys)
            if len(_key_resp_2_allKeys):
                key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                key_resp_2.duration = _key_resp_2_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
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
    thisExp.addData('instrTraining.stopped', globalClock.getTime(format='float'))
    thisExp.nextEntry()
    # the Routine "instrTraining" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    blocks = data.TrialHandler(nReps=1.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(orderFile),
        seed=None, name='blocks')
    thisExp.addLoop(blocks)  # add the loop to the experiment
    thisBlock = blocks.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            globals()[paramName] = thisBlock[paramName]
    
    for thisBlock in blocks:
        currentLoop = blocks
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
        if thisBlock != None:
            for paramName in thisBlock:
                globals()[paramName] = thisBlock[paramName]
        
        # --- Prepare to start Routine "startBlock" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('startBlock.started', globalClock.getTime(format='float'))
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
        frameN = -1
        
        # --- Run Routine "startBlock" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blockStart* updates
            
            # if blockStart is starting this frame...
            if blockStart.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blockStart.frameNStart = frameN  # exact frame index
                blockStart.tStart = t  # local t and not account for scr refresh
                blockStart.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blockStart, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blockStart.started')
                # update status
                blockStart.status = STARTED
                blockStart.setAutoDraw(True)
            
            # if blockStart is active this frame...
            if blockStart.status == STARTED:
                # update params
                pass
            
            # *key_resp* updates
            waitOnFlip = False
            
            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                # update status
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in startBlockComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "startBlock" ---
        for thisComponent in startBlockComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('startBlock.stopped', globalClock.getTime(format='float'))
        # the Routine "startBlock" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        trials = data.TrialHandler(nReps=1, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=data.importConditions(condsFile),
            seed=None, name='trials')
        thisExp.addLoop(trials)  # add the loop to the experiment
        thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        for thisTrial in trials:
            currentLoop = trials
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
            )
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    globals()[paramName] = thisTrial[paramName]
            
            # --- Prepare to start Routine "audioTrial" ---
            continueRoutine = True
            # update component parameters for each repeat
            thisExp.addData('audioTrial.started', globalClock.getTime(format='float'))
            sound_1.setSound(audiofile, hamming=True)
            sound_1.setVolume(1.0, log=False)
            sound_1.seek(0)
            # Run 'Begin Routine' code from hideMouse_2
            win.mouseVisible = False 
            
            # keep track of which components have finished
            audioTrialComponents = [sound_1, fixation, screenAfterAudio]
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
            routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # if sound_1 is starting this frame...
                if sound_1.status == NOT_STARTED and frameN >= 0.0:
                    # keep track of start time/frame for later
                    sound_1.frameNStart = frameN  # exact frame index
                    sound_1.tStart = t  # local t and not account for scr refresh
                    sound_1.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('sound_1.started', tThisFlipGlobal)
                    # update status
                    sound_1.status = STARTED
                    sound_1.play(when=win)  # sync with win flip
                # update sound_1 status according to whether it's playing
                if sound_1.isPlaying:
                    sound_1.status = STARTED
                elif sound_1.isFinished:
                    sound_1.status = FINISHED
                
                # *fixation* updates
                
                # if fixation is starting this frame...
                if fixation.status == NOT_STARTED and frameN >= 0:
                    # keep track of start time/frame for later
                    fixation.frameNStart = frameN  # exact frame index
                    fixation.tStart = t  # local t and not account for scr refresh
                    fixation.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.started')
                    # update status
                    fixation.status = STARTED
                    fixation.setAutoDraw(True)
                
                # if fixation is active this frame...
                if fixation.status == STARTED:
                    # update params
                    pass
                
                # if fixation is stopping this frame...
                if fixation.status == STARTED:
                    if bool(sound_1.status==FINISHED):
                        # keep track of stop time/frame for later
                        fixation.tStop = t  # not accounting for scr refresh
                        fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'fixation.stopped')
                        # update status
                        fixation.status = FINISHED
                        fixation.setAutoDraw(False)
                
                # *screenAfterAudio* updates
                
                # if screenAfterAudio is starting this frame...
                if screenAfterAudio.status == NOT_STARTED and frameN >= fixation.status==FINISHED  :
                    # keep track of start time/frame for later
                    screenAfterAudio.frameNStart = frameN  # exact frame index
                    screenAfterAudio.tStart = t  # local t and not account for scr refresh
                    screenAfterAudio.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(screenAfterAudio, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'screenAfterAudio.started')
                    # update status
                    screenAfterAudio.status = STARTED
                    screenAfterAudio.setAutoDraw(True)
                
                # if screenAfterAudio is active this frame...
                if screenAfterAudio.status == STARTED:
                    # update params
                    pass
                
                # if screenAfterAudio is stopping this frame...
                if screenAfterAudio.status == STARTED:
                    # is it time to stop? (based on local clock)
                    if tThisFlip > 2 -frameTolerance:
                        # keep track of stop time/frame for later
                        screenAfterAudio.tStop = t  # not accounting for scr refresh
                        screenAfterAudio.tStopRefresh = tThisFlipGlobal  # on global time
                        screenAfterAudio.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'screenAfterAudio.stopped')
                        # update status
                        screenAfterAudio.status = FINISHED
                        screenAfterAudio.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
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
            thisExp.addData('audioTrial.stopped', globalClock.getTime(format='float'))
            sound_1.pause()  # ensure sound has stopped at end of Routine
            # the Routine "audioTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "trial" ---
            continueRoutine = True
            # update component parameters for each repeat
            thisExp.addData('trial.started', globalClock.getTime(format='float'))
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
            trialClock = core.Clock()
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
            routineForceEnded = not continueRoutine
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
                if participantResponseTime == None:
                    participantResponseTime = trialClock.getTime()
                
                #switch to the next trial when audio ended and response time (10 seconds) is over 
                if participantResponseTime and trialClock.getTime() - participantResponseTime > 10 and not blankScreenAfterResponse.status == STARTED:
                    continueRoutine = False
                
                # *blankScreen* updates
                
                # if blankScreen is starting this frame...
                if blankScreen.status == NOT_STARTED and screenAfterAudio.status==FINISHED:
                    # keep track of start time/frame for later
                    blankScreen.frameNStart = frameN  # exact frame index
                    blankScreen.tStart = t  # local t and not account for scr refresh
                    blankScreen.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blankScreen, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blankScreen.started')
                    # update status
                    blankScreen.status = STARTED
                    blankScreen.setAutoDraw(True)
                
                # if blankScreen is active this frame...
                if blankScreen.status == STARTED:
                    # update params
                    pass
                
                # if blankScreen is stopping this frame...
                if blankScreen.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blankScreen.tStartRefresh + 1.0-frameTolerance:
                        # keep track of stop time/frame for later
                        blankScreen.tStop = t  # not accounting for scr refresh
                        blankScreen.tStopRefresh = tThisFlipGlobal  # on global time
                        blankScreen.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blankScreen.stopped')
                        # update status
                        blankScreen.status = FINISHED
                        blankScreen.setAutoDraw(False)
                
                # *call1* updates
                
                # if call1 is starting this frame...
                if call1.status == NOT_STARTED and blankScreen.status==FINISHED:
                    # keep track of start time/frame for later
                    call1.frameNStart = frameN  # exact frame index
                    call1.tStart = t  # local t and not account for scr refresh
                    call1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(call1, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'call1.started')
                    # update status
                    call1.status = STARTED
                    call1.setAutoDraw(True)
                
                # if call1 is active this frame...
                if call1.status == STARTED:
                    # update params
                    pass
                
                # if call1 is stopping this frame...
                if call1.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        call1.tStop = t  # not accounting for scr refresh
                        call1.tStopRefresh = tThisFlipGlobal  # on global time
                        call1.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'call1.stopped')
                        # update status
                        call1.status = FINISHED
                        call1.setAutoDraw(False)
                
                # *call2* updates
                
                # if call2 is starting this frame...
                if call2.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    call2.frameNStart = frameN  # exact frame index
                    call2.tStart = t  # local t and not account for scr refresh
                    call2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(call2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'call2.started')
                    # update status
                    call2.status = STARTED
                    call2.setAutoDraw(True)
                
                # if call2 is active this frame...
                if call2.status == STARTED:
                    # update params
                    pass
                
                # if call2 is stopping this frame...
                if call2.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        call2.tStop = t  # not accounting for scr refresh
                        call2.tStopRefresh = tThisFlipGlobal  # on global time
                        call2.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'call2.stopped')
                        # update status
                        call2.status = FINISHED
                        call2.setAutoDraw(False)
                
                # *call3* updates
                
                # if call3 is starting this frame...
                if call3.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    call3.frameNStart = frameN  # exact frame index
                    call3.tStart = t  # local t and not account for scr refresh
                    call3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(call3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'call3.started')
                    # update status
                    call3.status = STARTED
                    call3.setAutoDraw(True)
                
                # if call3 is active this frame...
                if call3.status == STARTED:
                    # update params
                    pass
                
                # if call3 is stopping this frame...
                if call3.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        call3.tStop = t  # not accounting for scr refresh
                        call3.tStopRefresh = tThisFlipGlobal  # on global time
                        call3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'call3.stopped')
                        # update status
                        call3.status = FINISHED
                        call3.setAutoDraw(False)
                
                # *call4* updates
                
                # if call4 is starting this frame...
                if call4.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    call4.frameNStart = frameN  # exact frame index
                    call4.tStart = t  # local t and not account for scr refresh
                    call4.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(call4, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'call4.started')
                    # update status
                    call4.status = STARTED
                    call4.setAutoDraw(True)
                
                # if call4 is active this frame...
                if call4.status == STARTED:
                    # update params
                    pass
                
                # if call4 is stopping this frame...
                if call4.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        call4.tStop = t  # not accounting for scr refresh
                        call4.tStopRefresh = tThisFlipGlobal  # on global time
                        call4.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'call4.stopped')
                        # update status
                        call4.status = FINISHED
                        call4.setAutoDraw(False)
                
                # *colour1* updates
                
                # if colour1 is starting this frame...
                if colour1.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    colour1.frameNStart = frameN  # exact frame index
                    colour1.tStart = t  # local t and not account for scr refresh
                    colour1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(colour1, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colour1.started')
                    # update status
                    colour1.status = STARTED
                    colour1.setAutoDraw(True)
                
                # if colour1 is active this frame...
                if colour1.status == STARTED:
                    # update params
                    pass
                
                # if colour1 is stopping this frame...
                if colour1.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        colour1.tStop = t  # not accounting for scr refresh
                        colour1.tStopRefresh = tThisFlipGlobal  # on global time
                        colour1.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'colour1.stopped')
                        # update status
                        colour1.status = FINISHED
                        colour1.setAutoDraw(False)
                
                # *colour2* updates
                
                # if colour2 is starting this frame...
                if colour2.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    colour2.frameNStart = frameN  # exact frame index
                    colour2.tStart = t  # local t and not account for scr refresh
                    colour2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(colour2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colour2.started')
                    # update status
                    colour2.status = STARTED
                    colour2.setAutoDraw(True)
                
                # if colour2 is active this frame...
                if colour2.status == STARTED:
                    # update params
                    pass
                
                # if colour2 is stopping this frame...
                if colour2.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        colour2.tStop = t  # not accounting for scr refresh
                        colour2.tStopRefresh = tThisFlipGlobal  # on global time
                        colour2.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'colour2.stopped')
                        # update status
                        colour2.status = FINISHED
                        colour2.setAutoDraw(False)
                
                # *colour3* updates
                
                # if colour3 is starting this frame...
                if colour3.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    colour3.frameNStart = frameN  # exact frame index
                    colour3.tStart = t  # local t and not account for scr refresh
                    colour3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(colour3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colour3.started')
                    # update status
                    colour3.status = STARTED
                    colour3.setAutoDraw(True)
                
                # if colour3 is active this frame...
                if colour3.status == STARTED:
                    # update params
                    pass
                
                # if colour3 is stopping this frame...
                if colour3.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        colour3.tStop = t  # not accounting for scr refresh
                        colour3.tStopRefresh = tThisFlipGlobal  # on global time
                        colour3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'colour3.stopped')
                        # update status
                        colour3.status = FINISHED
                        colour3.setAutoDraw(False)
                
                # *colour4* updates
                
                # if colour4 is starting this frame...
                if colour4.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    colour4.frameNStart = frameN  # exact frame index
                    colour4.tStart = t  # local t and not account for scr refresh
                    colour4.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(colour4, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colour4.started')
                    # update status
                    colour4.status = STARTED
                    colour4.setAutoDraw(True)
                
                # if colour4 is active this frame...
                if colour4.status == STARTED:
                    # update params
                    pass
                
                # if colour4 is stopping this frame...
                if colour4.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        colour4.tStop = t  # not accounting for scr refresh
                        colour4.tStopRefresh = tThisFlipGlobal  # on global time
                        colour4.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'colour4.stopped')
                        # update status
                        colour4.status = FINISHED
                        colour4.setAutoDraw(False)
                
                # *number1* updates
                
                # if number1 is starting this frame...
                if number1.status == NOT_STARTED and blankScreen.status==FINISHED:
                    # keep track of start time/frame for later
                    number1.frameNStart = frameN  # exact frame index
                    number1.tStart = t  # local t and not account for scr refresh
                    number1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(number1, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'number1.started')
                    # update status
                    number1.status = STARTED
                    number1.setAutoDraw(True)
                
                # if number1 is active this frame...
                if number1.status == STARTED:
                    # update params
                    pass
                
                # if number1 is stopping this frame...
                if number1.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        number1.tStop = t  # not accounting for scr refresh
                        number1.tStopRefresh = tThisFlipGlobal  # on global time
                        number1.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'number1.stopped')
                        # update status
                        number1.status = FINISHED
                        number1.setAutoDraw(False)
                
                # *number2* updates
                
                # if number2 is starting this frame...
                if number2.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    number2.frameNStart = frameN  # exact frame index
                    number2.tStart = t  # local t and not account for scr refresh
                    number2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(number2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'number2.started')
                    # update status
                    number2.status = STARTED
                    number2.setAutoDraw(True)
                
                # if number2 is active this frame...
                if number2.status == STARTED:
                    # update params
                    pass
                
                # if number2 is stopping this frame...
                if number2.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        number2.tStop = t  # not accounting for scr refresh
                        number2.tStopRefresh = tThisFlipGlobal  # on global time
                        number2.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'number2.stopped')
                        # update status
                        number2.status = FINISHED
                        number2.setAutoDraw(False)
                
                # *number3* updates
                
                # if number3 is starting this frame...
                if number3.status == NOT_STARTED and blankScreen.status==FINISHED:
                    # keep track of start time/frame for later
                    number3.frameNStart = frameN  # exact frame index
                    number3.tStart = t  # local t and not account for scr refresh
                    number3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(number3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'number3.started')
                    # update status
                    number3.status = STARTED
                    number3.setAutoDraw(True)
                
                # if number3 is active this frame...
                if number3.status == STARTED:
                    # update params
                    pass
                
                # if number3 is stopping this frame...
                if number3.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        number3.tStop = t  # not accounting for scr refresh
                        number3.tStopRefresh = tThisFlipGlobal  # on global time
                        number3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'number3.stopped')
                        # update status
                        number3.status = FINISHED
                        number3.setAutoDraw(False)
                
                # *number4* updates
                
                # if number4 is starting this frame...
                if number4.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    number4.frameNStart = frameN  # exact frame index
                    number4.tStart = t  # local t and not account for scr refresh
                    number4.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(number4, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'number4.started')
                    # update status
                    number4.status = STARTED
                    number4.setAutoDraw(True)
                
                # if number4 is active this frame...
                if number4.status == STARTED:
                    # update params
                    pass
                
                # if number4 is stopping this frame...
                if number4.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        number4.tStop = t  # not accounting for scr refresh
                        number4.tStopRefresh = tThisFlipGlobal  # on global time
                        number4.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'number4.stopped')
                        # update status
                        number4.status = FINISHED
                        number4.setAutoDraw(False)
                # *mouseClickOnCall* updates
                
                # if mouseClickOnCall is starting this frame...
                if mouseClickOnCall.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    mouseClickOnCall.frameNStart = frameN  # exact frame index
                    mouseClickOnCall.tStart = t  # local t and not account for scr refresh
                    mouseClickOnCall.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mouseClickOnCall, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.addData('mouseClickOnCall.started', t)
                    # update status
                    mouseClickOnCall.status = STARTED
                    prevButtonState = mouseClickOnCall.getPressed()  # if button is down already this ISN'T a new click
                if mouseClickOnCall.status == STARTED:  # only update if started and not finished!
                    buttons = mouseClickOnCall.getPressed()
                    if buttons != prevButtonState:  # button state changed?
                        prevButtonState = buttons
                        if sum(buttons) > 0:  # state changed to a new click
                            # check if the mouse was inside our 'clickable' objects
                            gotValidClick = False
                            clickableList = environmenttools.getFromNames([call1, call2, call3, call4], namespace=locals())
                            for obj in clickableList:
                                # is this object clicked on?
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
                                continueRoutine = False  # end routine on response
                # Run 'Each Frame' code from disableCallButtons
                            if gotValidClick:
                                mouseClickOnCall.status = FINISHED
                                if call1.name != mouseClickOnCall.clicked_name[-1]: call1.opacity = 0.2
                                if call2.name != mouseClickOnCall.clicked_name[-1]: call2.opacity = 0.2
                                if call3.name != mouseClickOnCall.clicked_name[-1]: call3.opacity = 0.2
                                if call4.name != mouseClickOnCall.clicked_name[-1]: call4.opacity = 0.2
                                continueRoutine = True
                # *mouseClickOnColour* updates
                
                # if mouseClickOnColour is starting this frame...
                if mouseClickOnColour.status == NOT_STARTED and mouseClickOnCall.getPressed()[0]:
                    # keep track of start time/frame for later
                    mouseClickOnColour.frameNStart = frameN  # exact frame index
                    mouseClickOnColour.tStart = t  # local t and not account for scr refresh
                    mouseClickOnColour.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mouseClickOnColour, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.addData('mouseClickOnColour.started', t)
                    # update status
                    mouseClickOnColour.status = STARTED
                    prevButtonState = mouseClickOnColour.getPressed()  # if button is down already this ISN'T a new click
                if mouseClickOnColour.status == STARTED:  # only update if started and not finished!
                    buttons = mouseClickOnColour.getPressed()
                    if buttons != prevButtonState:  # button state changed?
                        prevButtonState = buttons
                        if sum(buttons) > 0:  # state changed to a new click
                            # check if the mouse was inside our 'clickable' objects
                            gotValidClick = False
                            clickableList = environmenttools.getFromNames([colour1, colour2, colour3, colour4], namespace=locals())
                            for obj in clickableList:
                                # is this object clicked on?
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
                                continueRoutine = False  # end routine on response
                # Run 'Each Frame' code from disableColourButtons
                            if gotValidClick:
                                mouseClickOnColour.status = FINISHED
                                if colour1.name != mouseClickOnColour.clicked_name[-1]: colour1.opacity = 0.2
                                if colour2.name != mouseClickOnColour.clicked_name[-1]: colour2.opacity = 0.2
                                if colour3.name != mouseClickOnColour.clicked_name[-1]: colour3.opacity = 0.2
                                if colour4.name != mouseClickOnColour.clicked_name[-1]: colour4.opacity = 0.2
                                continueRoutine = True
                # *mouseClickOnNumber* updates
                
                # if mouseClickOnNumber is starting this frame...
                if mouseClickOnNumber.status == NOT_STARTED and mouseClickOnColour.status ==FINISHED:
                    # keep track of start time/frame for later
                    mouseClickOnNumber.frameNStart = frameN  # exact frame index
                    mouseClickOnNumber.tStart = t  # local t and not account for scr refresh
                    mouseClickOnNumber.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mouseClickOnNumber, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.addData('mouseClickOnNumber.started', t)
                    # update status
                    mouseClickOnNumber.status = STARTED
                    prevButtonState = mouseClickOnNumber.getPressed()  # if button is down already this ISN'T a new click
                if mouseClickOnNumber.status == STARTED:  # only update if started and not finished!
                    buttons = mouseClickOnNumber.getPressed()
                    if buttons != prevButtonState:  # button state changed?
                        prevButtonState = buttons
                        if sum(buttons) > 0:  # state changed to a new click
                            # check if the mouse was inside our 'clickable' objects
                            gotValidClick = False
                            clickableList = environmenttools.getFromNames([number1, number2, number3, number4], namespace=locals())
                            for obj in clickableList:
                                # is this object clicked on?
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
                                continueRoutine = False  # end routine on response
                # Run 'Each Frame' code from disableNumberButtons
                            if gotValidClick:
                                mouseClickOnNumber.status = FINISHED
                                if number1.name != mouseClickOnNumber.clicked_name[-1]: number1.opacity = 0.2
                                if number2.name != mouseClickOnNumber.clicked_name[-1]: number2.opacity = 0.2
                                if number3.name != mouseClickOnNumber.clicked_name[-1]: number3.opacity = 0.2
                                if number4.name != mouseClickOnNumber.clicked_name[-1]: number4.opacity = 0.2
                              #  continueRoutine = True
                
                # *blankScreenAfterResponse* updates
                
                # if blankScreenAfterResponse is starting this frame...
                if blankScreenAfterResponse.status == NOT_STARTED and mouseClickOnNumber.status==FINISHED:
                    # keep track of start time/frame for later
                    blankScreenAfterResponse.frameNStart = frameN  # exact frame index
                    blankScreenAfterResponse.tStart = t  # local t and not account for scr refresh
                    blankScreenAfterResponse.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blankScreenAfterResponse, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blankScreenAfterResponse.started')
                    # update status
                    blankScreenAfterResponse.status = STARTED
                    blankScreenAfterResponse.setAutoDraw(True)
                
                # if blankScreenAfterResponse is active this frame...
                if blankScreenAfterResponse.status == STARTED:
                    # update params
                    pass
                
                # if blankScreenAfterResponse is stopping this frame...
                if blankScreenAfterResponse.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blankScreenAfterResponse.tStartRefresh + 0.6-frameTolerance:
                        # keep track of stop time/frame for later
                        blankScreenAfterResponse.tStop = t  # not accounting for scr refresh
                        blankScreenAfterResponse.tStopRefresh = tThisFlipGlobal  # on global time
                        blankScreenAfterResponse.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blankScreenAfterResponse.stopped')
                        # update status
                        blankScreenAfterResponse.status = FINISHED
                        blankScreenAfterResponse.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
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
            thisExp.addData('trial.stopped', globalClock.getTime(format='float'))
            # store data for trials (TrialHandler)
            trials.addData('mouseClickOnCall.x', mouseClickOnCall.x)
            trials.addData('mouseClickOnCall.y', mouseClickOnCall.y)
            trials.addData('mouseClickOnCall.leftButton', mouseClickOnCall.leftButton)
            trials.addData('mouseClickOnCall.midButton', mouseClickOnCall.midButton)
            trials.addData('mouseClickOnCall.rightButton', mouseClickOnCall.rightButton)
            trials.addData('mouseClickOnCall.time', mouseClickOnCall.time)
            trials.addData('mouseClickOnCall.clicked_name', mouseClickOnCall.clicked_name)
            # store data for trials (TrialHandler)
            trials.addData('mouseClickOnColour.x', mouseClickOnColour.x)
            trials.addData('mouseClickOnColour.y', mouseClickOnColour.y)
            trials.addData('mouseClickOnColour.leftButton', mouseClickOnColour.leftButton)
            trials.addData('mouseClickOnColour.midButton', mouseClickOnColour.midButton)
            trials.addData('mouseClickOnColour.rightButton', mouseClickOnColour.rightButton)
            trials.addData('mouseClickOnColour.time', mouseClickOnColour.time)
            trials.addData('mouseClickOnColour.clicked_name', mouseClickOnColour.clicked_name)
            # store data for trials (TrialHandler)
            trials.addData('mouseClickOnNumber.x', mouseClickOnNumber.x)
            trials.addData('mouseClickOnNumber.y', mouseClickOnNumber.y)
            trials.addData('mouseClickOnNumber.leftButton', mouseClickOnNumber.leftButton)
            trials.addData('mouseClickOnNumber.midButton', mouseClickOnNumber.midButton)
            trials.addData('mouseClickOnNumber.rightButton', mouseClickOnNumber.rightButton)
            trials.addData('mouseClickOnNumber.time', mouseClickOnNumber.time)
            trials.addData('mouseClickOnNumber.clicked_name', mouseClickOnNumber.clicked_name)
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
            
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
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
    # completed 1.0 repeats of 'blocks'
    
    
    # --- Prepare to start Routine "thanks" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('thanks.started', globalClock.getTime(format='float'))
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
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *thanksText* updates
        
        # if thanksText is starting this frame...
        if thanksText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            thanksText.frameNStart = frameN  # exact frame index
            thanksText.tStart = t  # local t and not account for scr refresh
            thanksText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(thanksText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'thanksText.started')
            # update status
            thanksText.status = STARTED
            thanksText.setAutoDraw(True)
        
        # if thanksText is active this frame...
        if thanksText.status == STARTED:
            # update params
            pass
        
        # *key_resp_5* updates
        waitOnFlip = False
        
        # if key_resp_5 is starting this frame...
        if key_resp_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_5.frameNStart = frameN  # exact frame index
            key_resp_5.tStart = t  # local t and not account for scr refresh
            key_resp_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_5, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_5.started')
            # update status
            key_resp_5.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_5.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_5.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_5.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_5_allKeys.extend(theseKeys)
            if len(_key_resp_5_allKeys):
                key_resp_5.keys = _key_resp_5_allKeys[-1].name  # just the last key pressed
                key_resp_5.rt = _key_resp_5_allKeys[-1].rt
                key_resp_5.duration = _key_resp_5_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
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
    thisExp.addData('thanks.stopped', globalClock.getTime(format='float'))
    thisExp.nextEntry()
    # the Routine "thanks" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if deviceManager.getDevice('eyetracker') is not None:
        deviceManager.removeDevice('eyetracker')
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    # shut down eyetracker, if there is one
    if deviceManager.getDevice('eyetracker') is not None:
        deviceManager.removeDevice('eyetracker')
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
