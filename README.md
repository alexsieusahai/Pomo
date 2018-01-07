# Pomo
A more fully fledged Pomodoro timer, contained completely on the command line. Tested using a _GNOME_ terminal.  

_Features:_  
- Includes pause and rewind functionality  
- Dropbox support for storing your logs and configurations across multiple systems  
- **(YET TO BE IMPLEMENTED)** A merging tool that lets you merge logs across multiple  
- Logs all of your pomodoros since you began using the application  
- All settings configurable without leaving the application  
- Shell script for convenient starting of application  
- **(YET TO BE IMPLEMENTED)** View your statistics on a myriad of time settings  

_Dependencies:_  
**NOTE:** To install `pip3`, type the below into your terminal:  
`sudo apt install python3-pip`  
  
- `pygame`; install with `pip3 install pygame`  
- `dropbox`; install with `pip3 install dropbox`  

_First time run:_  
1. Make sure that you have the dependencies installed!  
2. `git clone https://github.com/ItsPax/Pomo` to get the source code for the application.  
3. Navigate to the directory.   
4. `./start` to start the application.  
5. Clean the log and start anew by typing in `cleanlog`. 
6. Enjoy!


_To do:_  
- Set up a merging utility so you can merge the local log and the dropbox log together, then upload the new dropbox log  
- Reorganize constants  
- Implement some user interface to change the configs in `config.txt` without the user having to manually edit `config.txt`  
- Implement a units solution for the rewind command in `pomodoro()`  
- Statistics for the week  
- Statistics for month by month, weekday, etc  
