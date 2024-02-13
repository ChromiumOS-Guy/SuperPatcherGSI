import os
import argparse
import shutil
import pathlib

TempDIR = os.getcwd() + "\\" + ".temp"
HERE = os.path.realpath(os.path.dirname(__file__))

def dir_path(string):
    if os.path.isdir(string):
        return os.path.realpath(string)
    else:
        raise NotADirectoryError(string)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-i' , '--input' , type=argparse.FileType('r') , help='''input the super.img that is going to be modifed, if super.img is sparse its going to temporarily be unsparsed''')
parser.add_argument('-o' , '--output', help="Directs the output to a name of your choice")
parser.add_argument('-s' , '--SLOT' , type=int , help="number of slots on the device can only be 1 (A) or 2 (A/B)")
parser.add_argument('-p', '--path' , type=dir_path , help="specifies input to be a folder and not an super.img")
args = parser.parse_args()

# err check
def check():
    err = ""
    try:
        if args.SLOT == 1 or args.SLOT == 2:
            pass
        else:
            print("Invalid Slot number ({slot})".format(slot=args.SLOT))
            err += " &SLOT"
        if args.input == None:
            if args.path != "":
                pass
            else:
                print("Invalid path at PATH please input a valid directory")
                err += " &InvalidPath"
        elif args.input.name.endswith(".img"):
            pass
        else:
            print("Invalid Format at INPUT please use .img file")
            err += " &InvalidFormatINPUT"
        if args.output.endswith(".img"):
            pass
        else:
            print("Invalid Format at INPUT please use .img file")
            err += " &InvalidFormatOUTPUT"
        if err == "":
            err = "OK"
    except ValueError:
        err = "Flag ValueError"
    except AttributeError:
        err = "Flag AttributeError"
    return err

# unpack / replacing

def lpunpack(): # PAIN just PAIN
    #!/usr/bin/python  # -*- coding: latin-1 -*-
    os.system("powershell {command}"
        .format(command=repr(".\'{dir}\\lpunpack.exe' {superimg} '{tempdir}'"
            .format(superimg=args.input.name, tempdir=TempDIR , dir=HERE))))

def IMGmanipulation(): # choose an img file to be replaced
    TempImgList = os.listdir(TempDIR)
    d = 0
    for img in TempImgList:
            if img.endswith(".img"):
                d += 1

    print("Chosse Operation:")
    if d != 0:
        print("1. Delete Partition")
        print("2. Replace Partition")
    print("3. Add Partition")
    Operation = input("select: ")
    if d == 0 and Operation != "3":
        IMGmanipulation()
    if Operation != "1" and Operation != "2" and Operation != "3":
        IMGmanipulation()
    i = 0
    if Operation == "2" or Operation == "1":
        for img in TempImgList:
            if img.endswith(".img"):
                print("option number " + str(i) + " " + TempImgList[i] + " size of (" + str(os.path.getsize(TempDIR + "\\" + img)) + ") bytes")
            i += 1
    while (True):
        try:
            imgnum = "0"
            if Operation == "2" or Operation == "1":
                imgnum = input("Please Choose: ")
            if int(imgnum) <= i - 1 or Operation == "3":
                while (True):
                    try:
                        if Operation == "1": # just making sure
                            os.remove(TempDIR + "\\" + TempImgList[int(imgnum)])
                            print("Partition Deleted!")
                            break
                        elif Operation == "2":
                            try:
                                while(True):
                                    replacmentpath = input("Please Input Path To Replacment Partition:\n")
                                    replacmentpath = str(pathlib.Path(replacmentpath).absolute())
                                    if replacmentpath.endswith(".img"):
                                        redo = input("Are you sure this is the path to file (Y/n): ")
                                        if redo == "Y" or redo == "y" or redo == "yes" or redo == "Yes" or redo == "": # just making sure
                                            shutil.copy(replacmentpath , TempDIR + "\\" + TempImgList[int(imgnum)])
                                            print("Partition Replaced!")
                                            break
                                    elif replacmentpath.endswith(" "):  # sometimes people tap space it ruins it and it can and will get confusing
                                        print("Path Ends With Space!!")
                                    else:
                                        print("Please Input a Valid Path to a IMG File!") 
                                break
                            except ValueError:
                                print("Please Input a Valid Path!")
                            except AttributeError:
                                print("How did you even manage to get AttributeError, this is here just incase !?")
                        elif Operation == "3":
                            name = ""
                            size = 0
                            while (True):
                                try:
                                    if name == "":
                                        name = input("Input Partition Name: ")
                                    size = input("Input Partition Size: ")
                                    print("name: " + name)
                                    print("size: " + size)
                                    redo = input("Is This Correct? (Y/n): ")
                                    if redo == "Y" or redo == "y" or redo == "yes" or redo == "Yes" or redo == "": # just making sure
                                        break
                                    name = ""
                                except ValueError:
                                    print("Please Put a Valid Number!")
                            os.system("powershell {command}"
                                .format(command="fsutil file createnew '{tempdir}\\{name}.img' {size}"
                                    .format(tempdir=TempDIR , name=name , size=int(size))))
                            break
                    except ValueError:
                        print("Please Put a Valid Number!")
                redo = input("Replace/Delete/Add another (Y/n): ")
                if redo == "Y" or redo == "y" or redo == "yes" or redo == "Yes": # just making sure
                    IMGmanipulation()
                break
            else:
                print("Please Put a Valid Number!")
        except ValueError:
            print("Please Put a Number In!")

def IMGsizeCALC(): # calculate size
    totalsize = 5120000 # a bit of overhead
    TempImgList = os.listdir(TempDIR)
    i = 0
    for img in TempImgList:
        if img.endswith(".img"):
            totalsize += os.path.getsize(TempDIR + "\\" + img)
        i += 1
    reminder = totalsize % 512 # making devision by 512
    totalsize += reminder
    return totalsize

# lpmake
def lpmake(devicesize , metadatasize):
    lpmake_args = " --device-size={devicesize}".format(devicesize=devicesize) + " --metadata-slots={slot}".format(slot=args.SLOT) + " --output {output}".format(output=args.output) + " --metadata-size {metadatasize}".format(metadatasize=metadatasize)
    sparse = input("make sparse (flashable with fastboot) ? (Y/n): ")
    if sparse == "Y" or sparse == "y" or sparse == "yes" or sparse == "Yes" or sparse == "": # just making sure
        lpmake_args += " --sparse"
    
    lpmake_args = lpmake_add_args(lpmake_args)
    print("============================")
    print("    using these flags:")
    print("============================")
    print(lpmake_args)
    print("============================")
    
    return os.system("powershell {command}"
        .format(command=".\'{dir}\\lpmake.exe' {lpargs}"
            .format(lpargs=lpmake_args , dir=HERE)))

def lpmake_add_args(lpmake_args):
    TempImgList = os.listdir(TempDIR)
    for img in TempImgList:
        if img.endswith(".img"):
            lpmake_args += " --partition={name}:none:{size}".format(name=os.path.splitext(img)[0] , size=os.path.getsize(TempDIR + "\\" + img))
            if os.path.getsize(TempDIR + "\\" + img) != 0:
                lpmake_args += " --image={name}={filedir}".format(name=os.path.splitext(img)[0] , filedir=repr((TempDIR + "\\" + img)))
    return lpmake_args

def testdvi512(num):
    if num % 512 == 0:
        return True
    else:
        return False

def copytotemp(cloneto , clonefrom):
    files = os.listdir(clonefrom)
    os.makedirs(cloneto)
    for file in files:
        print("copying " + file)
        shutil.copy2(clonefrom + "\\" + file , cloneto)
    #shutil.copytree(clonefrom, cloneto)

def main():
    err = check()

    if err != "OK":
        print("error code ({error}) exiting...!".format(error=err))
        return err
    else:
        print("flags successfully verified and appear to be correct, error code ({error})".format(error=err))
    if args.path != None:
        print("============================")
        print("   copying to temp dir...")
        print("============================")
        copytotemp(TempDIR , args.path)
    else:
        print("============================")
        print("        unpacking...")
        print("============================")
        lpunpack()
    print("============================")
    print("      img manipulation ")
    print("============================")
    
    
    IMGmanipulation() # IMG manipulation of selected partition
    #let user choose size
    metadatasize = 512000
    devicesize = IMGsizeCALC()
    print("============================")
    try:
        dvsize = input("device size (super.img size) in bytes must be evenly divisible by 512, default ({devicesize}) bytes: ".format(devicesize=devicesize))
        if dvsize != "" and testdvi512(int(dvsize)):
            devicesize = int(dvsize)
    except ValueError:
        print("Invalid Number skipping ..!")
    
    try:
        mdsize = input("metadata size in bytes must be evenly divisible by 512 default=~0.5KiB: ")
        if mdsize != "" and testdvi512(int(dvsize)):
            metadatasize = int(mdsize)
    except ValueError:
        print("Invalid Number skipping ..!")
    
    #repack
    lperr = lpmake(devicesize , metadatasize)
    err = lperr if lperr != 0 else err # give lpmake error as external code if there was an error
    print("============================")
    print("        cleaning...")
    print("============================")
    shutil.rmtree(TempDIR) # clean tmp dir
    return err # return err code to external

try:
    err = main()
except KeyboardInterrupt:
    print("\n============================")
    print("        cleaning...")
    print("============================")
    shutil.rmtree(TempDIR) # clean tmp dir
exit(err)