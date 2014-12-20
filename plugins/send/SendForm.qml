import QtQuick 2.3
import QtQuick.Controls 1.0;
import QtQuick.Layouts 1.0;
import QtQuick.Dialogs 1.1;
import QtQuick.Window 2.1;
import QtQuick.Controls.Styles 1.1

Rectangle {
    id: sendPane
    property alias buttonText: sendButton.text
    property alias sources: sourceList.model
    property alias source: sourceList.currentText
    property alias destination: txTo.text
    property alias quantity: txValue.text

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



