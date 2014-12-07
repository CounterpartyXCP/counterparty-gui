from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import logging

class ContractsScreen(QWidget):

    def __init__(self):
        super().__init__() 

        self.name = "Contracts"
        self.icon = QIcon('assets/signature-icon.png')

        label = QLabel("Contracts")
        layout = QVBoxLayout()
        layout.addWidget(label) 

        self.setLayout(layout)
        #self.setStyleSheet("background-color: blue;")
        self.resize(640,480)