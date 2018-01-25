import pandas as pd
from ggplot import *

def printGraphs():
    data = pd.read_csv('pomo-log.txt', sep = " ", header = None)
    # add weekday
    data.columns = ("Year", "Month","Day", "Weekday", "Hour", "Minute", "Length of Pomodoro (Seconds)")
    #print(ggplot(data, aes('Day', 'Length of Pomodoro (Seconds)',color = "Year")) + \
    #        geom_point())
    data['MonthlyTotal'] = data.groupby(['Month'])['Length of Pomodoro (Seconds)'].transform('sum') # gets you the monthly total of the data given
    data['WeekdayTotal'] = data.groupby(['Weekday'])['Length of Pomodoro (Seconds)'].transform('sum') # gets you the monthly total of the data given
    data['TimeSpentThatDay'] = data.groupby(['Year', 'Month','Day'])['Length of Pomodoro (Seconds)'].transform('sum') # gets you the monthly total of the data given
    data['TimeSpentDuringHour'] = data.groupby(['Hour'])['Length of Pomodoro (Seconds)'].transform('sum') # gets you the monthly total of the data given
    print(data)


printGraphs()
