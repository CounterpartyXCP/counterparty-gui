import argparse
import appdirs
import logging
import os
import configparser
import sys
import json
import codecs

logger = logging.getLogger(__name__)

from PyQt5 import QtGui, QtCore, QtWidgets

from counterpartylib.lib import config, log

from counterpartycli import client, server
from counterpartycli.util import add_config_arguments
from counterpartycli.setup import generate_config_files, generate_config_file

from counterpartygui import tr

APP_NAME = 'counterparty-gui'
APP_VERSION = '1.0.0'

CONFIG_ARGS = client.CONFIG_ARGS + [
    [('--poll-interval',), {'type': int, 'default': 60000, 'help': 'poll interval, in miliseconds (default: 60000)'}]
]

class Config():
    def __init__(self, splash=None):
        self.PLUGINS = ['send', 'test']
        self.splash = splash
        self.initialize()

    def initialize(self, openDialog=False):
        configdir = appdirs.user_config_dir(appauthor=config.XCP_NAME, appname=config.APP_NAME, roaming=True)
        configfile = os.path.join(configdir, 'client.conf')
        config_exists = os.path.exists(configfile)

        if not config_exists:
            generate_config_file(configfile, client.CONFIG_ARGS)

        # Parse command-line arguments.
        parser = argparse.ArgumentParser(prog=APP_NAME, description=tr('Counterparty CLI for counterparty-server'), add_help=False, conflict_handler='resolve')
        parser.add_argument('-h', '--help', dest='help', action='store_true', help=tr('show this help message and exit'))
        parser.add_argument('-V', '--version', action='version', version="{} v{}".format(APP_NAME, APP_VERSION))
        parser.add_argument('--config-file', help=tr('the location of the counterparty-client configuration file'))

        self.args = parser.parse_known_args()[0]

        if not config_exists or openDialog:
            is_splash_visible = False
            if self.splash:
                is_splash_visible = self.splash.isVisible()
                if is_splash_visible:
                    self.splash.hide()
            configfile = getattr(self.args, 'config_file', None) or configfile
            configUI = ConfigDialog(configfile, newconfig=not config_exists)
            configUI.exec()
            if is_splash_visible:
                self.splash.show()

        parser = add_config_arguments(parser, CONFIG_ARGS, 'client.conf', config_file_arg_name='client_config_file')

        self.args = parser.parse_args()

        dargs = vars(self.args)
        for argName in dargs:
            print('{}: {}'.format(argName.upper(), dargs[argName]))
            setattr(self, argName.upper(), dargs[argName])

        # Help message
        if self.args.help:
            parser.print_help()
            sys.exit()

        # Logging
        log.set_up(logger, verbose=self.args.verbose)
            

class ConfigDialog(QtWidgets.QDialog):
    def __init__(self, configfile, newconfig=False, parent=None):
        super().__init__(parent)  

        logger.debug(tr('Loading configuration file: `{}`').format(configfile))
        knownConfig = configparser.ConfigParser()
        with codecs.open(configfile, 'r', encoding='utf8') as fp:
            knownConfig.readfp(fp)

        if 'Default' in knownConfig:
            knownConfig = dict(knownConfig['Default'])
        else:
            knownConfig = {}

        self.setMinimumWidth(400)
        self.setModal(True)
        self.setWindowTitle(tr('Configuration'))

        tabs = QtWidgets.QTabWidget()

        serverConfigWidget = ServerConfigPage(knownConfig, newconfig)
        walletConfigWidget = WalletConfigPage(knownConfig)
        advancedConfigWidget = AdvancedConfigPage(knownConfig)

        tabs.addTab(serverConfigWidget, tr("Counterparty Server"))
        tabs.addTab(walletConfigWidget, tr("Walet"))
        tabs.addTab(advancedConfigWidget, tr("Advanced"))

        tabLayout = QtWidgets.QVBoxLayout()
        tabLayout.addWidget(tabs)

        def onServersSelected():
            config = {}
            config.update(serverConfigWidget.getServerConfig())
            config.update(walletConfigWidget.getWalletConfig())
            config.update(advancedConfigWidget.getAdvancedConfig())
            knownConfig.update(config)
            print(knownConfig)
            generate_config_file(configfile, client.CONFIG_ARGS, known_config=knownConfig, overwrite=True)
            self.close()

        selectionCompletedBtn = QtWidgets.QPushButton(tr("Ok"))
        selectionCompletedBtn.clicked.connect(onServersSelected)
        tabLayout.addWidget(selectionCompletedBtn)

        self.setLayout(tabLayout)

        
