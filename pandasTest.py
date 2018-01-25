import pandas as pd

data = pd.read_csv('pomo-log.txt', sep = " ", header = None)
data.columns = ("Date", "Time", "Length of Pomodoro")
print(data)
