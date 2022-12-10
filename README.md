# SuperPatcherGSI
Autmated Script to Patch a Super.img with a GSI in python 3

### How to run on windows
```powershell
python .\SuperPatcherGSI.py -i super.img (input) -o super.new.img (output) -g lineageOS.img (GSI) -s 2 (device slots)
```

### Command Flags:
```
usage: SuperPatcherGSI.py [-h] [-i INPUT] [-o OUTPUT] [-g GSI] [-s SLOT]

options:
  -h, --help            displays all flags and there purpose
  -i INPUT, --input INPUT
                        input the super.img that is going to be modifed, if super.img is sparse its going to
                        temporarily be unsparsed
  -o OUTPUT, --output OUTPUT
                        Directs the output to a name of your choice
  -g GSI, --gsi GSI     GSI (Generic System Image) that will be replacing the existing system.img (Stock Rom)
  -s SLOT, --SLOT SLOT  number of slots on the device can only be 1 (A) or 2 (A/B)
```

### lpmake errors: 
lpmake has no documentation (that I have heard of) except this one page here (https://android.googlesource.com/platform/system/extras/+/master/partition_tools/)

so I'm giving a very small list of lpmake errors which I know how to fix or the meaning of:

Errors  | Meaning/Fix
------------- | -------------
Not enough space on device for partition (PARTITION NAME HERE) with size (PARTITION SIZE HERE)  | this means that the --device-size flag for lpmake was set with a maximum size which is smaller than all the partitions (unpacked img files + GSI) combined.
[liblp]Partition should only have linear extents: (PARTITION NAME HERE)  | this error code can be resolved by deleteing said partition (which rectifies the error) and just reflashing stock rom (stock super.img) first and then flashing the GSI modifed super.img, (works for me that may not be the case for you keep that in mind while trying this out).


### sources:
using lpmake for windows from (https://github.com/affggh/lpmake_and_lpunpack_cygwin)

using lpunpack.py from (https://github.com/unix3dgforce/lpunpack)
