import logging
import json
import os
import sys
from decimal import Decimal as D

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QJSValue

from PyQt5 import QtWidgets, QtCore, QtGui

from counterpartygui.api import CounterpartydAPI
from counterpartygui.config import Config

CURR_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))

class MenuItem(QLabel):
    def __init__(self, text, parent=None):
        QLabel.__init__(self, parent)
        self.parent = parent
        self.setText(text)

    def activate(self):
        pluginIndex = self.property('pluginIndex')
        actionValue = self.property('actionValue')
        # display the plugin
        self.parent.stackedWidget.setCurrentIndex(pluginIndex)
        # call the plugin callback
        self.parent.plugins[pluginIndex].onMenuAction(actionValue)
        # change style
        if self.parent.currentMenuItem:
            self.parent.currentMenuItem.setProperty('active', 'false')
        self.setProperty('active', 'true')
        self.parent.currentMenuItem = self
        self.parent.refreshStyleSheet()

    def mouseReleaseEvent(self, event):
        self.activate()

class GUI(QMainWindow):

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.resize(1024, 680)
        self.setWindowTitle("Counterparty GUI")

        def openPreference():
            self.config.initialize(openDialog=True)
            self.loadPlugins()

        # Add Preferences menu 
        mainMenuBar = QMenuBar()
        newAct = QAction("Preferences...", self)
        newAct.triggered.connect(openPreference)
        fileMenu = mainMenuBar.addMenu("Counterparty GUI")
        fileMenu.addAction(newAct)
        self.setMenuBar(mainMenuBar)

        self.loadPlugins()

    def loadPlugins(self):

        # init toolbar
        if hasattr(self, 'toolbar'):
            self.removeToolBar(self.toolbar)
            del(self.toolbar)
            
        self.toolbar = QToolBar()
        self.toolbar.setAutoFillBackground(True);
        self.toolbar.setObjectName('menu')
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon|Qt.AlignLeft)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.currentMenuItem = None

        # init QML plugin container
        if hasattr(self, 'stackedWidget'):
            del(self.stackedWidget)

        self.stackedWidget = QStackedWidget(self)
        self.plugins = []

        # init clientapi
        self.xcpApi = CounterpartydAPI(self.config)

        actionIndex = 0
        for pluginName in self.config.PLUGINS:
            view = QQuickView();
            view.setFlags(Qt.SubWindow)

            # add clientapi into the plugin context
            context = view.rootContext()

            context.setContextProperty("xcpApi", self.xcpApi)
            context.setContextProperty("GUI", self)

            # load QML file
            plugin_index_path = 'plugins/{}/index.qml'.format(pluginName)
            view.setSource(QUrl(plugin_index_path))
            
            plugin = view.rootObject()
            pluginIndex = len(self.plugins)
            self.plugins.append(plugin)

            # call plugin init callback
            plugin.init()

            # generate the left menu
            menu = plugin.property('menu')
            if isinstance(menu, QJSValue):
                menu = menu.toVariant()
            if menu and isinstance(menu, dict) and 'items' in menu and isinstance(menu['items'], list):
                # menu title
                if 'groupLabel' in menu:
                    menuGroupLabel = QLabel(menu['groupLabel'])
                    menuGroupLabel.setProperty('isGroupLabel', 'true')
                    self.toolbar.addWidget(menuGroupLabel)
                # menu item
                items = []
                for menuItem in menu['items']:
                    if isinstance(menuItem, dict) and 'label' in menuItem  and 'value' in menuItem:
                        items.append(MenuItem(menuItem['label'], self))
                        items[-1].setProperty('pluginIndex', pluginIndex)
                        items[-1].setProperty('actionValue', menuItem['value'])
                        items[-1].setProperty('isAction', 'true') 
                        self.toolbar.addWidget(items[-1])
                        if self.currentMenuItem is None:
                            self.currentMenuItem = items[-1]

            # add the plugin in the container
            container = QWidget.createWindowContainer(view, self)
            self.stackedWidget.addWidget(container)

        # display the plugin container
        self.currentMenuItem.activate()
        self.refreshStyleSheet()
        self.setCentralWidget(self.stackedWidget)
        
        self.show()

    def refreshStyleSheet(self):
        self.setStyleSheet('''
            QToolBar#menu { background-color: #ececec; border: 1px solid #ececec; border-right-color: #000; }
            QToolBar#menu QLabel { width:100%; text-align:left; padding:3px; margin:0; }
            QToolBar#menu QLabel[isAction="true"]:hover { background-color:#CCC; }
            QToolBar#menu QLabel[active="true"] { background-color:#CCC; }
            QToolBar#menu QLabel[isAction="true"] { padding-left: 15px; }
            QToolBar#menu QLabel[isGroupLabel="true"] { color:#888888; text-transform:uppercase; }
        ''')

    # used in QML to display a confirm dialog
    @pyqtSlot(QVariant, QVariant, result=QVariant)
    def confirm(self, title, text):
        result = QMessageBox.question(self, title, text)
        if result == QMessageBox.Yes:
            return True
        else:
            return False

    # used in QML to display a message dialog
    @pyqtSlot(QVariant, QVariant)
    def alert(self, title, text):
        QMessageBox.information(self, title, text)
        
def main():
    app = QApplication(sys.argv)
    splash_path = os.path.join(CURR_DIR, '..', 'assets', 'splash.png')
    splash_pix = QtGui.QPixmap(splash_path)
    splash = QtWidgets.QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    splash.showMessage("Loading wallet...", Qt.AlignBottom | Qt.AlignHCenter);

    app.processEvents()

    config = Config()
    screen = GUI(config)

    def quitApp():
        sys.exit()

    app.aboutToQuit.connect(quitApp)

    splash.finish(screen)
    app.exec()

