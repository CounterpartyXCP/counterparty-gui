import QtQuick 2.3
import QtQuick.Controls 1.0;

Rectangle {
    property alias listModel: txModel

    anchors {
        left: parent.left
        right: parent.right
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
            font.pointSize: 12
            color: styleData.textColor
            elide: styleData.elideMode
            font.bold: true
        }
    }

    Component {
        id: defaultCell
        Text {
            width: parent.width
            font.pointSize: 12
            text: styleData.value
            anchors.left: parent.left
            anchors.leftMargin: 3
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
        }
    }

    TableView {
        id: txTableView
        anchors.fill : parent
        TableViewColumn{ role: "type" ; title: qsTr("type") ; width: 50 ; delegate: defaultCell }
        TableViewColumn{ role: "value" ; title: qsTr("Amount") ; width: 100 ; delegate: alignRightCell }
        TableViewColumn{ role: "from" ; title: qsTr("From") ; width: 280 ; delegate: defaultCell }
        TableViewColumn{ role: "to" ; title:qsTr("To") ; width: 280 ; delegate: defaultCell }
        TableViewColumn{ role: "block_index" ; title: qsTr("Block #") ; width: 100 ; delegate: alignRightCell }

        model: ListModel {
            id: txModel
            Component.onCompleted: {
            }
        }
    }
}
