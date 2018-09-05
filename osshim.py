import os
import sys
import platform
import pipes

###
### The point of this file is to abstract out our OS level calls so we can shim
### in some test methods. #testing 
### 
mswindows = (sys.platform == "win32")

if mswindows:
    from subprocess import list2cmdline
    quote_args = list2cmdline
else:
    # POSIX
    from pipes import quote

    def quote_args(seq):
        return ' '.join(quote(arg) for arg in seq)


def movieFolder():
	if (sys.platform == "win32"):
		return "C:\\Media\\"
	else:
		return "/media/nas/afschuld/Movies"

def tvFolder():
	if (sys.platform == "win32"):
		return "C:\\Media\\TV"
	else:
		return "/media/nas/afschuld/TV Shows/"

def makeSureTargetDirExists(targetdir):
    if isdir(targetdir):
        return
    pathparts = os.path.split(targetdir)
    makeSureTargetDirExists(pathparts[0])
    os.system('mkdir ' + pipes.quote(targetdir))
    #print('mkdir ' + pipes.quote(pathparts[1]))
    if (platform.system() != "Windows"):
        os.system('chmod 775 ' + pipes.quote(targetdir))
        #print('chmod 775 ' + pipes.quote(targetdir))

def link(source, target, targetdir):
    makeSureTargetDirExists(targetdir)
    if (platform.system() == "Windows"):
        cmd = 'mklink '
        flag = "/H"
        if (os.path.isdir(source)):
            flag = "/J"
        
        cmd += quote_args([flag, source, target])
        os.system(cmd)
    else:
        #cmd = 'mkdir ' + pipes.quote(targetdir)
        #print cmd
        #os.system(cmd)
        cmd = 'ln ' + pipes.quote(source) +' '+ pipes.quote(targetdir)
        #print cmd
        os.system(cmd)
        cmd = 'chmod 664 ' + pipes.quote(target)
        #print cmd
        os.system(cmd)
        cmd = 'chmod 775 ' + pipes.quote(targetdir)
        #print cmd
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
