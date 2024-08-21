from PyQt6.QtWidgets import (
    QWidget,
    QPushButton, QLabel,
    QLineEdit, QVBoxLayout,
    QGridLayout, QFileDialog,
    QListWidget, QHBoxLayout,
    QRadioButton, QCheckBox
)
from PyQt6.QtCore import (
     Qt, pyqtSignal
)
from PyQt6.QtGui import QIcon
import os
import shutil
import time
# local
import Interactor
import DIR_Manipulator
import cross_windows

# Globals

# Directory name
SuperPartitionDIR = DIR_Manipulator.TempDIR + "\\SuperPartiton" if Interactor.platform == 0 else DIR_Manipulator.TempDIR + "/SuperPartiton"


# Window


# Super Partition Editor Screen
class SuperPartitionEditorWindow(QWidget):

    switch_window = pyqtSignal()

    SLOTS = 2

    def __init__(self, INPUT):
        super().__init__()
        self.resize(400,400) # define Window Size
        self.setWindowIcon(QIcon("assets/icon.png")) # Define Icon
        self.setWindowTitle("SuperPartitionEditor") # Define Title

        layout = QVBoxLayout() # add main layout
        layout.setContentsMargins(20, 20 ,20 ,20)
        self.setLayout(layout)

        title = QLabel("THIS is Temporary UI") # Warn user
        title.setStyleSheet("font-size: 18px;")
        layout.addWidget(title, 0, Qt.AlignmentFlag.AlignCenter)
        self.LAYOUT = layout

        self.label1 = QLabel("Hange Tight We Are Extracting the Partitions !: ") # assure user
        self.label1.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.label1, 1, Qt.AlignmentFlag.AlignCenter)
        err = extract(INPUT)
        if err != 0:
            self.label1.setText("Extraction Failed!, program will restart in 5 Seconds") # try to restart
            time.sleep(5)
            self.switch_window.emit()
            
        else:
            self.label1.setText("IMG Manipulation!") # change message to content of first part of editor
        

        self.IMG_Manipulation() # manipulate IMG files

        self.SLOTS = 2 # replaces flag logic
        self.Aslot = QRadioButton()
        self.Aslot.clicked.connect(self.slotA)
        self.Bslot = QRadioButton()
        self.Bslot.clicked.connect(self.slotB)
        self.Bslot.setChecked(True)

        self.sparse = QCheckBox()
        self.sparse.setChecked(True)

        self.label3 = QLabel("A Only: ")
        self.label4 = QLabel(" A/B: ")
        self.label5 = QLabel(" : ")
        self.label6 = QLabel("Make Sparse: ")

        self.paramater_selector = QHBoxLayout() # add all above Widgets to a Layout
        self.paramater_selector.addWidget(self.label3, 0, Qt.AlignmentFlag.AlignCenter)
        self.paramater_selector.addWidget(self.Aslot, 1, Qt.AlignmentFlag.AlignCenter)
        self.paramater_selector.addWidget(self.label4, 2, Qt.AlignmentFlag.AlignCenter)
        self.paramater_selector.addWidget(self.Bslot, 3, Qt.AlignmentFlag.AlignCenter)
        self.paramater_selector.addWidget(self.label5, 4, Qt.AlignmentFlag.AlignCenter)
        self.paramater_selector.addWidget(self.label6, 5, Qt.AlignmentFlag.AlignCenter)
        self.paramater_selector.addWidget(self.sparse, 5, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.paramater_selector, 2) # add Layout to Main Layout

        self.label2 = QLabel("Output: ") # replaces flag logic and adds finish button
        self.input1 = QLineEdit()
        self.input1.setFixedWidth(120)
        self.output = QPushButton("output")
        self.output.clicked.connect(self.OutputBtn)
        self.finishbtn2 = QPushButton("Finish")
        self.finishbtn2.clicked.connect(self.finishbutton)

        self.OutputBtnFileDialog = QFileDialog(self) # output file dialog
        self.OutputBtnFileDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        self.OutputBtnFileDialog.accepted.connect(self.OutputBtnFileDialogLogic)

        self.paramater_selector2 = QHBoxLayout() # add all above Widgets to a Layout
        self.paramater_selector2.addWidget(self.label2, 0, Qt.AlignmentFlag.AlignCenter)
        self.paramater_selector2.addWidget(self.input1, 1, Qt.AlignmentFlag.AlignCenter)
        self.paramater_selector2.addWidget(self.output, 2, Qt.AlignmentFlag.AlignCenter)
        self.paramater_selector2.addWidget(self.finishbtn2, 3, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.paramater_selector2, 3) # add Layout to Main LAyout

        self.label2.hide() # hide said Widgets so they won't render ontop of first part of editor
        self.input1.hide()
        self.output.hide()
        self.finishbtn2.hide()

        self.label3.hide()
        self.label4.hide()
        self.label5.hide()
        self.label6.hide()
        self.sparse.hide()
        self.Aslot.hide()
        self.Bslot.hide()


    # Repacking stage
    # Slot RadioButtons
    def slotA(self):
        self.SLOTS = 1
    
    def slotB(self):
        self.SLOTS = 2

    # output button
    def OutputBtn(self):
        self.OutputBtnFileDialog.show()
        self.setDisabled = True

    def OutputBtnFileDialogLogic(self):
        self.input1.setText(self.OutputBtnFileDialog.selectedFiles()[0])
        self.setDisabled = False

    # finish button
    def finishbutton(self):
        err = Interactor.lpmake(
            lpmake_args(self.input1.text(), 
                        self.SLOTS, 
                        self.sparse.isChecked())) # pass lpmake code to lperr and run lpmake function
        if err != 0:
            self.label1.setText("something has gone wrong (" + str(err) + ")")
        else:
            self.label1.setText("Success!")
        
        shutil.rmtree(DIR_Manipulator.TempDIR) # clean tmp dir
        self.switch_window.emit()

    # IMG Manipulation from here on out 
    def IMG_Manipulation(self):
        self.Deletebtn = QPushButton("Delete") # add manipulation buttons
        self.Deletebtn.clicked.connect(self.deletebtn)

        self.Replacebtn = QPushButton("Replace")
        self.Replacebtn.clicked.connect(self.replacebtn)

        self.Addbtn = QPushButton("Add Dummy IMG")
        self.Addbtn.clicked.connect(self.addbtn)
        
        self.spacer = QLabel(" : ") # add a spacer

        self.Nextimgbtn = QPushButton("Next") # add a next button
        self.Nextimgbtn.clicked.connect(self.nextimgbtn)

        self.selector_buttons = QHBoxLayout()
        self.selector_buttons.addWidget(self.Deletebtn, 0, Qt.AlignmentFlag.AlignCenter)
        self.selector_buttons.addWidget(self.Replacebtn, 1, Qt.AlignmentFlag.AlignCenter)
        self.selector_buttons.addWidget(self.Addbtn, 2, Qt.AlignmentFlag.AlignCenter)
        self.selector_buttons.addWidget(self.spacer, 3, Qt.AlignmentFlag.AlignCenter)
        self.selector_buttons.addWidget(self.Nextimgbtn, 4, Qt.AlignmentFlag.AlignCenter)
        self.LAYOUT.addLayout(self.selector_buttons, 3) # add above widget to a Layout then add the Layout tot the Main Layout

        self.IMG_option_list() # generate the IMG list

        self.ReplaceBtnFileDialog = QFileDialog(self) # Replace IMG file dialog
        self.ReplaceBtnFileDialog.setFileMode(QFileDialog.FileMode.ExistingFiles) # make sure file exists!
        self.ReplaceBtnFileDialog.setNameFilter("Raw Disk Files (*.img)")
        self.ReplaceBtnFileDialog.accepted.connect(self.ReplaceBtnFileDialogLogic)
    
    # IMG_option_list
    def IMG_option_list(self):
        self.imgoptionlist = QListWidget() # make a list Widget
        for img in DIR_Manipulator.IMGLIST(SuperPartitionDIR): # loop for img files
            self.imgoptionlist.addItem("(" + img + ") size of (" + str(os.path.getsize(SuperPartitionDIR + "/" + img)) + ") bytes") # add img files name & size to list
        self.LAYOUT.addWidget(self.imgoptionlist, 2, Qt.AlignmentFlag.AlignCenter) # add list to Layout

    # delete button
    def deletebtn(self):
        try: # I'm using this very annoying function (self.imgoptionlist.currentItem().text()) to be able to tell if user selected a img or not among other things
            self.confirm_window = cross_windows.Confirmation_Window(self.imgoptionlist.currentItem().text()) # add a Confirmation_Window
            self.confirm_window.confirmed.connect(self.deletebtnconfirm) # link signals
            self.confirm_window.denied.connect(self.deletebtndeny)
            self.confirm_window.show()
            self.setDisabled = True # Disable self until confirmation screen signal
        except AttributeError:
            pass
    
    def deletebtnconfirm(self):
        if Interactor.platform == 1: # delete selected .img on Linux platform
            os.remove(SuperPartitionDIR + "/" + DIR_Manipulator.IMGLIST(SuperPartitionDIR)[self.imgoptionlist.currentIndex().row()])
        if Interactor.platform == 0: # delete selected .img on Windows platform
            os.remove(SuperPartitionDIR + "\\" + DIR_Manipulator.IMGLIST(SuperPartitionDIR)[self.imgoptionlist.currentIndex().row()])
        
        self.LAYOUT.removeWidget(self.imgoptionlist) # delete img list
        self.IMG_option_list() # regenrate img list
        self.confirm_window.hide()
        self.setDisabled = False # enable self
        print("Partition Deleted!")
    
    def deletebtndeny(self):
        self.confirm_window.hide()
        self.setDisabled = False
        print("Partition Skipped!")

    # replace button
    def replacebtn(self):
        try:
            self.imgoptionlist.currentItem().text() # I'm using this very annoying function to be able to tell if user selected a img or not
            self.ReplaceBtnFileDialog.show() # enable File DIalog
            self.setDisabled = True
        except AttributeError:
            pass
    
    def ReplaceBtnFileDialogLogic(self):
        if Interactor.platform == 1: # replace .img for Linux Platform
            shutil.copy(self.ReplaceBtnFileDialog.selectedFiles()[0] , SuperPartitionDIR + "/" + DIR_Manipulator.IMGLIST(SuperPartitionDIR)[self.imgoptionlist.currentIndex().row()])
        if Interactor.platform == 0: # replace .img for Windows Platform
            shutil.copy(self.ReplaceBtnFileDialog.selectedFiles()[0] , SuperPartitionDIR + "\\" + DIR_Manipulator.IMGLIST(SuperPartitionDIR)[self.imgoptionlist.currentIndex().row()])

        self.LAYOUT.removeWidget(self.imgoptionlist)
        self.IMG_option_list()
        self.setDisabled = False
        print("Partition Replaced!")

    # add button
    def addbtn(self):
        self.addimg_window = AddImg() # make add img Window
        self.addimg_window.confirmed.connect(self.addimg)
        self.addimg_window.denied.connect(self.denyaddimg)
        self.addimg_window.show()
        self.setDisabled = True
    
    def addimg(self, name):
        if Interactor.platform == 1: # add a .img in Linux Platform
            os.system("dd if=/dev/zero of='{tempdir}/{name}.img' bs=1 count=0".format(tempdir=SuperPartitionDIR , name=name))
        elif Interactor.platform == 0: # add a .img in Windows Platform
            os.system("powershell {command}"
                .format(command="fsutil file createnew '{tempdir}\\{name}.img' 0"
                .format(tempdir=SuperPartitionDIR , name=name)))
        
        self.LAYOUT.removeWidget(self.imgoptionlist)
        self.IMG_option_list() # regenerate img list
        self.addimg_window.hide()
        self.setDisabled = False

    def denyaddimg(self):
        self.addimg_window.hide()
        self.setDisabled = False
    
    # finish button
    def nextimgbtn(self):
        self.confirm_window = cross_windows.Confirmation_Window("Are you sure you want to finish editing the IMG?") # go to next part of editor
        self.confirm_window.confirmed.connect(self.nextimgbtnconfirm)
        self.confirm_window.denied.connect(self.nextimgbtndeny)
        self.confirm_window.show()
        self.setDisabled = True
    
    def nextimgbtnconfirm(self): # hide previous content and show next content
        # hide
        self.imgoptionlist.hide()
        self.Deletebtn.hide()
        self.Replacebtn.hide()
        self.Addbtn.hide()
        self.spacer.hide()
        self.Nextimgbtn.hide()
        self.confirm_window.hide()
        self.label1.setText("Set parameters:")
        # show
        self.label2.show()
        self.input1.show()
        self.output.show()
        self.finishbtn2.show()

        self.label3.show()
        self.label4.show()
        self.label5.show()
        self.label6.show()
        self.sparse.show()
        self.Aslot.show()
        self.Bslot.show()

        self.setDisabled = False
    
    def nextimgbtndeny(self):
        self.confirm_window.hide()
        self.setDisabled = False

