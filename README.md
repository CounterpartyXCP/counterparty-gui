counterpartygui
================

# Description

`counterpartygui` is a PyQT5 GUI for [`counterpartyd`](https://github.com/CounterpartyXCP/counterpartyd).

# Requirements

* [Python 3](http://python.org)
* [Python 3 packages](https://github.com/CounterpartyXCP/counterparty-gui/blob/develop/pip-requirements.txt)
* [PyQT5](http://www.riverbankcomputing.com/software/pyqt/download5)
* [`counterpartyd`](https://github.com/CounterpartyXCP/counterpartyd).

# Installation

In order for counterpartygui to function, it must be able to communicate with a
running instance of counterpartyd.
counterpartygui needs to know at least the JSON‐RPC password of the counterpartyd
with which it is supposed to communicate. The simplest way to set this is to
include it in all command‐line invocations of counterpartygui, such as
`./counterpartygui.py --backend-rpc-user=USER --backend-rpc-password=PASSWORD`. To make this and other
options persistent across counterpartygui sessions, one may store the desired
settings in a configuration file specific to counterpartygui.
If and only if counterpartygui is to be run on the Bitcoin testnet, with the
`--testnet` CLI option, counterpartyd must be set to do the same (`--testnet=1`).

# Configuration file

OS  | Path
------------- | -------------
MacOS | ~/Library/Application Support/counterpartygui/counterpartygui.conf
XP | C:\Documents and Settings\username\Application Data\counterpartygui\counterpartygui.conf
Vista, 7 | C:\Users\username\AppData\Roaming\counterpartyd\counterpartygui.conf
Linux | ~/.config/counterpartygui/counterpartygui.conf

A counterpartygui configuration file looks like this:

	[Default]
	backend-rpc-user=USER
	backend-rpc-password=PASSWORD
    testnet=1

# Build

Mac OS X: `python setup.py py2app`

Windows: `python setup.py py2exe`

# Usage

The command‐line syntax of counterpartygui is that of
`./counterpartygui.py {OPTIONS}`.

For a summary of the command‐line arguments and options, see
`./counterpartygui.py --help`.

# Plugins

In counterpartygui everything is a plugin. The core application only manages the left menu. Each plugin adds one or more items in this menu. When the user clicks on one of these items, the core application displays the corresponding plugin in the main window.

A plugin is defined by the following conventions:

* it must live in the folder `plugins/{PLUGIN_NAME}/`
* PLUGIN_NAME folder must contains at least one file `index.qml` that contains the QML root object
* the root object in `index.qml` must contains two javascript callbacks: `init()` and `onMenuAction(itemValue)`. The former is called once, when the application initialises plugins. The latter is called when the user clicks on a menu item that belongs to the plugin.
* the root object in `index.qml` must contains a property `root.menu`. It contains the list of items to dsplay in the left menu and can be populated in the `init()` callback. 
* the QML context contains:
    - an instance of CounterpartydAPI (core/api.py) to make any RPC call to the counterpartyd API with Javascript, 
    - an instance of GUI (core/gui.py) to display messages or ask confirmations.

Example:

```
	function sendAsset() {
		// prepare the query
        var query = {
            'method': 'do_send',
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

        // ask a confirmation
        if (GUI.confirm("Confirm send", confirmMessage)) {
        	// make the RPC call
            var result = xcpApi.call(query);
            if (result) {
            	// display the transaction hash
                GUI.alert("Transaction done", result);
            }
        }
    }
```




