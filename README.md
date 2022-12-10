# SuperPatcherGSI
Autmated Script to Patch a Super.img with a GSI in python 3

using lpmake for windows from (https://github.com/affggh/lpmake_and_lpunpack_cygwin)

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

so I'm giving a very small list of lpmake errors which I know how to fix or I the meaning of:

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
