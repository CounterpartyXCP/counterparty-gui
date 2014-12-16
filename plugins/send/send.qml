import QtQuick 2.0
import QtQuick.Controls 1.0;
import QtQuick.Layouts 1.0;
import QtQuick.Dialogs 1.0;
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
        var assetInfo = xcpApi.getAssetInfo(itemValue);

        balance.text = '<b>' + itemValue + '</b><br />' + assetInfo['balance'];
        sendButton.text = 'Send ' + itemValue;

        var sources = [];
        for (var address in assetInfo['addresses']) {
            var label = address;
            label += ' [' + assetInfo['addresses'][address] + ']';
            sources.push(label);
        }
        sourceList.model = sources;
    }

    ColumnLayout {
        id: mainLayout
        spacing: 10
        anchors.left: root.left
        anchors.right: root.right

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
                    style: TextFieldStyle {
                        background: Rectangle {
                            implicitWidth: 200
                            border.color: "#cccccc"
                            border.width: 1
                        }
                    }
                    placeholderText: "Address"
                }

                Text {
                    text: "Amount"
                }

                // There's something off with the row layout where textfields won't listen to the width setting
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
                        var source = sourceList.currentText.split(" ").shift();
                        console.log("clicked: " + source);
                    }
                }
            }


        }
    }



}
