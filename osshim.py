import os
import sys
import platform
import pipes

###
### The point of this file is to abstract out our OS level calls so we can shim
### in some test methods. #testing
###
mswindows = (sys.platform == "win32")

def debuglog(log):
    if not os.environ.get("DEBUG"):
        return
    print(log)

if mswindows:
    from subprocess import list2cmdline
    quote_args = list2cmdline
else:
    # POSIX
    from pipes import quote

    def quote_args(seq):
        return ' '.join(quote(arg) for arg in seq)


def movieFolder():
    # check to see if the user passes in a movies directory
    env_movie = os.environ.get('MOVIE')
    if env_movie:
        return env_movie
    
    if (sys.platform == "win32"):
        return "C:\\Media\\"
    else:
        return "/afschuld/Movies/"

def tvFolder():
    env_tv = os.environ.get('TV')
    if env_tv:
        return env_tv
    
    if (sys.platform == "win32"):
        return "C:\\Media\\TV"
    else:
        return "/afschuld/TV Shows/"

def makeSureTargetDirExists(targetdir):
    if isdir(targetdir):
        return
    if (platform.system() == "Windows"):
        os.makedirs(targetdir)
        debuglog('created directories to ' + targetdir)
    else:
        pathparts = os.path.split(targetdir)
        makeSureTargetDirExists(pathparts[0])
        os.system('mkdir ' + pipes.quote(targetdir))
        debuglog('mkdir ' + pipes.quote(pathparts[1]))
        os.system('chmod 775 ' + pipes.quote(targetdir))
        debuglog('chmod 775 ' + pipes.quote(targetdir))

def link(source, target, targetdir):
    makeSureTargetDirExists(targetdir)
    if (platform.system() == "Windows"):
        cmd = 'mklink '
        flag = "/H"
        if (os.path.isdir(source)):
            flag = "/J"

        cmd += quote_args([flag, target, source])
        os.system(cmd)
    else:
        #cmd = 'mkdir ' + pipes.quote(targetdir)
        #print cmd
        #os.system(cmd)
        target_file = pipes.quote(targetdir)
        if os.path.exists(target_file):
            print("Not re-creating hardlink at: " + target_file)
        else:
            cmd = 'ln ' + pipes.quote(source) +' '+ target_file
            debuglog(cmd)
            os.system(cmd)
        cmd = 'chmod 775 ' + pipes.quote(target)
        debuglog(cmd)
        
        os.system(cmd)
        cmd = 'chmod 775 ' + pipes.quote(targetdir)
        debuglog(cmd)
        os.system(cmd)

    return "linked " + source + " => " + targetdir

def listdir(path):
    return os.listdir(path)

def isdir(path):
    return os.path.isdir(path)

def allowFolderLink():
    if (sys.platform == "win32"):
        return True
    else:
        return False

def extract(source, target):
    if (platform.system() == "Windows"):
        # Todo: unrar here
        a = []
    else:
        b = []

    return "extracted " + source + " => " + target

def findShow(showName):
    return ""
