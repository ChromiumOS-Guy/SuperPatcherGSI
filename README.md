# SuperPatcherGSI
Autmated Script to Patch a Super.img with a GSI in python 3

Linux/Windows 64-bit ONLY

### Linux (64-bit)
```bash
./SuperPatcherGSI-x64.AppImage -i super.img (input) -o super.new.img (output) -s 2 (device slots)
```
Linux AppImage dosen't have the -p flag it gets reconized automaticlly so -p is incoperated into -i

## Command Flags (Linux):
```
usage: SuperPatcherGSI.py [-h] [-i INPUT] [-o OUTPUT] [-s SLOT] [-p PATH]

options:
  -h                    show this help message and exit
  -i INPUT
                        Input the super.img that is going to be modifed, if super.img is sparse its
                        going to temporarily be unsparsed
                        you can also input a directory with files to be packed to an super.img
  -o OUTPUT
                        Directs the output to a name of your choice
  -s slots              Number of slots on the device can only be 1 (A) or 2 (A/B)

```

### Windows (64-bit)
```powershell
python .\SuperPatcherGSI.py -i super.img (input) -o super.new.img (output) -s 2 (device slots)
```

## Command Flags (Windows):
```
usage: SuperPatcherGSI.py [-h] [-i INPUT] [-o OUTPUT] [-s SLOT] [-p PATH]

options:
  -h                    show this help message and exit
  -i INPUT
                        Input the super.img that is going to be modifed, if super.img is sparse its
                        going to temporarily be unsparsed
                        you can also input a directory with files to be packed to an super.img
  -p PATH               Replacment for INPUT incase you already have an unpacked super.img
                        you can refer the path to the unpacked super.img folder
  -o OUTPUT
                        Directs the output to a name of your choice
  -s slots              Number of slots on the device can only be 1 (A) or 2 (A/B)

```

python version used to test / build the linux/windows script (Python 3.10.6)

### Known Issues:
 1. for some pepole lpunpack.py crashes i need to find a fix for that somehow?

### lpmake errors: 
lpmake has no documentation (that I have heard of) except this one page here (https://android.googlesource.com/platform/system/extras/+/master/partition_tools/)

so I'm giving a very small list of lpmake errors which I know how to fix or the meaning of (relevant to the script):

Errors  | Meaning/Fix
------------- | -------------
Not enough space on device for partition (PARTITION NAME HERE) with size (PARTITION SIZE HERE)  | this means that the --device-size flag for lpmake was set with a maximum size which is smaller than all the partitions (unpacked img files + GSI) combined.
Invalid sparse file format at header magic / Invalid sparse file format at header | this is actually a warning and can be ignored its actually a good sign if you get this warning


### sources:
using lpmake for linux from (https://ci.android.com/builds/branches/aosp-master/grid)

using lpmake for windows from (https://github.com/affggh/lpmake_and_lpunpack_cygwin)

using lpunpack.py from (https://github.com/unix3dgforce/lpunpack), Compiled to .exe for Windows Version.
