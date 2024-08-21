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
    try:
        for file in files:
            print("copying " + file) # print to console file name
            if Interactor.platform == 1: # if Platform is Linux
                shutil.copy2(clonefrom + "/" + file , cloneto) # clone to TempDIR
            if Interactor.platform == 0: # if platform is Windows
                shutil.copy2(clonefrom + "\\" + file , cloneto) # cloen to TempDIR
    except IsADirectoryError:
        err = 1
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

# test if Divisable by 512
def testdvi512(num): # test if number is divisable by 512
    if num % 512 == 0: # return true if yes
        return True
    else: # false if no
        return False

# delete TempDIR
def deletetempDIR():
    if os.path.exists(TempDIR):
        shutil.rmtree(TempDIR)