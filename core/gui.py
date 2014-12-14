from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
import logging

from core.api import CounterpartydAPI

class GUI(QMainWindow):

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.resize(800, 600)
        self.setWindowTitle("Counterparty Wallet")

        # init toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon|Qt.AlignLeading)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        actionGroup = QActionGroup(self)
        actionGroup.setExclusive(True)

        # init QML plugin container
        self.stackedWidget = QStackedWidget()
        self.plugins = []

        # init xcpApi
        self.xcpApi = CounterpartydAPI(config) 

        for pluginName in self.config.PLUGINS:
            view = QQuickView();
            # add xcpApi into the plugin context
            context = view.rootContext()
            context.setContextProperty("xcpApi", self.xcpApi)
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
                    toolbar.addWidget(menuGroupLabel)
                # menu item
                for menuItem in menu['items']:
                    if isinstance(menuItem, dict) and 'label' in menuItem  and 'value' in menuItem:
                        actionIndex = len(actionGroup.actions())
                        action = QAction(menuItem['label'], actionGroup)
                        action.setProperty('pluginIndex', pluginIndex)
                        action.setProperty('actionValue', menuItem['value'])
                        action.setCheckable(True)
                        toolbar.addAction(action)
                # menu separator
                if 'groupLabel' in menu:
                    toolbar.addSeparator()

            # add the plugin in the container
            container = QWidget.createWindowContainer(view, self);
            self.stackedWidget.addWidget(container)

        # connect menu action to the plugin callback
        actionGroup.triggered.connect(self.onMenuAction)

        # display the plugin container
        self.setCentralWidget(self.stackedWidget)
        self.show()

    def onMenuAction(self, action):
        pluginIndex = action.property('pluginIndex')
        actionValue = action.property('actionValue')
        # display the plugin
        self.stackedWidget.setCurrentIndex(pluginIndex)
        # call the plugin callback
        self.plugins[pluginIndex].onMenuAction(actionValue)
           

   