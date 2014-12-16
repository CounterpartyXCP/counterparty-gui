from PyQt5.QtCore import QObject, QVariant, pyqtSlot
import logging
import requests
import sys
import json
from decimal import Decimal as D

UNIT = 100000000

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, D):
            return format(obj, '.8f')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

# TODO: display message box
class CounterpartydRPCError(Exception):
    pass

class CounterpartydAPI(QObject):
    def __init__(self, config):
        super(CounterpartydAPI, self).__init__()
        self.config = config
        self.rpcSession = requests.Session()

    def query(self, method, params):
        headers = {'content-type': 'application/json'}
        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }
        logging.error(payload)
        TRIES = 12
        for i in range(TRIES):
            try:
                response = self.rpcSession.post(self.config.BACKEND_RPC, data=json.dumps(payload), headers=headers, verify=self.config.BACKEND_RPC_SSL_VERIFY)
                if i > 0: logging.debug('Status: Successfully connected.', file=sys.stderr)
                break
            except requests.exceptions.SSLError as e:
                raise e
            except requests.exceptions.ConnectionError:
                logging.debug('Could not connect to Counterpartyd. (Try {}/{})'.format(i+1, TRIES))
                time.sleep(5)

        if response == None:
            if self.config.TESTNET: network = 'testnet'
            else: network = 'mainnet'
            raise CounterpartydRPCError('Cannot communicate with Counterpartyd {}.'.format(network))
        elif response.status_code != 200:
            raise CounterpartydRPCError(str(response.status_code) + ' ' + response.reason)

        responseJson = response.json()

        if 'error' not in responseJson.keys() or responseJson['error'] == None:
            return responseJson['result']
        else:
            raise CounterpartydRPCError('{}'.format(responseJson['error']))

    @pyqtSlot(QVariant, result=QVariant)
    def call(self, query):
        # TODO: hack, find a real solution
        for key in query['params']:
            if key in ['quantity']:
                query['params'][key] = int(query['params'][key])
                
        result = self.query(query['method'], query['params'])
        return QVariant(result)

    @pyqtSlot(result=QVariant)
    def getBalances(self):
        btcWallet = self.query('get_wallet', {})
        addresses = []
        balanceByAsset = { 'BTC': D(0) }
        for address in btcWallet:
            addresses.append(address)
            balanceByAsset['BTC'] += D(btcWallet[address])

        assetBalances = self.query('get_balances', {'filters': [('address', 'IN', addresses),]})
        for balance in assetBalances:
            asset = balance['asset']
            if asset not in balanceByAsset:
                balanceByAsset[asset] = D(0)
            balanceByAsset[asset] += D(balance['quantity']) / UNIT

        for asset in balanceByAsset:
            balanceByAsset[asset] = format(balanceByAsset[asset], '.8f')

        return QVariant(balanceByAsset)

    @pyqtSlot(QVariant, result=QVariant)
    def getAssetInfo(self, asset):
        btcWallet = self.query('get_wallet', {})
        addresses = []

        btcBalance = D(0)
        for address in btcWallet:
            addresses.append(address)
            btcBalance += D(btcWallet[address])

        if asset == 'BTC':
            return QVariant({
                'balance': format(btcBalance, '.8f'),
                'addresses': btcWallet
            })

        else:
            balances = self.query('get_balances', {'filters': [('address', 'IN', addresses), ('asset', '==', asset)]})

            assetBalance = D(0)
            assetWallet = {}
            for balance in balances:
                quantity = D(balance['quantity']) / UNIT
                assetBalance += quantity
                assetWallet[balance['address']] = format(quantity, '.8f')

            result = {
                'balance': format(assetBalance, '.8f'),
                'addresses': assetWallet
            }

            logging.error(result)

            return QVariant(result)


    @pyqtSlot(QVariant)
    def log(self, message):
        logging.error("FROM QML:")
        logging.error(message)


