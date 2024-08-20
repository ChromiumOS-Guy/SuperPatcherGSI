import os
import argparse
import shutil
import pathlib
# local
import Interactor
import DIR_Manipulator
import SuperPartitionManipulator


# figure out if platform is Linux or Windows
platform = Interactor.platform

# decides if input is path or file 
def mod_path(string):
    if os.path.isfile(string): # check if its a file
        return string
    elif os.path.isdir(string): # check if its a Directory == path
        return os.path.realpath(string)

# init argparse
parser = argparse.ArgumentParser(add_help=True)
# add flags
parser.add_argument('-i' , '--input' , type=mod_path , help='''Input the super.img that is going to be modifed if super.img is sparse its going to temporarily be unsparsed, you can also input a directory with files to be packed to an super.img''')
parser.add_argument('-o' , '--output', help="Directs the output to a name of your choice")
parser.add_argument('-s' , '--SLOT' , type=int , help="number of slots on the device can only be 1 (A) or 2 (A/B)")
args = parser.parse_args() # get flags


# err check
def check():
    
    err = ""
    try:
        if args.SLOT == 1 or args.SLOT == 2: # check if slot flag has correct value
            pass
        else: # errors out if anything that isn't 1 (A) or 2 (A/B) is inputed into slot flag
            print("Invalid Slot number ({slot})".format(slot=args.SLOT))
            err += " &SLOT"
        if args.input.endswith(".img") and os.path.isfile(args.input): # check if input flag is a file and ends with a .img
            pass
        elif os.path.isdir(args.input): # check if input is a path
            pass 
        else: # errors out if it isn't a path nor a .img file
            print("Invalid Format at INPUT please use .img file or valid directory")
            err += " &InvalidFormatINPUT"
        if args.output.endswith(".img"): # checks that output format is .img
            pass
        else: # errors out if output format is not .img
            print("Invalid Format at OUTPUT please use .img file")
            err += " &InvalidFormatOUTPUT"
        if err == "": #if everything checks then signal OK err code
            err = "OK"
    except ValueError: # catch value errors from inputing strings in integers and vis-versa
        err = "Flag ValueError"
    except AttributeError: # catch attribute errors if any are found
        err = "Flag AttributeError"
    return err

