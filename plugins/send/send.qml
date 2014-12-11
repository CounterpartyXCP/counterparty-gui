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

    function init() {
        root.menu = {
            'groupLabel': 'Wallet',
            'items': [
                { 'label': 'BTC (3.02)', 'value': 'BTC' },
                { 'label': 'XCP (3.02)', 'value': 'XCP' },
                { 'label': 'GOLD (3.02)', 'value': 'GOLD' }
            ]
        }
    }

    function onMenuAction(itemValue) {
        var query = {
            'command': 'get_balances',
            'params': {
                'addresses':['address1', 'address2']
            }
        }
        var result = xcpApi.call(query)
        balance.text = "clicked: " + itemValue + ' ' + result["toto"];
    }

    RowLayout {
        id: mainLayout
        spacing: 10
        anchors.fill: parent

        Text {
            id: balance
            text: "<b>BTC</b> 5.12345678"
            anchors.topMargin: 10
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            font.pixelSize: 30
        }
    }



}
