# Pull Request Template

## Type of change

- [ ] Bug fix
- [ ] Feature
- [ ] "Documentation" (readme) update

## Description

*describe here*

## Notice
if you don't want to wait for a new release for you're changes to be applied you should package in the appropriate formats for Windows and Linux (Linux being AppImage and Windows being a .zip file)
and include them here by attaching the files in the pull request NOT in the code!

## Checklist
be sure to test for both Windows & Linux

--- Flags

- [ ] Slot flag works
- [ ] Output flag works
- [ ] Input flag works
- [ ] Help flag works

--- CLI

- [ ] Extracting from super.img
- [ ] Extracting from folder
- [ ] Adding a dummy .img file
- [ ] Replacing a .img file
- [ ] Removing a .img file
- [ ] Device size override works
- [ ] Metadata size override works
- [ ] Sparse override works
- [ ] Able to make new super.img

--- Optional

- [ ] new AppImage works
- [ ] new Windows files work after setup from .zip



## Recommendations
- its best to use a standard ROM like LineageOS or AOSP can be found <a href="https://github.com/phhusson/treble_experimentations/wiki/Generic-System-Image-%28GSI%29-list"> here </a>
- use a known working super.img with stock paritions so you can test functions and confirm it still works afterwards. 

