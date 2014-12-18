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
        txModel.clear()
        root.currentAsset = itemValue;

        var assetInfo = xcpApi.getAssetInfo(root.currentAsset);

        balance.text = '<b>' + root.currentAsset + '</b><br />' + assetInfo['balance'];
        sendButton.text = 'Send ' + root.currentAsset;

        var sources = [];
        for (var address in assetInfo['addresses']) {
            var label = address;
            label += ' [' + assetInfo['addresses'][address] + ']';
            sources.push(label);
        }
        sourceList.model = sources;

        for (var t in assetInfo['sends']) {
            var tx = assetInfo['sends'][t]
            xcpApi.log(tx)
            txModel.append({
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
                'source': sourceList.currentText.split(" ").shift(),
                'destination': txTo.text,
                'asset': root.currentAsset,
                'quantity': parseInt((parseFloat(txValue.text) * 100000000).toFixed(0))
            }
        }

        var confirmMessage = "Do you really want to send " +
                             txValue.text + " " + root.currentAsset +
                             " to " + txTo.text;

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

        Text {
            id: balance
            font.pixelSize: 30
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 10
            anchors.topMargin: 10
        }

        Rectangle {
            id: sendPane
            color: "#ececec"
            border.color: "#cccccc"
            border.width: 1
            height: sendForm.height + 20
            anchors {
                top: balance.bottom
                topMargin: 10
                left: parent.left
                leftMargin: 5
                right: parent.right
                rightMargin: 5
            }

            GridLayout {
                id: sendForm
                columns: 2
                anchors {
                    top: parent.top
                    topMargin: 10
                    horizontalCenter: parent.horizontalCenter
                }

                Text {
                    id: sourceListLabel
                    text: "Source"
                }

                ComboBox {
                    id: sourceList
                    anchors.right: parent.right
                    anchors.left: sourceListLabel.right
                    anchors.leftMargin: 10
                }

                Text {
                    text: "To"
                }

                TextField {
                    id: txTo
                    activeFocusOnPress: true
                    focus: true
                    style: TextFieldStyle {
                        background: Rectangle {
                            implicitWidth: 200
                            border.color: "#cccccc"
                            border.width: 1
                        }
                    }
                    placeholderText: "Address"
                    enabled: true
                }

                Text {
                    text: "Amount"
                }

                TextField {
                    id: txValue
                    style: TextFieldStyle {
                        background: Rectangle {
                            implicitWidth: 100
                            border.color: "#cccccc"
                            border.width: 1
                        }
                    }
                    placeholderText: "0.00"
                }

                Button {
                    Layout.columnSpan: 2
                    anchors.horizontalCenter: parent.horizontalCenter
                    id: sendButton
                    text: "Send"
                    onClicked: {
                        sendAsset();
                    }
                }
            }
        }

        Rectangle {
            anchors {
                left: parent.left
                right: parent.right
                top: sendPane.bottom
                topMargin: 10
                bottom: parent.bottom
            }

            Component {
                id: alignRightCell
                Text {
                    width: parent.width
                    anchors.right: parent.right
                    text: styleData.value
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    font.pixelSize: 10
                    color: styleData.textColor
                    elide: styleData.elideMode
                    font.bold: true
                }
            }


            TableView {
                id: txTableView
                anchors.fill : parent
                TableViewColumn{ role: "type" ; title: "type" ; width: 50 }
                TableViewColumn{ role: "value" ; title: "Amount" ; width: 100 ; delegate: alignRightCell }
                TableViewColumn{ role: "from" ; title: "From" ; width: 280 }
                TableViewColumn{ role: "to" ; title: "To" ; width: 280 }
                TableViewColumn{ role: "block_index" ; title: "Block #" ; width: 100 ; delegate: alignRightCell }

                model: ListModel {
                    id: txModel
                    Component.onCompleted: {
                    }
                }

            }
        }
    }
}
