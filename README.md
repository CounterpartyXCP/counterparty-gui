counterparty-gui
================

# Description

`counterparty-gui` is a PyQT5 GUI for [`counterparty-lib`](https://github.com/CounterpartyXCP/counterpartyd).

# Requirements

* [Python 3](http://python.org)
* [PyQT5](http://www.riverbankcomputing.com/software/pyqt/download5)
* [`counterparty-cli`](https://github.com/CounterpartyXCP/counterparty-cli)
* [`Bitcoin Core`](https://bitcoin.org/en/download) (OR [`btcwallet`](https://github.com/btcsuite/btcwallet) OR [`Electrum`](https://electrum.org/download.html))

# Installation

**Linux and Mac OS X**

```
$ git clone https://github.com/CounterpartyXCP/counterparty-gui.git
$ cd counterparty-gui
$ pip3 install -r requirements.txt
$ python3 setup.py install
```

**Windows**

Download and execute the MSI [installer](https://github.com/CounterpartyXCP/counterparty-gui/releases).

# Usage

The command‐line syntax of counterparty-gui is that of
`./counterparty-gui.py {OPTIONS}`.

For a summary of the command‐line options, see
`./counterparty-gui.py --help`.

# Plugins

In counterparty-gui everything is a plugin. The core application only manages the left menu. Each plugin adds one or more items in this menu. When the user clicks on one of these items, the core application displays the corresponding plugin in the main window.

A plugin is defined by the following conventions:

* it must live in the folder `plugins/{PLUGIN_NAME}/`
* PLUGIN_NAME folder must contains at least one file `index.qml` that contains the QML root object
* the root object in `index.qml` must contains 3 javascript callbacks: 
    
    - `init()`, called once, when the application initialises plugins.  
    - `onMenuAction(itemValue)`, called when the user clicks on a menu item that belongs to the plugin.
    - `onMessage(messageName, messageData)`, for now called only when a new block is parsed by the Counterparty server with `messageName` equal to `new_block`.

* the root object in `index.qml` must contains a property `root.menu`. It contains the list of items to dsplay in the left menu and can be populated in the `init()` callback. 
* the QML context contains:
    - an instance of CounterpartydAPI (core/api.py) to make any RPC call to the counterpartyd API or the Wallet with Javascript, 
    - an instance of GUI (core/gui.py) to display messages or ask confirmations.

Example:

```
	function sendAsset() {
		// prepare the query
        var query = {
            'method': 'create_send',
            'params': {
                'source':  sendFormComp.source,
                'destination': sendFormComp.destination,
                'asset': root.currentAsset,
                'quantity': sendFormComp.quantity
            }
        }

        // prepare the confirmation message
        var confirmMessage = "Do you really want to send " +
                             sendFormComp.quantity + " " + root.currentAsset +
                             " to " + sendFormComp.destination;

        if (GUI.confirm("Confirm send", confirmMessage)) {
            // Compose transaction
            var unsigned_hex = xcpApi.call(query);
            if (unsigned_hex) {
                // Sign transaction
                var signed_hex = xcpApi.call({'method': 'sign_raw_transaction', 'params': {'tx_hex': unsigned_hex}});
                if (signed_hex) {
                    // Broadcast transaction
                    var tx_hash = xcpApi.call({'method': 'send_raw_transaction', 'params': {'tx_hex': signed_hex}});
                    // display transaction hash
                    if (tx_hash) {
                        GUI.alert("Transaction done", tx_hash);
                    }
                }
            }
        }
    }
```




