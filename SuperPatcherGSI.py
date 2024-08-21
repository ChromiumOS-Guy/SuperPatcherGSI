from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QPushButton, QLabel,
    QLineEdit,
    QGridLayout, QFileDialog,
    QListWidget,
)
from PyQt6.QtCore import (
     Qt, pyqtSignal
)
from PyQt6.QtGui import QIcon
import sys

# local
import DIR_Manipulator
import SuperPartitionManipulator


# Input Screen
class Input_Window(QWidget):
    switch_window = pyqtSignal(str ,int)

    def __init__(self):
        super().__init__()
        self.resize(200,200) # define window size
        self.setWindowIcon(QIcon("assets/icon.png")) # add Icon
        self.setWindowTitle("INPUT SELECTION") # define title

        layout = QGridLayout()
        layout.setContentsMargins(20, 20 ,20 ,20) # define margins from window edge
        self.setLayout(layout)

        title = QLabel("THIS is Temporary UI") # Warn User
        title.setStyleSheet("font-size: 18px;")
        layout.addWidget(title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        self.optionlist = QListWidget() # select window to go to
        self.optionlist.addItem("Super Partition Editor")
        layout.addWidget(self.optionlist, 1, 1, Qt.AlignmentFlag.AlignCenter)

        label1 = QLabel("Input File: ") # standard GUI Directory Inputs
        layout.addWidget(label1, 2, 0)

        label2 = QLabel("Input Directory: ")
        layout.addWidget(label2, 3, 0)

        self.input1 = QLineEdit() # Technaclliy these are the True Inputs
        layout.addWidget(self.input1, 2, 1)

        self.input2 = QLineEdit()
        layout.addWidget(self.input2, 3, 1)

        self.FileDialog1 = QFileDialog(self) # file Dialogs and buttons
        self.FileDialog1.setFileMode(QFileDialog.FileMode.ExistingFiles)
        self.FileDialog1.setNameFilter("Raw Disk Files (*.img)")
        self.FileDialog1.accepted.connect(self.FileDialogLogic1)

        browsefiles1 = QPushButton("browse files")
        browsefiles1.clicked.connect(self.browsefiles1)
        layout.addWidget(browsefiles1, 2 , 3, Qt.AlignmentFlag.AlignRight)

        self.FileDialog2 = QFileDialog(self)
        self.FileDialog2.setFileMode(QFileDialog.FileMode.Directory)
        self.FileDialog2.accepted.connect(self.FileDialogLogic2)

        browsefiles2 = QPushButton("browse files")
        browsefiles2.clicked.connect(self.browsefiles2)
        layout.addWidget(browsefiles2, 3 , 3, Qt.AlignmentFlag.AlignRight)


        apply = QPushButton("Apply") # apply input and switch window
        apply.setFixedWidth(120)
        apply.clicked.connect(self.applyinput)
        layout.addWidget(apply, 4 , 1, Qt.AlignmentFlag.AlignCenter)

    def browsefiles1(self): # file Dialog and Button Functions
        self.FileDialog1.show()

    def FileDialogLogic1(self):
        self.input1.setText(self.FileDialog1.selectedFiles()[0])
        self.input2.setText("")
    
    def browsefiles2(self):
        self.FileDialog2.show()

    def FileDialogLogic2(self):
        self.input2.setText(self.FileDialog2.selectedFiles()[0])
        self.input1.setText("")

    def applyinput(self): # apply input and switch to next screen in controller
        INPUT = ""

        if self.input1.text() != "":
            INPUT = self.input1.text()
        elif self.input2.text() != "":
            INPUT = self.input2.text()
        else:
            print("Invalid Input!")
            exit(1)

        self.switch_window.emit(INPUT, self.optionlist.currentIndex().row())



app = QApplication(sys.argv)


# Controller LOGIC
class Controller:

    current_window : QWidget = QWidget()

    def __init__(self):
        pass

    def show_input(self): # could be called a "main menu" but its more like a selector with an INPUT
        self.input_window = Input_Window()
        self.input_window.switch_window.connect(self.window_selector)
        self.current_window.hide() # hide current window
        self.input_window.show()

    def window_selector(self, INPUT, INDEX): # allows for switching of windows depnding on selection in input_window
        self.input_window.hide()
        if INDEX == 0:
            self.show_super_partition_editor(INPUT)
        elif INDEX == 1: # future stuff
            pass

    def show_super_partition_editor(self, INPUT):
        self.super_partition_editor_window = SuperPartitionManipulator.SuperPartitionEditorWindow(INPUT)
        self.super_partition_editor_window.switch_window.connect(self.show_input) # return to input window when
        self.current_window = self.super_partition_editor_window # allows other windows to accese this one by making it current window
        self.super_partition_editor_window.show()


controller = Controller() # start of program!
controller.show_input()

sys.exit(app.exec(), # run program
         DIR_Manipulator.deletetempDIR() # delete Temporary Directory on exit
) # end of program