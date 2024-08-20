import os
# local
import Interactor
import DIR_Manipulator

# Globals

# Directory name
SuperPartitionDIR = DIR_Manipulator.TempDIR + "\\SuperPartiton" if Interactor.platform == 0 else DIR_Manipulator.TempDIR + "/SuperPartiton"


# Functions


# lpunpack or copy from dir
def extract(INPUT : str) -> int:
    err = 0
    if os.path.isdir(INPUT): # if input is path
        err = DIR_Manipulator.copytotemp(SuperPartitionDIR , INPUT) # copy to TempDIR
    elif INPUT.endswith(".img"): # if input is a .img file
        err = Interactor.lpunpack(INPUT, SuperPartitionDIR) # unpack super.img
    else:
        err = "{INPUT} is a Invalid path or file!".format(INPUT=INPUT)
    return err

# partition arg generation
def lpmake_img_args(lpmake_args , DIR) -> str:
    if Interactor.platform == 1: # Linux
        for img in DIR_Manipulator.IMGLIST(DIR): 
            if img.endswith(".img"): # disregard everything that isn't .img file
                lpmake_args += " --partition={name}:none:{size}".format(name=os.path.splitext(img)[0] , size=os.path.getsize(DIR + "/" + img)) # add partition name & size
                if os.path.getsize(DIR + "/" + img) != 0: # add .img file location only if it actually stores data and is not a dummy .img file
                    lpmake_args += " --image={name}={filedir}".format(name=os.path.splitext(img)[0] , filedir=(DIR + "/" + img)) # add corresponding parition image and its dir location
    elif Interactor.platform == 0: # Windows
        for img in DIR_Manipulator.IMGLIST(DIR):
            if img.endswith(".img"): # disregard everything that isn't .img file
                lpmake_args += " --partition={name}:none:{size}".format(name=os.path.splitext(img)[0] , size=os.path.getsize(DIR + "\\" + img)) # add partition name & size
                if os.path.getsize(DIR + "\\" + img) != 0: # add .img file location only if it actually stores data and is not a dummy .img file
                    lpmake_args += " --image={name}={filedir}".format(name=os.path.splitext(img)[0] , filedir=repr((DIR + "\\" + img))) # add corresponding parition image and its dir location
    return lpmake_args

# lpmake full arg generation
def lpmake_args(OUTPUT : str , SLOT : int = 2 , sparseable : bool = True , devicesize : int = 0 , metadatasize : int = 512000) -> str: # function for assembling lpmake flags 
    if devicesize == 0:
        devicesize = DIR_Manipulator.IMGsizeCALC(SuperPartitionDIR)

    lpmake_args = (
        " --device-size={devicesize}".format(devicesize=devicesize) # add size of super.img
        + " --metadata-slots={slot}".format(slot=SLOT) # define type of device the super.img is for s=1 (A) s=2 (A/B)
        + " --output {output}".format(output=OUTPUT) # define output path
        + " --metadata-size {metadatasize}".format(metadatasize=metadatasize) # define metadata size
        + " --sparse" if sparseable else "" # make flashable with fastboot
    )  
    
    lpmake_args = lpmake_img_args(lpmake_args, SuperPartitionDIR) # add partitions

    return lpmake_args