class ServerConfigPage(QtWidgets.QWidget):
    def __init__(self, knownConfig, newconfig=False, parent=None):
        super().__init__(parent)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(mainLayout)

        with open('servers.json') as f:
            self.public_servers = json.load(f)

        self.radioButtonGroup = QtWidgets.QButtonGroup(self)
        for server in self.public_servers:
            radioButton = QtWidgets.QRadioButton(server['connect'])
            radioButton.setProperty('ssl', server['ssl'])
            radioButton.setProperty('public', True)
            if newconfig and server['connect'] == self.public_servers[0]['connect']:
                radioButton.setChecked(True)
            elif server['connect'] == knownConfig.get('counterparty-rpc-connect'):
                radioButton.setChecked(True)
            self.radioButtonGroup.addButton(radioButton)
            mainLayout.addWidget(radioButton)

        radioButton = QtWidgets.QRadioButton(tr('Private server:'))
        radioButton.setProperty('public', False)
        privateServerGroupBoxDisabled = True
        if not self.radioButtonGroup.checkedButton():
            radioButton.setChecked(True)
            privateServerGroupBoxDisabled = False
        self.radioButtonGroup.addButton(radioButton)
        mainLayout.addWidget(radioButton)

        def onChangeSelectedServer(button):
            if not button.property('public'):
                groupBox.setDisabled(False)
            else:
                groupBox.setDisabled(True)

        self.radioButtonGroup.buttonReleased.connect(onChangeSelectedServer)

        groupBox = QtWidgets.QGroupBox(self)
        groupBoxLayout = QtWidgets.QVBoxLayout()
        groupBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        serverLabel = QtWidgets.QLabel(tr('Host'))
        groupBoxLayout.addWidget(serverLabel)
        self.serverTextField = QtWidgets.QLineEdit()
        self.serverTextField.setToolTip(tr('the hostname or IP of the counterparty JSON-RPC server'))
        self.serverTextField.setText(knownConfig.get('counterparty-rpc-connect', 'localhost'))
        groupBoxLayout.addWidget(self.serverTextField)

        portLabel = QtWidgets.QLabel(tr('Port'))
        groupBoxLayout.addWidget(portLabel)
        self.portTextField = QtWidgets.QSpinBox()
        self.portTextField.setRange(1, 65535)
        self.portTextField.setToolTip(tr('the counterparty JSON-RPC port to connect to'))
        try:
            self.portTextField.setValue(int(knownConfig.get('counterparty-rpc-port', '4000')))
        except ValueError:
            self.portTextField.setValue(4000)
        groupBoxLayout.addWidget(self.portTextField)

        userLabel = QtWidgets.QLabel(tr('User'))
        groupBoxLayout.addWidget(userLabel)
        self.userTextField = QtWidgets.QLineEdit()
        self.userTextField.setToolTip(tr('the username used to communicate with counterparty over JSON-RPC'))
        self.userTextField.setText(knownConfig.get('counterparty-rpc-user', 'rpc'))
        groupBoxLayout.addWidget(self.userTextField)

        passwordLabel = QtWidgets.QLabel(tr('Password'))
        groupBoxLayout.addWidget(passwordLabel)
        self.passwordTextField = QtWidgets.QLineEdit()
        self.passwordTextField.setToolTip(tr('the password used to communicate with counterparty over JSON-RPC'))
        self.passwordTextField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordTextField.setText(knownConfig.get('counterparty-rpc-password', ''))
        groupBoxLayout.addWidget(self.passwordTextField)

        self.useSSLCheckbox = QtWidgets.QCheckBox(tr('Use SSL to connect to counterparty'))
        self.useSSLCheckbox.setChecked(bool(int(knownConfig.get('counterparty-rpc-ssl', '0'))))
        groupBoxLayout.addWidget(self.useSSLCheckbox)

        self.verifySSLCheckbox = QtWidgets.QCheckBox(tr('Verify SSL certificate of counterparty (disallow use of self-signed certificates)'))
        self.verifySSLCheckbox.setChecked(bool(int(knownConfig.get('counterparty-rpc-ssl-verify', '0'))))
        groupBoxLayout.addWidget(self.verifySSLCheckbox)

        groupBox.setLayout(groupBoxLayout)
        groupBox.setDisabled(privateServerGroupBoxDisabled)
        mainLayout.addWidget(groupBox)

    def getServerConfig(self):
        config = {}
        selectedServerButton = self.radioButtonGroup.checkedButton()
        if not selectedServerButton.property('public'):
            config['counterparty-rpc-connect'] = self.serverTextField.text()
            config['counterparty-rpc-port'] = self.portTextField.value()
            config['counterparty-rpc-user'] = self.userTextField.text()
            config['counterparty-rpc-password'] = self.passwordTextField.text()
            config['counterparty-rpc-ssl'] = self.useSSLCheckbox.isChecked()
            config['counterparty-rpc-ssl-verify'] = self.verifySSLCheckbox.isChecked()
        else:
            config['counterparty-rpc-connect'] = selectedServerButton.text()
            config['counterparty-rpc-port'] = ''
            config['counterparty-rpc-user'] = ''
            config['counterparty-rpc-password'] = ''
            config['counterparty-rpc-ssl'] = selectedServerButton.property('ssl')
            config['counterparty-rpc-ssl-verify'] = True
        return config


