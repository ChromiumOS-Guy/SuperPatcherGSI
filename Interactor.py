import os
import platform


# Globals

# Check platform
platform = 1 if platform.system() == 'Linux' else 0 if platform.system() == 'Windows' else 2
# 0 = Windows
# 1 = Linux
# 2 = Unknown

# Find current script Directory
HERE = os.path.realpath(os.path.dirname(__file__))

 
# Functions

# unpack super.img

def lpunpack(SUPER : __file__, TempDIR : __path__) -> str:
    #!/usr/bin/python  # -*- coding: latin-1 -*-
    err
    if platform == 1: # if platform is Linux (platform == 1) then launch lpunpack.py on Linux
        err = os.system("python3 '{dir}/lpunpack.py' {superimg} '{tempdir}'".format(superimg=SUPER, tempdir=TempDIR , dir=HERE))
    if platform == 0:# if platform is Windows (platform == 0) then launch lpunpack.py on Windows
        err = os.system("python '{dir}\lpunpack.py' {superimg} '{tempdir}'".format(superimg=SUPER, tempdir=TempDIR , dir=HERE))
    return str(err)

# repack patched super.img

def lpmake(lpmake_args) -> str:
    if platform == 1: # run lpmake for Linux Platform with flag chain
        return os.system("'{dir}/bin/lpmake' {lpargs}".format(lpargs=lpmake_args , dir=HERE))
    if platform == 0: # run lpmake for Windows Platform with flag chain
        return os.system("powershell {command}"
        .format(command=".\'{dir}\\bin\\lpmake.exe' {lpargs}"
            .format(lpargs=lpmake_args , dir=HERE)))

