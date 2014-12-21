import QtQuick 2.3

Rectangle {
    id: header
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    color: "#ececec"
    height: (balance.height * 2) + 20
    property alias text: balance.text

    Text {
        id: balance
        font.pixelSize: 30
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 10
        anchors.topMargin: 10
    }
}
