from PyQt5.QtCore import QObject, QVariant, pyqtSlot
import logging
import requests
import sys
import json

class CounterpartydRPCError(Exception): pass

class CounterpartydAPI(QObject):
    def __init__(self, config):
        super(CounterpartydAPI, self).__init__()
        self.config = config
        self.rpcSession = requests.Session()

    def query(self, payload, headers):
        TRIES = 12
        for i in range(TRIES):
            try:
                response = self.rpcSession.post(self.config.BACKEND_RPC, data=json.dumps(payload), headers=headers, verify=self.config.BACKEND_RPC_SSL_VERIFY)
                if i > 0: logging.debug('Status: Successfully connected.', file=sys.stderr)
                return response
            except requests.exceptions.SSLError as e:
                raise e
            except requests.exceptions.ConnectionError:
                logging.debug('Could not connect to Counterpartyd. (Try {}/{})'.format(i+1, TRIES))
                time.sleep(5)
        return None

    @pyqtSlot(QVariant, result=QVariant)
    def call(self, query):
        headers = {'content-type': 'application/json'}
        payload = {
            "method": query['method'],
            "params": query['params'],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = self.query(payload, headers)

        if response == None:
            if self.config.TESTNET: network = 'testnet'
            else: network = 'mainnet'
            raise CounterpartydRPCError('Cannot communicate with Counterpartyd {}.'.format(network))
        elif response.status_code != 200:
            raise CounterpartydRPCError(str(response.status_code) + ' ' + response.reason)

        response_json = response.json()
        logging.error(response_json)
        if 'error' not in response_json.keys() or response_json['error'] == None:
            return QVariant(response_json['result'])
        else:
            raise CounterpartydRPCError('{}'.format(response_json['error']))

