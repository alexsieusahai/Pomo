import math

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
        with open(logName,'w') as f:
            f.write("")

def exitAndGoodbye():
    print("Goodbye!")
    exit()

def getWeekday(day,month,year):
    """
    INPUTS:
        day - what day of the month it is (1-31)
        month - what month it is (1-12)
        year: - what year it is (arbitrary integer)
    RETURNS:
        weekday given the specified inputs
    ACKNOWLEDGEMENTS:
        https://blog.artofmemory.com/how-to-calculate-the-day-of-the-week-4203.html
    """
    yearCode = ((year%100)+(year%100)//4)%7
    monthDict = {1:0, 2:3, 3:3, 4:6, 5:1, 6:4, 7:6, 8:2, 9:5, 10:0, 11:3, 12:5}
    monthCode = monthDict[month]
    centuryCode = 6
    leapYearCode = 0
    if ((not (year%4) and (year%100)) or not (year%400)):
        leapYearCode = 1
    weekdayDict = {0:'Sunday', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday'}
    return weekdayDict[(yearCode+monthCode+centuryCode+day-leapYearCode)%7]

#def changeConfig():
    # allows the user to change the configs set
