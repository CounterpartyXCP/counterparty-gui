from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import logging

class GUI(QMainWindow):

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.resize(640,480)
        self.setWindowTitle("Counterparty Wallet")

        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setIconSize(QSize(50,50))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon|Qt.AlignLeading)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)

        actions = []
        action_group = QActionGroup(self)
        action_group.setExclusive(True)
        screenWidgets = []
        self.stackedWidget = QStackedWidget()

        for ScreenClass in self.config.screenClassList:
            screenWidgets.append(ScreenClass())
            self.stackedWidget.addWidget(screenWidgets[-1])
            actions.append(QAction(screenWidgets[-1].icon, screenWidgets[-1].name, action_group))
            actions[-1].setCheckable(True)
            # hackish
            connect_code = 'actions[{}].toggled.connect(lambda checked: self.onScreenChanged(screenWidgets[{}].name, {}, checked))'
            screenIndex = len(actions) - 1
            eval(connect_code.format(screenIndex, screenIndex, screenIndex), locals())

        
        toolbar.addActions(tuple(actions))
        actions[0].setChecked(True)
        self.setCentralWidget(self.stackedWidget)
    
        self.show()

    def onScreenChanged(self, screenName, screenIndex, visibility):

        if visibility:
            logging.error(screenName + ': ' + str(screenIndex))
            self.stackedWidget.setCurrentIndex(screenIndex)

   