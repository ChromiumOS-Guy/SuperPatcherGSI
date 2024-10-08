# SuperPatcherGSI
Automated Script to Patch a Super.img with a GSI in python 3,

I am open to pull requests (to indev-release) if you have any.

Linux/Windows 64-bit ONLY

## WARNING!:
This tool is made with the assumption that it's users understand the risks involved in modifying Android's super partition and its potential consequences. I am not responsible for any damage caused by using this script.

### Before proceeding:

  * Always back up your original super.img partition and do not delete it until you are confident the patched version works correctly, This backup is nice to have if the need for recovery arises.
    
  * Make sure to flash the vbmeta partition with the disable_verity flag for changes to presist because in some cases they don't.
    
  * I recommend reviewing the scripts code to understand its functionality and potential risks.

While the script is designed to operate within a contained directory, improper usage could still lead to unexpected behavior.

### Additional Resources

  * https://youtu.be/Yj19JewRmSA
    
  * https://xdaforums.com/t/editing-system-img-inside-super-img-and-flashing-our-modifications.4196625/#post-84024089

By using this tool, you acknowledge and accept the inherent risks involved.


## Linux (64-bit)
```bash
./SuperPatcherGSI-x64.AppImage -i super.img (input) -o super.new.img (output) -s 2 (device slots)
```

## Windows (64-bit)
```powershell
python .\SuperPatcherGSI.py -i super.img (input) -o super.new.img (output) -s 2 (device slots)
```

### Command Flags:
```
usage: SuperPatcherGSI.py [-h] [-i INPUT] [-o OUTPUT] [-s SLOT]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input the super.img that is going to be modifed if
                        super.img is sparse its going to temporarily be
                        unsparsed, you can also input a directory with files
                        to be packed to an super.img
  -o OUTPUT, --output OUTPUT
                        Directs the output to a name of your choice
  -s SLOT, --SLOT SLOT  number of slots on the device can only be 1 (A) or 2
                        (A/B)
```

python version used to test/build the linux/windows script (Python 3.10.6)

### Known Issues:
 * for some pepole lpunpack.py crashes i need to find a fix for that somehow?

### lpmake errors: 
lpmake has no documentation (that I have heard of) except this one page here (https://android.googlesource.com/platform/system/extras/+/master/partition_tools/)

so I'm giving a very small list of lpmake errors which I know how to fix or the meaning of (relevant to the script):

Errors  | Meaning/Fix
------------- | -------------
Not enough space on device for partition (PARTITION NAME HERE) with size (PARTITION SIZE HERE)  | this means that the --device-size flag for lpmake was set with a maximum size which is smaller than all the partitions (unpacked img files + GSI) combined.
Invalid sparse file format at header magic / Invalid sparse file format at header | this is actually a warning and can be ignored its actually a good sign if you get this warning


### sources:
* using lpmake for linux from (https://ci.android.com/builds/branches/aosp-master/grid)

* using lpmake for windows from (https://github.com/affggh/lpmake_and_lpunpack_cygwin)

* using lpunpack.py from (https://github.com/unix3dgforce/lpunpack), Compiled to .exe for Windows Version.
