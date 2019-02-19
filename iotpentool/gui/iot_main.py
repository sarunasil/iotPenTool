# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './iot_main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 600)
        MainWindow.setDocumentMode(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.result_txt = QtWidgets.QTextEdit(self.centralwidget)
        self.result_txt.setEnabled(True)
        self.result_txt.setGeometry(QtCore.QRect(220, 60, 571, 461))
        self.result_txt.setObjectName("result_txt")
        self.top_label = QtWidgets.QLabel(self.centralwidget)
        self.top_label.setGeometry(QtCore.QRect(220, 10, 311, 41))
        self.top_label.setObjectName("top_label")
        self.btn_1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_1.setGeometry(QtCore.QRect(110, 60, 101, 41))
        self.btn_1.setObjectName("btn_1")
        self.cmd_input_txt = QtWidgets.QTextEdit(self.centralwidget)
        self.cmd_input_txt.setEnabled(True)
        self.cmd_input_txt.setGeometry(QtCore.QRect(30, 350, 171, 31))
        self.cmd_input_txt.setReadOnly(False)
        self.cmd_input_txt.setObjectName("cmd_input_txt")
        self.btn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_2.setGeometry(QtCore.QRect(110, 130, 101, 41))
        self.btn_2.setObjectName("btn_2")
        self.btn_3 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_3.setGeometry(QtCore.QRect(110, 200, 101, 41))
        self.btn_3.setObjectName("btn_3")
        self.btn_4 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_4.setGeometry(QtCore.QRect(110, 270, 101, 41))
        self.btn_4.setObjectName("btn_4")
        self.btn_ok = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ok.setGeometry(QtCore.QRect(140, 450, 61, 41))
        self.btn_ok.setObjectName("btn_ok")
        self.arg_input_txt = QtWidgets.QTextEdit(self.centralwidget)
        self.arg_input_txt.setEnabled(True)
        self.arg_input_txt.setGeometry(QtCore.QRect(30, 400, 171, 31))
        self.arg_input_txt.setObjectName("arg_input_txt")
        self.error_txt = QtWidgets.QTextEdit(self.centralwidget)
        self.error_txt.setEnabled(True)
        self.error_txt.setGeometry(QtCore.QRect(800, 60, 311, 461))
        self.error_txt.setObjectName("error_txt")
        self.top_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.top_label_2.setGeometry(QtCore.QRect(800, 10, 311, 41))
        self.top_label_2.setObjectName("top_label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1112, 22))
        self.menubar.setObjectName("menubar")
        self.menuOne = QtWidgets.QMenu(self.menubar)
        self.menuOne.setObjectName("menuOne")
        self.menuTwo = QtWidgets.QMenu(self.menubar)
        self.menuTwo.setObjectName("menuTwo")
        self.menuExit = QtWidgets.QMenu(self.menubar)
        self.menuExit.setObjectName("menuExit")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuOne.menuAction())
        self.menubar.addAction(self.menuTwo.menuAction())
        self.menubar.addAction(self.menuExit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IoT Penetration testing DEMO"))
        self.top_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Some text label</span></p></body></html>"))
        self.btn_1.setText(_translate("MainWindow", "Btn1"))
        self.cmd_input_txt.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ls</p></body></html>"))
        self.btn_2.setText(_translate("MainWindow", "Btn2"))
        self.btn_3.setText(_translate("MainWindow", "Btn3"))
        self.btn_4.setText(_translate("MainWindow", "Btn4"))
        self.btn_ok.setText(_translate("MainWindow", "OK"))
        self.arg_input_txt.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.top_label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">ERROR msg</span></p></body></html>"))
        self.menuOne.setTitle(_translate("MainWindow", "O&ne"))
        self.menuTwo.setTitle(_translate("MainWindow", "&Two"))
        self.menuExit.setTitle(_translate("MainWindow", "E&xit"))

