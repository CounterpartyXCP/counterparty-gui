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
            var amount = Math.round(Number(balances[asset]) * 100) / 100;
            var label = asset + ' (' + amount + ')';
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
