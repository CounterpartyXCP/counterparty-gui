from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
import logging

from core.api import CounterpartydAPI

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

class PluginContainer(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

    def requestActivate(self):
        logging.error("requestActivate()!")


class GUI(QMainWindow):

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.resize(1024, 680)
        self.setWindowTitle("Counterparty GUI")

        # init toolbar
        toolbar = QToolBar()
        toolbar.setAutoFillBackground(True);
        toolbar.setObjectName('menu')
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon|Qt.AlignLeft)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        self.currentMenuItem = None

        # init QML plugin container
        self.stackedWidget = QStackedWidget(self)
        self.plugins = []

        # init xcpApi
        self.xcpApi = CounterpartydAPI(config) 
        actionIndex = 0
        for pluginName in self.config.PLUGINS:
            view = QQuickView();
            view.setFlags(Qt.SubWindow)

            # add xcpApi into the plugin context
            context = view.rootContext()
            context.setContextProperty("xcpApi", self.xcpApi)
            context.setContextProperty("GUI", self)

            # load QML file
            view.setSource(QUrl('plugins/{}/{}.qml'.format(pluginName, pluginName)));            
            
            plugin = view.rootObject()
            pluginIndex = len(self.plugins)
            self.plugins.append(plugin)

            # call plugin init callback
            plugin.init()

            # generate the left menu
            menu = plugin.property('menu')
            if menu and isinstance(menu, dict) and 'items' in menu and isinstance(menu['items'], list):
                # menu title
                if 'groupLabel' in menu:
                    menuGroupLabel = QLabel(menu['groupLabel'])
                    menuGroupLabel.setProperty('isGroupLabel', 'true')
                    toolbar.addWidget(menuGroupLabel)
                # menu item
                items = []
                for menuItem in menu['items']:
                    if isinstance(menuItem, dict) and 'label' in menuItem  and 'value' in menuItem:
                        items.append(MenuItem(menuItem['label'], self))
                        items[-1].setProperty('pluginIndex', pluginIndex)
                        items[-1].setProperty('actionValue', menuItem['value'])
                        items[-1].setProperty('isAction', 'true') 
                        toolbar.addWidget(items[-1])
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

    @pyqtSlot(QVariant, QVariant, result=QVariant)
    def confirm(self, title, text):
        result = QMessageBox.question(self, title, text)
        if result == QMessageBox.Yes:
            return True
        else:
            return False

    @pyqtSlot(QVariant, QVariant)
    def alert(self, title, text):
        QMessageBox.information(self, title, text)
        
   