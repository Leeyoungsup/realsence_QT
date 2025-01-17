# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'z:\Workspace\YS_Lee\realsense\code\realsence_QT-1\front.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1768, 1018)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setGeometry(QtCore.QRect(100, 0, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playButton.sizePolicy().hasHeightForWidth())
        self.playButton.setSizePolicy(sizePolicy)
        self.playButton.setObjectName("playButton")
        self.cameraList = QtWidgets.QListWidget(self.centralwidget)
        self.cameraList.setGeometry(QtCore.QRect(0, 30, 256, 301))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameraList.sizePolicy().hasHeightForWidth())
        self.cameraList.setSizePolicy(sizePolicy)
        self.cameraList.setObjectName("cameraList")
        self.viewContainer = QtWidgets.QWidget(self.centralwidget)
        self.viewContainer.setGeometry(QtCore.QRect(269, 29, 1061, 961))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewContainer.sizePolicy().hasHeightForWidth())
        self.viewContainer.setSizePolicy(sizePolicy)
        self.viewContainer.setObjectName("viewContainer")
        self.wholeCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.wholeCheck.setGeometry(QtCore.QRect(10, 0, 81, 16))
        self.wholeCheck.setObjectName("wholeCheck")
        self.recordButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordButton.setGeometry(QtCore.QRect(180, 0, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recordButton.sizePolicy().hasHeightForWidth())
        self.recordButton.setSizePolicy(sizePolicy)
        self.recordButton.setObjectName("recordButton")
        self.outputEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.outputEdit.setGeometry(QtCore.QRect(270, 0, 761, 20))
        self.outputEdit.setObjectName("outputEdit")
        self.outputpathButton = QtWidgets.QPushButton(self.centralwidget)
        self.outputpathButton.setGeometry(QtCore.QRect(1040, 0, 51, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputpathButton.sizePolicy().hasHeightForWidth())
        self.outputpathButton.setSizePolicy(sizePolicy)
        self.outputpathButton.setObjectName("outputpathButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1330, 40, 91, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.checktreeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.checktreeWidget.setGeometry(QtCore.QRect(1340, 60, 421, 911))
        self.checktreeWidget.setStyleSheet("QTreeWidget::item {\n"
"                border: 1px solid #dcdcdc;\n"
"            }\n"
"            QTreeWidget::item:selected {\n"
"                background-color: #000000;\n"
"            }\n"
"            QTreeWidget::header {\n"
"                background-color: #000000;\n"
"                border: 1px solid #dcdcdc;\n"
"            }")
        self.checktreeWidget.setObjectName("checktreeWidget")
        self.checktreeWidget.headerItem().setText(0, "1")
        self.numberEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.numberEdit.setGeometry(QtCore.QRect(1180, 0, 151, 20))
        self.numberEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numberEdit.setObjectName("numberEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1090, 0, 81, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(1420, 30, 51, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetButton.sizePolicy().hasHeightForWidth())
        self.resetButton.setSizePolicy(sizePolicy)
        self.resetButton.setObjectName("resetButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(1640, 30, 121, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setObjectName("saveButton")
        self.speakProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.speakProgressBar.setGeometry(QtCore.QRect(10, 950, 251, 23))
        self.speakProgressBar.setProperty("value", 24)
        self.speakProgressBar.setObjectName("speakProgressBar")
        self.LLMButton = QtWidgets.QPushButton(self.centralwidget)
        self.LLMButton.setGeometry(QtCore.QRect(0, 902, 261, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LLMButton.sizePolicy().hasHeightForWidth())
        self.LLMButton.setSizePolicy(sizePolicy)
        self.LLMButton.setObjectName("LLMButton")
        self.speakEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.speakEdit.setGeometry(QtCore.QRect(0, 400, 261, 451))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speakEdit.sizePolicy().hasHeightForWidth())
        self.speakEdit.setSizePolicy(sizePolicy)
        self.speakEdit.setObjectName("speakEdit")
        self.transferButton = QtWidgets.QPushButton(self.centralwidget)
        self.transferButton.setGeometry(QtCore.QRect(0, 860, 261, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transferButton.sizePolicy().hasHeightForWidth())
        self.transferButton.setSizePolicy(sizePolicy)
        self.transferButton.setObjectName("transferButton")
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(0, 380, 261, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setObjectName("clearButton")
        self.miscComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.miscComboBox.setGeometry(QtCore.QRect(50, 330, 151, 22))
        self.miscComboBox.setObjectName("miscComboBox")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(-10, 330, 51, 16))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setGeometry(QtCore.QRect(204, 330, 51, 23))
        self.testButton.setObjectName("testButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1768, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.playButton.setText(_translate("MainWindow", "재생"))
        self.wholeCheck.setText(_translate("MainWindow", "전체 선택"))
        self.recordButton.setText(_translate("MainWindow", "녹화"))
        self.outputpathButton.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "Check List"))
        self.label_2.setText(_translate("MainWindow", "수험번호 : "))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.saveButton.setText(_translate("MainWindow", "SAVE"))
        self.LLMButton.setText(_translate("MainWindow", "LLM"))
        self.transferButton.setText(_translate("MainWindow", "Speak Transfer"))
        self.clearButton.setText(_translate("MainWindow", "Clear"))
        self.label_3.setText(_translate("MainWindow", "MISC:"))
        self.testButton.setText(_translate("MainWindow", "Test"))
