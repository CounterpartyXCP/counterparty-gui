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
