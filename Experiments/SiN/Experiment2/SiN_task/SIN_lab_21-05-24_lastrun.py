#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.1.1),
    on May 22, 2024, at 15:54
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
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware, parallel
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# Run 'Before Experiment' code from prep_instrRest_pre
#import psychopy
from psychopy import sound
import psychopy.visual
import psychopy.event
import psychopy.core

clock = psychopy.core.Clock() 
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
        originPath='Y:\\Projects\\Spinco\\SINEEG\\Scripts\\Experiments\\SiN\\Experiment2\\SiN_task\\SIN_lab_21-05-24_lastrun.py',
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
            size=[2560, 1440], fullscr=_fullScr, screen=1,
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
    ioSession = ioServer = eyetracker = None
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    if deviceManager.getDevice('key_resp_inst_2') is None:
        # initialise key_resp_inst_2
        key_resp_inst_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_inst_2',
        )
    if deviceManager.getDevice('key_resp_instRest_pre') is None:
        # initialise key_resp_instRest_pre
        key_resp_instRest_pre = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_instRest_pre',
        )
    # create speaker 'beep_rest_pre_start'
    deviceManager.addDevice(
        deviceName='beep_rest_pre_start',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=-1
    )
    # create speaker 'beep_rest_pre_end'
    deviceManager.addDevice(
        deviceName='beep_rest_pre_end',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=-1
    )
    if deviceManager.getDevice('key_resp_inst_4') is None:
        # initialise key_resp_inst_4
        key_resp_inst_4 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_inst_4',
        )
    if deviceManager.getDevice('key_resp_inst_3') is None:
        # initialise key_resp_inst_3
        key_resp_inst_3 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_inst_3',
        )
    if deviceManager.getDevice('key_resp_inst') is None:
        # initialise key_resp_inst
        key_resp_inst = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_inst',
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
    if deviceManager.getDevice('key_resp_instRest_post') is None:
        # initialise key_resp_instRest_post
        key_resp_instRest_post = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_instRest_post',
        )
    # create speaker 'beep_rest_post_start'
    deviceManager.addDevice(
        deviceName='beep_rest_post_start',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=-1
    )
    # create speaker 'beep_rest_post_end'
    deviceManager.addDevice(
        deviceName='beep_rest_post_end',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=-1
    )
    if deviceManager.getDevice('key_resp_6') is None:
        # initialise key_resp_6
        key_resp_6 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_6',
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
            backend='PsychToolbox',
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
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
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
    
    # --- Initialize components for Routine "instrStart" ---
    instr_start = visual.TextStim(win=win, name='instr_start',
        text='WILKOMMEN!  \n-------------------------------------------------------------------------------\nDieses Experiment besteht aus 3 Teilen:\n\n1. Eine kurze Sequenz in Ruhe mit geschlossenen Augen.\n\n3. Der Hauptteil besteht aus 6 Blöcken mit Pausen dazwischen. \n\n3. Nochmals eine kurze Sequenz in Ruhe mit geschlossenen Augen.\n\n\n\n<Klicken Sie auf die Abstandstaste/spacebar um fortzufahren >\n',
        font='Arial',
        pos=(0, 0), height=0.03, wrapWidth=1, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_inst_2 = keyboard.Keyboard(deviceName='key_resp_inst_2')
    
    # --- Initialize components for Routine "instrRest_PRE" ---
    # Run 'Begin Experiment' code from prep_instrRest_pre
    #if (SubjectNumber % 2 == 0):
    #    Order=ABCD
    #else:
    #    Order=CDBA
        
    
            
    instrRest_pre = visual.TextStim(win=win, name='instrRest_pre',
        text='Sind Sie bereit?\n\n-------------------------------------------------------------------------------\n\nZu Beginn, bleiben Sie bitte während 5 Minuten so still wie möglich sitzen schauen Sie das Kreuz in der Mitte des Bildschirms an. \n\nEin ‘beep’ kennzeichnet den Start und das Ende der Aufnahme. \n\nBitte versuchen Sie, während dieser Aufnahme bis zum Ende so still wie möglich zu sitzen und den Blick auf das Kreuz zu fixieren.\n \n\n<Klicken Sie auf die Abstandstaste/spacebar um fortzufahren >\n',
        font='Arial',
        pos=(0, 0), height=0.04, wrapWidth=1, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp_instRest_pre = keyboard.Keyboard(deviceName='key_resp_instRest_pre')
    pp_instrRest_PRE = parallel.ParallelPort(address='0x3FE8')
    
    # --- Initialize components for Routine "restTrial_pre" ---
    beep_rest_pre_start = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='beep_rest_pre_start',    name='beep_rest_pre_start'
    )
    beep_rest_pre_start.setVolume(1.0)
    fixation_1 = visual.ShapeStim(
        win=win, name='fixation_1', vertices='cross',
        size=(0.05, 0.05),
        ori=0.0, pos=(0, 0), anchor='center',
        lineWidth=0.5,     colorSpace='rgb',  lineColor=[1.0000, -1.0000, -1.0000], fillColor=[1.0000, -1.0000, -1.0000],
        opacity=0.75, depth=-1.0, interpolate=True)
    screenAfterAudio_3 = visual.ImageStim(
        win=win,
        name='screenAfterAudio_3', 
        image='images/grayScreen.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    beep_rest_pre_end = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='beep_rest_pre_end',    name='beep_rest_pre_end'
    )
    beep_rest_pre_end.setVolume(1.0)
    pp_rest_pre_start = parallel.ParallelPort(address='0x3FE8')
    
    # --- Initialize components for Routine "instrMain_1" ---
    instr_start_1 = visual.TextStim(win=win, name='instr_start_1',
        text='Sehr gut! Nun fahren wir mit dem Hauptteil fort. \n-------------------------------------------------------------------------------\n\nFolgend werden Sie verschiedene strukturierte Sätze mit jeweils drei wechselnden Wörtern hören: \n\nVorsicht *__*, geh sofort zum *__* Feld von der Spalte *__*.\n\n\nFür jedes der freien Felder gibt es acht mögliche Worte, zum Beispiel:  \n\nVorsicht *Adler/Eule/Ratte/Tiger/Velo/Auto/Messer/Gabel*, geh sofort zum *gelben/grünen/roten/weissen/blauen/braunen/pinken/schwarezn* Feld von der Spalte *eins/zwei/drei/vier/fünf/sechs/neun/null*.\n\n\n\n<Klicken Sie auf die Abstandstaste/spacebar um fortzufahren >',
        font='Arial',
        pos=(0, 0), height=0.03, wrapWidth=1, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_inst_4 = keyboard.Keyboard(deviceName='key_resp_inst_4')
    
    # --- Initialize components for Routine "instrMain_2" ---
    pp_instr_start_2 = parallel.ParallelPort(address='0x3FE8')
    instr_start_2 = visual.TextStim(win=win, name='instr_start_2',
        text='Hören Sie bitte gut zu. \n\nIhre Aufgabe ist es, nach jedem Satz die zu den drei Wörtern passenden Bilder der Reihenfolge nach mit der Maus auf dem Bildschirm anzuklicken. \n\nEinige der Sätze werden relativ einfach sein, andere etwas anspruchsvoller, und gewisse scheinen gänzlich unverständlich. \n\nVersuchen Sie bitte, unabhängig von der Bedingung so gut wie möglich hinzuhören und eine Antwort zu geben. Wenn Sie es nicht verstanden haben, dürfen Sie raten. \n\n\n<Klicken Sie auf die Abstandstaste/spacebar um zu beginnen>\n\n',
        font='Arial',
        pos=(0, 0), height=0.03, wrapWidth=1, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp_inst_3 = keyboard.Keyboard(deviceName='key_resp_inst_3')
    
    # --- Initialize components for Routine "instrTask" ---
    instrTaskText = visual.TextStim(win=win, name='instrTaskText',
        text='Sind Sie bereit, mit der Aufgabe zu beginnen? Sollten Sie noch Fragen haben, wenden Sie sich bitte an die Versuchsleitenden.\n\nVersuchen Sie, sich während der gesamten Aufgabe so wenig wie möglich zu bewegen. \u2028\n\n<Klicken Sie auf die Abstandstaste/spacebar um fortzufahren >\n',
        font='Arial',
        pos=(0, 0), height=0.04, wrapWidth=1, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    pp_instrTask = parallel.ParallelPort(address='0x3FE8')
    key_resp_inst = keyboard.Keyboard(deviceName='key_resp_inst')
    # Run 'Begin Experiment' code from getOrder
    orderFile = "order" + expInfo['order']+ ".csv"
    print('^^^^^----^-^')
    print(orderFile)
    
    # --- Initialize components for Routine "startBlock" ---
    blockStart = visual.TextStim(win=win, name='blockStart',
        text='Anfang des nächsten Blocks\n\n<Klicken Sie auf die Abstandstaste/spacebar um fortzufahren >\n ',
        font='Arial',
        pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    pp_blockstart = parallel.ParallelPort(address='0x3FE8')
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    # Run 'Begin Experiment' code from getOrder_2
    orderFile = "order" + expInfo['order']+ ".csv"
    print(orderFile)
    
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
    pp_t0_start = parallel.ParallelPort(address='0x3FE8')
    pp_t1_start = parallel.ParallelPort(address='0x3FE8')
    pp_t1_end = parallel.ParallelPort(address='0x3FE8')
    pp_t2_start = parallel.ParallelPort(address='0x3FE8')
    pp_t2_end = parallel.ParallelPort(address='0x3FE8')
    pp_t3_start = parallel.ParallelPort(address='0x3FE8')
    pp_end = parallel.ParallelPort(address='0x3FE8')
    
    # --- Initialize components for Routine "trial" ---
    # Run 'Begin Experiment' code from mapStimuliLabels
    # Mappings for stimuli properties
    mapCallSign = {
      "call1": "Adl",
      "call2": "Eul",
      "call3": "Rat",
      "call4": "Tig",
      "call5": "Vel",
      "call6": "Aut",
      "call7": "Mes",
      "call8": "Gab",
      }
      
    mapColour = {
      "colour1": "gel",
      "colour2": "gru",
      "colour3": "rot",
      "colour4": "wei",
      "colour5": "bla",
      "colour6": "bra",
      "colour7": "pin",
      "colour8": "sch"
      }
      
    mapNumber = {
      "number1": "Ein",
      "number2": "Zwe",
      "number3": "Dre",
      "number4": "Vie",
      "number5": "Fun",
      "number6": "Sec",
      "number7": "Neu",
      "number8": "Nul"
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
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(-0.4, 0.4375), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-5.0)
    call2 = visual.ImageStim(
        win=win,
        name='call2', 
        image='images/Eul.png', mask=None, anchor='center',
        ori=0, pos=(-0.4, .3125), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-6.0)
    call3 = visual.ImageStim(
        win=win,
        name='call3', 
        image='images/Rat.png', mask=None, anchor='center',
        ori=0, pos=(-0.4, .1875), size=(0.10, 0.10),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-7.0)
    call4 = visual.ImageStim(
        win=win,
        name='call4', 
        image='images/Tig.png', mask=None, anchor='center',
        ori=0, pos=(-0.4, 0.0625), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-8.0)
    call5 = visual.ImageStim(
        win=win,
        name='call5', 
        image='images/Vel.png', mask=None, anchor='center',
        ori=0, pos=(-0.4, -0.0625), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-9.0)
    call6 = visual.ImageStim(
        win=win,
        name='call6', 
        image='images/Aut.png', mask=None, anchor='center',
        ori=0, pos=(-0.4, -0.1875), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-10.0)
    call7 = visual.ImageStim(
        win=win,
        name='call7', 
        image='images/Mes.png', mask=None, anchor='center',
        ori=0, pos=(-0.4, -.3125), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-11.0)
    call8 = visual.ImageStim(
        win=win,
        name='call8', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(-0.4, -0.4375), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-12.0)
    colour1 = visual.ImageStim(
        win=win,
        name='colour1', 
        image='images/gel.png', mask=None, anchor='center',
        ori=0, pos=(0.0, 0.4375), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-13.0)
    colour2 = visual.ImageStim(
        win=win,
        name='colour2', 
        image='images/gru.png', mask=None, anchor='center',
        ori=0, pos=(0.0, .3125), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-14.0)
    colour3 = visual.ImageStim(
        win=win,
        name='colour3', 
        image='images/rot.png', mask=None, anchor='center',
        ori=0, pos=(0.0, 0.1875), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-15.0)
    colour4 = visual.ImageStim(
        win=win,
        name='colour4', 
        image='images/wei.png', mask=None, anchor='center',
        ori=0, pos=(0.0, 0.0625), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-16.0)
    colour5 = visual.ImageStim(
        win=win,
        name='colour5', 
        image='images/bla.png', mask=None, anchor='center',
        ori=0, pos=(0.0, -0.0625), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-17.0)
    colour6 = visual.ImageStim(
        win=win,
        name='colour6', 
        image='images/bra.png', mask=None, anchor='center',
        ori=0, pos=(0.0, -0.1875), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-18.0)
    colour7 = visual.ImageStim(
        win=win,
        name='colour7', 
        image='images/pin.png', mask=None, anchor='center',
        ori=0, pos=(0.0, -.3125), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-19.0)
    colour8 = visual.ImageStim(
        win=win,
        name='colour8', 
        image='images/sch.png', mask=None, anchor='center',
        ori=0, pos=(0.0, -0.4375), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-20.0)
    number1 = visual.ImageStim(
        win=win,
        name='number1', 
        image='images/Ein.png', mask=None, anchor='center',
        ori=0, pos=(0.4, 0.4375), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-21.0)
    number2 = visual.ImageStim(
        win=win,
        name='number2', 
        image='images/Zwe.png', mask=None, anchor='center',
        ori=0, pos=(0.4, .3125), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-22.0)
    number3 = visual.ImageStim(
        win=win,
        name='number3', 
        image='images/Dre.png', mask=None, anchor='center',
        ori=0, pos=(0.4, 0.1875), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-23.0)
    number4 = visual.ImageStim(
        win=win,
        name='number4', 
        image='images/Vie.png', mask=None, anchor='center',
        ori=0, pos=(0.4, 0.0625), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-24.0)
    number5 = visual.ImageStim(
        win=win,
        name='number5', 
        image='images/Fue.png', mask=None, anchor='center',
        ori=0, pos=(0.4, -0.0625), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-25.0)
    number6 = visual.ImageStim(
        win=win,
        name='number6', 
        image='images/Sec.png', mask=None, anchor='center',
        ori=0, pos=(0.4, -0.1875), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-26.0)
    number7 = visual.ImageStim(
        win=win,
        name='number7', 
        image='images/Neu.png', mask=None, anchor='center',
        ori=0, pos=(0.4, -0.3125), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-27.0)
    number8 = visual.ImageStim(
        win=win,
        name='number8', 
        image='images/Nul.png', mask=None, anchor='center',
        ori=0, pos=(0.4, -0.4375), size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-28.0)
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
        texRes=128, interpolate=True, depth=-37.0)
    pp_respGrid = parallel.ParallelPort(address='0x3FE8')
    
    # --- Initialize components for Routine "endBlock" ---
    blockEnds = visual.TextStim(win=win, name='blockEnds',
        text='Blockende',
        font='Arial',
        pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    pp_blockends = parallel.ParallelPort(address='0x3FE8')
    
    # --- Initialize components for Routine "instrRest_POST" ---
    instrRest_post = visual.TextStim(win=win, name='instrRest_post',
        text='Sehr gut!\n------------------------------------------------------------------------------\n\nUm die Aufnahme zu beenden, bitten wir Sie, nochmals 5 Minuten so still wie möglich zu sitzen und die Augen geschlossen zu halten. \n\nEin ‘beep’ wird den Anfang und das Ende der Aufnahme angeben. Bitte sitzen Sie so still wie möglich und halten Sie die Augen geschlossen bis der zweite Ton erklingt.\n\n\n<Klicken Sie auf die Abstandstaste/spacebar um fortzufahren > \n',
        font='Arial',
        pos=(0, 0), height=0.04, wrapWidth=1, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    pp_rest_post = parallel.ParallelPort(address='0x3FE8')
    key_resp_instRest_post = keyboard.Keyboard(deviceName='key_resp_instRest_post')
    
    # --- Initialize components for Routine "restTrial_post" ---
    beep_rest_post_start = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='beep_rest_post_start',    name='beep_rest_post_start'
    )
    beep_rest_post_start.setVolume(1.0)
    fixation_3 = visual.ShapeStim(
        win=win, name='fixation_3', vertices='cross',
        size=(0.05, 0.05),
        ori=0.0, pos=(0, 0), anchor='center',
        lineWidth=0.5,     colorSpace='rgb',  lineColor=[1.0000, -1.0000, -1.0000], fillColor=[1.0000, -1.0000, -1.0000],
        opacity=0.75, depth=-1.0, interpolate=True)
    screenAfterAudio_4 = visual.ImageStim(
        win=win,
        name='screenAfterAudio_4', 
        image='images/grayScreen.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    beep_rest_post_end = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='beep_rest_post_end',    name='beep_rest_post_end'
    )
    beep_rest_post_end.setVolume(1.0)
    pp_rest_pre_start_2 = parallel.ParallelPort(address='0x3FE8')
    
    # --- Initialize components for Routine "thanks_end" ---
    thanksText_end = visual.TextStim(win=win, name='thanksText_end',
        text='Sehr gut!   :  )  \n\nVIELEN DANK für Ihre Kollaboration und Zeit.\n',
        font='Arial',
        pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_6 = keyboard.Keyboard(deviceName='key_resp_6')
    
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
    
    # --- Prepare to start Routine "instrStart" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('instrStart.started', globalClock.getTime(format='float'))
    key_resp_inst_2.keys = []
    key_resp_inst_2.rt = []
    _key_resp_inst_2_allKeys = []
    # Run 'Begin Routine' code from hideMouse_5
    win.mouseVisible = False 
    # keep track of which components have finished
    instrStartComponents = [instr_start, key_resp_inst_2]
    for thisComponent in instrStartComponents:
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
    
    # --- Run Routine "instrStart" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instr_start* updates
        
        # if instr_start is starting this frame...
        if instr_start.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            instr_start.frameNStart = frameN  # exact frame index
            instr_start.tStart = t  # local t and not account for scr refresh
            instr_start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_start, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instr_start.started')
            # update status
            instr_start.status = STARTED
            instr_start.setAutoDraw(True)
        
        # if instr_start is active this frame...
        if instr_start.status == STARTED:
            # update params
            pass
        
        # *key_resp_inst_2* updates
        waitOnFlip = False
        
        # if key_resp_inst_2 is starting this frame...
        if key_resp_inst_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_inst_2.frameNStart = frameN  # exact frame index
            key_resp_inst_2.tStart = t  # local t and not account for scr refresh
            key_resp_inst_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_inst_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_inst_2.started')
            # update status
            key_resp_inst_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_inst_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_inst_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_inst_2.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_inst_2.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_inst_2_allKeys.extend(theseKeys)
            if len(_key_resp_inst_2_allKeys):
                key_resp_inst_2.keys = _key_resp_inst_2_allKeys[-1].name  # just the last key pressed
                key_resp_inst_2.rt = _key_resp_inst_2_allKeys[-1].rt
                key_resp_inst_2.duration = _key_resp_inst_2_allKeys[-1].duration
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
        for thisComponent in instrStartComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instrStart" ---
    for thisComponent in instrStartComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('instrStart.stopped', globalClock.getTime(format='float'))
    thisExp.nextEntry()
    # the Routine "instrStart" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "instrRest_PRE" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('instrRest_PRE.started', globalClock.getTime(format='float'))
    key_resp_instRest_pre.keys = []
    key_resp_instRest_pre.rt = []
    _key_resp_instRest_pre_allKeys = []
    # Run 'Begin Routine' code from hideMouse_3
    win.mouseVisible = False 
    # keep track of which components have finished
    instrRest_PREComponents = [instrRest_pre, key_resp_instRest_pre, pp_instrRest_PRE]
    for thisComponent in instrRest_PREComponents:
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
    
    # --- Run Routine "instrRest_PRE" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instrRest_pre* updates
        
        # if instrRest_pre is starting this frame...
        if instrRest_pre.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            instrRest_pre.frameNStart = frameN  # exact frame index
            instrRest_pre.tStart = t  # local t and not account for scr refresh
            instrRest_pre.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instrRest_pre, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instrRest_pre.started')
            # update status
            instrRest_pre.status = STARTED
            instrRest_pre.setAutoDraw(True)
        
        # if instrRest_pre is active this frame...
        if instrRest_pre.status == STARTED:
            # update params
            pass
        
        # *key_resp_instRest_pre* updates
        waitOnFlip = False
        
        # if key_resp_instRest_pre is starting this frame...
        if key_resp_instRest_pre.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_instRest_pre.frameNStart = frameN  # exact frame index
            key_resp_instRest_pre.tStart = t  # local t and not account for scr refresh
            key_resp_instRest_pre.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_instRest_pre, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_instRest_pre.started')
            # update status
            key_resp_instRest_pre.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_instRest_pre.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_instRest_pre.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_instRest_pre.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_instRest_pre.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_instRest_pre_allKeys.extend(theseKeys)
            if len(_key_resp_instRest_pre_allKeys):
                key_resp_instRest_pre.keys = _key_resp_instRest_pre_allKeys[-1].name  # just the last key pressed
                key_resp_instRest_pre.rt = _key_resp_instRest_pre_allKeys[-1].rt
                key_resp_instRest_pre.duration = _key_resp_instRest_pre_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        # *pp_instrRest_PRE* updates
        
        # if pp_instrRest_PRE is starting this frame...
        if pp_instrRest_PRE.status == NOT_STARTED and instrRest_pre.status==FINISHED:
            # keep track of start time/frame for later
            pp_instrRest_PRE.frameNStart = frameN  # exact frame index
            pp_instrRest_PRE.tStart = t  # local t and not account for scr refresh
            pp_instrRest_PRE.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pp_instrRest_PRE, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'pp_instrRest_PRE.started')
            # update status
            pp_instrRest_PRE.status = STARTED
            pp_instrRest_PRE.status = STARTED
            win.callOnFlip(pp_instrRest_PRE.setData, int(55))
        
        # if pp_instrRest_PRE is stopping this frame...
        if pp_instrRest_PRE.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pp_instrRest_PRE.tStartRefresh + 0.01-frameTolerance:
                # keep track of stop time/frame for later
                pp_instrRest_PRE.tStop = t  # not accounting for scr refresh
                pp_instrRest_PRE.tStopRefresh = tThisFlipGlobal  # on global time
                pp_instrRest_PRE.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'pp_instrRest_PRE.stopped')
                # update status
                pp_instrRest_PRE.status = FINISHED
                win.callOnFlip(pp_instrRest_PRE.setData, int(0))
        
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
        for thisComponent in instrRest_PREComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instrRest_PRE" ---
    for thisComponent in instrRest_PREComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('instrRest_PRE.stopped', globalClock.getTime(format='float'))
    if pp_instrRest_PRE.status == STARTED:
        win.callOnFlip(pp_instrRest_PRE.setData, int(0))
    thisExp.nextEntry()
    # the Routine "instrRest_PRE" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "restTrial_pre" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('restTrial_pre.started', globalClock.getTime(format='float'))
    beep_rest_pre_start.setSound('click_beep.wav', hamming=True)
    beep_rest_pre_start.setVolume(1.0, log=False)
    beep_rest_pre_start.seek(0)
    # Run 'Begin Routine' code from hideMouse_8
    win.mouseVisible = False 
    
    beep_rest_pre_end.setSound('click_beep.wav', hamming=True)
    beep_rest_pre_end.setVolume(1.0, log=False)
    beep_rest_pre_end.seek(0)
    # keep track of which components have finished
    restTrial_preComponents = [beep_rest_pre_start, fixation_1, screenAfterAudio_3, beep_rest_pre_end, pp_rest_pre_start]
    for thisComponent in restTrial_preComponents:
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
    
    # --- Run Routine "restTrial_pre" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # if beep_rest_pre_start is starting this frame...
        if beep_rest_pre_start.status == NOT_STARTED and instrRest_pre.status==FINISHED:
            # keep track of start time/frame for later
            beep_rest_pre_start.frameNStart = frameN  # exact frame index
            beep_rest_pre_start.tStart = t  # local t and not account for scr refresh
            beep_rest_pre_start.tStartRefresh = tThisFlipGlobal  # on global time
            # update status
            beep_rest_pre_start.status = STARTED
            beep_rest_pre_start.play(when=win)  # sync with win flip
        # update beep_rest_pre_start status according to whether it's playing
        if beep_rest_pre_start.isPlaying:
            beep_rest_pre_start.status = STARTED
        elif beep_rest_pre_start.isFinished:
            beep_rest_pre_start.status = FINISHED
        
        # *fixation_1* updates
        
        # if fixation_1 is starting this frame...
        if fixation_1.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            fixation_1.frameNStart = frameN  # exact frame index
            fixation_1.tStart = t  # local t and not account for scr refresh
            fixation_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_1.started')
            # update status
            fixation_1.status = STARTED
            fixation_1.setAutoDraw(True)
        
        # if fixation_1 is active this frame...
        if fixation_1.status == STARTED:
            # update params
            pass
        
        # if fixation_1 is stopping this frame...
        if fixation_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fixation_1.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                fixation_1.tStop = t  # not accounting for scr refresh
                fixation_1.tStopRefresh = tThisFlipGlobal  # on global time
                fixation_1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_1.stopped')
                # update status
                fixation_1.status = FINISHED
                fixation_1.setAutoDraw(False)
        
        # *screenAfterAudio_3* updates
        
        # if screenAfterAudio_3 is starting this frame...
        if screenAfterAudio_3.status == NOT_STARTED and frameN >= fixation_1.status==FINISHED  :
            # keep track of start time/frame for later
            screenAfterAudio_3.frameNStart = frameN  # exact frame index
            screenAfterAudio_3.tStart = t  # local t and not account for scr refresh
            screenAfterAudio_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(screenAfterAudio_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'screenAfterAudio_3.started')
            # update status
            screenAfterAudio_3.status = STARTED
            screenAfterAudio_3.setAutoDraw(True)
        
        # if screenAfterAudio_3 is active this frame...
        if screenAfterAudio_3.status == STARTED:
            # update params
            pass
        
        # if screenAfterAudio_3 is stopping this frame...
        if screenAfterAudio_3.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > 2 -frameTolerance:
                # keep track of stop time/frame for later
                screenAfterAudio_3.tStop = t  # not accounting for scr refresh
                screenAfterAudio_3.tStopRefresh = tThisFlipGlobal  # on global time
                screenAfterAudio_3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'screenAfterAudio_3.stopped')
                # update status
                screenAfterAudio_3.status = FINISHED
                screenAfterAudio_3.setAutoDraw(False)
        
        # if beep_rest_pre_end is starting this frame...
        if beep_rest_pre_end.status == NOT_STARTED and fixation_1.status == FINISHED:
            # keep track of start time/frame for later
            beep_rest_pre_end.frameNStart = frameN  # exact frame index
            beep_rest_pre_end.tStart = t  # local t and not account for scr refresh
            beep_rest_pre_end.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('beep_rest_pre_end.started', tThisFlipGlobal)
            # update status
            beep_rest_pre_end.status = STARTED
            beep_rest_pre_end.play(when=win)  # sync with win flip
        # update beep_rest_pre_end status according to whether it's playing
        if beep_rest_pre_end.isPlaying:
            beep_rest_pre_end.status = STARTED
        elif beep_rest_pre_end.isFinished:
            beep_rest_pre_end.status = FINISHED
        # *pp_rest_pre_start* updates
        
        # if pp_rest_pre_start is starting this frame...
        if pp_rest_pre_start.status == NOT_STARTED and beep_rest_pre_start.status==STARTED:
            # keep track of start time/frame for later
            pp_rest_pre_start.frameNStart = frameN  # exact frame index
            pp_rest_pre_start.tStart = t  # local t and not account for scr refresh
            pp_rest_pre_start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pp_rest_pre_start, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'pp_rest_pre_start.started')
            # update status
            pp_rest_pre_start.status = STARTED
            pp_rest_pre_start.status = STARTED
            win.callOnFlip(pp_rest_pre_start.setData, int(8))
        
        # if pp_rest_pre_start is stopping this frame...
        if pp_rest_pre_start.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pp_rest_pre_start.tStartRefresh + 0.01-frameTolerance:
                # keep track of stop time/frame for later
                pp_rest_pre_start.tStop = t  # not accounting for scr refresh
                pp_rest_pre_start.tStopRefresh = tThisFlipGlobal  # on global time
                pp_rest_pre_start.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'pp_rest_pre_start.stopped')
                # update status
                pp_rest_pre_start.status = FINISHED
                win.callOnFlip(pp_rest_pre_start.setData, int(0))
        
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
        for thisComponent in restTrial_preComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "restTrial_pre" ---
    for thisComponent in restTrial_preComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('restTrial_pre.stopped', globalClock.getTime(format='float'))
    beep_rest_pre_start.pause()  # ensure sound has stopped at end of Routine
    beep_rest_pre_end.pause()  # ensure sound has stopped at end of Routine
    if pp_rest_pre_start.status == STARTED:
        win.callOnFlip(pp_rest_pre_start.setData, int(0))
    thisExp.nextEntry()
    # the Routine "restTrial_pre" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "instrMain_1" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('instrMain_1.started', globalClock.getTime(format='float'))
    key_resp_inst_4.keys = []
    key_resp_inst_4.rt = []
    _key_resp_inst_4_allKeys = []
    # Run 'Begin Routine' code from hideMouse_12
    win.mouseVisible = False 
    # keep track of which components have finished
    instrMain_1Components = [instr_start_1, key_resp_inst_4]
    for thisComponent in instrMain_1Components:
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
    
    # --- Run Routine "instrMain_1" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instr_start_1* updates
        
        # if instr_start_1 is starting this frame...
        if instr_start_1.status == NOT_STARTED and beep_rest_pre_end.status == FINISHED:
            # keep track of start time/frame for later
            instr_start_1.frameNStart = frameN  # exact frame index
            instr_start_1.tStart = t  # local t and not account for scr refresh
            instr_start_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_start_1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instr_start_1.started')
            # update status
            instr_start_1.status = STARTED
            instr_start_1.setAutoDraw(True)
        
        # if instr_start_1 is active this frame...
        if instr_start_1.status == STARTED:
            # update params
            pass
        
        # *key_resp_inst_4* updates
        waitOnFlip = False
        
        # if key_resp_inst_4 is starting this frame...
        if key_resp_inst_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_inst_4.frameNStart = frameN  # exact frame index
            key_resp_inst_4.tStart = t  # local t and not account for scr refresh
            key_resp_inst_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_inst_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_inst_4.started')
            # update status
            key_resp_inst_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_inst_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_inst_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_inst_4.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_inst_4.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_inst_4_allKeys.extend(theseKeys)
            if len(_key_resp_inst_4_allKeys):
                key_resp_inst_4.keys = _key_resp_inst_4_allKeys[-1].name  # just the last key pressed
                key_resp_inst_4.rt = _key_resp_inst_4_allKeys[-1].rt
                key_resp_inst_4.duration = _key_resp_inst_4_allKeys[-1].duration
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
        for thisComponent in instrMain_1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instrMain_1" ---
    for thisComponent in instrMain_1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('instrMain_1.stopped', globalClock.getTime(format='float'))
    thisExp.nextEntry()
    # the Routine "instrMain_1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "instrMain_2" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('instrMain_2.started', globalClock.getTime(format='float'))
    key_resp_inst_3.keys = []
    key_resp_inst_3.rt = []
    _key_resp_inst_3_allKeys = []
    # Run 'Begin Routine' code from hideMouse_7
    win.mouseVisible = False 
    # keep track of which components have finished
    instrMain_2Components = [pp_instr_start_2, instr_start_2, key_resp_inst_3]
    for thisComponent in instrMain_2Components:
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
    
    # --- Run Routine "instrMain_2" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # *pp_instr_start_2* updates
        
        # if pp_instr_start_2 is starting this frame...
        if pp_instr_start_2.status == NOT_STARTED and instr_start_1.status==FINISHED:
            # keep track of start time/frame for later
            pp_instr_start_2.frameNStart = frameN  # exact frame index
            pp_instr_start_2.tStart = t  # local t and not account for scr refresh
            pp_instr_start_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pp_instr_start_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'pp_instr_start_2.started')
            # update status
            pp_instr_start_2.status = STARTED
            pp_instr_start_2.status = STARTED
            win.callOnFlip(pp_instr_start_2.setData, int(55))
        
        # if pp_instr_start_2 is stopping this frame...
        if pp_instr_start_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pp_instr_start_2.tStartRefresh + 0.01-frameTolerance:
                # keep track of stop time/frame for later
                pp_instr_start_2.tStop = t  # not accounting for scr refresh
                pp_instr_start_2.tStopRefresh = tThisFlipGlobal  # on global time
                pp_instr_start_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'pp_instr_start_2.stopped')
                # update status
                pp_instr_start_2.status = FINISHED
                win.callOnFlip(pp_instr_start_2.setData, int(0))
        
        # *instr_start_2* updates
        
        # if instr_start_2 is starting this frame...
        if instr_start_2.status == NOT_STARTED and instr_start_1.status == FINISHED:
            # keep track of start time/frame for later
            instr_start_2.frameNStart = frameN  # exact frame index
            instr_start_2.tStart = t  # local t and not account for scr refresh
            instr_start_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_start_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instr_start_2.started')
            # update status
            instr_start_2.status = STARTED
            instr_start_2.setAutoDraw(True)
        
        # if instr_start_2 is active this frame...
        if instr_start_2.status == STARTED:
            # update params
            pass
        
        # *key_resp_inst_3* updates
        waitOnFlip = False
        
        # if key_resp_inst_3 is starting this frame...
        if key_resp_inst_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_inst_3.frameNStart = frameN  # exact frame index
            key_resp_inst_3.tStart = t  # local t and not account for scr refresh
            key_resp_inst_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_inst_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_inst_3.started')
            # update status
            key_resp_inst_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_inst_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_inst_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_inst_3.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_inst_3.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_inst_3_allKeys.extend(theseKeys)
            if len(_key_resp_inst_3_allKeys):
                key_resp_inst_3.keys = _key_resp_inst_3_allKeys[-1].name  # just the last key pressed
                key_resp_inst_3.rt = _key_resp_inst_3_allKeys[-1].rt
                key_resp_inst_3.duration = _key_resp_inst_3_allKeys[-1].duration
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
        for thisComponent in instrMain_2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instrMain_2" ---
    for thisComponent in instrMain_2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('instrMain_2.stopped', globalClock.getTime(format='float'))
    if pp_instr_start_2.status == STARTED:
        win.callOnFlip(pp_instr_start_2.setData, int(0))
    thisExp.nextEntry()
    # the Routine "instrMain_2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "instrTask" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('instrTask.started', globalClock.getTime(format='float'))
    key_resp_inst.keys = []
    key_resp_inst.rt = []
    _key_resp_inst_allKeys = []
    # Run 'Begin Routine' code from hideMouse
    win.mouseVisible = False 
    # keep track of which components have finished
    instrTaskComponents = [instrTaskText, pp_instrTask, key_resp_inst]
    for thisComponent in instrTaskComponents:
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
    
    # --- Run Routine "instrTask" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instrTaskText* updates
        
        # if instrTaskText is starting this frame...
        if instrTaskText.status == NOT_STARTED and frameN >= 0.0:
            # keep track of start time/frame for later
            instrTaskText.frameNStart = frameN  # exact frame index
            instrTaskText.tStart = t  # local t and not account for scr refresh
            instrTaskText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instrTaskText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instrTaskText.started')
            # update status
            instrTaskText.status = STARTED
            instrTaskText.setAutoDraw(True)
        
        # if instrTaskText is active this frame...
        if instrTaskText.status == STARTED:
            # update params
            pass
        # *pp_instrTask* updates
        
        # if pp_instrTask is starting this frame...
        if pp_instrTask.status == NOT_STARTED and instrTaskText.status==FINISHED:
            # keep track of start time/frame for later
            pp_instrTask.frameNStart = frameN  # exact frame index
            pp_instrTask.tStart = t  # local t and not account for scr refresh
            pp_instrTask.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pp_instrTask, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'pp_instrTask.started')
            # update status
            pp_instrTask.status = STARTED
            pp_instrTask.status = STARTED
            win.callOnFlip(pp_instrTask.setData, int(5))
        
        # if pp_instrTask is stopping this frame...
        if pp_instrTask.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pp_instrTask.tStartRefresh + 0.01-frameTolerance:
                # keep track of stop time/frame for later
                pp_instrTask.tStop = t  # not accounting for scr refresh
                pp_instrTask.tStopRefresh = tThisFlipGlobal  # on global time
                pp_instrTask.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'pp_instrTask.stopped')
                # update status
                pp_instrTask.status = FINISHED
                win.callOnFlip(pp_instrTask.setData, int(0))
        
        # *key_resp_inst* updates
        waitOnFlip = False
        
        # if key_resp_inst is starting this frame...
        if key_resp_inst.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_inst.frameNStart = frameN  # exact frame index
            key_resp_inst.tStart = t  # local t and not account for scr refresh
            key_resp_inst.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_inst, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_inst.started')
            # update status
            key_resp_inst.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_inst.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_inst.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_inst.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_inst.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_inst_allKeys.extend(theseKeys)
            if len(_key_resp_inst_allKeys):
                key_resp_inst.keys = _key_resp_inst_allKeys[-1].name  # just the last key pressed
                key_resp_inst.rt = _key_resp_inst_allKeys[-1].rt
                key_resp_inst.duration = _key_resp_inst_allKeys[-1].duration
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
        for thisComponent in instrTaskComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instrTask" ---
    for thisComponent in instrTaskComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('instrTask.stopped', globalClock.getTime(format='float'))
    if pp_instrTask.status == STARTED:
        win.callOnFlip(pp_instrTask.setData, int(0))
    thisExp.nextEntry()
    # the Routine "instrTask" was not non-slip safe, so reset the non-slip timer
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
        startBlockComponents = [blockStart, pp_blockstart, key_resp]
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
            if blockStart.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
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
            # *pp_blockstart* updates
            
            # if pp_blockstart is starting this frame...
            if pp_blockstart.status == NOT_STARTED and blockStart.status==STARTED:
                # keep track of start time/frame for later
                pp_blockstart.frameNStart = frameN  # exact frame index
                pp_blockstart.tStart = t  # local t and not account for scr refresh
                pp_blockstart.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(pp_blockstart, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'pp_blockstart.started')
                # update status
                pp_blockstart.status = STARTED
                pp_blockstart.status = STARTED
                win.callOnFlip(pp_blockstart.setData, int(6))
            
            # if pp_blockstart is stopping this frame...
            if pp_blockstart.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > pp_blockstart.tStartRefresh + 0.01-frameTolerance:
                    # keep track of stop time/frame for later
                    pp_blockstart.tStop = t  # not accounting for scr refresh
                    pp_blockstart.tStopRefresh = tThisFlipGlobal  # on global time
                    pp_blockstart.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_blockstart.stopped')
                    # update status
                    pp_blockstart.status = FINISHED
                    win.callOnFlip(pp_blockstart.setData, int(0))
            
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
        if pp_blockstart.status == STARTED:
            win.callOnFlip(pp_blockstart.setData, int(0))
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
            # Run 'Begin Routine' code from code
            # Detect trial start time 
            myClock = core.Clock()
            now = myClock.getTime()
            pp_start_time = now
            
            
            # Run 'Begin Routine' code from hideMouse_2
            win.mouseVisible = False 
            
            # keep track of which components have finished
            audioTrialComponents = [sound_1, fixation, screenAfterAudio, pp_start, pp_t0_start, pp_t1_start, pp_t1_end, pp_t2_start, pp_t2_end, pp_t3_start, pp_end]
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
                if sound_1.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
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
                # *pp_start* updates
                
                # if pp_start is starting this frame...
                if pp_start.status == NOT_STARTED and pp_start_time + 0.08:
                    # keep track of start time/frame for later
                    pp_start.frameNStart = frameN  # exact frame index
                    pp_start.tStart = t  # local t and not account for scr refresh
                    pp_start.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(pp_start, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_start.started')
                    # update status
                    pp_start.status = STARTED
                    pp_start.status = STARTED
                    win.callOnFlip(pp_start.setData, int(1))
                
                # if pp_start is stopping this frame...
                if pp_start.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > pp_start.tStartRefresh + 0.01-frameTolerance:
                        # keep track of stop time/frame for later
                        pp_start.tStop = t  # not accounting for scr refresh
                        pp_start.tStopRefresh = tThisFlipGlobal  # on global time
                        pp_start.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'pp_start.stopped')
                        # update status
                        pp_start.status = FINISHED
                        win.callOnFlip(pp_start.setData, int(0))
                # *pp_t0_start* updates
                
                # if pp_t0_start is starting this frame...
                if pp_t0_start.status == NOT_STARTED and tThisFlip >= firstSound_tmin-frameTolerance:
                    # keep track of start time/frame for later
                    pp_t0_start.frameNStart = frameN  # exact frame index
                    pp_t0_start.tStart = t  # local t and not account for scr refresh
                    pp_t0_start.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(pp_t0_start, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_t0_start.started')
                    # update status
                    pp_t0_start.status = STARTED
                    pp_t0_start.status = STARTED
                    win.callOnFlip(pp_t0_start.setData, int(trigger_start))
                
                # if pp_t0_start is stopping this frame...
                if pp_t0_start.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > pp_t0_start.tStartRefresh + 0.01-frameTolerance:
                        # keep track of stop time/frame for later
                        pp_t0_start.tStop = t  # not accounting for scr refresh
                        pp_t0_start.tStopRefresh = tThisFlipGlobal  # on global time
                        pp_t0_start.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'pp_t0_start.stopped')
                        # update status
                        pp_t0_start.status = FINISHED
                        win.callOnFlip(pp_t0_start.setData, int(0))
                # *pp_t1_start* updates
                
                # if pp_t1_start is starting this frame...
                if pp_t1_start.status == NOT_STARTED and tThisFlip >= token_1_tmin-frameTolerance:
                    # keep track of start time/frame for later
                    pp_t1_start.frameNStart = frameN  # exact frame index
                    pp_t1_start.tStart = t  # local t and not account for scr refresh
                    pp_t1_start.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(pp_t1_start, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_t1_start.started')
                    # update status
                    pp_t1_start.status = STARTED
                    pp_t1_start.status = STARTED
                    win.callOnFlip(pp_t1_start.setData, int(trigger_call))
                
                # if pp_t1_start is stopping this frame...
                if pp_t1_start.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > pp_t1_start.tStartRefresh + 0.01-frameTolerance:
                        # keep track of stop time/frame for later
                        pp_t1_start.tStop = t  # not accounting for scr refresh
                        pp_t1_start.tStopRefresh = tThisFlipGlobal  # on global time
                        pp_t1_start.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'pp_t1_start.stopped')
                        # update status
                        pp_t1_start.status = FINISHED
                        win.callOnFlip(pp_t1_start.setData, int(0))
                # *pp_t1_end* updates
                
                # if pp_t1_end is starting this frame...
                if pp_t1_end.status == NOT_STARTED and tThisFlip >= token_1_tmax-frameTolerance:
                    # keep track of start time/frame for later
                    pp_t1_end.frameNStart = frameN  # exact frame index
                    pp_t1_end.tStart = t  # local t and not account for scr refresh
                    pp_t1_end.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(pp_t1_end, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_t1_end.started')
                    # update status
                    pp_t1_end.status = STARTED
                    pp_t1_end.status = STARTED
                    win.callOnFlip(pp_t1_end.setData, int(trigger_call_end))
                
                # if pp_t1_end is stopping this frame...
                if pp_t1_end.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > pp_t1_end.tStartRefresh + 0.01-frameTolerance:
                        # keep track of stop time/frame for later
                        pp_t1_end.tStop = t  # not accounting for scr refresh
                        pp_t1_end.tStopRefresh = tThisFlipGlobal  # on global time
                        pp_t1_end.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'pp_t1_end.stopped')
                        # update status
                        pp_t1_end.status = FINISHED
                        win.callOnFlip(pp_t1_end.setData, int(0))
                # *pp_t2_start* updates
                
                # if pp_t2_start is starting this frame...
                if pp_t2_start.status == NOT_STARTED and tThisFlip >= token_2_tmin-frameTolerance:
                    # keep track of start time/frame for later
                    pp_t2_start.frameNStart = frameN  # exact frame index
                    pp_t2_start.tStart = t  # local t and not account for scr refresh
                    pp_t2_start.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(pp_t2_start, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_t2_start.started')
                    # update status
                    pp_t2_start.status = STARTED
                    pp_t2_start.status = STARTED
                    win.callOnFlip(pp_t2_start.setData, int(trigger_col))
                
                # if pp_t2_start is stopping this frame...
                if pp_t2_start.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > pp_t2_start.tStartRefresh + 0.01-frameTolerance:
                        # keep track of stop time/frame for later
                        pp_t2_start.tStop = t  # not accounting for scr refresh
                        pp_t2_start.tStopRefresh = tThisFlipGlobal  # on global time
                        pp_t2_start.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'pp_t2_start.stopped')
                        # update status
                        pp_t2_start.status = FINISHED
                        win.callOnFlip(pp_t2_start.setData, int(0))
                # *pp_t2_end* updates
                
                # if pp_t2_end is starting this frame...
                if pp_t2_end.status == NOT_STARTED and tThisFlip >= token_2_tmax-frameTolerance:
                    # keep track of start time/frame for later
                    pp_t2_end.frameNStart = frameN  # exact frame index
                    pp_t2_end.tStart = t  # local t and not account for scr refresh
                    pp_t2_end.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(pp_t2_end, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_t2_end.started')
                    # update status
                    pp_t2_end.status = STARTED
                    pp_t2_end.status = STARTED
                    win.callOnFlip(pp_t2_end.setData, int(trigger_col_end))
                
                # if pp_t2_end is stopping this frame...
                if pp_t2_end.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > pp_t2_end.tStartRefresh + 0.01-frameTolerance:
                        # keep track of stop time/frame for later
                        pp_t2_end.tStop = t  # not accounting for scr refresh
                        pp_t2_end.tStopRefresh = tThisFlipGlobal  # on global time
                        pp_t2_end.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'pp_t2_end.stopped')
                        # update status
                        pp_t2_end.status = FINISHED
                        win.callOnFlip(pp_t2_end.setData, int(0))
                # *pp_t3_start* updates
                
                # if pp_t3_start is starting this frame...
                if pp_t3_start.status == NOT_STARTED and tThisFlip >= token_3_tmin-frameTolerance:
                    # keep track of start time/frame for later
                    pp_t3_start.frameNStart = frameN  # exact frame index
                    pp_t3_start.tStart = t  # local t and not account for scr refresh
                    pp_t3_start.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(pp_t3_start, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_t3_start.started')
                    # update status
                    pp_t3_start.status = STARTED
                    pp_t3_start.status = STARTED
                    win.callOnFlip(pp_t3_start.setData, int(trigger_num))
                
                # if pp_t3_start is stopping this frame...
                if pp_t3_start.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > pp_t3_start.tStartRefresh + 0.01-frameTolerance:
                        # keep track of stop time/frame for later
                        pp_t3_start.tStop = t  # not accounting for scr refresh
                        pp_t3_start.tStopRefresh = tThisFlipGlobal  # on global time
                        pp_t3_start.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'pp_t3_start.stopped')
                        # update status
                        pp_t3_start.status = FINISHED
                        win.callOnFlip(pp_t3_start.setData, int(0))
                # *pp_end* updates
                
                # if pp_end is starting this frame...
                if pp_end.status == NOT_STARTED and tThisFlip >= lastSound_tmax-frameTolerance:
                    # keep track of start time/frame for later
                    pp_end.frameNStart = frameN  # exact frame index
                    pp_end.tStart = t  # local t and not account for scr refresh
                    pp_end.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(pp_end, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_end.started')
                    # update status
                    pp_end.status = STARTED
                    pp_end.status = STARTED
                    win.callOnFlip(pp_end.setData, int(trigger_end))
                
                # if pp_end is stopping this frame...
                if pp_end.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > pp_end.tStartRefresh + 0.01-frameTolerance:
                        # keep track of stop time/frame for later
                        pp_end.tStop = t  # not accounting for scr refresh
                        pp_end.tStopRefresh = tThisFlipGlobal  # on global time
                        pp_end.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'pp_end.stopped')
                        # update status
                        pp_end.status = FINISHED
                        win.callOnFlip(pp_end.setData, int(0))
                
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
            if pp_start.status == STARTED:
                win.callOnFlip(pp_start.setData, int(0))
            if pp_t0_start.status == STARTED:
                win.callOnFlip(pp_t0_start.setData, int(0))
            if pp_t1_start.status == STARTED:
                win.callOnFlip(pp_t1_start.setData, int(0))
            if pp_t1_end.status == STARTED:
                win.callOnFlip(pp_t1_end.setData, int(0))
            if pp_t2_start.status == STARTED:
                win.callOnFlip(pp_t2_start.setData, int(0))
            if pp_t2_end.status == STARTED:
                win.callOnFlip(pp_t2_end.setData, int(0))
            if pp_t3_start.status == STARTED:
                win.callOnFlip(pp_t3_start.setData, int(0))
            if pp_end.status == STARTED:
                win.callOnFlip(pp_end.setData, int(0))
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
            call5.opacity = 1
            call6.opacity = 1
            call7.opacity = 1
            call8.opacity = 1
            
            colour1.opacity = 1
            colour2.opacity = 1
            colour3.opacity = 1
            colour4.opacity = 1
            colour5.opacity = 1
            colour6.opacity = 1
            colour7.opacity = 1
            colour8.opacity = 1
            
            number1.opacity = 1
            number2.opacity = 1
            number3.opacity = 1
            number4.opacity = 1
            number5.opacity = 1
            number6.opacity = 1
            number7.opacity = 1
            number8.opacity = 1
            # Run 'Begin Routine' code from switchToNextTrialAfterResponseTimeOver
            participantResponseTime = None
            trialClock = core.Clock()
            # Run 'Begin Routine' code from printoutCorrectAnswersForDebugging
            print("%s, %s, %s" % (callSign,colour,number))
            call1.setImage('images/Adl.png')
            call8.setImage('images/Gab.png')
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
            trialComponents = [blankScreen, call1, call2, call3, call4, call5, call6, call7, call8, colour1, colour2, colour3, colour4, colour5, colour6, colour7, colour8, number1, number2, number3, number4, number5, number6, number7, number8, mouseClickOnCall, mouseClickOnColour, mouseClickOnNumber, blankScreenAfterResponse, pp_respGrid]
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
                
                # *call5* updates
                
                # if call5 is starting this frame...
                if call5.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    call5.frameNStart = frameN  # exact frame index
                    call5.tStart = t  # local t and not account for scr refresh
                    call5.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(call5, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'call5.started')
                    # update status
                    call5.status = STARTED
                    call5.setAutoDraw(True)
                
                # if call5 is active this frame...
                if call5.status == STARTED:
                    # update params
                    pass
                
                # if call5 is stopping this frame...
                if call5.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        call5.tStop = t  # not accounting for scr refresh
                        call5.tStopRefresh = tThisFlipGlobal  # on global time
                        call5.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'call5.stopped')
                        # update status
                        call5.status = FINISHED
                        call5.setAutoDraw(False)
                
                # *call6* updates
                
                # if call6 is starting this frame...
                if call6.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    call6.frameNStart = frameN  # exact frame index
                    call6.tStart = t  # local t and not account for scr refresh
                    call6.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(call6, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'call6.started')
                    # update status
                    call6.status = STARTED
                    call6.setAutoDraw(True)
                
                # if call6 is active this frame...
                if call6.status == STARTED:
                    # update params
                    pass
                
                # if call6 is stopping this frame...
                if call6.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        call6.tStop = t  # not accounting for scr refresh
                        call6.tStopRefresh = tThisFlipGlobal  # on global time
                        call6.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'call6.stopped')
                        # update status
                        call6.status = FINISHED
                        call6.setAutoDraw(False)
                
                # *call7* updates
                
                # if call7 is starting this frame...
                if call7.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    call7.frameNStart = frameN  # exact frame index
                    call7.tStart = t  # local t and not account for scr refresh
                    call7.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(call7, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'call7.started')
                    # update status
                    call7.status = STARTED
                    call7.setAutoDraw(True)
                
                # if call7 is active this frame...
                if call7.status == STARTED:
                    # update params
                    pass
                
                # if call7 is stopping this frame...
                if call7.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        call7.tStop = t  # not accounting for scr refresh
                        call7.tStopRefresh = tThisFlipGlobal  # on global time
                        call7.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'call7.stopped')
                        # update status
                        call7.status = FINISHED
                        call7.setAutoDraw(False)
                
                # *call8* updates
                
                # if call8 is starting this frame...
                if call8.status == NOT_STARTED and blankScreen.status==FINISHED:
                    # keep track of start time/frame for later
                    call8.frameNStart = frameN  # exact frame index
                    call8.tStart = t  # local t and not account for scr refresh
                    call8.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(call8, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'call8.started')
                    # update status
                    call8.status = STARTED
                    call8.setAutoDraw(True)
                
                # if call8 is active this frame...
                if call8.status == STARTED:
                    # update params
                    pass
                
                # if call8 is stopping this frame...
                if call8.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        call8.tStop = t  # not accounting for scr refresh
                        call8.tStopRefresh = tThisFlipGlobal  # on global time
                        call8.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'call8.stopped')
                        # update status
                        call8.status = FINISHED
                        call8.setAutoDraw(False)
                
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
                
                # *colour5* updates
                
                # if colour5 is starting this frame...
                if colour5.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    colour5.frameNStart = frameN  # exact frame index
                    colour5.tStart = t  # local t and not account for scr refresh
                    colour5.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(colour5, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colour5.started')
                    # update status
                    colour5.status = STARTED
                    colour5.setAutoDraw(True)
                
                # if colour5 is active this frame...
                if colour5.status == STARTED:
                    # update params
                    pass
                
                # if colour5 is stopping this frame...
                if colour5.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        colour5.tStop = t  # not accounting for scr refresh
                        colour5.tStopRefresh = tThisFlipGlobal  # on global time
                        colour5.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'colour5.stopped')
                        # update status
                        colour5.status = FINISHED
                        colour5.setAutoDraw(False)
                
                # *colour6* updates
                
                # if colour6 is starting this frame...
                if colour6.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    colour6.frameNStart = frameN  # exact frame index
                    colour6.tStart = t  # local t and not account for scr refresh
                    colour6.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(colour6, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colour6.started')
                    # update status
                    colour6.status = STARTED
                    colour6.setAutoDraw(True)
                
                # if colour6 is active this frame...
                if colour6.status == STARTED:
                    # update params
                    pass
                
                # if colour6 is stopping this frame...
                if colour6.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        colour6.tStop = t  # not accounting for scr refresh
                        colour6.tStopRefresh = tThisFlipGlobal  # on global time
                        colour6.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'colour6.stopped')
                        # update status
                        colour6.status = FINISHED
                        colour6.setAutoDraw(False)
                
                # *colour7* updates
                
                # if colour7 is starting this frame...
                if colour7.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    colour7.frameNStart = frameN  # exact frame index
                    colour7.tStart = t  # local t and not account for scr refresh
                    colour7.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(colour7, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colour7.started')
                    # update status
                    colour7.status = STARTED
                    colour7.setAutoDraw(True)
                
                # if colour7 is active this frame...
                if colour7.status == STARTED:
                    # update params
                    pass
                
                # if colour7 is stopping this frame...
                if colour7.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        colour7.tStop = t  # not accounting for scr refresh
                        colour7.tStopRefresh = tThisFlipGlobal  # on global time
                        colour7.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'colour7.stopped')
                        # update status
                        colour7.status = FINISHED
                        colour7.setAutoDraw(False)
                
                # *colour8* updates
                
                # if colour8 is starting this frame...
                if colour8.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    colour8.frameNStart = frameN  # exact frame index
                    colour8.tStart = t  # local t and not account for scr refresh
                    colour8.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(colour8, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colour8.started')
                    # update status
                    colour8.status = STARTED
                    colour8.setAutoDraw(True)
                
                # if colour8 is active this frame...
                if colour8.status == STARTED:
                    # update params
                    pass
                
                # if colour8 is stopping this frame...
                if colour8.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        colour8.tStop = t  # not accounting for scr refresh
                        colour8.tStopRefresh = tThisFlipGlobal  # on global time
                        colour8.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'colour8.stopped')
                        # update status
                        colour8.status = FINISHED
                        colour8.setAutoDraw(False)
                
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
                
                # *number5* updates
                
                # if number5 is starting this frame...
                if number5.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    number5.frameNStart = frameN  # exact frame index
                    number5.tStart = t  # local t and not account for scr refresh
                    number5.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(number5, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'number5.started')
                    # update status
                    number5.status = STARTED
                    number5.setAutoDraw(True)
                
                # if number5 is active this frame...
                if number5.status == STARTED:
                    # update params
                    pass
                
                # if number5 is stopping this frame...
                if number5.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        number5.tStop = t  # not accounting for scr refresh
                        number5.tStopRefresh = tThisFlipGlobal  # on global time
                        number5.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'number5.stopped')
                        # update status
                        number5.status = FINISHED
                        number5.setAutoDraw(False)
                
                # *number6* updates
                
                # if number6 is starting this frame...
                if number6.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    number6.frameNStart = frameN  # exact frame index
                    number6.tStart = t  # local t and not account for scr refresh
                    number6.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(number6, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'number6.started')
                    # update status
                    number6.status = STARTED
                    number6.setAutoDraw(True)
                
                # if number6 is active this frame...
                if number6.status == STARTED:
                    # update params
                    pass
                
                # if number6 is stopping this frame...
                if number6.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        number6.tStop = t  # not accounting for scr refresh
                        number6.tStopRefresh = tThisFlipGlobal  # on global time
                        number6.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'number6.stopped')
                        # update status
                        number6.status = FINISHED
                        number6.setAutoDraw(False)
                
                # *number7* updates
                
                # if number7 is starting this frame...
                if number7.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    number7.frameNStart = frameN  # exact frame index
                    number7.tStart = t  # local t and not account for scr refresh
                    number7.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(number7, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'number7.started')
                    # update status
                    number7.status = STARTED
                    number7.setAutoDraw(True)
                
                # if number7 is active this frame...
                if number7.status == STARTED:
                    # update params
                    pass
                
                # if number7 is stopping this frame...
                if number7.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        number7.tStop = t  # not accounting for scr refresh
                        number7.tStopRefresh = tThisFlipGlobal  # on global time
                        number7.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'number7.stopped')
                        # update status
                        number7.status = FINISHED
                        number7.setAutoDraw(False)
                
                # *number8* updates
                
                # if number8 is starting this frame...
                if number8.status == NOT_STARTED and blankScreen.status ==FINISHED:
                    # keep track of start time/frame for later
                    number8.frameNStart = frameN  # exact frame index
                    number8.tStart = t  # local t and not account for scr refresh
                    number8.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(number8, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'number8.started')
                    # update status
                    number8.status = STARTED
                    number8.setAutoDraw(True)
                
                # if number8 is active this frame...
                if number8.status == STARTED:
                    # update params
                    pass
                
                # if number8 is stopping this frame...
                if number8.status == STARTED:
                    if bool(blankScreenAfterResponse.status == STARTED):
                        # keep track of stop time/frame for later
                        number8.tStop = t  # not accounting for scr refresh
                        number8.tStopRefresh = tThisFlipGlobal  # on global time
                        number8.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'number8.stopped')
                        # update status
                        number8.status = FINISHED
                        number8.setAutoDraw(False)
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
                            clickableList = environmenttools.getFromNames([call1, call2, call3, call4, call5, call6, call7, call8], namespace=locals())
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
                                if call5.name != mouseClickOnCall.clicked_name[-1]: call5.opacity = 0.2
                                if call6.name != mouseClickOnCall.clicked_name[-1]: call6.opacity = 0.2
                                if call7.name != mouseClickOnCall.clicked_name[-1]: call7.opacity = 0.2
                                if call8.name != mouseClickOnCall.clicked_name[-1]: call8.opacity = 0.2
                                continueRoutine = True
                # *mouseClickOnColour* updates
                
                # if mouseClickOnColour is starting this frame...
                if mouseClickOnColour.status == NOT_STARTED and mouseClickOnCall.status == FINISHED:
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
                            clickableList = environmenttools.getFromNames([colour1, colour2, colour3, colour4, colour5, colour6, colour7, colour8], namespace=locals())
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
                                if colour5.name != mouseClickOnColour.clicked_name[-1]: colour5.opacity = 0.2
                                if colour6.name != mouseClickOnColour.clicked_name[-1]: colour6.opacity = 0.2
                                if colour7.name != mouseClickOnColour.clicked_name[-1]: colour7.opacity = 0.2
                                if colour8.name != mouseClickOnColour.clicked_name[-1]: colour8.opacity = 0.2
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
                            clickableList = environmenttools.getFromNames([number1, number2, number3, number4, number5, number6, number7, number8], namespace=locals())
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
                                if number5.name != mouseClickOnNumber.clicked_name[-1]: number5.opacity = 0.2
                                if number6.name != mouseClickOnNumber.clicked_name[-1]: number6.opacity = 0.2
                                if number7.name != mouseClickOnNumber.clicked_name[-1]: number7.opacity = 0.2
                                if number8.name != mouseClickOnNumber.clicked_name[-1]: number8.opacity = 0.2
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
                # *pp_respGrid* updates
                
                # if pp_respGrid is starting this frame...
                if pp_respGrid.status == NOT_STARTED and blankScreen.status==FINISHED:
                    # keep track of start time/frame for later
                    pp_respGrid.frameNStart = frameN  # exact frame index
                    pp_respGrid.tStart = t  # local t and not account for scr refresh
                    pp_respGrid.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(pp_respGrid, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_respGrid.started')
                    # update status
                    pp_respGrid.status = STARTED
                    pp_respGrid.status = STARTED
                    win.callOnFlip(pp_respGrid.setData, int(7))
                
                # if pp_respGrid is stopping this frame...
                if pp_respGrid.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > pp_respGrid.tStartRefresh + 0.01-frameTolerance:
                        # keep track of stop time/frame for later
                        pp_respGrid.tStop = t  # not accounting for scr refresh
                        pp_respGrid.tStopRefresh = tThisFlipGlobal  # on global time
                        pp_respGrid.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'pp_respGrid.stopped')
                        # update status
                        pp_respGrid.status = FINISHED
                        win.callOnFlip(pp_respGrid.setData, int(0))
                
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
            if pp_respGrid.status == STARTED:
                win.callOnFlip(pp_respGrid.setData, int(0))
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
        
        # --- Prepare to start Routine "endBlock" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('endBlock.started', globalClock.getTime(format='float'))
        # Run 'Begin Routine' code from hideMouse_10
        win.mouseVisible = False 
        # keep track of which components have finished
        endBlockComponents = [blockEnds, pp_blockends]
        for thisComponent in endBlockComponents:
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
        
        # --- Run Routine "endBlock" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blockEnds* updates
            
            # if blockEnds is starting this frame...
            if blockEnds.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                blockEnds.frameNStart = frameN  # exact frame index
                blockEnds.tStart = t  # local t and not account for scr refresh
                blockEnds.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blockEnds, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blockEnds.started')
                # update status
                blockEnds.status = STARTED
                blockEnds.setAutoDraw(True)
            
            # if blockEnds is active this frame...
            if blockEnds.status == STARTED:
                # update params
                pass
            
            # if blockEnds is stopping this frame...
            if blockEnds.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > blockEnds.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    blockEnds.tStop = t  # not accounting for scr refresh
                    blockEnds.tStopRefresh = tThisFlipGlobal  # on global time
                    blockEnds.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blockEnds.stopped')
                    # update status
                    blockEnds.status = FINISHED
                    blockEnds.setAutoDraw(False)
            # *pp_blockends* updates
            
            # if pp_blockends is starting this frame...
            if pp_blockends.status == NOT_STARTED and blockEnds.status==FINISHED:
                # keep track of start time/frame for later
                pp_blockends.frameNStart = frameN  # exact frame index
                pp_blockends.tStart = t  # local t and not account for scr refresh
                pp_blockends.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(pp_blockends, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'pp_blockends.started')
                # update status
                pp_blockends.status = STARTED
                pp_blockends.status = STARTED
                win.callOnFlip(pp_blockends.setData, int(60))
            
            # if pp_blockends is stopping this frame...
            if pp_blockends.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > pp_blockends.tStartRefresh + 0.01-frameTolerance:
                    # keep track of stop time/frame for later
                    pp_blockends.tStop = t  # not accounting for scr refresh
                    pp_blockends.tStopRefresh = tThisFlipGlobal  # on global time
                    pp_blockends.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'pp_blockends.stopped')
                    # update status
                    pp_blockends.status = FINISHED
                    win.callOnFlip(pp_blockends.setData, int(0))
            
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
            for thisComponent in endBlockComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "endBlock" ---
        for thisComponent in endBlockComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('endBlock.stopped', globalClock.getTime(format='float'))
        if pp_blockends.status == STARTED:
            win.callOnFlip(pp_blockends.setData, int(0))
        # the Routine "endBlock" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed 1.0 repeats of 'blocks'
    
    
    # --- Prepare to start Routine "instrRest_POST" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('instrRest_POST.started', globalClock.getTime(format='float'))
    key_resp_instRest_post.keys = []
    key_resp_instRest_post.rt = []
    _key_resp_instRest_post_allKeys = []
    # Run 'Begin Routine' code from hideMouse_4
    win.mouseVisible = False 
    # keep track of which components have finished
    instrRest_POSTComponents = [instrRest_post, pp_rest_post, key_resp_instRest_post]
    for thisComponent in instrRest_POSTComponents:
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
    
    # --- Run Routine "instrRest_POST" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instrRest_post* updates
        
        # if instrRest_post is starting this frame...
        if instrRest_post.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instrRest_post.frameNStart = frameN  # exact frame index
            instrRest_post.tStart = t  # local t and not account for scr refresh
            instrRest_post.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instrRest_post, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instrRest_post.started')
            # update status
            instrRest_post.status = STARTED
            instrRest_post.setAutoDraw(True)
        
        # if instrRest_post is active this frame...
        if instrRest_post.status == STARTED:
            # update params
            pass
        # *pp_rest_post* updates
        
        # if pp_rest_post is starting this frame...
        if pp_rest_post.status == NOT_STARTED and instrRest_post.status == STARTED:
            # keep track of start time/frame for later
            pp_rest_post.frameNStart = frameN  # exact frame index
            pp_rest_post.tStart = t  # local t and not account for scr refresh
            pp_rest_post.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pp_rest_post, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'pp_rest_post.started')
            # update status
            pp_rest_post.status = STARTED
            pp_rest_post.status = STARTED
            win.callOnFlip(pp_rest_post.setData, int(55))
        
        # if pp_rest_post is stopping this frame...
        if pp_rest_post.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pp_rest_post.tStartRefresh + 0.01-frameTolerance:
                # keep track of stop time/frame for later
                pp_rest_post.tStop = t  # not accounting for scr refresh
                pp_rest_post.tStopRefresh = tThisFlipGlobal  # on global time
                pp_rest_post.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'pp_rest_post.stopped')
                # update status
                pp_rest_post.status = FINISHED
                win.callOnFlip(pp_rest_post.setData, int(0))
        
        # *key_resp_instRest_post* updates
        waitOnFlip = False
        
        # if key_resp_instRest_post is starting this frame...
        if key_resp_instRest_post.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_instRest_post.frameNStart = frameN  # exact frame index
            key_resp_instRest_post.tStart = t  # local t and not account for scr refresh
            key_resp_instRest_post.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_instRest_post, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_instRest_post.started')
            # update status
            key_resp_instRest_post.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_instRest_post.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_instRest_post.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_instRest_post.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_instRest_post.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_instRest_post_allKeys.extend(theseKeys)
            if len(_key_resp_instRest_post_allKeys):
                key_resp_instRest_post.keys = _key_resp_instRest_post_allKeys[-1].name  # just the last key pressed
                key_resp_instRest_post.rt = _key_resp_instRest_post_allKeys[-1].rt
                key_resp_instRest_post.duration = _key_resp_instRest_post_allKeys[-1].duration
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
        for thisComponent in instrRest_POSTComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instrRest_POST" ---
    for thisComponent in instrRest_POSTComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('instrRest_POST.stopped', globalClock.getTime(format='float'))
    if pp_rest_post.status == STARTED:
        win.callOnFlip(pp_rest_post.setData, int(0))
    thisExp.nextEntry()
    # the Routine "instrRest_POST" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "restTrial_post" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('restTrial_post.started', globalClock.getTime(format='float'))
    beep_rest_post_start.setSound('click_beep.wav', hamming=True)
    beep_rest_post_start.setVolume(1.0, log=False)
    beep_rest_post_start.seek(0)
    # Run 'Begin Routine' code from hideMouse_9
    win.mouseVisible = False 
    
    beep_rest_post_end.setSound('click_beep.wav', hamming=True)
    beep_rest_post_end.setVolume(1.0, log=False)
    beep_rest_post_end.seek(0)
    # keep track of which components have finished
    restTrial_postComponents = [beep_rest_post_start, fixation_3, screenAfterAudio_4, beep_rest_post_end, pp_rest_pre_start_2]
    for thisComponent in restTrial_postComponents:
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
    
    # --- Run Routine "restTrial_post" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # if beep_rest_post_start is starting this frame...
        if beep_rest_post_start.status == NOT_STARTED and instrRest_post.status == FINISHED:
            # keep track of start time/frame for later
            beep_rest_post_start.frameNStart = frameN  # exact frame index
            beep_rest_post_start.tStart = t  # local t and not account for scr refresh
            beep_rest_post_start.tStartRefresh = tThisFlipGlobal  # on global time
            # update status
            beep_rest_post_start.status = STARTED
            beep_rest_post_start.play(when=win)  # sync with win flip
        # update beep_rest_post_start status according to whether it's playing
        if beep_rest_post_start.isPlaying:
            beep_rest_post_start.status = STARTED
        elif beep_rest_post_start.isFinished:
            beep_rest_post_start.status = FINISHED
        
        # *fixation_3* updates
        
        # if fixation_3 is starting this frame...
        if fixation_3.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            fixation_3.frameNStart = frameN  # exact frame index
            fixation_3.tStart = t  # local t and not account for scr refresh
            fixation_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_3.started')
            # update status
            fixation_3.status = STARTED
            fixation_3.setAutoDraw(True)
        
        # if fixation_3 is active this frame...
        if fixation_3.status == STARTED:
            # update params
            pass
        
        # if fixation_3 is stopping this frame...
        if fixation_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fixation_3.tStartRefresh + 300-frameTolerance:
                # keep track of stop time/frame for later
                fixation_3.tStop = t  # not accounting for scr refresh
                fixation_3.tStopRefresh = tThisFlipGlobal  # on global time
                fixation_3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_3.stopped')
                # update status
                fixation_3.status = FINISHED
                fixation_3.setAutoDraw(False)
        
        # *screenAfterAudio_4* updates
        
        # if screenAfterAudio_4 is starting this frame...
        if screenAfterAudio_4.status == NOT_STARTED and frameN >= fixation_3.status==FINISHED  :
            # keep track of start time/frame for later
            screenAfterAudio_4.frameNStart = frameN  # exact frame index
            screenAfterAudio_4.tStart = t  # local t and not account for scr refresh
            screenAfterAudio_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(screenAfterAudio_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'screenAfterAudio_4.started')
            # update status
            screenAfterAudio_4.status = STARTED
            screenAfterAudio_4.setAutoDraw(True)
        
        # if screenAfterAudio_4 is active this frame...
        if screenAfterAudio_4.status == STARTED:
            # update params
            pass
        
        # if screenAfterAudio_4 is stopping this frame...
        if screenAfterAudio_4.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > 2-frameTolerance:
                # keep track of stop time/frame for later
                screenAfterAudio_4.tStop = t  # not accounting for scr refresh
                screenAfterAudio_4.tStopRefresh = tThisFlipGlobal  # on global time
                screenAfterAudio_4.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'screenAfterAudio_4.stopped')
                # update status
                screenAfterAudio_4.status = FINISHED
                screenAfterAudio_4.setAutoDraw(False)
        
        # if beep_rest_post_end is starting this frame...
        if beep_rest_post_end.status == NOT_STARTED and fixation_3.status == FINISHED:
            # keep track of start time/frame for later
            beep_rest_post_end.frameNStart = frameN  # exact frame index
            beep_rest_post_end.tStart = t  # local t and not account for scr refresh
            beep_rest_post_end.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('beep_rest_post_end.started', tThisFlipGlobal)
            # update status
            beep_rest_post_end.status = STARTED
            beep_rest_post_end.play(when=win)  # sync with win flip
        # update beep_rest_post_end status according to whether it's playing
        if beep_rest_post_end.isPlaying:
            beep_rest_post_end.status = STARTED
        elif beep_rest_post_end.isFinished:
            beep_rest_post_end.status = FINISHED
        # *pp_rest_pre_start_2* updates
        
        # if pp_rest_pre_start_2 is starting this frame...
        if pp_rest_pre_start_2.status == NOT_STARTED and beep_rest_post_start.status==STARTED:
            # keep track of start time/frame for later
            pp_rest_pre_start_2.frameNStart = frameN  # exact frame index
            pp_rest_pre_start_2.tStart = t  # local t and not account for scr refresh
            pp_rest_pre_start_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pp_rest_pre_start_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'pp_rest_pre_start_2.started')
            # update status
            pp_rest_pre_start_2.status = STARTED
            pp_rest_pre_start_2.status = STARTED
            win.callOnFlip(pp_rest_pre_start_2.setData, int(9))
        
        # if pp_rest_pre_start_2 is stopping this frame...
        if pp_rest_pre_start_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pp_rest_pre_start_2.tStartRefresh + 0.01-frameTolerance:
                # keep track of stop time/frame for later
                pp_rest_pre_start_2.tStop = t  # not accounting for scr refresh
                pp_rest_pre_start_2.tStopRefresh = tThisFlipGlobal  # on global time
                pp_rest_pre_start_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'pp_rest_pre_start_2.stopped')
                # update status
                pp_rest_pre_start_2.status = FINISHED
                win.callOnFlip(pp_rest_pre_start_2.setData, int(0))
        
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
        for thisComponent in restTrial_postComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "restTrial_post" ---
    for thisComponent in restTrial_postComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('restTrial_post.stopped', globalClock.getTime(format='float'))
    beep_rest_post_start.pause()  # ensure sound has stopped at end of Routine
    beep_rest_post_end.pause()  # ensure sound has stopped at end of Routine
    if pp_rest_pre_start_2.status == STARTED:
        win.callOnFlip(pp_rest_pre_start_2.setData, int(0))
    thisExp.nextEntry()
    # the Routine "restTrial_post" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "thanks_end" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('thanks_end.started', globalClock.getTime(format='float'))
    key_resp_6.keys = []
    key_resp_6.rt = []
    _key_resp_6_allKeys = []
    # Run 'Begin Routine' code from hideMouse_11
    win.mouseVisible = False 
    # keep track of which components have finished
    thanks_endComponents = [thanksText_end, key_resp_6]
    for thisComponent in thanks_endComponents:
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
    
    # --- Run Routine "thanks_end" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *thanksText_end* updates
        
        # if thanksText_end is starting this frame...
        if thanksText_end.status == NOT_STARTED and beep_rest_post_end.status == FINISHED:
            # keep track of start time/frame for later
            thanksText_end.frameNStart = frameN  # exact frame index
            thanksText_end.tStart = t  # local t and not account for scr refresh
            thanksText_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(thanksText_end, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'thanksText_end.started')
            # update status
            thanksText_end.status = STARTED
            thanksText_end.setAutoDraw(True)
        
        # if thanksText_end is active this frame...
        if thanksText_end.status == STARTED:
            # update params
            pass
        
        # if thanksText_end is stopping this frame...
        if thanksText_end.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > thanksText_end.tStartRefresh + 20-frameTolerance:
                # keep track of stop time/frame for later
                thanksText_end.tStop = t  # not accounting for scr refresh
                thanksText_end.tStopRefresh = tThisFlipGlobal  # on global time
                thanksText_end.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'thanksText_end.stopped')
                # update status
                thanksText_end.status = FINISHED
                thanksText_end.setAutoDraw(False)
        
        # *key_resp_6* updates
        waitOnFlip = False
        
        # if key_resp_6 is starting this frame...
        if key_resp_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_6.frameNStart = frameN  # exact frame index
            key_resp_6.tStart = t  # local t and not account for scr refresh
            key_resp_6.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_6, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_6.started')
            # update status
            key_resp_6.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_6.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_6.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_6.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_6.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_6_allKeys.extend(theseKeys)
            if len(_key_resp_6_allKeys):
                key_resp_6.keys = _key_resp_6_allKeys[-1].name  # just the last key pressed
                key_resp_6.rt = _key_resp_6_allKeys[-1].rt
                key_resp_6.duration = _key_resp_6_allKeys[-1].duration
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
        for thisComponent in thanks_endComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "thanks_end" ---
    for thisComponent in thanks_endComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('thanks_end.stopped', globalClock.getTime(format='float'))
    thisExp.nextEntry()
    # the Routine "thanks_end" was not non-slip safe, so reset the non-slip timer
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
