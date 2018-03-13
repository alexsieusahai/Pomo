import time # time
import datetime # metadata
import math # floor
import sys # stdout and stdin
import pygame # for audio
import select # for select()

import pomoQoL

import updateLog # contains all the log dropbox stuff
import dropbox

TOKEN = ''

POMODORO_CYCLE_LENGTH = 1 #default is 25*60
POMODORO_BREAK_LENGTH = 1 #default is 5*60
GOAL_POMODOROS = 1
GOAL_POMODOROS_LEFT = GOAL_POMODOROS
KEYBOARD_LOCKOUT_ON_BREAK = False #default is False
# NOTE: Eventually, load these constants from a config.txt file
# - don't forget to build a text interface to let the user edit them!
POMODORO_CYCLE_LENGTH=raw_input("Cycle length->")
POMODORO_BREAK_LENGTH=raw_input("Break Length->")
KEYBOARD_LOCKOUT_ON_BREAK=raw_input("Keyboard lockout.True or False.->")



# names of the files pertinent to Pomo
LOGNAME = 'pomo-log.txt' # by default
CONFIGNAME = 'pomo-config.txt' # by default aswell

# functionality
def init():
    #initializb the parts of pygame that let you play sound
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.wav") # drop test.wav in current directory
    global POMODORO_BREAK_LENGTH
    global POMODORO_CYCLE_LENGTH
    global GOAL_POMODOROS
    global GOAL_POMODOROS_LEFT
    global KEYBOARD_LOCKOUT_ON_BREAK
    global dbx

    # initialize the dropbox object
    TOKEN = updateLog.getToken()
    dbx = dropbox.Dropbox(TOKEN.access_token)

    # handle the dropbox login
    updateLog.verifyLogin(dbx)
    updateLog.getUpdatedLog(dbx)

    # load the configurations for the constants located in config
    with open(CONFIGNAME,'r') as f:
        for line in f.readlines():
            line = line.split()
            if line[0] == "POMODORO_CYCLE_LENGTH":
                POMODORO_CYCLE_LENGTH = int(line[1])
            if line[0] == "POMODORO_BREAK_LENGTH":
                POMODORO_BREAK_LENGTH = int(line[1])
            if line[0] == "GOAL_POMODOROS":
                GOAL_POMODOROS = int(line[1])
            if line[0] == "KEYBOARD_LOCKOUT_ON_BREAK":
                KEYBOARD_LOCKOUT_ON_BREAK = bool(line[1])
            if line[0] == "GOAL_POMODOROS_LEFT":
                goalCheck = int(line[1])

    # now lets check the date compared to the last date loaded up using the epoch and the concept of an epsilon
    # this will let us see if we should change goal pomodoros left to goal pomodoros without having to go through all the data
    # lets read the last line in config to see the last time we finished a pomodoro
    # this is a very inefficient procedure since I have to go through all lines in the config file; a better solution will be implemented when i learn sql and switch to an sql db
    with open(LOGNAME,'r') as f:
        lines = f.readlines()
    if len(lines) > 1: # if there's at least one entry
        lastDate = lines[-2].split()[0]
        print("Welcome back! The last day you used this application was "+lastDate+'.')
    else:
        lastDate = "0000-00-00"
    currentDate = str(datetime.datetime.today()).split()[0]
    if lastDate != currentDate:
        GOAL_POMODOROS_LEFT = GOAL_POMODOROS
    else:
        GOAL_POMODOROS_LEFT = goalCheck


