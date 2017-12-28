import time
import datetime
import math
import sys

POMODORO_CYCLE_LENGTH = 1 #default is 25*60
POMODORO_BREAK_LENGTH = 1 #default is 5*60
GOAL_POMODOROS = 1
GOAL_POMODOROS_LEFT = GOAL_POMODOROS
KEYBOARD_LOCKOUT_ON_BREAK = False #default is False
# NOTE: Eventually, load these constants from a config.txt file
# - don't forget to build a text interface to let the user edit them!

# functionality
def init():
    global POMODORO_BREAK_LENGTH
    global POMODORO_CYCLE_LENGTH
    global GOAL_POMODOROS
    global GOAL_POMODOROS_LEFT
    global KEYBOARD_LOCKOUT_ON_BREAK

    # load the configurations for the constants located in config
    with open('config','r') as f:
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
    with open('log','r') as f:
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
    startTime = time.time()
    while (time.time()-startTime < POMODORO_CYCLE_LENGTH):
        sys.stdout.write("Work Time! Time Remaining: "+minsSecsString(POMODORO_CYCLE_LENGTH-(time.time()-startTime))+'\r')
        sys.stdout.flush()

    print("Good job! Writing to log...")
    with open('log','a') as f:
        f.write(str(datetime.datetime.today()))
        f.write('\n')
        f.write(str(POMODORO_CYCLE_LENGTH))
        f.write('\n')

    GOAL_POMODOROS_LEFT -= 1
    print("Beginning break...")
    # maybe lock out the keyboard using sys, ik kenboo said he did something similar with his gesture controlled youtube player
    startTime = time.time()
    while(time.time()-startTime < POMODORO_BREAK_LENGTH):
        sys.stdout.write("Break Time! Time Remaining: "+minsSecsString(POMODORO_BREAK_LENGTH-(time.time()-startTime))+'\r')
        sys.stdout.flush()
    print()

    with open('config','r') as f:
        lines = f.readlines()
        lines[4] = "GOAL_POMODOROS_LEFT "+str(GOAL_POMODOROS_LEFT)
    with open('config','w') as f:
        f.writelines(lines)


# quality of life commands
def cleanCmd(roughCmd):
    # cleanCmd takes in a string roughCmd, then outputs a "cleaned" version that is only lower case letters
    cleanedCmd = ""
    for c in roughCmd:
        if ord(c) >= 97 and ord(c) <= 122:
            cleanedCmd += c
    return cleanedCmd.lower()

def minsSecsString(secondsElapsed):
    # 72.78676 seconds => 01:12:79 (mins:secs:millis)
    mins = str(math.floor(secondsElapsed/60))
    while len(mins) < 2:
        mins = '0' + mins

    secs = str(math.floor(secondsElapsed)%60)
    while len(secs) < 2:
        secs = '0' + secs

    # want the last 2 digits for millis
    millis = str(round((secondsElapsed-math.floor(secondsElapsed))*100))
    while len(millis) < 2:
        millis = '0' + millis
    if (len(millis) == 3):
        millis = millis[:-1]
    # *100 moves decimal places of all digits up by 2, and code before *100 gets the decimal value of secondsElapsed
    # then round gives you the rounded value that we wanted to begin with
    return mins+':'+secs+':'+millis

def cleanLog():
    # this function cleans the log, removing all data
    print("Are you sure you want to clean the log?")
    print("Enter y for yes, and n for no.")
    arg = input()
    if cleanCmd(arg) == 'y':
        print("Okay! Cleaning log now...")
        with open('log','w') as f:
            f.write("")

