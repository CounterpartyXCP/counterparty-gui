import argparse
import appdirs
import logging, os, configparser


def defaultBackendRpcPort(config):
    if config.TESTNET:
        return 14000
    else:
        return 4000

ARGS = [
    {'name': 'data-dir', 'params': {'help': 'the directory in which to keep the config file and log file, by default'}},
    {'name': 'config-file', 'params': {'help': 'the location of the configuration file'}},
    {'name': 'testnet', 'params': {'action': 'store_true', 'help': 'use BTC testnet addresses and block numbers'}},
    {'name': 'backend-rpc-connect', 'params': {'help': 'the hostname or IP of the backend bitcoind JSON-RPC server'}, 'default': 'localhost'},
    {'name': 'backend-rpc-port', 'params': {'type': int, 'help': 'the backend JSON-RPC port to connect to'}, 'default': defaultBackendRpcPort},
    {'name': 'backend-rpc-user', 'params': {'help': 'the username used to communicate with backend over JSON-RPC'}, 'default': 'rpc'},
    {'name': 'backend-rpc-password', 'params': {'help': 'the password used to communicate with backend over JSON-RPC'}},
    {'name': 'backend-rpc-ssl', 'params': {'action': 'store_true', 'help': 'use SSL to connect to backend (default: false)'}},
    {'name': 'backend-rpc-ssl-verify', 'params': {'action': 'store_true', 'help':'verify SSL certificate of backend; disallow use of self‐signed certificates (default: false)'}},
    {'name': 'plugins', 'params': {'action': 'append', 'help': 'active plugins'}, 'default': ['send', 'test']}
]

class Config:
    def __init__(self):

        # get args
        parser = argparse.ArgumentParser(prog="Conterpartyd GUI", description='the GUI for Counterpartyd')
        for arg in ARGS:
            parser.add_argument('--{}'.format(arg['name']), **arg['params'])
        self.args = vars(parser.parse_args())

        # Data directory
        if self.args['data_dir']:
            dataDir = self.args.pop('data_dir')
        else:
            dataDir = appdirs.user_config_dir(appauthor='Counterparty', appname='counterpartygui', roaming=True)
        if not os.path.isdir(dataDir): os.mkdir(dataDir)

        # Configuration file
        if self.args['config_file']:
            configPath = self.args.pop('config_file')
        else:
            configPath = os.path.join(dataDir, 'counterpartygui.conf')
        configFile = configparser.ConfigParser()
        configFile.read(configPath)
        hasConfig = 'Default' in configFile
        
        def getDefaultValue(key):
            if hasConfig and key in configFile['Default'] and configFile['Default'][key]:
                return configFile['Default'][key]
            else:
                for arg in ARGS:
                    if arg['name'] == key and 'default' in arg:
                        if callable(arg['default']):
                            return arg['default'](self)
                        else:
                            return arg['default']
            # Todo: `required` field and exception
            return None

        # set variables
        self.DATA_DIR = dataDir
        for arg in ARGS:
            argName = arg['name'].replace('-', '_')
            if self.args[argName] is None:
                self.args[argName] = getDefaultValue(arg['name'])
            setattr(self, argName.upper(), self.args[argName])

        protocol = 'https' if self.BACKEND_RPC_SSL else 'http'
        self.BACKEND_RPC = '{}://{}:{}@{}:{}'.format(protocol, self.BACKEND_RPC_USER, self.BACKEND_RPC_PASSWORD, self.BACKEND_RPC_CONNECT, self.BACKEND_RPC_PORT) 

    