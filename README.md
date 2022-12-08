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