class WalletConfigPage(QtWidgets.QWidget):
    def __init__(self, knownConfig, parent=None):
        super().__init__(parent)

        self.wallets = [
            (tr('Bitcoin Core'), 'bitcoincore'), 
            (tr('btcwallet'), 'btcwallet'),
            (tr('Electrum'), 'electrum')
        ]

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(mainLayout)

        self.radioButtonGroup = QtWidgets.QButtonGroup(self)
        for wallet in self.wallets:
            radioButton = QtWidgets.QRadioButton(wallet[0])
            radioButton.setProperty('name', wallet[1])
            if wallet[1] == knownConfig.get('wallet-name', 'bitcoincore'):
                radioButton.setChecked(True)
            self.radioButtonGroup.addButton(radioButton)
            mainLayout.addWidget(radioButton)

        groupBox = QtWidgets.QGroupBox(self)
        groupBoxLayout = QtWidgets.QVBoxLayout()
        groupBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        serverLabel = QtWidgets.QLabel(tr('Host'))
        groupBoxLayout.addWidget(serverLabel)
        self.serverTextField = QtWidgets.QLineEdit()
        self.serverTextField.setToolTip(tr('the hostname or IP of the wallet server'))
        self.serverTextField.setText(knownConfig.get('wallet-connect', 'localhost'))
        groupBoxLayout.addWidget(self.serverTextField)

        portLabel = QtWidgets.QLabel(tr('Port'))
        groupBoxLayout.addWidget(portLabel)
        self.portTextField = QtWidgets.QSpinBox()
        self.portTextField.setRange(1, 65535)
        self.portTextField.setToolTip(tr('the wallet port to connect to'))
        try:
            self.portTextField.setValue(int(knownConfig.get('wallet-port', '8332')))
        except ValueError:
            self.portTextField.setValue(8332)
        groupBoxLayout.addWidget(self.portTextField)

        userLabel = QtWidgets.QLabel(tr('User'))
        groupBoxLayout.addWidget(userLabel)
        self.userTextField = QtWidgets.QLineEdit()
        self.userTextField.setToolTip(tr('the username used to communicate with the wallet'))
        self.userTextField.setText(knownConfig.get('wallet-user', 'bitcoinrpc'))
        groupBoxLayout.addWidget(self.userTextField)

        passwordLabel = QtWidgets.QLabel(tr('Password'))
        groupBoxLayout.addWidget(passwordLabel)
        self.passwordTextField = QtWidgets.QLineEdit()
        self.passwordTextField.setToolTip(tr('the password used to communicate with the wallet'))
        self.passwordTextField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordTextField.setText(knownConfig.get('wallet-password', ''))
        groupBoxLayout.addWidget(self.passwordTextField)

        self.useSSLCheckbox = QtWidgets.QCheckBox(tr('Use SSL to connect to wallet'))
        self.useSSLCheckbox.setChecked(bool(int(knownConfig.get('wallet-ssl', '0'))))
        groupBoxLayout.addWidget(self.useSSLCheckbox)

        self.verifySSLCheckbox = QtWidgets.QCheckBox(tr('Verify SSL certificate of wallet (disallow use of self-signed certificates)'))
        self.verifySSLCheckbox.setChecked(bool(int(knownConfig.get('wallet-ssl-verify', '0'))))
        groupBoxLayout.addWidget(self.verifySSLCheckbox)

        groupBox.setLayout(groupBoxLayout)
        mainLayout.addWidget(groupBox)

    def getWalletConfig(self):
        config = {}
        config['wallet-name'] = self.radioButtonGroup.checkedButton().property('name')
        config['wallet-connect'] = self.serverTextField.text()
        config['wallet-port'] = self.portTextField.value()
        config['wallet-user'] = self.userTextField.text()
        config['wallet-password'] = self.passwordTextField.text()
        config['wallet-ssl'] = self.useSSLCheckbox.isChecked()
        config['wallet-ssl-verify'] = self.verifySSLCheckbox.isChecked()
        return config