def pomodoro():
    global GOAL_POMODOROS_LEFT

    print("You have "+str(GOAL_POMODOROS_LEFT)+" pomodoros left for today!")
    if (GOAL_POMODOROS <= 0):
        print("Look at you! Working so hard!")

    # printing some basic instructions
    print("Instructions: ")
    print("Press \"p\" to pause, and \"r\" to rewind to the beginning. If you want to rewind a certain amount backwards, supply a number after \"r\".")
    print("For example, \"r 10\" rewinds the timer back by 10 seconds.")
    print("To issue your command, press enter.")
    # add a minutes-seconds option for rewind later maybe
    startTime = time.time()
    while (time.time()-startTime < POMODORO_CYCLE_LENGTH):
        sys.stdout.write("Work Time! Time Remaining: "+pomoQoL.minsSecsString(POMODORO_CYCLE_LENGTH-(time.time()-startTime))+'\r')
        sys.stdout.flush()
        if select.select([sys.stdin],[],[], 0)[0]:
                # there is some data on stdin
                pomCmd = input().split()
                timeStartPause = time.time()
                if pomCmd[0] == 'p':
                        # pause
                        print("Press \"p\" and then enter to unpause.")
                        while True:
                            unpauseCheck = input()
                            if unpauseCheck == 'p':
                                # unpause
                                timeEndPause = time.time()
                                # decrement the time spent paused from start
                                startTime -= timeStartPause-timeEndPause
                                break;
                if pomCmd[0] == 'r':
                    if len(pomCmd) > 1:
                        try:
                            startTime += int(pomCmd[1])
                            # don't go farther than the cycle set
                            # should I let the user go farther than the cycle set?
                            # for now yes, idk if it's good design or not
                        except ValueError:
                            print("It appears you didn't give me an integer as the second argument for r!")
                    else:
                        # rewind back to start, which is the same thing as
                        # subtracting all the time before
                        startTime -= startTime - time.time()

    print("Good job! Writing to log...")
    with open(LOGNAME,'a') as f:
        dateTime = ' '.join(str(datetime.datetime.today()).split('-')).split(' ')
        hoursMinutesSeconds = str(dateTime[3]).split(':')
        f.write(dateTime[0]+' '+dateTime[1]+' '+dateTime[2]+' '+pomoQoL.getWeekday(int(dateTime[2]),int(dateTime[1]),int(dateTime[0]))+' '+hoursMinutesSeconds[0]+' '+hoursMinutesSeconds[1]+' ')
        f.write(str(POMODORO_CYCLE_LENGTH))
        f.write('\n')

    GOAL_POMODOROS_LEFT -= 1
    with open(CONFIGNAME,'r') as f:
        lines = f.readlines()
        lines[4] = "GOAL_POMODOROS_LEFT "+str(GOAL_POMODOROS_LEFT)
    with open(CONFIGNAME,'w') as f:
        f.writelines(lines)
    print("Uploading log...")
    updateLog.uploadLog(dbx)

    pygame.mixer.music.play() # the file loaded is located in init()
    print("Beginning break...")
    # maybe lock out the keyboard using sys, ik kenta said he did something similar with his gesture controlled youtube player
    startTime = time.time()
    while(time.time()-startTime < POMODORO_BREAK_LENGTH):
        sys.stdout.write("Break Time! Time Remaining: "+pomoQoL.minsSecsString(POMODORO_BREAK_LENGTH-(time.time()-startTime))+'\r')
        sys.stdout.flush()
        if select.select([sys.stdin],[],[], 0)[0]:
                # there is some data on stdin
                pomCmd = input().split()
                timeStartPause = time.time()
                if pomCmd[0] == 'p':
                        # pause
                        print("Press \"p\" and then enter to unpause.")
                        while True:
                            unpauseCheck = input()
                            if unpauseCheck == 'p':
                                # unpause
                                timeEndPause = time.time()
                                # decrement the time spent paused from start
                                startTime -= timeStartPause-timeEndPause
                                break;
                if pomCmd[0] == 'r':
                    if len(pomCmd) > 1:
                        try:
                            startTime += int(pomCmd[1])
                            # don't go farther than the cycle set
                            # should I let the user go farther than the cycle set?
                            # for now yes, idk if it's good design or not
                        except ValueError:
                            print("It appears you didn't give me an integer as the second argument for r!")
                    else:
                        # rewind back to start, which is the same thing as
                        # subtracting all the time before
                        startTime -= startTime - time.time()
    pygame.mixer.music.play()
    print()