# VERY TEMPORARY CLI
def IMGmanipulation(): # choose an img file to be replaced
    TempImgList = os.listdir(SuperPartitionManipulator.SuperPartitionDIR) # get a list of all files in TempDIR Directory 
    d = 0
    for img in TempImgList: # filter everything except .img files
            if img.endswith(".img"):
                d += 1
    print("Chosse Operation:")
    if d != 0: # if d == 0 then there are not .img to delete or replace so hide options
        print("1. Delete Partition")
        print("2. Replace Partition")
    print("3. Add Partition")
    Operation = input("select: ")
    if d == 0 and Operation != "3": #restart function if user chooses an option that isn't useable without pre-existing .img files
        IMGmanipulation()
    if Operation != "1" and Operation != "2" and Operation != "3": # if operation is not supported then restart function
        IMGmanipulation()
    i = 0
    if Operation == "2" or Operation == "1": # if operation was not create an .img file then print a list of available .img files to console
        for img in TempImgList:
            if img.endswith(".img"):
                print("option number " + str(i) + " " + TempImgList[i] + " size of (" + str(os.path.getsize(SuperPartitionManipulator.SuperPartitionDIR + "/" + img)) + ") bytes")
            i += 1
    while (True): # main function logic
        try:
            imgnum = "0"
            if Operation == "2" or Operation == "1": # if operation requieres a pre-existing .img then prompt user to select which .img to affect
                imgnum = input("Please Choose: ") 
            if int(imgnum) <= i - 1 or Operation == "3": # check that selected .img isn't out of bounds if user selected a .img to affect
                while (True):
                    try:
                        if Operation == "1": # if user choose to delete a .img 
                            if platform == 1: # delete selected .img on Linux platform
                                os.remove(SuperPartitionManipulator.SuperPartitionDIR + "/" + TempImgList[int(imgnum)])
                            if platform == 0: # delete selected .img on Windows platform
                                os.remove(SuperPartitionManipulator.SuperPartitionDIR + "\\" + TempImgList[int(imgnum)])
                            print("Partition Deleted!")
                            break # exit second while loop
                        elif Operation == "2": # if user choose to replace
                            try:
                                while(True):
                                    replacmentpath = input("Please Input Path To Replacment Partition:\n") # ask for replacment .img path
                                    replacmentpath = str(pathlib.Path(replacmentpath).absolute()) # get replacment .img absolute path 
                                    if replacmentpath.endswith(".img"): # make sure path ends with a .img file extention
                                        redo = input("Are you sure this is the path to file (Y/n): ") # make user confirm choice 
                                        if redo == "Y" or redo == "y" or redo == "yes" or redo == "Yes" or redo == "": # if user confirms then replace .img else repeat while loop
                                            if platform == 1: # replace .img for Linux Platform
                                                shutil.copy(replacmentpath , SuperPartitionManipulator.SuperPartitionDIR + "/" + TempImgList[int(imgnum)])
                                            if platform == 0: # replace .img for Windows Platform
                                                shutil.copy(replacmentpath , SuperPartitionManipulator.SuperPartitionDIR + "\\" + TempImgList[int(imgnum)])
                                            print("Partition Replaced!")
                                            break # exit third while loop
                                    elif replacmentpath.endswith(" "):  # prints error if path is invalid and repeats while loop
                                        print("Path Ends With Space!!")
                                    else:
                                        print("Please Input a Valid Path to a IMG File!") 
                                break # exit second while loop
                            except ValueError: # if path value is invalid or not a string
                                print("Please Input a Valid Path!")
                            except AttributeError: # failsafe incase I missed an bug 
                                print("How did you even manage to get AttributeError, this is here just incase !?")
                        elif Operation == "3": # if user choose to add an .img file
                            name = ""
                            size = 0
                            while (True):
                                try:
                                    if name == "": # if name is empty then ask for name
                                        name = input("Input Partition Name: ")
                                    size = input("Input Partition Size: ") # ask for size
                                    print("name: " + name) # print inputed name
                                    print("size: " + size) # print inputed size
                                    redo = input("Is This Correct? (Y/n): ") # ask for confirmation
                                    if redo == "Y" or redo == "y" or redo == "yes" or redo == "Yes" or redo == "":
                                        break
                                    name = ""
                                except ValueError: # catch if user inputs a string instead of size
                                    print("Please Put a Valid Number!")
                            if platform == 1: # add a .img in Linux Platform
                                os.system("dd if=/dev/zero of='{tempdir}/{name}.img' bs=1 count={size}".format(tempdir=SuperPartitionManipulator.SuperPartitionDIR , name=name , size=size))
                            if platform == 0: # add a .img in Windows Platform
                                os.system("powershell {command}"
                                .format(command="fsutil file createnew '{tempdir}\\{name}.img' {size}"
                                    .format(tempdir=SuperPartitionManipulator.SuperPartitionDIR , name=name , size=int(size))))
                            break # exit second while loop
                    except ValueError: # catch if string inputed instead of number (int)
                        print("Please Put a Valid Number!")
                redo = input("Replace/Delete/Add another (Y/n): ") # ask if user want to delete/replace/add another .img
                if redo == "Y" or redo == "y" or redo == "yes" or redo == "Yes" or redo == "": # just making sure
                    IMGmanipulation()
                break # exit first while loop
            else:
                print("Please Put a Valid Number!")
        except ValueError:
            print("Please Put a Number In!")


def testdvi512(num): # test if number is divisable by 512
    if num % 512 == 0: # return true if yes
        return True
    else: # false if no
        return False


def main(): # script main()
    err = check() # check err 

    if err != "OK": # if error code isn't OK then print error message and exit
        print("error code ({error}) exiting...!".format(error=err))
        return err
    else: # else print to console a confirmation message
        print("flags successfully verified and appear to be correct, error code ({error})".format(error=err))
    
    print("============================")
    print("        extracting...")
    print("============================")
    SuperPartitionManipulator.extract(args.input)

    print("============================")
    print("      img manipulation ")
    print("============================")
    do = input("Replace/Delete/Add (Y/n): ") # ask user if they want to affect existing .img files or create new ones
    if do == "Y" or do == "y" or do == "yes" or do == "Yes" or do == "": # just making sure
        IMGmanipulation() # IMG manipulation of selected partition
    print("============================")
    
    #repack: note add sparse, devicesize and metadatasize options after convertion to GUI
    lpmake_args = SuperPartitionManipulator.lpmake_args(args.output , args.SLOT)
    print("============================")
    print("     using these flags")
    print("============================")
    print(lpmake_args)
    print("============================")
    lperr = Interactor.lpmake(lpmake_args) # pass lpmake code to lperr and run lpmake function
    err = lperr if lperr != 0 else err # give lpmake error as external code if there was an error
    print("============================")
    print("        cleaning...")
    print("============================")
    shutil.rmtree(DIR_Manipulator.TempDIR) # clean tmp dir
    return err # return err code to external

try:
    err = main() # run script main()
except KeyboardInterrupt: # clean if interrupted
    print("\n============================")
    print("        cleaning...")
    print("============================")
    shutil.rmtree(DIR_Manipulator.TempDIR) # clean tmp dir
exit(err)
