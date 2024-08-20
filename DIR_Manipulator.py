import os
import shutil
# local
import Interactor


# Globals

# make temporary Directory based on platform
TempDIR = (os.getcwd() + "\\" + ".temp") if Interactor.platform == 0 else (os.getcwd() + "/" + ".temp")


# Functions

# List with .img files
def IMGLIST(DIR : str) -> list:
    if os.path.exists(DIR):
        TempImgList = os.listdir(DIR) # list TempDIR files
        IMGLIST : list = []
        for img in TempImgList: 
            if img.endswith(".img"): # disregard everything that doesn't have the .img extention
                IMGLIST.append(img)
        return IMGLIST
    else:
        return []

# Copy function
def copytotemp(cloneto , clonefrom) -> int: # copy input path files to TempDIR
    files = os.listdir(clonefrom) # list input path files
    if not os.path.exists(cloneto):
        os.makedirs(cloneto) # make dir to clone to
    err = 0
    for file in files:
        print("copying " + file) # print to console file name
        if Interactor.platform == 1: # if Platform is Linux
            err = shutil.copy2(clonefrom + "/" + file , cloneto) # clone to TempDIR
        if Interactor.platform == 0: # if platform is Windows
            err = shutil.copy2(clonefrom + "\\" + file , cloneto) # cloen to TempDIR
    return err
    #shutil.copytree(clonefrom, cloneto)

# total super partition size
def IMGsizeCALC(DIR : str) -> int: # calculate size
    totalsize = 5120000 # a bit of overhead lpmake bugs out if there isn't a couple of Kb of overhead
    i = 0
    for img in IMGLIST(DIR):
        if Interactor.platform == 1: # if Platform is Linux
            totalsize += os.path.getsize(DIR + "/" + img) # get size of .img
        elif Interactor.platform == 0: # if Platform is Windows
            totalsize += os.path.getsize(DIR + "\\" + img) # get size of .img
        i += 1
    totalsize += totalsize % 512 # add devision reminder of 512 to totalsize thus making it divisable by 512 (block size)
    return totalsize