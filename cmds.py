import time
import datetime 
import math

POMODORO_CYCLE_LENGTH = 0 #normally pomodoro cycle lengths are set to this
# NOTE: Eventually, load this from a config.txt file

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
    secs = str(math.floor(secondsElapsed)%60)
    # want the last 2 digits for millis
    millis = str(round((secondsElapsed-math.floor(secondsElapsed))*100))
    # *100 moves decimal places of all digits up by 2, and code before *100 gets the decimal value of secondsElapsed
    # then round gives you the rounded value that we wanted to begin with 
    return mins+':'+secs+':'+millis

# functionality
def pomodoro():
    startTime = time.time()
    while (time.time()-startTime < POMODORO_CYCLE_LENGTH):
        print("Time Remaining: "+minsSecsString(POMODORO_CYCLE_LENGTH-(time.time()-startTime)))
    print("Good job! Writing to log...")
    print(datetime.datetime.today())
    with open('log','a') as f:
        f.write(str(datetime.datetime.today()))
        f.write('\n')
        f.write(str(POMODORO_CYCLE_LENGTH))
        f.write('\n')
    
def cleanLog():
    # this function cleans the log, removing all data
    print("Are you sure you want to clean the log?")
    print("Enter y for yes, and n for no.")
    arg = input()
    if cleanCmd(arg) == 'y':
        print("Okay! Cleaning log now...")
        with open('log','w') as f:
            f.write("")
    
