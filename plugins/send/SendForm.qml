import QtQuick 2.3
import QtQuick.Controls 1.0;
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.0;

GroupBox {
    id: sendPane
    property alias buttonText: sendButton.text
    property alias sources: sourceList.model
    property alias source: sourceList.currentText
    property alias destination: txTo.text
    property alias quantity: txValue.text

    height: sendForm.height + 20
    anchors {
        topMargin: 5
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
            horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: sourceListLabel
            text: qsTr("Source")
            font.pointSize: 14
        }

        RowLayout {
            anchors.right: parent.right
            anchors.left: sourceListLabel.right
            anchors.leftMargin: 10

            ComboBox {
                id: sourceList
                implicitWidth: 400
            }

            Button {
                id: copyButton
                iconSource: "copy.png"
                onClicked: {
                    copySourceToClipboard();
                }
            }
        }

        Text {
            text: qsTr("To")
            font.pointSize: 14
        }

        TextField {
            id: txTo
            style: TextFieldStyle {
                background: Rectangle {
                    implicitWidth: 400
                    border.color: "#cccccc"
                    border.width: 1
                }
            }
            font.pointSize: 14
            placeholderText: qsTr("Address")
            enabled: true
        }

        Text {
            text: qsTr("Amount")
            font.pointSize: 14
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
            font.pointSize: 14
            placeholderText: "0.00"
        }

        Button {
            Layout.columnSpan: 2
            anchors.horizontalCenter: parent.horizontalCenter
            id: sendButton
            text: qsTr("Send")
            onClicked: {
                sendAsset();
            }
        }
    }
}



