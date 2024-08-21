from PyQt6.QtWidgets import (
    QWidget,
    QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout,
)
from PyQt6.QtCore import (
     Qt, pyqtSignal
)

from PyQt6.QtGui import QIcon

# confirmation window
class Confirmation_Window(QWidget):
    confirmed = pyqtSignal()
    denied = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.resize(200,200) # define size
        self.setWindowIcon(QIcon("assets/icon.png")) # add Icon
        self.setWindowTitle("Confirmation Window") # Window Title

        layout = QVBoxLayout() # make main Layout
        layout.setContentsMargins(20, 20 ,20 ,20) # define margins from window edge
        self.setLayout(layout) # add main layout
        
        title = QLabel("THIS is Temporary UI") # Warn user this is Temporary
        title.setStyleSheet("font-size: 18px;") # add CSS
        layout.addWidget(title, 0, Qt.AlignmentFlag.AlignCenter) # add title widget to layout

        label1 = QLabel(text) # make a label with passthrough text
        label1.setStyleSheet("font-size: 16px;") # add CSS
        layout.addWidget(label1, 1) # add label Widget

        acceptbtn = QPushButton("YES") # make yes button
        acceptbtn.clicked.connect(self.acceptbtn) # connect clicked signal to function acceptbtn

        denybtn = QPushButton("NO") # make no button
        denybtn.clicked.connect(self.denybtn) # connect clicked signal to function denybtn

        self.selector_buttons = QHBoxLayout() # make a HBoxLayout
        self.selector_buttons.addWidget(acceptbtn, 0, Qt.AlignmentFlag.AlignCenter) # add acceptbtn to HBoxLayout
        self.selector_buttons.addWidget(denybtn, 1, Qt.AlignmentFlag.AlignCenter) # add denybtn to HBoxLayout
        layout.addLayout(self.selector_buttons, 2) # add HBoxLayout to Main Layout (VBoxLayout)

    def acceptbtn(self): # emit confirmed signal or denied signal
        self.confirmed.emit() 
    def denybtn(self):
        self.denied.emit()