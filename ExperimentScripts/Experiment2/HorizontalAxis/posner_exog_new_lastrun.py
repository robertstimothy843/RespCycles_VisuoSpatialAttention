#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on April 11, 2025, at 15:44
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

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'posner_endo_new1'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': '',
    'session': '001',
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
_winSize = [2560, 1440]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

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
        originPath='D:\\experiment_2\\Exogenous New (horizontal_axis)\\posner_exog_new_lastrun.py',
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
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('exp')
        )
    
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
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0.5294, 0.5294, 0.5294], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0.5294, 0.5294, 0.5294]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
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
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('key_control') is None:
        # initialise key_control
        key_control = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_control',
        )
    if deviceManager.getDevice('key_control2') is None:
        # initialise key_control2
        key_control2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_control2',
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    if deviceManager.getDevice('key_control3') is None:
        # initialise key_control3
        key_control3 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_control3',
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
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
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
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


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
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
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
    
    # --- Initialize components for Routine "instructions" ---
    instructions_txt = visual.TextStim(win=win, name='instructions_txt',
        text="Welcome to the experiment!\n\n\n\n\nINSTRUCTIONS:\n\nBreathe deeply and regularly throughout the experiment.\nHold your breathe for a second right after each inhalation and exhalation.\nRest the index finger of your dominant hand on the space bar throughout the experiment.\n\nYou will see a fixation cross with two boxes. Keep looking directly at the fixation cross at all times.\n\nOne of the two boxes will flicker for a short time.\nThen a black star might randomly appear either in the left or in the right box.\n\nPlease press the space bar as quickly as possible whenever you see the black STAR.\nBut don't press the space bar if there is no star - this will occasionally happen.",
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_control = keyboard.Keyboard(deviceName='key_control')
    
    # --- Initialize components for Routine "ready" ---
    ready_txt = visual.TextStim(win=win, name='ready_txt',
        text='ready',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "fix" ---
    fixation = visual.ImageStim(
        win=win,
        name='fixation', 
        image='fixation.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.8, 0.182),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    key_control2 = keyboard.Keyboard(deviceName='key_control2')
    fixation_cross = visual.TextStim(win=win, name='fixation_cross',
        text='+',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "cue" ---
    cube = visual.ImageStim(
        win=win,
        name='cube', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.8, 0.182),
        color=[1.0000, 1.0000, 1.0000], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    fixation_cross_cue = visual.TextStim(win=win, name='fixation_cross_cue',
        text='+',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "target" ---
    star = visual.ImageStim(
        win=win,
        name='star', 
        image='target_star.png', mask=None, anchor='center',
        ori=0.0, pos=[0,0], draggable=False, size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    fixation_target = visual.ImageStim(
        win=win,
        name='fixation_target', 
        image='fixation.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.8, 0.182),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    fixation_cross_target = visual.TextStim(win=win, name='fixation_cross_target',
        text='+',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # --- Initialize components for Routine "ready" ---
    ready_txt = visual.TextStim(win=win, name='ready_txt',
        text='ready',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "fix" ---
    fixation = visual.ImageStim(
        win=win,
        name='fixation', 
        image='fixation.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.8, 0.182),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    key_control2 = keyboard.Keyboard(deviceName='key_control2')
    fixation_cross = visual.TextStim(win=win, name='fixation_cross',
        text='+',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "cue" ---
    cube = visual.ImageStim(
        win=win,
        name='cube', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.8, 0.182),
        color=[1.0000, 1.0000, 1.0000], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    fixation_cross_cue = visual.TextStim(win=win, name='fixation_cross_cue',
        text='+',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "target" ---
    star = visual.ImageStim(
        win=win,
        name='star', 
        image='target_star.png', mask=None, anchor='center',
        ori=0.0, pos=[0,0], draggable=False, size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    fixation_target = visual.ImageStim(
        win=win,
        name='fixation_target', 
        image='fixation.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.8, 0.182),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    fixation_cross_target = visual.TextStim(win=win, name='fixation_cross_target',
        text='+',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # --- Initialize components for Routine "break_2" ---
    text = visual.TextStim(win=win, name='text',
        text="Let's have a break!",
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_control3 = keyboard.Keyboard(deviceName='key_control3')
    
    # --- Initialize components for Routine "ready" ---
    ready_txt = visual.TextStim(win=win, name='ready_txt',
        text='ready',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "fix" ---
    fixation = visual.ImageStim(
        win=win,
        name='fixation', 
        image='fixation.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.8, 0.182),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    key_control2 = keyboard.Keyboard(deviceName='key_control2')
    fixation_cross = visual.TextStim(win=win, name='fixation_cross',
        text='+',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "cue" ---
    cube = visual.ImageStim(
        win=win,
        name='cube', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.8, 0.182),
        color=[1.0000, 1.0000, 1.0000], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    fixation_cross_cue = visual.TextStim(win=win, name='fixation_cross_cue',
        text='+',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "target" ---
    star = visual.ImageStim(
        win=win,
        name='star', 
        image='target_star.png', mask=None, anchor='center',
        ori=0.0, pos=[0,0], draggable=False, size=(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    fixation_target = visual.ImageStim(
        win=win,
        name='fixation_target', 
        image='fixation.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.8, 0.182),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    fixation_cross_target = visual.TextStim(win=win, name='fixation_cross_target',
        text='+',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
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
    
    # --- Prepare to start Routine "instructions" ---
    # create an object to store info about Routine instructions
    instructions = data.Routine(
        name='instructions',
        components=[instructions_txt, key_control],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_control
    key_control.keys = []
    key_control.rt = []
    _key_control_allKeys = []
    # store start times for instructions
    instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions.tStart = globalClock.getTime(format='float')
    instructions.status = STARTED
    thisExp.addData('instructions.started', instructions.tStart)
    instructions.maxDuration = None
    # keep track of which components have finished
    instructionsComponents = instructions.components
    for thisComponent in instructions.components:
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
    
    # --- Run Routine "instructions" ---
    instructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instructions_txt* updates
        
        # if instructions_txt is starting this frame...
        if instructions_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructions_txt.frameNStart = frameN  # exact frame index
            instructions_txt.tStart = t  # local t and not account for scr refresh
            instructions_txt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructions_txt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructions_txt.started')
            # update status
            instructions_txt.status = STARTED
            instructions_txt.setAutoDraw(True)
        
        # if instructions_txt is active this frame...
        if instructions_txt.status == STARTED:
            # update params
            pass
        
        # *key_control* updates
        waitOnFlip = False
        
        # if key_control is starting this frame...
        if key_control.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_control.frameNStart = frameN  # exact frame index
            key_control.tStart = t  # local t and not account for scr refresh
            key_control.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_control, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_control.started')
            # update status
            key_control.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_control.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_control.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_control.status == STARTED and not waitOnFlip:
            theseKeys = key_control.getKeys(keyList=['up'], ignoreKeys=["escape"], waitRelease=False)
            _key_control_allKeys.extend(theseKeys)
            if len(_key_control_allKeys):
                key_control.keys = _key_control_allKeys[-1].name  # just the last key pressed
                key_control.rt = _key_control_allKeys[-1].rt
                key_control.duration = _key_control_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            instructions.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions" ---
    for thisComponent in instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions
    instructions.tStop = globalClock.getTime(format='float')
    instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions.stopped', instructions.tStop)
    # check responses
    if key_control.keys in ['', [], None]:  # No response was made
        key_control.keys = None
    thisExp.addData('key_control.keys',key_control.keys)
    if key_control.keys != None:  # we had a response
        thisExp.addData('key_control.rt', key_control.rt)
        thisExp.addData('key_control.duration', key_control.duration)
    thisExp.nextEntry()
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "ready" ---
    # create an object to store info about Routine ready
    ready = data.Routine(
        name='ready',
        components=[ready_txt],
    )
    ready.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for ready
    ready.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    ready.tStart = globalClock.getTime(format='float')
    ready.status = STARTED
    thisExp.addData('ready.started', ready.tStart)
    ready.maxDuration = None
    # keep track of which components have finished
    readyComponents = ready.components
    for thisComponent in ready.components:
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
    
    # --- Run Routine "ready" ---
    ready.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 3.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *ready_txt* updates
        
        # if ready_txt is starting this frame...
        if ready_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ready_txt.frameNStart = frameN  # exact frame index
            ready_txt.tStart = t  # local t and not account for scr refresh
            ready_txt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ready_txt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ready_txt.started')
            # update status
            ready_txt.status = STARTED
            ready_txt.setAutoDraw(True)
        
        # if ready_txt is active this frame...
        if ready_txt.status == STARTED:
            # update params
            pass
        
        # if ready_txt is stopping this frame...
        if ready_txt.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > 3-frameTolerance:
                # keep track of stop time/frame for later
                ready_txt.tStop = t  # not accounting for scr refresh
                ready_txt.tStopRefresh = tThisFlipGlobal  # on global time
                ready_txt.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'ready_txt.stopped')
                # update status
                ready_txt.status = FINISHED
                ready_txt.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            ready.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ready.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "ready" ---
    for thisComponent in ready.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for ready
    ready.tStop = globalClock.getTime(format='float')
    ready.tStopRefresh = tThisFlipGlobal
    thisExp.addData('ready.stopped', ready.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if ready.maxDurationReached:
        routineTimer.addTime(-ready.maxDuration)
    elif ready.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-3.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    practice = data.TrialHandler2(
        name='practice',
        nReps=1.0, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('practice_conditions.xlsx'), 
        seed=None, 
    )
    thisExp.addLoop(practice)  # add the loop to the experiment
    thisPractice = practice.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPractice.rgb)
    if thisPractice != None:
        for paramName in thisPractice:
            globals()[paramName] = thisPractice[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisPractice in practice:
        currentLoop = practice
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisPractice.rgb)
        if thisPractice != None:
            for paramName in thisPractice:
                globals()[paramName] = thisPractice[paramName]
        
        # --- Prepare to start Routine "fix" ---
        # create an object to store info about Routine fix
        fix = data.Routine(
            name='fix',
            components=[fixation, key_control2, fixation_cross],
        )
        fix.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_control2
        key_control2.keys = []
        key_control2.rt = []
        _key_control2_allKeys = []
        # store start times for fix
        fix.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        fix.tStart = globalClock.getTime(format='float')
        fix.status = STARTED
        thisExp.addData('fix.started', fix.tStart)
        fix.maxDuration = None
        # keep track of which components have finished
        fixComponents = fix.components
        for thisComponent in fix.components:
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
        
        # --- Run Routine "fix" ---
        # if trial has changed, end Routine now
        if isinstance(practice, data.TrialHandler2) and thisPractice.thisN != practice.thisTrial.thisN:
            continueRoutine = False
        fix.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
            
            # *key_control2* updates
            waitOnFlip = False
            
            # if key_control2 is starting this frame...
            if key_control2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_control2.frameNStart = frameN  # exact frame index
                key_control2.tStart = t  # local t and not account for scr refresh
                key_control2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_control2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_control2.started')
                # update status
                key_control2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_control2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_control2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_control2.status == STARTED and not waitOnFlip:
                theseKeys = key_control2.getKeys(keyList=['up', 'down'], ignoreKeys=["escape"], waitRelease=False)
                _key_control2_allKeys.extend(theseKeys)
                if len(_key_control2_allKeys):
                    key_control2.keys = _key_control2_allKeys[-1].name  # just the last key pressed
                    key_control2.rt = _key_control2_allKeys[-1].rt
                    key_control2.duration = _key_control2_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # *fixation_cross* updates
            
            # if fixation_cross is starting this frame...
            if fixation_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross.frameNStart = frameN  # exact frame index
                fixation_cross.tStart = t  # local t and not account for scr refresh
                fixation_cross.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_cross.started')
                # update status
                fixation_cross.status = STARTED
                fixation_cross.setAutoDraw(True)
            
            # if fixation_cross is active this frame...
            if fixation_cross.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                fix.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in fix.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "fix" ---
        for thisComponent in fix.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for fix
        fix.tStop = globalClock.getTime(format='float')
        fix.tStopRefresh = tThisFlipGlobal
        thisExp.addData('fix.stopped', fix.tStop)
        # check responses
        if key_control2.keys in ['', [], None]:  # No response was made
            key_control2.keys = None
        practice.addData('key_control2.keys',key_control2.keys)
        if key_control2.keys != None:  # we had a response
            practice.addData('key_control2.rt', key_control2.rt)
            practice.addData('key_control2.duration', key_control2.duration)
        # the Routine "fix" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "cue" ---
        # create an object to store info about Routine cue
        cue = data.Routine(
            name='cue',
            components=[cube, fixation_cross_cue],
        )
        cue.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        cube.setImage(cue_img)
        # store start times for cue
        cue.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        cue.tStart = globalClock.getTime(format='float')
        cue.status = STARTED
        thisExp.addData('cue.started', cue.tStart)
        cue.maxDuration = None
        # keep track of which components have finished
        cueComponents = cue.components
        for thisComponent in cue.components:
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
        
        # --- Run Routine "cue" ---
        # if trial has changed, end Routine now
        if isinstance(practice, data.TrialHandler2) and thisPractice.thisN != practice.thisTrial.thisN:
            continueRoutine = False
        cue.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.05:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *cube* updates
            
            # if cube is starting this frame...
            if cube.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                cube.frameNStart = frameN  # exact frame index
                cube.tStart = t  # local t and not account for scr refresh
                cube.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(cube, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cube.started')
                # update status
                cube.status = STARTED
                cube.setAutoDraw(True)
            
            # if cube is active this frame...
            if cube.status == STARTED:
                # update params
                pass
            
            # if cube is stopping this frame...
            if cube.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > cube.tStartRefresh + 0.05-frameTolerance:
                    # keep track of stop time/frame for later
                    cube.tStop = t  # not accounting for scr refresh
                    cube.tStopRefresh = tThisFlipGlobal  # on global time
                    cube.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'cube.stopped')
                    # update status
                    cube.status = FINISHED
                    cube.setAutoDraw(False)
            
            # *fixation_cross_cue* updates
            
            # if fixation_cross_cue is starting this frame...
            if fixation_cross_cue.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross_cue.frameNStart = frameN  # exact frame index
                fixation_cross_cue.tStart = t  # local t and not account for scr refresh
                fixation_cross_cue.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross_cue, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_cross_cue.started')
                # update status
                fixation_cross_cue.status = STARTED
                fixation_cross_cue.setAutoDraw(True)
            
            # if fixation_cross_cue is active this frame...
            if fixation_cross_cue.status == STARTED:
                # update params
                pass
            
            # if fixation_cross_cue is stopping this frame...
            if fixation_cross_cue.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_cross_cue.tStartRefresh + 0.05-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_cross_cue.tStop = t  # not accounting for scr refresh
                    fixation_cross_cue.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_cross_cue.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_cross_cue.stopped')
                    # update status
                    fixation_cross_cue.status = FINISHED
                    fixation_cross_cue.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                cue.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in cue.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "cue" ---
        for thisComponent in cue.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for cue
        cue.tStop = globalClock.getTime(format='float')
        cue.tStopRefresh = tThisFlipGlobal
        thisExp.addData('cue.stopped', cue.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if cue.maxDurationReached:
            routineTimer.addTime(-cue.maxDuration)
        elif cue.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.050000)
        
        # --- Prepare to start Routine "target" ---
        # create an object to store info about Routine target
        target = data.Routine(
            name='target',
            components=[star, fixation_target, fixation_cross_target, key_resp],
        )
        target.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        star.setPos((target_x, 0.005))
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # store start times for target
        target.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        target.tStart = globalClock.getTime(format='float')
        target.status = STARTED
        thisExp.addData('target.started', target.tStart)
        target.maxDuration = None
        # keep track of which components have finished
        targetComponents = target.components
        for thisComponent in target.components:
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
        
        # --- Run Routine "target" ---
        # if trial has changed, end Routine now
        if isinstance(practice, data.TrialHandler2) and thisPractice.thisN != practice.thisTrial.thisN:
            continueRoutine = False
        target.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *star* updates
            
            # if star is starting this frame...
            if star.status == NOT_STARTED and tThisFlip >= cue_soa-frameTolerance:
                # keep track of start time/frame for later
                star.frameNStart = frameN  # exact frame index
                star.tStart = t  # local t and not account for scr refresh
                star.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(star, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'star.started')
                # update status
                star.status = STARTED
                star.setAutoDraw(True)
            
            # if star is active this frame...
            if star.status == STARTED:
                # update params
                pass
            
            # if star is stopping this frame...
            if star.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > star.tStartRefresh + 2.0-frameTolerance:
                    # keep track of stop time/frame for later
                    star.tStop = t  # not accounting for scr refresh
                    star.tStopRefresh = tThisFlipGlobal  # on global time
                    star.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'star.stopped')
                    # update status
                    star.status = FINISHED
                    star.setAutoDraw(False)
            
            # *fixation_target* updates
            
            # if fixation_target is starting this frame...
            if fixation_target.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_target.frameNStart = frameN  # exact frame index
                fixation_target.tStart = t  # local t and not account for scr refresh
                fixation_target.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_target, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_target.started')
                # update status
                fixation_target.status = STARTED
                fixation_target.setAutoDraw(True)
            
            # if fixation_target is active this frame...
            if fixation_target.status == STARTED:
                # update params
                pass
            
            # if fixation_target is stopping this frame...
            if fixation_target.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_target.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_target.tStop = t  # not accounting for scr refresh
                    fixation_target.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_target.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_target.stopped')
                    # update status
                    fixation_target.status = FINISHED
                    fixation_target.setAutoDraw(False)
            
            # *fixation_cross_target* updates
            
            # if fixation_cross_target is starting this frame...
            if fixation_cross_target.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross_target.frameNStart = frameN  # exact frame index
                fixation_cross_target.tStart = t  # local t and not account for scr refresh
                fixation_cross_target.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross_target, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_cross_target.started')
                # update status
                fixation_cross_target.status = STARTED
                fixation_cross_target.setAutoDraw(True)
            
            # if fixation_cross_target is active this frame...
            if fixation_cross_target.status == STARTED:
                # update params
                pass
            
            # if fixation_cross_target is stopping this frame...
            if fixation_cross_target.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_cross_target.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_cross_target.tStop = t  # not accounting for scr refresh
                    fixation_cross_target.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_cross_target.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_cross_target.stopped')
                    # update status
                    fixation_cross_target.status = FINISHED
                    fixation_cross_target.setAutoDraw(False)
            
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
            
            # if key_resp is stopping this frame...
            if key_resp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp.tStop = t  # not accounting for scr refresh
                    key_resp.tStopRefresh = tThisFlipGlobal  # on global time
                    key_resp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp.stopped')
                    # update status
                    key_resp.status = FINISHED
                    key_resp.status = FINISHED
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
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                target.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in target.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "target" ---
        for thisComponent in target.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for target
        target.tStop = globalClock.getTime(format='float')
        target.tStopRefresh = tThisFlipGlobal
        thisExp.addData('target.stopped', target.tStop)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        practice.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            practice.addData('key_resp.rt', key_resp.rt)
            practice.addData('key_resp.duration', key_resp.duration)
        # the Routine "target" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'practice'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "ready" ---
    # create an object to store info about Routine ready
    ready = data.Routine(
        name='ready',
        components=[ready_txt],
    )
    ready.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for ready
    ready.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    ready.tStart = globalClock.getTime(format='float')
    ready.status = STARTED
    thisExp.addData('ready.started', ready.tStart)
    ready.maxDuration = None
    # keep track of which components have finished
    readyComponents = ready.components
    for thisComponent in ready.components:
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
    
    # --- Run Routine "ready" ---
    ready.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 3.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *ready_txt* updates
        
        # if ready_txt is starting this frame...
        if ready_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ready_txt.frameNStart = frameN  # exact frame index
            ready_txt.tStart = t  # local t and not account for scr refresh
            ready_txt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ready_txt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ready_txt.started')
            # update status
            ready_txt.status = STARTED
            ready_txt.setAutoDraw(True)
        
        # if ready_txt is active this frame...
        if ready_txt.status == STARTED:
            # update params
            pass
        
        # if ready_txt is stopping this frame...
        if ready_txt.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > 3-frameTolerance:
                # keep track of stop time/frame for later
                ready_txt.tStop = t  # not accounting for scr refresh
                ready_txt.tStopRefresh = tThisFlipGlobal  # on global time
                ready_txt.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'ready_txt.stopped')
                # update status
                ready_txt.status = FINISHED
                ready_txt.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            ready.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ready.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "ready" ---
    for thisComponent in ready.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for ready
    ready.tStop = globalClock.getTime(format='float')
    ready.tStopRefresh = tThisFlipGlobal
    thisExp.addData('ready.stopped', ready.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if ready.maxDurationReached:
        routineTimer.addTime(-ready.maxDuration)
    elif ready.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-3.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    block1 = data.TrialHandler2(
        name='block1',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('conditions.xlsx'), 
        seed=None, 
    )
    thisExp.addLoop(block1)  # add the loop to the experiment
    thisBlock1 = block1.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock1.rgb)
    if thisBlock1 != None:
        for paramName in thisBlock1:
            globals()[paramName] = thisBlock1[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlock1 in block1:
        currentLoop = block1
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlock1.rgb)
        if thisBlock1 != None:
            for paramName in thisBlock1:
                globals()[paramName] = thisBlock1[paramName]
        
        # --- Prepare to start Routine "fix" ---
        # create an object to store info about Routine fix
        fix = data.Routine(
            name='fix',
            components=[fixation, key_control2, fixation_cross],
        )
        fix.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_control2
        key_control2.keys = []
        key_control2.rt = []
        _key_control2_allKeys = []
        # store start times for fix
        fix.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        fix.tStart = globalClock.getTime(format='float')
        fix.status = STARTED
        thisExp.addData('fix.started', fix.tStart)
        fix.maxDuration = None
        # keep track of which components have finished
        fixComponents = fix.components
        for thisComponent in fix.components:
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
        
        # --- Run Routine "fix" ---
        # if trial has changed, end Routine now
        if isinstance(block1, data.TrialHandler2) and thisBlock1.thisN != block1.thisTrial.thisN:
            continueRoutine = False
        fix.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
            
            # *key_control2* updates
            waitOnFlip = False
            
            # if key_control2 is starting this frame...
            if key_control2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_control2.frameNStart = frameN  # exact frame index
                key_control2.tStart = t  # local t and not account for scr refresh
                key_control2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_control2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_control2.started')
                # update status
                key_control2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_control2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_control2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_control2.status == STARTED and not waitOnFlip:
                theseKeys = key_control2.getKeys(keyList=['up', 'down'], ignoreKeys=["escape"], waitRelease=False)
                _key_control2_allKeys.extend(theseKeys)
                if len(_key_control2_allKeys):
                    key_control2.keys = _key_control2_allKeys[-1].name  # just the last key pressed
                    key_control2.rt = _key_control2_allKeys[-1].rt
                    key_control2.duration = _key_control2_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # *fixation_cross* updates
            
            # if fixation_cross is starting this frame...
            if fixation_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross.frameNStart = frameN  # exact frame index
                fixation_cross.tStart = t  # local t and not account for scr refresh
                fixation_cross.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_cross.started')
                # update status
                fixation_cross.status = STARTED
                fixation_cross.setAutoDraw(True)
            
            # if fixation_cross is active this frame...
            if fixation_cross.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                fix.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in fix.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "fix" ---
        for thisComponent in fix.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for fix
        fix.tStop = globalClock.getTime(format='float')
        fix.tStopRefresh = tThisFlipGlobal
        thisExp.addData('fix.stopped', fix.tStop)
        # check responses
        if key_control2.keys in ['', [], None]:  # No response was made
            key_control2.keys = None
        block1.addData('key_control2.keys',key_control2.keys)
        if key_control2.keys != None:  # we had a response
            block1.addData('key_control2.rt', key_control2.rt)
            block1.addData('key_control2.duration', key_control2.duration)
        # the Routine "fix" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "cue" ---
        # create an object to store info about Routine cue
        cue = data.Routine(
            name='cue',
            components=[cube, fixation_cross_cue],
        )
        cue.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        cube.setImage(cue_img)
        # store start times for cue
        cue.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        cue.tStart = globalClock.getTime(format='float')
        cue.status = STARTED
        thisExp.addData('cue.started', cue.tStart)
        cue.maxDuration = None
        # keep track of which components have finished
        cueComponents = cue.components
        for thisComponent in cue.components:
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
        
        # --- Run Routine "cue" ---
        # if trial has changed, end Routine now
        if isinstance(block1, data.TrialHandler2) and thisBlock1.thisN != block1.thisTrial.thisN:
            continueRoutine = False
        cue.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.05:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *cube* updates
            
            # if cube is starting this frame...
            if cube.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                cube.frameNStart = frameN  # exact frame index
                cube.tStart = t  # local t and not account for scr refresh
                cube.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(cube, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cube.started')
                # update status
                cube.status = STARTED
                cube.setAutoDraw(True)
            
            # if cube is active this frame...
            if cube.status == STARTED:
                # update params
                pass
            
            # if cube is stopping this frame...
            if cube.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > cube.tStartRefresh + 0.05-frameTolerance:
                    # keep track of stop time/frame for later
                    cube.tStop = t  # not accounting for scr refresh
                    cube.tStopRefresh = tThisFlipGlobal  # on global time
                    cube.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'cube.stopped')
                    # update status
                    cube.status = FINISHED
                    cube.setAutoDraw(False)
            
            # *fixation_cross_cue* updates
            
            # if fixation_cross_cue is starting this frame...
            if fixation_cross_cue.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross_cue.frameNStart = frameN  # exact frame index
                fixation_cross_cue.tStart = t  # local t and not account for scr refresh
                fixation_cross_cue.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross_cue, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_cross_cue.started')
                # update status
                fixation_cross_cue.status = STARTED
                fixation_cross_cue.setAutoDraw(True)
            
            # if fixation_cross_cue is active this frame...
            if fixation_cross_cue.status == STARTED:
                # update params
                pass
            
            # if fixation_cross_cue is stopping this frame...
            if fixation_cross_cue.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_cross_cue.tStartRefresh + 0.05-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_cross_cue.tStop = t  # not accounting for scr refresh
                    fixation_cross_cue.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_cross_cue.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_cross_cue.stopped')
                    # update status
                    fixation_cross_cue.status = FINISHED
                    fixation_cross_cue.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                cue.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in cue.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "cue" ---
        for thisComponent in cue.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for cue
        cue.tStop = globalClock.getTime(format='float')
        cue.tStopRefresh = tThisFlipGlobal
        thisExp.addData('cue.stopped', cue.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if cue.maxDurationReached:
            routineTimer.addTime(-cue.maxDuration)
        elif cue.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.050000)
        
        # --- Prepare to start Routine "target" ---
        # create an object to store info about Routine target
        target = data.Routine(
            name='target',
            components=[star, fixation_target, fixation_cross_target, key_resp],
        )
        target.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        star.setPos((target_x, 0.005))
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # store start times for target
        target.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        target.tStart = globalClock.getTime(format='float')
        target.status = STARTED
        thisExp.addData('target.started', target.tStart)
        target.maxDuration = None
        # keep track of which components have finished
        targetComponents = target.components
        for thisComponent in target.components:
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
        
        # --- Run Routine "target" ---
        # if trial has changed, end Routine now
        if isinstance(block1, data.TrialHandler2) and thisBlock1.thisN != block1.thisTrial.thisN:
            continueRoutine = False
        target.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *star* updates
            
            # if star is starting this frame...
            if star.status == NOT_STARTED and tThisFlip >= cue_soa-frameTolerance:
                # keep track of start time/frame for later
                star.frameNStart = frameN  # exact frame index
                star.tStart = t  # local t and not account for scr refresh
                star.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(star, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'star.started')
                # update status
                star.status = STARTED
                star.setAutoDraw(True)
            
            # if star is active this frame...
            if star.status == STARTED:
                # update params
                pass
            
            # if star is stopping this frame...
            if star.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > star.tStartRefresh + 2.0-frameTolerance:
                    # keep track of stop time/frame for later
                    star.tStop = t  # not accounting for scr refresh
                    star.tStopRefresh = tThisFlipGlobal  # on global time
                    star.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'star.stopped')
                    # update status
                    star.status = FINISHED
                    star.setAutoDraw(False)
            
            # *fixation_target* updates
            
            # if fixation_target is starting this frame...
            if fixation_target.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_target.frameNStart = frameN  # exact frame index
                fixation_target.tStart = t  # local t and not account for scr refresh
                fixation_target.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_target, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_target.started')
                # update status
                fixation_target.status = STARTED
                fixation_target.setAutoDraw(True)
            
            # if fixation_target is active this frame...
            if fixation_target.status == STARTED:
                # update params
                pass
            
            # if fixation_target is stopping this frame...
            if fixation_target.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_target.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_target.tStop = t  # not accounting for scr refresh
                    fixation_target.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_target.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_target.stopped')
                    # update status
                    fixation_target.status = FINISHED
                    fixation_target.setAutoDraw(False)
            
            # *fixation_cross_target* updates
            
            # if fixation_cross_target is starting this frame...
            if fixation_cross_target.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross_target.frameNStart = frameN  # exact frame index
                fixation_cross_target.tStart = t  # local t and not account for scr refresh
                fixation_cross_target.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross_target, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_cross_target.started')
                # update status
                fixation_cross_target.status = STARTED
                fixation_cross_target.setAutoDraw(True)
            
            # if fixation_cross_target is active this frame...
            if fixation_cross_target.status == STARTED:
                # update params
                pass
            
            # if fixation_cross_target is stopping this frame...
            if fixation_cross_target.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_cross_target.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_cross_target.tStop = t  # not accounting for scr refresh
                    fixation_cross_target.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_cross_target.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_cross_target.stopped')
                    # update status
                    fixation_cross_target.status = FINISHED
                    fixation_cross_target.setAutoDraw(False)
            
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
            
            # if key_resp is stopping this frame...
            if key_resp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp.tStop = t  # not accounting for scr refresh
                    key_resp.tStopRefresh = tThisFlipGlobal  # on global time
                    key_resp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp.stopped')
                    # update status
                    key_resp.status = FINISHED
                    key_resp.status = FINISHED
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
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                target.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in target.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "target" ---
        for thisComponent in target.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for target
        target.tStop = globalClock.getTime(format='float')
        target.tStopRefresh = tThisFlipGlobal
        thisExp.addData('target.stopped', target.tStop)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        block1.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            block1.addData('key_resp.rt', key_resp.rt)
            block1.addData('key_resp.duration', key_resp.duration)
        # the Routine "target" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'block1'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "break_2" ---
    # create an object to store info about Routine break_2
    break_2 = data.Routine(
        name='break_2',
        components=[text, key_control3],
    )
    break_2.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_control3
    key_control3.keys = []
    key_control3.rt = []
    _key_control3_allKeys = []
    # store start times for break_2
    break_2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    break_2.tStart = globalClock.getTime(format='float')
    break_2.status = STARTED
    thisExp.addData('break_2.started', break_2.tStart)
    break_2.maxDuration = None
    # keep track of which components have finished
    break_2Components = break_2.components
    for thisComponent in break_2.components:
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
    
    # --- Run Routine "break_2" ---
    break_2.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        
        # if text is stopping this frame...
        if text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                text.tStop = t  # not accounting for scr refresh
                text.tStopRefresh = tThisFlipGlobal  # on global time
                text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text.stopped')
                # update status
                text.status = FINISHED
                text.setAutoDraw(False)
        
        # *key_control3* updates
        waitOnFlip = False
        
        # if key_control3 is starting this frame...
        if key_control3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_control3.frameNStart = frameN  # exact frame index
            key_control3.tStart = t  # local t and not account for scr refresh
            key_control3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_control3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_control3.started')
            # update status
            key_control3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_control3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_control3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_control3.status == STARTED and not waitOnFlip:
            theseKeys = key_control3.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_control3_allKeys.extend(theseKeys)
            if len(_key_control3_allKeys):
                key_control3.keys = _key_control3_allKeys[-1].name  # just the last key pressed
                key_control3.rt = _key_control3_allKeys[-1].rt
                key_control3.duration = _key_control3_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break_2.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in break_2.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "break_2" ---
    for thisComponent in break_2.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for break_2
    break_2.tStop = globalClock.getTime(format='float')
    break_2.tStopRefresh = tThisFlipGlobal
    thisExp.addData('break_2.stopped', break_2.tStop)
    # check responses
    if key_control3.keys in ['', [], None]:  # No response was made
        key_control3.keys = None
    thisExp.addData('key_control3.keys',key_control3.keys)
    if key_control3.keys != None:  # we had a response
        thisExp.addData('key_control3.rt', key_control3.rt)
        thisExp.addData('key_control3.duration', key_control3.duration)
    thisExp.nextEntry()
    # the Routine "break_2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "ready" ---
    # create an object to store info about Routine ready
    ready = data.Routine(
        name='ready',
        components=[ready_txt],
    )
    ready.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for ready
    ready.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    ready.tStart = globalClock.getTime(format='float')
    ready.status = STARTED
    thisExp.addData('ready.started', ready.tStart)
    ready.maxDuration = None
    # keep track of which components have finished
    readyComponents = ready.components
    for thisComponent in ready.components:
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
    
    # --- Run Routine "ready" ---
    ready.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 3.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *ready_txt* updates
        
        # if ready_txt is starting this frame...
        if ready_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ready_txt.frameNStart = frameN  # exact frame index
            ready_txt.tStart = t  # local t and not account for scr refresh
            ready_txt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ready_txt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ready_txt.started')
            # update status
            ready_txt.status = STARTED
            ready_txt.setAutoDraw(True)
        
        # if ready_txt is active this frame...
        if ready_txt.status == STARTED:
            # update params
            pass
        
        # if ready_txt is stopping this frame...
        if ready_txt.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > 3-frameTolerance:
                # keep track of stop time/frame for later
                ready_txt.tStop = t  # not accounting for scr refresh
                ready_txt.tStopRefresh = tThisFlipGlobal  # on global time
                ready_txt.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'ready_txt.stopped')
                # update status
                ready_txt.status = FINISHED
                ready_txt.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            ready.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ready.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "ready" ---
    for thisComponent in ready.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for ready
    ready.tStop = globalClock.getTime(format='float')
    ready.tStopRefresh = tThisFlipGlobal
    thisExp.addData('ready.stopped', ready.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if ready.maxDurationReached:
        routineTimer.addTime(-ready.maxDuration)
    elif ready.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-3.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    block2 = data.TrialHandler2(
        name='block2',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('conditions.xlsx'), 
        seed=None, 
    )
    thisExp.addLoop(block2)  # add the loop to the experiment
    thisBlock2 = block2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock2.rgb)
    if thisBlock2 != None:
        for paramName in thisBlock2:
            globals()[paramName] = thisBlock2[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlock2 in block2:
        currentLoop = block2
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlock2.rgb)
        if thisBlock2 != None:
            for paramName in thisBlock2:
                globals()[paramName] = thisBlock2[paramName]
        
        # --- Prepare to start Routine "fix" ---
        # create an object to store info about Routine fix
        fix = data.Routine(
            name='fix',
            components=[fixation, key_control2, fixation_cross],
        )
        fix.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_control2
        key_control2.keys = []
        key_control2.rt = []
        _key_control2_allKeys = []
        # store start times for fix
        fix.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        fix.tStart = globalClock.getTime(format='float')
        fix.status = STARTED
        thisExp.addData('fix.started', fix.tStart)
        fix.maxDuration = None
        # keep track of which components have finished
        fixComponents = fix.components
        for thisComponent in fix.components:
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
        
        # --- Run Routine "fix" ---
        # if trial has changed, end Routine now
        if isinstance(block2, data.TrialHandler2) and thisBlock2.thisN != block2.thisTrial.thisN:
            continueRoutine = False
        fix.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
            
            # *key_control2* updates
            waitOnFlip = False
            
            # if key_control2 is starting this frame...
            if key_control2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_control2.frameNStart = frameN  # exact frame index
                key_control2.tStart = t  # local t and not account for scr refresh
                key_control2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_control2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_control2.started')
                # update status
                key_control2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_control2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_control2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_control2.status == STARTED and not waitOnFlip:
                theseKeys = key_control2.getKeys(keyList=['up', 'down'], ignoreKeys=["escape"], waitRelease=False)
                _key_control2_allKeys.extend(theseKeys)
                if len(_key_control2_allKeys):
                    key_control2.keys = _key_control2_allKeys[-1].name  # just the last key pressed
                    key_control2.rt = _key_control2_allKeys[-1].rt
                    key_control2.duration = _key_control2_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # *fixation_cross* updates
            
            # if fixation_cross is starting this frame...
            if fixation_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross.frameNStart = frameN  # exact frame index
                fixation_cross.tStart = t  # local t and not account for scr refresh
                fixation_cross.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_cross.started')
                # update status
                fixation_cross.status = STARTED
                fixation_cross.setAutoDraw(True)
            
            # if fixation_cross is active this frame...
            if fixation_cross.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                fix.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in fix.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "fix" ---
        for thisComponent in fix.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for fix
        fix.tStop = globalClock.getTime(format='float')
        fix.tStopRefresh = tThisFlipGlobal
        thisExp.addData('fix.stopped', fix.tStop)
        # check responses
        if key_control2.keys in ['', [], None]:  # No response was made
            key_control2.keys = None
        block2.addData('key_control2.keys',key_control2.keys)
        if key_control2.keys != None:  # we had a response
            block2.addData('key_control2.rt', key_control2.rt)
            block2.addData('key_control2.duration', key_control2.duration)
        # the Routine "fix" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "cue" ---
        # create an object to store info about Routine cue
        cue = data.Routine(
            name='cue',
            components=[cube, fixation_cross_cue],
        )
        cue.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        cube.setImage(cue_img)
        # store start times for cue
        cue.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        cue.tStart = globalClock.getTime(format='float')
        cue.status = STARTED
        thisExp.addData('cue.started', cue.tStart)
        cue.maxDuration = None
        # keep track of which components have finished
        cueComponents = cue.components
        for thisComponent in cue.components:
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
        
        # --- Run Routine "cue" ---
        # if trial has changed, end Routine now
        if isinstance(block2, data.TrialHandler2) and thisBlock2.thisN != block2.thisTrial.thisN:
            continueRoutine = False
        cue.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.05:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *cube* updates
            
            # if cube is starting this frame...
            if cube.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                cube.frameNStart = frameN  # exact frame index
                cube.tStart = t  # local t and not account for scr refresh
                cube.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(cube, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cube.started')
                # update status
                cube.status = STARTED
                cube.setAutoDraw(True)
            
            # if cube is active this frame...
            if cube.status == STARTED:
                # update params
                pass
            
            # if cube is stopping this frame...
            if cube.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > cube.tStartRefresh + 0.05-frameTolerance:
                    # keep track of stop time/frame for later
                    cube.tStop = t  # not accounting for scr refresh
                    cube.tStopRefresh = tThisFlipGlobal  # on global time
                    cube.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'cube.stopped')
                    # update status
                    cube.status = FINISHED
                    cube.setAutoDraw(False)
            
            # *fixation_cross_cue* updates
            
            # if fixation_cross_cue is starting this frame...
            if fixation_cross_cue.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross_cue.frameNStart = frameN  # exact frame index
                fixation_cross_cue.tStart = t  # local t and not account for scr refresh
                fixation_cross_cue.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross_cue, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_cross_cue.started')
                # update status
                fixation_cross_cue.status = STARTED
                fixation_cross_cue.setAutoDraw(True)
            
            # if fixation_cross_cue is active this frame...
            if fixation_cross_cue.status == STARTED:
                # update params
                pass
            
            # if fixation_cross_cue is stopping this frame...
            if fixation_cross_cue.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_cross_cue.tStartRefresh + 0.05-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_cross_cue.tStop = t  # not accounting for scr refresh
                    fixation_cross_cue.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_cross_cue.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_cross_cue.stopped')
                    # update status
                    fixation_cross_cue.status = FINISHED
                    fixation_cross_cue.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                cue.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in cue.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "cue" ---
        for thisComponent in cue.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for cue
        cue.tStop = globalClock.getTime(format='float')
        cue.tStopRefresh = tThisFlipGlobal
        thisExp.addData('cue.stopped', cue.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if cue.maxDurationReached:
            routineTimer.addTime(-cue.maxDuration)
        elif cue.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.050000)
        
        # --- Prepare to start Routine "target" ---
        # create an object to store info about Routine target
        target = data.Routine(
            name='target',
            components=[star, fixation_target, fixation_cross_target, key_resp],
        )
        target.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        star.setPos((target_x, 0.005))
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # store start times for target
        target.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        target.tStart = globalClock.getTime(format='float')
        target.status = STARTED
        thisExp.addData('target.started', target.tStart)
        target.maxDuration = None
        # keep track of which components have finished
        targetComponents = target.components
        for thisComponent in target.components:
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
        
        # --- Run Routine "target" ---
        # if trial has changed, end Routine now
        if isinstance(block2, data.TrialHandler2) and thisBlock2.thisN != block2.thisTrial.thisN:
            continueRoutine = False
        target.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *star* updates
            
            # if star is starting this frame...
            if star.status == NOT_STARTED and tThisFlip >= cue_soa-frameTolerance:
                # keep track of start time/frame for later
                star.frameNStart = frameN  # exact frame index
                star.tStart = t  # local t and not account for scr refresh
                star.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(star, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'star.started')
                # update status
                star.status = STARTED
                star.setAutoDraw(True)
            
            # if star is active this frame...
            if star.status == STARTED:
                # update params
                pass
            
            # if star is stopping this frame...
            if star.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > star.tStartRefresh + 2.0-frameTolerance:
                    # keep track of stop time/frame for later
                    star.tStop = t  # not accounting for scr refresh
                    star.tStopRefresh = tThisFlipGlobal  # on global time
                    star.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'star.stopped')
                    # update status
                    star.status = FINISHED
                    star.setAutoDraw(False)
            
            # *fixation_target* updates
            
            # if fixation_target is starting this frame...
            if fixation_target.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_target.frameNStart = frameN  # exact frame index
                fixation_target.tStart = t  # local t and not account for scr refresh
                fixation_target.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_target, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_target.started')
                # update status
                fixation_target.status = STARTED
                fixation_target.setAutoDraw(True)
            
            # if fixation_target is active this frame...
            if fixation_target.status == STARTED:
                # update params
                pass
            
            # if fixation_target is stopping this frame...
            if fixation_target.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_target.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_target.tStop = t  # not accounting for scr refresh
                    fixation_target.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_target.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_target.stopped')
                    # update status
                    fixation_target.status = FINISHED
                    fixation_target.setAutoDraw(False)
            
            # *fixation_cross_target* updates
            
            # if fixation_cross_target is starting this frame...
            if fixation_cross_target.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross_target.frameNStart = frameN  # exact frame index
                fixation_cross_target.tStart = t  # local t and not account for scr refresh
                fixation_cross_target.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross_target, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_cross_target.started')
                # update status
                fixation_cross_target.status = STARTED
                fixation_cross_target.setAutoDraw(True)
            
            # if fixation_cross_target is active this frame...
            if fixation_cross_target.status == STARTED:
                # update params
                pass
            
            # if fixation_cross_target is stopping this frame...
            if fixation_cross_target.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_cross_target.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_cross_target.tStop = t  # not accounting for scr refresh
                    fixation_cross_target.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_cross_target.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation_cross_target.stopped')
                    # update status
                    fixation_cross_target.status = FINISHED
                    fixation_cross_target.setAutoDraw(False)
            
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
            
            # if key_resp is stopping this frame...
            if key_resp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp.tStop = t  # not accounting for scr refresh
                    key_resp.tStopRefresh = tThisFlipGlobal  # on global time
                    key_resp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp.stopped')
                    # update status
                    key_resp.status = FINISHED
                    key_resp.status = FINISHED
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
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                target.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in target.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "target" ---
        for thisComponent in target.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for target
        target.tStop = globalClock.getTime(format='float')
        target.tStopRefresh = tThisFlipGlobal
        thisExp.addData('target.stopped', target.tStop)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        block2.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            block2.addData('key_resp.rt', key_resp.rt)
            block2.addData('key_resp.duration', key_resp.duration)
        # the Routine "target" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'block2'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
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
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
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
