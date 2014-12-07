from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import logging

class DexScreen(QWidget):

    def __init__(self):
        super().__init__() 

        self.name = "DEX"
        self.icon = QIcon('assets/competitors-icon.png')

        label = QLabel("DEX")
        layout = QVBoxLayout()
        layout.addWidget(label) 

        self.setLayout(layout)
        #self.setStyleSheet("background-color: red;")
        self.resize(640,480)