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
            'groupLabel': 'TEST',
            'items': [
                { 'label': 'menu 1', 'value': 'menu 1' },
                { 'label': 'menu 2', 'value': 'menu 2' }
            ]
        }
    }

    function onMenuAction(itemValue) {
        screenTitle.text = itemValue;
    }

    RowLayout {
        id: mainLayout
        spacing: 10
        anchors.fill: parent

        Text {
            id: screenTitle
            anchors.topMargin: 10
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            font.pixelSize: 30
        }

    }



}
