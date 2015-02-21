import logging
import requests
import sys
import json
import time
from decimal import Decimal as D

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox, QWidget

from counterpartycli import clientapi

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
        QMessageBox.critical(QWidget(), "RPC Error", message)
        raise Exception(message)

class CounterpartydAPI(QObject):
    def __init__(self, config):
        super(CounterpartydAPI, self).__init__()
        clientapi.initialize(testnet=config.TESTNET, testcoin=False,
                            counterparty_rpc_connect=config.COUNTERPARTY_RPC_CONNECT, counterparty_rpc_port=config.COUNTERPARTY_RPC_PORT, 
                            counterparty_rpc_user=config.COUNTERPARTY_RPC_USER, counterparty_rpc_password=config.COUNTERPARTY_RPC_PASSWORD,
                            counterparty_rpc_ssl=config.COUNTERPARTY_RPC_SSL, counterparty_rpc_ssl_verify=config.COUNTERPARTY_RPC_SSL_VERIFY,
                            wallet_name=config.WALLET_NAME, wallet_connect=config.WALLET_CONNECT, wallet_port=config.WALLET_PORT, 
                            wallet_user=config.WALLET_USER, wallet_password=config.WALLET_PASSWORD,
                            wallet_ssl=config.WALLET_SSL, wallet_ssl_verify=config.WALLET_SSL_VERIFY)

    @pyqtSlot(QVariant, result=QVariant)
    def call(self, query):
        # TODO: hack, find a real solution
        print(query)
        try:
            for key in query['params']:
                if key in ['quantity']:
                    query['params'][key] = int(query['params'][key])
        except:
            pass

        try:
            result = clientapi.call(query['method'], query['params'])
        except Exception as e:
            raise CounterpartydRPCError(str(e))
        
        # TODO: hack, find a real solution
        result = json.dumps(result, cls=DecimalEncoder)
        result = json.loads(result)

        print(result)
        return QVariant(result)
        