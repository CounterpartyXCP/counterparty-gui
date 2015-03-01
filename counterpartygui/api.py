import logging
import requests
import sys
import json
import time
from decimal import Decimal as D

from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox, QWidget, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtQml import QJSValue
from counterpartycli import clientapi
from counterpartycli.wallet import LockedWalletError
from counterpartygui import tr

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, D):
            return format(obj, '.8f')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

# TODO: display message box
class CounterpartydRPCError(Exception):
    def __init__(self, message):
        super().__init__(message)
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setModal(True)
        msgBox.show()
        raise Exception(message)

class InputDialog(QDialog):
    def __init__(self, message, is_password=False, parent=None):
        super().__init__(parent) 

        self.message = message
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        label = QLabel(message)
        self.layout.addWidget(label)
        self.input = QLineEdit()
        if is_password:
            self.input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.input)

        def onOkPushed():
            self.close()

        okBtn = QPushButton(tr("Ok"))
        okBtn.clicked.connect(onOkPushed)
        self.layout.addWidget(okBtn)

        self.exec()

    def value(self):
        return self.input.text()

    @staticmethod
    def input(message, is_password=False):
        askValue = InputDialog(message, is_password=is_password)
        return askValue.value()

class CounterpartydAPI(QObject):
    def __init__(self, config):
        super(CounterpartydAPI, self).__init__()
        clientapi.initialize(testnet=config.TESTNET, testcoin=False,
                            counterparty_rpc_connect=config.COUNTERPARTY_RPC_CONNECT, counterparty_rpc_port=config.COUNTERPARTY_RPC_PORT, 
                            counterparty_rpc_user=config.COUNTERPARTY_RPC_USER, counterparty_rpc_password=config.COUNTERPARTY_RPC_PASSWORD,
                            counterparty_rpc_ssl=config.COUNTERPARTY_RPC_SSL, counterparty_rpc_ssl_verify=config.COUNTERPARTY_RPC_SSL_VERIFY,
                            wallet_name=config.WALLET_NAME, wallet_connect=config.WALLET_CONNECT, wallet_port=config.WALLET_PORT, 
                            wallet_user=config.WALLET_USER, wallet_password=config.WALLET_PASSWORD,
                            wallet_ssl=config.WALLET_SSL, wallet_ssl_verify=config.WALLET_SSL_VERIFY,
                            requests_timeout=config.REQUESTS_TIMEOUT)

    @pyqtSlot(QVariant, result=QVariant)
    def call(self, query):
        if isinstance(query, QJSValue):
            query = query.toVariant()
        # TODO: hack, find a real solution
        print(query)
        try:
            for key in query['params']:
                if key in ['quantity']:
                    query['params'][key] = int(query['params'][key])
        except:
            pass

        try:
            result = clientapi.call(query['method'], query['params'], input_method=InputDialog.input)
        except LockedWalletError as e:
            passphrase = InputDialog.input(message=tr('Enter your wallet passhrase:'), is_password=True)
            try:
                clientapi.call('unlock', {'passphrase': passphrase})
                return self.call(query)
            except Exception as e:
                raise CounterpartydRPCError(str(e))
        except Exception as e:
            raise CounterpartydRPCError(str(e))
        
        # TODO: hack, find a real solution
        result = json.dumps(result, cls=DecimalEncoder)
        result = json.loads(result)

        print(result)
        return QVariant(result)
        