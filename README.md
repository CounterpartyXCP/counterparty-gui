counterpartygui
================

# Description
`counterpartygui` is a PyQT5 GUI for [`counterpartyd`](https://github.com/CounterpartyXCP/counterpartyd).

# Requirements
* [Python 3](http://python.org)
* [Python 3 packages](https://github.com/CounterpartyXCP/counterpartygui/blob/master/pip-requirements.txt)
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
A counterpartyd configuration file looks like this:

	[Default]
	backend-rpc-user=USER
	backend-rpc-password=PASSWORD

If and only if counterpartygui is to be run on the Bitcoin testnet, with the
`--testnet` CLI option, counterpartyd must be set to do the same (`--testnet=1`).

# Usage
The command‐line syntax of counterpartygui is that of
`./counterpartygui.py {OPTIONS}`.

For a summary of the command‐line arguments and options, see
`./counterpartygui.py --help`.

# Plugins

In counterpartygui everything is plugin. The core application only manages the left menu. Each plugin adds one or more items in this menu. The core application display the corresponding plugin in the main window, each time the user click on one of this item.

A plugin is defined by the following conventions:

* it must live in the folder `plugins/{PLUGIN_NAME}/`
* PLUGIN_NAME folder must contains at least one file `index.qml` that contains the QML root object
* the root object in `index.qml` must contains two javascript callbacks: `init()` and `onMenuAction(itemValue)`. The former is called once when the application initialise the plugins. The latter is called when the user click on a menu item that belongs to the plugin.
* the root object in `index.qml` must contains a property `root.menu` that define the items to dsplay in the left menu of the application. This poperty can be populated in the `init()` callback. 
* the QML context contains an instance of CounterpartydAPI that can be used in javascript to make any RPC call to the counterpartyd API, and a instance of GUI to display alert or confirmation box. For instance :

```
	function sendAsset() {
        var query = {
            'method': 'do_send',
            'params': {
                'source':  sendFormComp.source,
                'destination': sendFormComp.destination,
                'asset': root.currentAsset,
                'quantity': sendFormComp.quantity
            }
        }

        var confirmMessage = "Do you really want to send " +
                             sendFormComp.quantity + " " + root.currentAsset +
                             " to " + sendFormComp.destination;

        if (GUI.confirm("Confirm send", confirmMessage)) {
            var result = xcpApi.call(query);
            if (result) {
                GUI.alert("Transaction done", result);
            }
        }
    }
```




