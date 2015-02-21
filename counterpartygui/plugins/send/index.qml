import QtQuick 2.3
import QtQuick.Layouts 1.0;

Rectangle {
    id: root
    anchors.fill: parent
    property variant menu
    property variant currentAsset

    // init callback
    function init() {
        // get balances for addresses in the wallet
        var wallet = xcpApi.call({'method': 'wallet', 'params': {}});
        var menu = {
            'groupLabel': 'Wallet',
            'items': []
        }
        // generate items of the left menu, one item per asset
        for (var asset in wallet['assets']) {
            var assetName = String(asset)
            // short the name if free asset
            if (assetName.substring(0,1) === "A") {
                assetName = assetName.substring(0,4) + '...' + assetName.substring(assetName.length - 4)
            }
            var amount = Number(wallet['assets'][asset]).toFixed(2)
            var label = assetName + ' <font style="color:#888888">[' + amount + ']</font>';
            if (asset === 'BTC' || asset === 'XCP') {
                menu['items'].unshift({'label': label, 'value': asset});
            } else {
                menu['items'].push({'label': label, 'value': asset});
            }
        }
        // set the menu property
        root.menu = menu
    }

    // onMenuAction callback. Called
    function onMenuAction(itemValue) {
        // empty the transactions List
        sendsListComp.listModel.clear()

        // set the current assets
        root.currentAsset = itemValue;

        // get balance by address and sends list for the current asset
        var assetInfo = xcpApi.call({'method': 'asset', 'params': {'asset_name': root.currentAsset}});

        // display the balance
        assetBalanceComp.text = '<b>' + root.currentAsset + '</b><br />' + assetInfo['balance'];

        // update text of the send button
        sendFormComp.buttonText = 'Send ' + root.currentAsset;

        // populate the list of source addresses
        var sources = [];
        for (var address in assetInfo['addresses']) {
            var label = address;
            label += ' [' + assetInfo['addresses'][address] + ']';
            sources.push(label);
        }
        sendFormComp.sources = sources;

        // populate the transactions list
        for (var t in assetInfo['sends']) {
            var tx = assetInfo['sends'][t]
            sendsListComp.listModel.append({
                type: tx['type'],
                value: tx['quantity'],
                from: tx['source'],
                to: tx['destination'],
                block_index: tx['block_index']
            });
        }
    }

    function sendAsset() {
        // prepare RPC call params
        var query = {
            'method': 'create_send',
            'params': {
                'source':  sendFormComp.source.split(" ").shift(),
                'destination': sendFormComp.destination,
                'asset': root.currentAsset,
                'quantity': parseInt((parseFloat(sendFormComp.quantity) * 100000000).toFixed(0))
            }
        }

        // prepare confirmation message
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

    // Screen
    ColumnLayout {
        id: mainLayout
        spacing: 10
        anchors.fill: root

        // AssetBalance.qml
        AssetBalance {
            id: assetBalanceComp
        }

        // SendForm.qml
        SendForm {
            id:sendFormComp
            anchors.top: assetBalanceComp.bottom
        }

        // SendsList.qml
        SendsList {
            id: sendsListComp
            anchors.top: sendFormComp.bottom
        }
    }
}
