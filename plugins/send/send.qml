import QtQuick 2.3
import QtQuick.Controls 1.0;
import QtQuick.Layouts 1.0;
import QtQuick.Dialogs 1.1;
import QtQuick.Window 2.1;
import QtQuick.Controls.Styles 1.1

Rectangle {
    id: root
    anchors.fill: parent
    property variant menu
    property variant currentAsset
    focus: true

    function init() {
        var balances = xcpApi.getBalances()
        var menu = {
            'groupLabel': 'Wallet',
            'items': []
        }
        for (var asset in balances) {
            var assetName = String(asset)
            if (assetName.substring(0,1) === "A") {
                assetName = assetName.substring(0,4) + '...' + assetName.substring(assetName.length - 4)
            }
            var amount = Number(balances[asset]).toFixed(2)
            var label = assetName + ' <font style="color:#888888">[' + amount + ']</font>';
            if (asset === 'BTC' || asset === 'XCP') {
                menu['items'].unshift({'label': label, 'value': asset});
            } else {
                menu['items'].push({'label': label, 'value': asset});
            }
        }
        root.menu = menu
    }

    function onMenuAction(itemValue) {
        sendsListComp.listModel.clear()
        root.currentAsset = itemValue;

        var assetInfo = xcpApi.getAssetInfo(root.currentAsset);

        balance.text = '<b>' + root.currentAsset + '</b><br />' + assetInfo['balance'];
        sendFormComp.buttonText = 'Send ' + root.currentAsset;

        var sources = [];
        for (var address in assetInfo['addresses']) {
            var label = address;
            label += ' [' + assetInfo['addresses'][address] + ']';
            sources.push(label);
        }
        sendFormComp.sources = sources;

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
        var query = {
            'method': 'do_send',
            'params': {
                'source':  sendFormComp.source.split(" ").shift(),
                'destination': sendFormComp.destination,
                'asset': root.currentAsset,
                'quantity': parseInt((parseFloat(sendFormComp.quantity) * 100000000).toFixed(0))
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


    ColumnLayout {
        id: mainLayout
        spacing: 10
        anchors.fill: root

        Rectangle {
            id: header
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            color: "#ececec"
            height: (balance.height * 2) + 20

            Text {
                id: balance
                font.pixelSize: 30
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.leftMargin: 10
                anchors.topMargin: 10
            }
        }

        SendForm {
            id:sendFormComp
            anchors.top: header.bottom
        }

        SendsList {
            id: sendsListComp
            anchors.top: sendFormComp.bottom
        }
    }

}
