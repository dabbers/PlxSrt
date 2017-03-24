import os
import sys
import platform

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
    return r"C:\Media\"

def tvFolder():
    return r"C:\Media\TV\"

def link(source, target):
    if (platform.system() == "Windows"):
        cmd = 'mklink '
        flag = "/H"
        if (os.path.isdir(source)):
            flag = "/J"
        
        cmd += quote_args([flag, source, target])

        os.system(cmd)
    else:
        cmd = 'ln ' + sourcedir + '/' + filename +' '+ target
        os.system(cmd)

    return "linked " + source + " => " target

def listdir(path):
    return os.listdir(path)

def isdir(path):
    return os.path.isdir(path)


def extract(source, target):
    if (platform.system() == "Windows"):
        # Todo: unrar here
        a = []
    else:
        b = []
    
    return "extracted " + source + " => " target

def findShow(showName):
    return ""