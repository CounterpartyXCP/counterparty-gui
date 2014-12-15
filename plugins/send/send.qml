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
            var label = assetName + ' (' + amount + ')';
            menu['items'].push({'label': label, 'value': asset})
        }
        root.menu = menu
    }

    function onMenuAction(itemValue) {

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
