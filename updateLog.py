import sys
import os

import dropbox
from dropbox.files import WriteMode
from dropbox import DropboxOAuth2FlowNoRedirect

import cmds # for config and log file names as constants

LOGPATH = '/'+'pomo-log.txt'

def verifyLogin(dbx):
    try:
        dbx.users_get_current_account()
        return True
    except dropbox.exceptions.AuthError:
        sys.exit("Authentication Failed. Please make sure you entered the correct username and password.")
        return False

def test(dbx):
    auth_flow = DropboxOAuth2FlowNoRedirect('9plb44sduiyoc4p','dvwyswuwvx3bhag')
    authorize_url = auth_flow.start()
    print(authorize_url)
    auth_code = input().strip()
    oauth_result = auth_flow.finish(auth_code)
    print(oauth_result)

## upload the pomo-log file to the users dropbox
#with open(cmds.logName, 'rb') as f:
#    print("Uploading " + cmds.logName + " to Dropbox...")
#    dbx.files_upload(f.read(), '/'+cmds.logName, mode=WriteMode('overwrite'))
#
## download the pomo-log file to the current path
#print("downloading the log file...")
#dbx.files_download('/'+cmds.logName)
#print("Done!")
#
## check out the metadata of the log file to get size here
#print(dbx.files_get_metadata('/'+cmds.logName).size)

# check for existence
def checkLogExists(dbx):
    try:
        dbx.files_get_metadata(LOGPATH)
        return True
    except:
        return False

def getUpdatedLog(dbx):
    if checkLogExists(dbx):
        # check to see if log has changed
        print("Verified that the log exists! Checking if the log size on server is smaller than the one locally...")
        if os.path.getsize(os.path.dirname(os.path.realpath(__file__))+LOGPATH) < dbx.files_get_metadata(LOGPATH).size:
            print("Grabbing the updated log from your Dropbox...")
            dbx.files_download_to_file('/home/pax/Pomo/pomo-log.txt',LOGPATH)
        elif os.path.getsize(os.path.dirname(os.path.realpath(__file__))+LOGPATH) == dbx.files_get_metadata(LOGPATH).size:
            print("Logs are the same! Doing nothing...")
        else:
            print("You have a log bigger than the one on your dropbox server. Uploading the one you have locally...")
            uploadLog(dbx)
    else:
        print("No log found on Dropbox server. Uploading the one locally...")
        uploadLog(dbx)

def uploadLog(dbx):
    with open('pomo-log.txt', 'rb') as f:
        print("Uploading log to your Dropbox...")
        dbx.files_upload(f.read(), LOGPATH,mode=WriteMode('overwrite'))
        print("Done!")

