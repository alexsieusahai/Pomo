import sys
import dropbox
from dropbox.files import WriteMode
import cmds # for config and log file names as constants
POMOPATH = '/Pomo' # path assumes beginning at tilde

dbx = dropbox.Dropbox('xglEndL0ibAAAAAAAAAAQWanVXdULHt4x0k5ULepFMxfRGdU7vLBd9soY6xodqiK')

try:
    dbx.users_get_current_account()
except dropbox.exceptions.AuthError:
    sys.exit("Authentication Failed. Please make sure you entered the correct username and password.")

## upload the pomo-log file to the users dropbox
#with open('pomo-log.txt', 'rb') as f:
#    print("Uploading " + 'pomo-log.txt' + " to Dropbox...")
#    dbx.files_upload(f.read(), '/'+'pomo-log.txt', mode=WriteMode('overwrite'))
#
## download the pomo-log file to the current path
#print("downloading the log file...")
#dbx.files_download('/'+'pomo-log.txt')
#print("Done!")
#
## check out the metadata of the log file to get size here
#print(dbx.files_get_metadata('/pomo-log.txt').size)


