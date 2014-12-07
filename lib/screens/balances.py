from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import *
import logging

from lib.flow_layout import FlowLayout

class AssetWidget(QFrame):
    def __init__(self, assetInfo, parent):
        super().__init__()

        self.parent = parent
        self.borderStyle = "border-radius: 0; border-color: #96918b; border-width: 1px; border-bottom-style: solid;"
        self.setStyleSheet(self.borderStyle)
        assetLayout = QGridLayout()
        assetLayout.setColumnStretch(1, 1)
        
        self.asset = assetInfo["asset"]
        assetLabel = QLabel(assetInfo["asset"])

        assetLabel.setStyleSheet("font-size: 24px; font-weight: bold; border:0")
        assetLayout.addWidget(assetLabel, 0, 0, 2, 1)

        assetAmount = QLabel(assetInfo["balance"])
        assetAmount.setAlignment(Qt.AlignRight)
        assetAmount.setStyleSheet("font-size:36px; border:0;")
        assetAmount.setContentsMargins(QMargins(20, 0, 20, 0))
        assetLayout.addWidget(assetAmount, 0, 1, 2, 1)

        assetAmountUnconfirmed = QLabel("Unconfirmed:")
        assetAmountUnconfirmed.setStyleSheet("border:0")
        assetLayout.addWidget(assetAmountUnconfirmed, 0, 2, 1, 1)

        assetAmountEscrowed = QLabel("Escrowed:")
        assetAmountEscrowed.setStyleSheet("border:0")
        assetLayout.addWidget(assetAmountEscrowed, 1, 2, 1, 1)

        assetAmountUnconfirmed = QLabel(assetInfo["unconfirmed_balance"])
        assetAmountUnconfirmed.setStyleSheet("border:0")
        assetAmountUnconfirmed.setAlignment(Qt.AlignRight)
        assetLayout.addWidget(assetAmountUnconfirmed, 0, 3, 1, 1)

        assetAmountEscrowed = QLabel(assetInfo["escrowed_balance"])
        assetAmountEscrowed.setStyleSheet("border:0")
        assetAmountEscrowed.setAlignment(Qt.AlignRight)
        assetLayout.addWidget(assetAmountEscrowed, 1, 3, 1, 1)

        assetLayout.setAlignment(Qt.AlignTop)
        self.setLayout(assetLayout)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.parent.activeAsset != self:
            if self.parent.activeAsset:
                self.parent.activeAsset.setStyleSheet(self.borderStyle)
            self.parent.activeAsset = self
            self.parent.activeAsset.setStyleSheet(self.borderStyle + "background: #CCC;")
            logging.error(self.parent.activeAsset.asset)

class BalancesScreen(QWidget):

    def __init__(self):
        super().__init__() 

        self.resize(640,480)
        self.name = "Balances"
        self.icon = QIcon('assets/wallet-icon.png')
        self.activeAsset = None

        assetInfo1 = {
            "asset": "BTC",
            "balance": "13.12345678",
            "unconfirmed_balance": "0.124434",
            "escrowed_balance": "4.35"
        }
        asset1 = AssetWidget(assetInfo1, self)

        assetInfo2 = {
            "asset": "XCP",
            "balance": "13.12345678",
            "unconfirmed_balance": "0.124434",
            "escrowed_balance": "4.35"
        }
        asset2 = AssetWidget(assetInfo2, self)

        assetInfo3 = {
            "asset": "GOLD",
            "balance": "13.12345678",
            "unconfirmed_balance": "0.124434",
            "escrowed_balance": "4.35"
        }
        asset3 = AssetWidget(assetInfo3, self)

        assetInfo4 = {
            "asset": "GOLD",
            "balance": "13.12345678",
            "unconfirmed_balance": "0.124434",
            "escrowed_balance": "4.35"
        }
        asset4 = AssetWidget(assetInfo4, self)

        assetInfo5 = {
            "asset": "GOLD",
            "balance": "13.12345678",
            "unconfirmed_balance": "0.124434",
            "escrowed_balance": "4.35"
        }
        asset5 = AssetWidget(assetInfo5, self)

        scrollArea = QScrollArea()
        scrollArea.setStyleSheet("QScrollArea { border:0 }")
        scrollArea.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(asset1) 
        layout.addWidget(asset2) 
        layout.addWidget(asset3)
        layout.addWidget(asset4) 
        layout.addWidget(asset5) 
        layout.setSpacing(0)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))

        widget = QWidget()
        widget.setLayout(layout)

        scrollArea.setWidget(widget)

        scrollLayout = QVBoxLayout()
        scrollLayout.addWidget(scrollArea) 

        self.setLayout(scrollLayout)
        
        #self.setStyleSheet("background-color: green;")