# AddImg Window
class AddImg(QWidget): # a reporpused confirmation Window (cross_windows.py) see the notes there they are more detailed.
        confirmed = pyqtSignal(str)
        denied = pyqtSignal()

        def __init__(self):
            super().__init__()
            self.resize(200,200)
            self.setWindowIcon(QIcon("assets/icon.png"))
            self.setWindowTitle("ADD IMG")

            layout = QGridLayout()
            layout.setContentsMargins(20, 20 ,20 ,20)
            self.setLayout(layout)
            
            title = QLabel("THIS is Temporary UI")
            title.setStyleSheet("font-size: 18px;")
            layout.addWidget(title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

            label1 = QLabel("dummy img name:") # standard Inputs
            layout.addWidget(label1, 1 , 0)

            self.input1 = QLineEdit()
            layout.addWidget(self.input1, 1, 1)

            acceptbtn = QPushButton("Accept")
            acceptbtn.clicked.connect(self.acceptbtn)

            denybtn = QPushButton("Deny")
            denybtn.clicked.connect(self.denybtn)

            
            layout.addWidget(acceptbtn, 2, 0, Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(denybtn, 2, 1, Qt.AlignmentFlag.AlignCenter)

        def acceptbtn(self):
            self.confirmed.emit(self.input1.text())
        def denybtn(self):
            self.denied.emit()


# Functions


# lpunpack or copy from dir
def extract(INPUT : str) -> int:
    err = 0
    if os.path.isdir(INPUT): # if input is path
        err = DIR_Manipulator.copytotemp(SuperPartitionDIR , INPUT) # copy to TempDIR
    elif INPUT.endswith(".img"): # if input is a .img file
        Interactor.lpunpack(INPUT, SuperPartitionDIR) # unpack super.img
    else:
        err = 1
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