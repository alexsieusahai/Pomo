import cmds

commandList = ["help","pomodoro","exit","cleanlog"]

print("Hello, and welcome to Pomo! If you have any features you want implemented, please log it as an issue or modify the source code and open a pull request.")
print("Made by Alexander Sieusahai (ItsPax).")
cmds.init()
while(True):
    print("Please enter a command or input \"help\" to see a list of commands.")
    cmd = input()
    cmd = cmds.cleanCmd(cmd)

    if (cmd == "help"):
        print("Available commands:")
        for command in commandList:
            print(command)
        #NOTE: Let the user learn more about each command through this later

    if (cmd == "pomodoro"):
        cmds.pomodoro()

    if (cmd == "exit"):
        exit()

    if (cmd == "cleanlog"):
        cmds.cleanLog()


