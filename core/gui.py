from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
import logging

class CounterpartydAPI(QObject):
    def __init__(self):
        super(CounterpartydAPI, self).__init__()

    @pyqtSlot(QVariant, result=QVariant)
    def call(self, query):
        return QVariant({"toto": query['command']})

class GUI(QMainWindow):

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.resize(800, 600)
        self.setWindowTitle("Counterparty Wallet")

        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon|Qt.AlignLeading)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)

        actionGroup = QActionGroup(self)
        actionGroup.setExclusive(True)

        self.stackedWidget = QStackedWidget()
        self.plugins = []

        self.xcpApi = CounterpartydAPI() 

        for pluginName in self.config.plugins:
            view = QQuickView();
            context = view.rootContext()
            context.setContextProperty("xcpApi", self.xcpApi)
            view.setSource(QUrl('plugins/{}/{}.qml'.format(pluginName, pluginName)));            
            
            plugin = view.rootObject()
            pluginIndex = len(self.plugins)
            self.plugins.append(plugin)
            plugin.init()
            menu = plugin.property('menu')

            if menu and isinstance(menu, dict) and 'items' in menu and isinstance(menu['items'], list):

                if 'groupLabel' in menu:
                    menuGroupLabel = QLabel(menu['groupLabel'])
                    toolbar.addWidget(menuGroupLabel)

                for menuItem in menu['items']:
                    if isinstance(menuItem, dict) and 'label' in menuItem  and 'value' in menuItem:
                        actionIndex = len(actionGroup.actions())
                        action = QAction(menuItem['label'], actionGroup)
                        action.setProperty('pluginIndex', pluginIndex)
                        action.setProperty('actionValue', menuItem['value'])
                        action.setCheckable(True)
                        toolbar.addAction(action)

                if 'groupLabel' in menu:
                    toolbar.addSeparator()

            container = QWidget.createWindowContainer(view, self);
            self.stackedWidget.addWidget(container)

        actionGroup.triggered.connect(self.onMenuAction)
        self.setCentralWidget(self.stackedWidget)
        
        self.show()

    def onMenuAction(self, action):
        pluginIndex = action.property('pluginIndex')
        actionValue = action.property('actionValue')
        self.stackedWidget.setCurrentIndex(pluginIndex)
        self.plugins[pluginIndex].onMenuAction(actionValue)
           

   