class AdvancedConfigPage(QtWidgets.QWidget):
    def __init__(self, knownConfig, parent=None):
        super().__init__(parent)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(mainLayout)

        self.useTestnet = QtWidgets.QCheckBox(tr('Use testnet network'))
        self.useTestnet.setChecked(bool(int(knownConfig.get('testnet', '0'))))
        mainLayout.addWidget(self.useTestnet)

        self.allowUnconfirmed = QtWidgets.QCheckBox(tr('Allow the spending of unconfirmed transaction outputs'))
        self.allowUnconfirmed.setChecked(bool(int(knownConfig.get('unconfirmed', '0'))))
        mainLayout.addWidget(self.allowUnconfirmed)

        encodingLabel = QtWidgets.QLabel(tr('Data encoding method'))
        mainLayout.addWidget(encodingLabel)
        self.encoding = QtWidgets.QComboBox()
        self.encoding.addItems(['auto', 'multisig', 'opreturn', 'pubkeyhash'])
        mainLayout.addWidget(self.encoding)

        feePerKbLabel = QtWidgets.QLabel(tr('Fee per kilobyte, in BTC'))
        mainLayout.addWidget(feePerKbLabel)
        self.feePerKbField = QtWidgets.QDoubleSpinBox()
        self.feePerKbField.setDecimals(8)
        self.feePerKbField.setMinimum(0.00000001)
        self.feePerKbField.setSingleStep(0.00000001)
        try:
            self.feePerKbField.setValue(float(knownConfig.get('fee-per-kb', config.DEFAULT_FEE_PER_KB / config.UNIT)))
        except ValueError:
            self.feePerKbField.setValue(config.DEFAULT_FEE_PER_KB / config.UNIT)
        mainLayout.addWidget(self.feePerKbField)

        regularDustSizeLabel = QtWidgets.QLabel(tr('Value for dust Pay-to-Pubkey-Hash outputs, in BTC'))
        mainLayout.addWidget(regularDustSizeLabel)
        self.regularDustSize = QtWidgets.QDoubleSpinBox()
        self.regularDustSize.setDecimals(8)
        self.regularDustSize.setMinimum(0.00000001)
        self.regularDustSize.setSingleStep(0.00000001)
        try:
            self.regularDustSize.setValue(float(knownConfig.get('regular-dust-size', config.DEFAULT_REGULAR_DUST_SIZE / config.UNIT)))
        except ValueError:
            self.regularDustSize.setValue(config.DEFAULT_REGULAR_DUST_SIZE / config.UNIT)
        mainLayout.addWidget(self.regularDustSize)

        multisigDustSizeLabel = QtWidgets.QLabel(tr('Value for dust OP_CHECKMULTISIG outputs, in BTC'))
        mainLayout.addWidget(multisigDustSizeLabel)
        self.multisigDustSize = QtWidgets.QDoubleSpinBox()
        self.multisigDustSize.setDecimals(8)
        self.multisigDustSize.setMinimum(0.00000001)
        self.multisigDustSize.setSingleStep(0.00000001)
        try:
            self.multisigDustSize.setValue(float(knownConfig.get('multisig-dust-size', config.DEFAULT_MULTISIG_DUST_SIZE / config.UNIT)))
        except ValueError:
            self.multisigDustSize.setValue(config.DEFAULT_MULTISIG_DUST_SIZE / config.UNIT)
        mainLayout.addWidget(self.multisigDustSize)

        opReturnValueLabel = QtWidgets.QLabel(tr('Value for OP_RETURN outputs, in BTC'))
        mainLayout.addWidget(opReturnValueLabel)
        self.opReturnValue = QtWidgets.QDoubleSpinBox()
        self.opReturnValue.setDecimals(8)
        self.opReturnValue.setMinimum(0)
        self.opReturnValue.setSingleStep(0.00000001)
        try:
            self.opReturnValue.setValue(float(knownConfig.get('op-return-value', config.DEFAULT_OP_RETURN_VALUE / config.UNIT)))
        except ValueError:
            self.opReturnValue.setValue(config.DEFAULT_OP_RETURN_VALUE / config.UNIT)
        mainLayout.addWidget(self.opReturnValue)

    def getAdvancedConfig(self):
        config = {}
        config['testnet'] = self.useTestnet.isChecked()
        config['unconfirmed'] = self.allowUnconfirmed.isChecked()
        config['fee-per-kb'] = self.feePerKbField.value()
        config['regular-dust-size'] = self.regularDustSize.value()
        config['multisig-dust-size'] = self.multisigDustSize.value()
        config['op-return-value'] = self.opReturnValue.value()
        return config

