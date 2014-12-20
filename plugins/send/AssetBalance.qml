import QtQuick 2.3
import QtQuick.Controls 1.0;
import QtQuick.Layouts 1.0;
import QtQuick.Dialogs 1.1;
import QtQuick.Window 2.1;
import QtQuick.Controls.Styles 1.1

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
